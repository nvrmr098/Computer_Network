# Report Summary

## Overview
The provided Wireshark dump was analyzed to identify communication patterns, active protocols, likely user or application behaviour, and possible security concerns.

## Key Findings
The analysis focused on the network, transport, and application layers.  
By reviewing protocol hierarchy, endpoints, conversations, and filtered packet details, it was possible to identify the main communicating hosts, common services, and traffic patterns that may indicate either normal usage or suspicious external activity.

## Main Observations
- Internal and external communication could be distinguished using IP addressing.
- The packet dump revealed which protocols were most active.
- The observed traffic gave clues about user behaviour, network services, and system roles.
- Some traffic appeared unnecessary, suspicious, or unsuitable for the internal network context.

## Firewall Response
Based on the findings, a set of PERMIT and DROP firewall rules was proposed.  
The purpose of these rules is to allow only expected communication and block external traffic that does not normally belong in the network.

## Conclusion
Wireshark analysis is useful not only for packet inspection, but also for inferring network structure, application usage, and security risks.  
The final firewall rules should be refined using the exact IP addresses, ports, and protocols identified in the capture.