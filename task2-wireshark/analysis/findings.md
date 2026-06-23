# findings.md

# Wireshark Findings

## 1. Internal Network

The capture shows an internal network using the private subnet:

```text
10.0.2.0/24
```

The following internal IP addresses were observed:

| IP Address    | Observation                                               |
| ------------- | --------------------------------------------------------- |
| `10.0.2.1`    | Internal private host, likely gateway or DNS-related host |
| `10.0.2.2`    | Main internal client and most active host                 |
| `10.0.2.3`    | Internal client active in DNS and HTTP traffic            |
| `10.0.2.255`  | Broadcast address for the internal subnet                 |
| `192.168.1.1` | Private IP used for DNS/router-related communication      |

## 2. External Hosts

The capture shows communication with several public external IP addresses.

| External IP Address | Observed Activity                     |
| ------------------- | ------------------------------------- |
| `74.125.225.212`    | Google-related HTTP traffic           |
| `74.125.142.125`    | Gmail/XMPP traffic on TCP port `5222` |
| `63.241.108.124`    | HTTP request to an advertising server |
| `170.149.168.130`   | NYTimes-related web traffic           |
| `192.122.184.83`    | External HTTP connection              |
| `192.122.184.91`    | External HTTP connection              |
| `4.27.15.252`       | High-volume external endpoint         |
| `8.254.4.124`       | High-volume external endpoint         |

## 3. Protocols Observed

The Protocol Hierarchy view showed that the capture contained 22,650 packets. The main protocols were:

| Protocol    | Observation                                     |
| ----------- | ----------------------------------------------- |
| IPv4        | Main network layer protocol                     |
| TCP         | Dominant transport protocol                     |
| UDP         | Used mainly for DNS and discovery services      |
| DNS         | Domain name lookups                             |
| HTTP        | Unencrypted web traffic                         |
| TLS/HTTPS   | Encrypted web/application traffic               |
| ARP         | Local address resolution                        |
| XMPP        | Gmail/chat-related traffic                      |
| FTP         | File transfer traffic                           |
| DHCP        | Address configuration traffic                   |
| NetBIOS/SMB | Windows local network discovery/sharing traffic |

## 4. DNS Activity

The DNS traffic showed that internal hosts queried several domains and services, including:

| Domain / Service                | Meaning                             |
| ------------------------------- | ----------------------------------- |
| `dropbox.com`                   | Dropbox-related activity            |
| `notify20.dropbox.com`          | Dropbox notification/update traffic |
| `nytimes.com`                   | New York Times website access       |
| `www.nytimes.com`               | New York Times website access       |
| `css.nyt.com`                   | NYTimes webpage resources           |
| `js.nyt.com`                    | NYTimes JavaScript resources        |
| `graphics8.nytimes.com`         | NYTimes images/graphics             |
| `ad.doubleclick.net`            | Advertising/tracking                |
| `pagead2.googlesyndication.com` | Google advertising                  |
| `s0.2mdn.net`                   | Advertising/media content           |
| `e3191.c.akamaiedge.net`        | CDN content delivery                |

## 5. Web and Application Activity

The capture shows normal user activity such as:

* Web browsing
* DNS lookups
* Dropbox-related communication
* NYTimes website access
* Google/Gmail communication
* Loading images, JavaScript, JSON, and webpage resources

However, some traffic should be reviewed because it may not be suitable for a company network:

* Unencrypted HTTP traffic
* FTP traffic
* XMPP/Gmail chat traffic on TCP port `5222`
* Advertising and tracking traffic
* Repeated TCP SYN connection attempts
* Connections to unknown high-volume external IP addresses

## 6. Security Implications

Unencrypted HTTP can expose browsing information and should be replaced with HTTPS where possible. FTP is insecure and should normally be blocked unless there is a clear business reason. XMPP traffic may represent chat or personal communication and should only be allowed if approved by company policy. Advertising and tracking traffic is not required for business use and can be blocked using DNS or web filtering.
