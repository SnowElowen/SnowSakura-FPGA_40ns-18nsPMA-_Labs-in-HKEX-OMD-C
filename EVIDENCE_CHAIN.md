# SnowSakura-FPGA — Evidence Chain and Final Parser Campaign

## Final public development interval — 2026-07-24

The HKEX OMD-C Exchange Feed Simulator and its downstream laboratory chain are complete, sealed, and retained as the Golden hardware source. SnowSakura now enters the final single-lane parser campaign.

Approximately **two to three months** are reserved for implementation, physical closure, and measurement without incremental public performance claims. **This is the last interim project update. The next repository update will be the final SnowSakura single-lane parser evidence package.**

Thank you to everyone who has watched, cloned, reviewed, challenged, or followed this work from simulation through real ZU15EG optical hardware.

---

## Frozen baseline identity

| Item | Frozen value |
|---|---|
| Repository | `SnowElowen/SnowSakura-FPGA_HKEX-OMD-C_40ns-Lab` |
| Baseline commit | [`03a769df45f8a6ac3244041a4167159c4bc82d85`](https://github.com/SnowElowen/SnowSakura-FPGA_HKEX-OMD-C_40ns-Lab/commit/03a769df45f8a6ac3244041a4167159c4bc82d85) |
| Primary device | Xilinx Zynq UltraScale+ `XCZU15EG-FFVB1156-2-I` |
| Serial rate | 10.3125 Gb/s |
| Proven optical direction | GTHE4_CHANNEL_X0Y6 / SFP2 TX → 10G-SR → OM4 → SFP1 / GTHE4_CHANNEL_X0Y7 RX |
| Frozen receive baseline | GTH Raw Mode, RX Buffer ON |
| Frozen transmit baseline | TX Buffer Bypass |
| Golden source | Custom Raw32 HKEX OMD-C laboratory feed |
| Active work | Final single-lane parser campaign |

The baseline commit is the public identity of the completed simulator. Later parser work must not silently change the meaning of this frozen evidence.

---

## Completed evidence chain

| Boundary | Public artifact | Exact observation | Evidence level |
|---|---|---|---|
| GT TX → optics → GT RX | [In-System IBERT Eye Scan](img/2026-07-23_ibert_eye_scan_open_ui_77_78.png) | X0Y7 RX sampler reports open UI 77.78% and open area 6720 at the configured 1e-10 dwell BER setting | Real hardware / analog receiver sampling |
| Raw32 receive and alignment | [RX capture and parser fields](img/2026-07-23_rx_capture_parser_fields.png) | `align_locked = 1`; registered 12-word capture advances through the programmed packet | Real hardware / RXUSRCLK-domain ILA |
| Packet-valid chain | [Packet-valid to parsed-valid](img/2026-07-23_packet_valid_parsed_valid.png) | `capture_index = 0...11`, then one-cycle `packet_valid`, then one-cycle `parsed_valid`; `parsed_error = 0` | Real hardware / cycle contract |
| Continuous packet stream | [Continuous multi-packet parser](img/2026-07-23_continuous_multi_packet_parser.png) | Repeated Add/Modify output across two-message, Heartbeat, and one-message packet forms | Real hardware / repeated protocol activity |
| Parser → state update | [Parser-to-book closure](img/2026-07-23_exchange_simulator_book_closure.png) | Repeated parser events drive the registered order-state laboratory chain with `position_error = 0` | Real hardware / stateful datapath |
| Book → registered export | [Top-of-book and snapshot](img/2026-07-23_exchange_simulator_snapshot_closure.png) | Snapshot version 1; offer level `0x12`; price `0x00007A12`; aggregate quantity `0x00000000000003E8` | Real hardware / registered output |
| Functional implementation chain | [Current progress](CURRENT_PROGRESS.md) | Simulation, synthesis, implementation, post-route timing, bitstream/ILA regression, and final Eye Scan are recorded for the sealed laboratory build | Cross-layer closure record |

### Protocol arithmetic locked by the evidence

| Packet form | Arithmetic | Encoded `PktSize / MsgCount` |
|---|---:|---:|
| Add Order | 16-byte Packet Header + 32-byte Msg30 | `16'h0030 / 1` |
| Heartbeat | 16-byte Packet Header and no message | `16'h0010 / 0` |
| Packed Add + Modify | 16-byte Packet Header + 32-byte Msg30 + 28-byte Msg31 | `16'h004C / 2` |

The Heartbeat has no message. Any held `MsgType` value is ignored when `MsgCount = 0`.

### Evidence scope kept separate

- The Eye Scan is receiver sampling-margin evidence for the tested X0Y6-to-X0Y7 optical path.
- The current BERT exercise depth is `10^8` bits. The final long-duration BER result will report its actual tested bit count and elapsed time.
- Add and Modify are exercised through the programmed hardware stream. Delete is closed in isolated RTL simulation in the sealed laboratory chain.
- The Golden source is a custom Raw32 laboratory stream. It is not described as an external production 10GBASE-R Ethernet feed.
- RX Buffer ON is the frozen delivery baseline. The 36–37 ns RX/TX Buffer Bypass blade remains a separate physical configuration and requires its own matched evidence.

---

## Final single-lane parser acceptance matrix

The final update will be published as one evidence package. A target becomes a completed claim only when the matching row is present.

| Final evidence | Required record | Pass condition |
|---|---|---|
| Build identity | Source commit, device, XCI/GT configuration identity, buffer mode, BIT/LTX pairing, clock ownership | One reproducible configuration; no mixed artifacts |
| Input contract | Registered parser input boundary, byte-0 definition, valid/start/complete semantics, supported message matrix | Every fixed slice maps to a documented byte offset |
| Protocol correctness | Packet/message lengths, Little-Endian reconstruction, Heartbeat behavior, sequence semantics, malformed-input handling | Reference vectors and RTL outputs agree byte-for-byte |
| Cycle contract | Source FDRE/Q → combinational logic → destination FDRE/D for every stage | Fixed latency; no hidden FIFO or uncounted pipeline |
| Physical topology | FDRE, LUT6/LUT5, CARRY8, MUXF7/F8, fanout and control-set audit | GTH RX Data Path remains at or below two LUT levels |
| Post-route STA | Setup, hold, logic levels, route delay, clock interaction, exceptions, high-fanout nets and unconstrained paths | WNS > 0, WHS > 0, zero failing endpoints, zero unintended unconstrained paths |
| Timing simulation | Post-implementation SDF with the same netlist and constraints | Expected pipeline/output contract survives annotated delay |
| Hardware parser regression | Continuous packet stream, accepted fields, valid/error counters and reset recovery | No unexplained parse errors or event loss in the recorded run |
| BER qualification | Exact pattern, direction, bit count, elapsed time and error count | Result reported from the tested configuration, without extrapolating beyond the measured count |
| Latency measurement | Exact start/end pins or registered boundaries, clock mode, sample count and observed distribution | Buffered single-lane result reported in ns for the measured build |
| Public claim boundary | Raw32 laboratory input versus production 10GBASE-R normalization stated explicitly | Published headline matches the hardware boundary actually tested |

If the final build uses RX Buffer ON, its measured buffered latency will be reported as the delivery result. A 36–37 ns result will be published only if the separate RX/TX Buffer Bypass configuration independently passes the same matrix.

---

## Frozen engineering rules for the final campaign

- Do not reopen the completed Exchange Feed Simulator, optical direction, Golden packet source, or sealed downstream laboratory chain without a new failure record.
- Do not substitute a clean functional waveform for post-route timing, or an Eye Scan for a long-duration BER result.
- Do not count PCS/Ethernet normalization inside parser latency unless those blocks are physically present and included in the measured boundary.
- Do not allow runtime barrel shifters, uncontrolled priority scans, Async FIFO, vendor MAC/AXI buffering, or hidden pipeline stages into the latency-critical path.
- Do not publish an intermediate latency number. The next number is the measured final result tied to one exact build.

---

## Closing note

SnowSakura began as an independent physical-layer engineering record and reached a real optical ZU15EG system through repeated simulation, synthesis, implementation, routed timing, GT diagnosis, ILA observation, and receiver measurement.

The laboratory source is finished. The remaining work is the final parser.

**The next update will be the final evidence package. Thank you for watching.**
