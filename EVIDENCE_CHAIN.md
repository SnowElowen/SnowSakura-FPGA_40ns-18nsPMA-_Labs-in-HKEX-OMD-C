# SnowSakura-FPGA — Final Evidence Chain

## Final public release — 2026-07-25

This document is the final evidence index for the completed SnowSakura-FPGA public project. It separates real hardware, implemented timing, protocol behavior, and architectural targets so that no claim crosses an unmeasured boundary.

## Build identity

| Item | Final value |
|---|---|
| Repository | `SnowElowen/SnowSakura-FPGA_HKEX-OMD-C_40ns-Lab` |
| Device | Xilinx Zynq UltraScale+ `XCZU15EG-FFVB1156-2-I` |
| Serial rate | 10.3125 Gb/s |
| Optical direction | X0Y6/SFP2 TX → 10G-SR/OM4 → SFP1/X0Y7 RX |
| GT baseline | Raw Mode, RX Buffer ON, TX Buffer Bypass |
| Source ownership | Golden top fabric TX source |
| Protocol source | custom Raw32 HKEX OMD-C laboratory stream |
| Public state | completed and frozen |

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
- The recorded BERT depth is `10^8` bits.
- The 12.420 ns waveform covers four register intervals between five FF boundaries; it is fabric timing, not full optical latency.
- The approximately 50 ns single-lane result belongs to the tested RX Buffer ON architecture.
- The 36–37 ns RX/TX Double-Bypass blade is preserved only as an architecture target and is not labelled as completed hardware.

## Final acceptance result

The public project closes the intended independent laboratory scope: source ownership, physical link, registered receive boundary, bounded alignment, protocol reconstruction, stateful downstream logic, post-route timing, implemented timing simulation, and hardware observation form one consistent evidence chain.

The project is complete and frozen. Any future implementation begins as a separate private collaboration with its own build identity and evidence matrix.