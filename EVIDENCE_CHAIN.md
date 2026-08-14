# SnowSakura-FPGA — Preserved Evidence Chain

## Preserved hardware release — 2026-07-25

## Active development resumed — 2026-08-14 UTC

This document is the preserved evidence index for SnowSakura-FPGA. Active development resumed on 2026-08-14 UTC. It separates real hardware, implemented timing, protocol behavior, and architectural targets so that no claim crosses an unmeasured boundary.

## Build identity

| Item | Preserved value |
|---|---|
| Repository | `SnowElowen/SnowSakura-FPGA_HKEX-OMD-C_40ns-Lab` |
| Device | Xilinx Zynq UltraScale+ `XCZU15EG-FFVB1156-2-I` |
| Serial rate | 10.3125 Gb/s |
| Optical direction | X0Y6/SFP2 TX → 10G-SR/OM4 → SFP1/X0Y7 RX |
| GT baseline | Raw Mode, RX Buffer ON, TX Buffer Bypass |
| Source ownership | Golden top fabric TX source |
| Protocol source | custom Raw32 HKEX OMD-C laboratory stream |
| Public state | active development resumed 2026-08-14 UTC; preserved single-line RX Buffer ON evidence |

## Evidence matrix

| Boundary | Public artifact | Exact observation | Evidence level |
|---|---|---|---|
| Golden top TX launch | [TX frame launch](img/2026-07-25_ila_tx_frame_launch.png) | frame start, busy transition, first programmed word | real hardware ILA |
| Golden top complete TX frame | [Complete frame](img/2026-07-25_ila_tx_complete_frame.png) | sequential word indices and programmed words before idle | real hardware ILA |
| Optical receiver margin | [IBERT Eye Scan](img/2026-07-23_ibert_eye_scan_open_ui_77_78.png) | open UI 77.78%, open area 6720, configured `1e-10` dwell BER | real hardware RX sampler |
| Raw32 receive/alignment | [RX capture](img/2026-07-23_rx_capture_parser_fields.png) | `align_locked = 1`, registered 12-word capture | real hardware RXUSRCLK ILA |
| Packet-to-parser contract | [Valid-chain capture](img/2026-07-23_packet_valid_parsed_valid.png) | capture index 0…11, packet-valid pulse, parsed-valid pulse, no parsed error | real hardware ILA |
| Repeated packet handling | [Continuous parser](img/2026-07-23_continuous_multi_packet_parser.png) | repeated Add/Modify output across two-message, Heartbeat, and one-message forms | real hardware ILA |
| Parser-to-state | [Book closure](img/2026-07-23_exchange_simulator_book_closure.png) | registered order-state activity with `position_error = 0` | real hardware ILA |
| Registered book export | [Snapshot closure](img/2026-07-23_exchange_simulator_snapshot_closure.png) | version 1, offer level `0x12`, price `0x00007A12`, quantity `0x3E8` | real hardware ILA |
| Five registered boundaries | [Post-Implementation Timing Simulation](img/2026-07-25_post_impl_rx3_parser1_tx1.png) | 12.420 ns across four intervals of RX3 + Parser1 + TX1 | implemented netlist simulation |
| Full implemented timing | [Timing summary](img/2026-07-25_post_impl_timing_summary.jpeg) | WNS `+0.239 ns`, WHS `+0.017 ns`, zero failing endpoints | post-route STA |
| RX registered boundary | [0.900 ns path audit](img/2026-07-25_rx_registered_path_0900ns.png) | 0 LUT levels, 0.546 ns total, `+0.379 ns` slack | post-route STA |

## Protocol arithmetic

| Packet | Byte arithmetic | Encoded value |
|---|---:|---:|
| Add Order | 16-byte Packet Header + 32-byte Msg30 | `PktSize = 16'h0030`, `MsgCount = 1` |
| Heartbeat | 16-byte Packet Header, no message | `PktSize = 16'h0010`, `MsgCount = 0` |
| Add + Modify | 16-byte Packet Header + 32-byte Msg30 + 28-byte Msg31 | `PktSize = 16'h004C`, `MsgCount = 2` |

The Heartbeat has no MsgType. Any retained MsgType bus value is invalid when `MsgCount = 0` and is ignored.

## Claim boundaries

- The programmed Raw32 laboratory stream proves the stated laboratory datapath; it is not a production 10GBASE-R venue input.
- The Eye Scan measures receiver sampling margin; it is not a substitute for a long-duration BER count.
- The current recorded BERT depth is `10^8` bits. A final `10^15`-bit counter record and matching Eye Scan will be appended only after the run is complete.
- The 12.420 ns waveform covers four register intervals between five FF boundaries; it is fabric timing, not full optical latency.
- The approximately 50 ns single-lane result belongs to the tested RX Buffer ON architecture.
- The 36–37 ns RX/TX Double-Bypass blade is preserved only as an architecture target and is not labelled as completed hardware.

## Active continuation boundary

The next engineering deliverable is a self-owned dual-line A/B arbitration simulation. It is outside the tested single-line RX Buffer ON physical result and therefore begins with a separate simulation evidence matrix: stimulus provenance, source-line timing, event and payload scoreboards, fixed-cycle latency checks, duplicate/gap/reorder cases, and explicit pass/fail counters.

A final X0Y7/SFP1 `10^15`-bit BER run and matching Eye Scan remain separate physical measurement tasks. They do not establish Double-Bypass or dual-line arbitration behaviour.

## Preserved acceptance result

The preserved single-line laboratory scope establishes source ownership, physical link, registered receive boundary, bounded alignment, protocol reconstruction, stateful downstream logic, post-route timing, implemented timing simulation, and hardware observation as one evidence chain.

The active dual-line arbitration stage begins in this repository with its own build identity and evidence matrix. It must not inherit the single-line RX Buffer ON timing or optical results as Double-Bypass proof.