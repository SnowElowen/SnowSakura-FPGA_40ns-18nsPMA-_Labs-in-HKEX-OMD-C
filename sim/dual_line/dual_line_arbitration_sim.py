#!/usr/bin/env python3
"""SnowSakura message-level Dual-Line A/B arbitration reference simulation.

This is a Control-Plane/Python reference model, not GTH or RTL.  Its job is to
freeze the message-level truth contract before a bounded two-cycle Fast-Plane
arbiter is mapped to FDRE/LUT/CARRY8 resources.

Contract:
  * A and B carry independently arriving copies of one ordered message stream.
  * Arbitration is by message SeqNum, never packet-byte equality.
  * A/B copies with the expected SeqNum must have identical metadata/payload.
  * A duplicate is emitted once; stale duplicate copies are discarded.
  * A missing expected SeqNum is a gap wait, not permission to emit SeqNum+1.
  * A detected payload conflict is terminal for the fast candidate model.
  * Every accepted decision appears at the modelled TX boundary exactly two
    arbitration cycles later.  Waiting for a missing expected message is
    explicitly counted separately from that two-cycle pipeline latency.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque, Dict, Iterable, List, Tuple


PIPELINE_CYCLES = 2


@dataclass(frozen=True)
class FeedEvent:
    line: str
    arrival_cycle: int
    seq_num: int
    payload: int
    msg_type: int = 30
    msg_size: int = 32

    def identity(self) -> Tuple[int, int, int]:
        return (self.msg_type, self.msg_size, self.payload)


@dataclass(frozen=True)
class OutputEvent:
    decision_cycle: int
    visible_cycle: int
    seq_num: int
    selected_line: str
    payload: int


class ArbitrationConflict(RuntimeError):
    pass


class StalledExpectedSeq(RuntimeError):
    pass


class DualLineReferenceArbiter:
    """Truth model for a single ordered message sequence with two UDP lines."""

    def __init__(self, initial_expected_seq: int) -> None:
        self.expected_seq = initial_expected_seq
        self.pending: Dict[str, Deque[FeedEvent]] = {"A": deque(), "B": deque()}
        self.outputs: List[OutputEvent] = []
        self.stats = defaultdict(int)

    def _discard_stale_heads(self) -> None:
        for line in ("A", "B"):
            queue = self.pending[line]
            while queue and queue[0].seq_num < self.expected_seq:
                queue.popleft()
                self.stats["stale_duplicate_drop"] += 1

    def step(self, cycle: int, arrivals: Iterable[FeedEvent]) -> bool:
        """Consume this cycle's arrivals and issue at most one message decision."""
        for event in arrivals:
            self.pending[event.line].append(event)
            self.stats[f"arrival_{event.line}"] += 1

        self._discard_stale_heads()
        a = self.pending["A"][0] if self.pending["A"] else None
        b = self.pending["B"][0] if self.pending["B"] else None
        a_match = a is not None and a.seq_num == self.expected_seq
        b_match = b is not None and b.seq_num == self.expected_seq

        if a_match and b_match:
            if a.identity() != b.identity():
                self.stats["payload_conflict"] += 1
                raise ArbitrationConflict(
                    f"cycle {cycle}: SeqNum {self.expected_seq} has A/B payload conflict"
                )
            self.pending["A"].popleft()
            self.pending["B"].popleft()
            self.stats["duplicate_masked"] += 1
            selected = a
        elif a_match:
            self.pending["A"].popleft()
            self.stats["selected_A"] += 1
            selected = a
        elif b_match:
            self.pending["B"].popleft()
            self.stats["selected_B"] += 1
            selected = b
        else:
            self.stats["gap_wait_cycle"] += 1
            return False

        self.outputs.append(
            OutputEvent(
                decision_cycle=cycle,
                visible_cycle=cycle + PIPELINE_CYCLES,
                seq_num=selected.seq_num,
                selected_line=selected.line,
                payload=selected.payload,
            )
        )
        self.expected_seq += 1
        self.stats["accepted"] += 1
        return True

    def run(self, events: Iterable[FeedEvent], final_seq_exclusive: int) -> List[OutputEvent]:
        by_cycle: Dict[int, List[FeedEvent]] = defaultdict(list)
        latest_arrival = 0
        for event in events:
            if event.line not in self.pending:
                raise ValueError(f"Unknown line {event.line!r}")
            by_cycle[event.arrival_cycle].append(event)
            latest_arrival = max(latest_arrival, event.arrival_cycle)

        cycle = 0
        idle_limit = latest_arrival + 32
        while self.expected_seq < final_seq_exclusive:
            self.step(cycle, by_cycle[cycle])
            cycle += 1
            if cycle > idle_limit:
                raise StalledExpectedSeq(
                    f"expected SeqNum {self.expected_seq} did not arrive by cycle {cycle}"
                )
        return self.outputs


