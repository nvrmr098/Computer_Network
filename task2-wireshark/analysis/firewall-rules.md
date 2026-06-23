# Firewall Rules

| Rule | Action | Source | Destination | Protocol/Port | Description |
|---:|---|---|---|---|---|
| 1 | PERMIT | 10.0.2.0/24 | 192.168.1.1 | UDP/TCP 53 | Allow DNS queries |
| 2 | PERMIT | 10.0.2.0/24 | External web servers | TCP 443 | Allow HTTPS |
| 3 | PERMIT | 10.0.2.0/24 | Approved web servers | TCP 80 | Allow required HTTP only |
| 4 | DROP | External networks | 10.0.2.0/24 | Any | Block unsolicited inbound traffic |
| 5 | DROP | 10.0.2.0/24 | External hosts | TCP 21 | Block FTP |
| 6 | DROP | 10.0.2.0/24 | External hosts | TCP 5222 | Block XMPP if not approved |
| 7 | DROP | 10.0.2.0/24 | Ad/tracking domains | HTTP/HTTPS | Block advertising/tracking |
| 8 | DROP | Any | Any | Any | Default deny |