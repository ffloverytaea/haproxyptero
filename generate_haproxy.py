import os

haproxy_cfg = "/home/container/haproxy.cfg"

raw = os.environ.get("FORWARD_CFG", "")
lines = raw.replace(',', ' ').split()

haproxy_content = [
    "global",
    "    log stdout format raw daemon",
    "    maxconn 1000",
    "",
    "defaults",
    "    mode tcp",
    "    timeout connect 10s",
    "    timeout client 1m",
    "    timeout server 1m",
    ""
]

for i, line in enumerate(lines):
    if line.startswith("TCP:"):
        parts = line[4:].split("-")
        local_port = parts[0]
        remote = parts[1]
        haproxy_content.append(f"frontend tcp{i}")
        haproxy_content.append(f"    bind *:{local_port}")
        haproxy_content.append(f"    default_backend tcp{i}-out")
        haproxy_content.append("")
        haproxy_content.append(f"backend tcp{i}-out")
        haproxy_content.append(f"    server target {remote}")
        haproxy_content.append("")

with open(haproxy_cfg, "w") as f:
    f.write("\n".join(haproxy_content))

print(f"[+] HAProxy config generated with {len(lines)} rules.")