def payload_for(seq_num: int) -> int:
    """Deterministic 96-bit stand-in for the parsed fixed-field event payload."""
    return ((seq_num * 0x1F123BB5) ^ 0x5A5AA55AF00DCAFE) & ((1 << 96) - 1)


def normal_events(first_seq: int, count: int) -> List[FeedEvent]:
    """A/B replay with skew, a one-line loss, stale duplicate, and B reordering."""
    events: List[FeedEvent] = []
    for offset in range(count):
        seq = first_seq + offset
        payload = payload_for(seq)
        a_cycle = 2 * offset
        b_cycle = 2 * offset + 1

        # A same-cycle copy exercises deterministic duplicate masking.  Other
        # copies remain skewed and exercise late stale-duplicate removal.
        if seq == first_seq + 3:
            b_cycle = a_cycle

        # A drops one message; B covers it.  B is deliberately early for another
        # message, so the model must wait for expected SeqNum rather than emit it.
        if seq != first_seq + 5:
            events.append(FeedEvent("A", a_cycle, seq, payload))
        if seq == first_seq + 8:
            b_cycle -= 3
        events.append(FeedEvent("B", b_cycle, seq, payload))

    # A late second copy of an already accepted message must be removed as stale.
    events.append(FeedEvent("A", 31, first_seq + 2, payload_for(first_seq + 2)))
    return sorted(events, key=lambda item: (item.arrival_cycle, item.line, item.seq_num))


def test_happy_path() -> str:
    first_seq = 1000
    count = 16
    arbiter = DualLineReferenceArbiter(first_seq)
    outputs = arbiter.run(normal_events(first_seq, count), first_seq + count)

    assert [event.seq_num for event in outputs] == list(range(first_seq, first_seq + count))
    assert len({event.seq_num for event in outputs}) == count
    assert all(event.visible_cycle - event.decision_cycle == PIPELINE_CYCLES for event in outputs)
    assert arbiter.stats["duplicate_masked"] == 1
    assert arbiter.stats["selected_B"] > 0  # A loss is actually covered by B.
    assert arbiter.stats["stale_duplicate_drop"] > 0

    return (
        "PASS happy-path: "
        f"accepted={arbiter.stats['accepted']} duplicate_masked={arbiter.stats['duplicate_masked']} "
        f"selected_A={arbiter.stats['selected_A']} selected_B={arbiter.stats['selected_B']} "
        f"stale_drop={arbiter.stats['stale_duplicate_drop']} "
        f"gap_wait_cycles={arbiter.stats['gap_wait_cycle']} fixed_pipeline={PIPELINE_CYCLES}"
    )


def test_conflict_detection() -> str:
    arbiter = DualLineReferenceArbiter(77)
    events = [
        FeedEvent("A", 0, 77, payload_for(77)),
        FeedEvent("B", 0, 77, payload_for(77) ^ 1),
    ]
    try:
        arbiter.run(events, 78)
    except ArbitrationConflict:
        assert arbiter.stats["payload_conflict"] == 1
        return "PASS conflict-path: mismatched A/B payload stopped the fast candidate model"
    raise AssertionError("payload conflict was silently accepted")


def test_missing_sequence_detection() -> str:
    arbiter = DualLineReferenceArbiter(500)
    events = [FeedEvent("A", 0, 501, payload_for(501))]
    try:
        arbiter.run(events, 502)
    except StalledExpectedSeq:
        return "PASS gap-path: SeqNum+1 never bypassed missing expected SeqNum"
    raise AssertionError("gap was silently skipped")


def main() -> None:
    print("SnowSakura dual-line arbitration reference simulation")
    print(test_happy_path())
    print(test_conflict_detection())
    print(test_missing_sequence_detection())
    print("RESULT: PASS — all message-level arbitration assertions held")


if __name__ == "__main__":
    main()
