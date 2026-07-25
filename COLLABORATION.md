# Private Bitstream and Protocol Collaboration

SnowSakura-FPGA is complete as a public project, but the engineering can be applied privately to a defined board and protocol.

## Available collaboration

- Board-specific FPGA `.bit` delivery with the matching `.ltx` debug package when appropriate.
- Custom exchange-feed and proprietary binary-protocol framing, normalization, fixed-field parsing, registered state updates, and deterministic output release.
- GTH/GTY lane bring-up, reference-clock/reset ownership, polarity, buffer-mode, Raw Mode, PRBS/BERT, Eye Scan, and ILA evidence.
- UltraScale+ physical implementation: FDRE/LUT/CARRY8 structure, fanout localization, Pblock/placement work, XDC/Tcl constraints, synthesis, implementation, and post-route STA.
- Protocol migration beyond HKEX OMD-C, provided that the wire format and target hardware contract are defined.

## Required technical contract

A serious request should provide:

1. target FPGA part number and board revision;
2. GT lane/pin map, reference-clock frequency, optics/cable path, and intended line rate;
3. line coding and transport boundary, such as Raw serial data, 64b/66b, Ethernet/IPv4/UDP, or a proprietary frame;
4. protocol specification and legal test vectors;
5. required parsed fields, output interface, and reset/CDC ownership;
6. latency boundary and clock frequency;
7. acceptance criteria for functional simulation, post-route STA, hardware ILA, BER/Eye Scan, and measured latency;
8. whether the deliverable is a private `.bit/.ltx` package, an integration build, architecture review, or protocol implementation.

## Delivery boundary

A compiled bitstream is tied to an exact device, board, GT configuration, clocks, lane map, constraints, and protocol contract. A `.bit` file from one hardware identity is not a portable executable for another board. Therefore delivery begins only after those inputs are frozen.

Private production RTL, GT integration, XDC/Tcl physical constraints, calibration logic, and board-specific implementation files are not published by default. Their availability depends on the agreed collaboration scope.

## Protocol scope

The architecture is protocol-independent at the registered normalization boundary. I can implement other exchange feeds, Ethernet-derived market-data formats, and proprietary binary protocols; the required PCS/framing work is explicitly included when the incoming wire stream requires it and is never hidden inside parser latency.

## Contact

**Snow Elowen**  
Email: `ruansheng333@gmail.com`  
GitHub: [SnowElowen](https://github.com/SnowElowen)

When contacting me, include the target device, line rate, protocol name/specification, desired output, and evidence requirements in the first message.