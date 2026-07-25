# SnowSakura-FPGA — Final Completed State

## Status

**Completed and frozen on 2026-07-25.**

The public SnowSakura-FPGA development cycle is finished. The final repository state records a real Puzhi ZU15EG optical laboratory chain, fabric-owned programmed transmission, Raw32 registered reception, bounded alignment, fixed HKEX OMD-C parsing, stateful order updates, 64-bit price-level aggregation, top-of-book selection, coherent snapshot export, implementation timing closure, Post-Implementation Timing Simulation, ILA evidence, and receiver Eye Scan evidence.

There is no active public next stage and no scheduled stream of incremental updates. The repository is retained as the final technical record and as the entry point for private bitstream or custom-protocol work.

## Frozen hardware identity

| Item | Frozen value |
|---|---|
| Device | `XCZU15EG-FFVB1156-2-I` |
| Serial rate | 10.3125 Gb/s |
| Physical direction | X0Y6/SFP2 TX → 10G-SR → OM4 → SFP1/X0Y7 RX |
| Receive baseline | GTH Raw Mode, RX Buffer ON |
| Transmit baseline | TX Buffer Bypass |
| Golden source | fabric-owned custom Raw32 OMD-C laboratory stream |
| User-clock class | 322.265625 MHz operating point / 322.56 MHz timing target |
| Registered fabric pipeline | RX ×3 + Parser ×1 + TX ×1 |

## Final evidence

| Boundary | Result |
|---|---|
| TX ownership | ILA captures frame start, busy state, sequential indices, and complete programmed data |
| Optical path | real SFP2/X0Y6 TX → OM4 → SFP1/X0Y7 RX |
| Eye Scan | 77.78% open UI and open area 6720 at configured `1e-10` dwell BER |
| BERT exercise | `10^8` recorded bits |
| Alignment | stable `align_locked = 1` |
| Parser | repeated `parsed_valid`, `parsed_error = 0` |
| Protocol forms | Add, Modify, two-message packet, and Heartbeat packet arithmetic demonstrated |
| Book state | Order State Delta, 64-bit aggregation, Top-of-Book, versioned snapshot |
| Implemented timing | WNS `+0.239 ns`, WHS `+0.017 ns`, zero failing endpoints |
| RX local path | 0 LUT levels, 0.546 ns delay, `+0.379 ns` slack under 0.900 ns |
| Implemented fabric timing | 12.420 ns across four intervals between five registered boundaries |

## Closed chain

~~~text
Golden fabric TX
    -> GTH/SFP/OM4/GTH RX
    -> registered Raw32 capture
    -> bounded marker/alignment
    -> 12 x 32-bit packet capture
    -> fixed Message 0 parser
    -> Order State Delta
    -> 64-bit Price-Level Aggregator
    -> Top-of-Book
    -> versioned Register Snapshot
~~~

Simulation, synthesis, implementation, post-route timing, bitstream/ILA regression, Post-Implementation Timing Simulation, and Eye Scan are all represented in the final evidence package.

## Final boundary

The completed public build uses a custom Raw32 laboratory source and RX Buffer ON. It is not a production 10GBASE-R HKEX feed, and the separate 36–37 ns RX/TX Double-Bypass architecture is not presented as a measured result.

Future engineering, if any, is private and contract-driven: a defined target board, GT/clock configuration, protocol wire format, expected outputs, test vectors, and acceptance matrix. See [COLLABORATION.md](COLLABORATION.md).