# methodology.md

# Methodology

The provided packet capture file was opened in Wireshark. The analysis focused on identifying internal and external hosts, protocols, ports, conversations, DNS queries, web traffic, and unusual connection attempts.

The following Wireshark tools were used:

## 1. Protocol Hierarchy

Path used:

`Statistics → Protocol Hierarchy`

This view was used to identify the main protocols inside the packet capture. It helped show that most traffic was TCP-based, with visible HTTP, TLS/HTTPS, DNS, UDP, ARP, XMPP, and FTP traffic.

## 2. Endpoints

Path used:

`Statistics → Endpoints → IPv4`

This view was used to identify internal and external IP addresses. Private IP ranges such as `10.0.2.x` and `192.168.1.1` were treated as internal/private addresses.

## 3. Conversations

Path used:

`Statistics → Conversations → IPv4`

This view was used to identify which hosts communicated with each other and which conversations used the most packets or bytes.

## 4. Display Filters

The following display filters were used:

```wireshark
dns
```

Used to inspect domain name lookups.

```wireshark
http
```

Used to inspect unencrypted web traffic.

```wireshark
tls
```

Used to inspect encrypted TLS/HTTPS traffic.

```wireshark
tcp.flags.syn == 1 && tcp.flags.ack == 0
```

Used to identify TCP connection attempts.

```wireshark
tcp.port != 80 && tcp.port != 443 && tcp.port != 53
```

Used to identify traffic using ports other than common web and DNS ports.

## 5. Screenshots

Screenshots were taken from Protocol Hierarchy, Endpoints, Conversations, DNS traffic, HTTP traffic, and unusual/non-standard traffic views. These screenshots are used as evidence in the final report.
