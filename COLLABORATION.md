# Collaboration

## Roadmap and availability

SnowSakura-FPGA is a continuing physical-layer engineering and evidence record, not a finished public release.

By my second-year summer at university, I will continue building SnowSakura and extend it across the full range of targeted binary market-data protocols. The public evidence chain will be expanded progressively as each layer is completed: protocol-validation results, post-route STA, SDF timing simulation, hardware link evidence, and measured results.

From my second-year summer onward, I will be available for either:

- **IP-isolated internship** arrangements; or
- **NDA-based technical engagements** that do not require an internship arrangement.

Firms, hedge funds, and specialist recruiters in **Hong Kong** or **Singapore** may contact me directly from that point onward.

## Potential technical scope

- Board-specific FPGA `.bit` delivery with the matching `.ltx` debug package where appropriate.
- Custom exchange-feed and proprietary binary-protocol framing, normalization, fixed-field parsing, registered state updates, and deterministic output release.
- GTH/GTY lane bring-up, reference-clock/reset ownership, polarity, buffer mode, Raw Mode, PRBS/BERT, Eye Scan, and ILA evidence.
- UltraScale+ physical implementation: FDRE/LUT/CARRY8 structure, fanout localization, Pblock/placement work, XDC/Tcl constraints, synthesis, implementation, and post-route STA.
- Protocol migration beyond HKEX OMD-C, provided that the wire format and target-hardware contract are defined.

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

## Delivery and IP boundary

A compiled bitstream is tied to an exact device, board, GT configuration, clocks, lane map, constraints, and protocol contract. A `.bit` file from one hardware identity is not a portable executable for another board. Delivery begins only after those inputs are frozen.

Private production RTL, GT integration, XDC/Tcl physical constraints, calibration logic, and board-specific implementation files are not published by default. Their availability depends on the agreed IP-isolation or NDA engagement scope.

## Contact

**Snow Elowen**  
Email: `ruansheng333@gmail.com`  
GitHub: [SnowElowen](https://github.com/SnowElowen)

When contacting me, include the target device, line rate, protocol name/specification, desired output, and evidence requirements in the first message.