"""Generate optional Full edition from separately labelled community candidates.

This module intentionally does not loosen the official-evidence requirements
for the original 24-domain core rule set.
"""
import ipaddress
import re
import subprocess

SUFFIXES = {
    "com", "cn", "hk", "com.hk", "com.cn", "net", "link", "io",
    "ca", "global", "cloud", "sg", "com.sg", "com.au",
    "nz", "app", "financial",
}
BANNED = {"amazonaws.com", "cloudfront.net", "qcloud.com", "myqcloud.com",
          "appsflyersdk.com", "play-analytics.com", "schwab.com",
          "interactivebrokers.com", "tradingview.com", "htisec.com"}


def check_domain(name):
    if name != name.lower() or len(name) > 253:
        raise ValueError(f"Invalid Full domain: {name}")
    pieces = name.split(".")
    if any(not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", x)
           for x in pieces):
        raise ValueError(f"Invalid Full label: {name}")
    suffix = max((x for x in SUFFIXES if name.endswith("." + x)), key=len, default=None)
    if suffix is None or len(pieces) != len(suffix.split(".")) + 1:
        raise ValueError(f"Only main domains are allowed: {name}")
    if name in BANNED:
        raise ValueError(f"Forbidden third-party domain: {name}")


def collect_full(root, core_groups):
    src = root / "source-full"
    expected = {k + ".txt" for k in core_groups} | {"ip-cidr.txt"}
    if {p.name for p in src.iterdir()} != expected:
        raise ValueError("source-full must match the six broker sources and ip-cidr.txt")
    combined, all_domains = {}, set()
    for broker, base in core_groups.items():
        domains = set(base)
        for lineno, raw in enumerate((src / (broker + ".txt")).read_text(encoding="utf-8").splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.count(",") != 1 or not line.startswith("DOMAIN-SUFFIX,"):
                raise ValueError(f"Invalid Full domain rule: {broker}:{lineno}")
            name = line.split(",", 1)[1]
            check_domain(name)
            if name in domains:
                raise ValueError(f"Repeated Full source domain: {name}")
            domains.add(name)
        if len(set(domains) & all_domains):
            raise ValueError(f"Full broker domain duplicated across groups: {broker}")
        all_domains.update(domains)
        combined[broker] = sorted(domains)
    if any(a != b and a.endswith("." + b) for a in all_domains for b in all_domains):
        raise ValueError("Full domain already covered by another suffix")
    ips = []
    for lineno, raw in enumerate((src / "ip-cidr.txt").read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(",")
        if len(parts) != 3 or parts[0] != "IP-CIDR" or parts[2] != "no-resolve":
            raise ValueError(f"Invalid Full IP-CIDR rule: {lineno}")
        network = ipaddress.ip_network(parts[1], strict=True)
        if not isinstance(network, ipaddress.IPv4Network) or not network.is_global:
            raise ValueError(f"Non-public Full network: {network}")
        if str(network) in ips:
            raise ValueError(f"Duplicate Full network: {network}")
        ips.append(str(network))
    return combined, sorted(all_domains), sorted(ips)


def classical_yaml(domains, ips):
    rules = [f"DOMAIN-SUFFIX,{d}" for d in domains]
    rules += [f"IP-CIDR,{n},no-resolve" for n in ips]
    return "payload:\n" + "".join(f"  - '{rule}'\n" for rule in rules)


def write_full(exe, out, broker_titles, groups, domains, ips):
    lines = ["# Community Full edition: shared IP networks may affect other applications."]
    for broker, title in broker_titles.items():
        lines.extend(["", f"# {title}"])
        lines.extend(f"DOMAIN-SUFFIX,{x}" for x in groups[broker])
    lines.extend(["", "# Shared-cloud IP ranges and other unverified community CIDRs"])
    lines.extend(f"IP-CIDR,{x},no-resolve" for x in ips)
    (out / "HK_Brokers_Full.list").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "HK_Brokers_Full_classical.yaml").write_text(classical_yaml(domains, ips), encoding="utf-8")
    (out / "HK_Brokers_Full.yaml").write_text(
        "payload:\n" + "".join(f"  - '+.{x}'\n" for x in domains), encoding="utf-8")
    subprocess.run([str(exe), "convert-ruleset", "domain", "yaml",
                    str(out / "HK_Brokers_Full.yaml"), str(out / "HK_Brokers_Full.mrs")],
                   check=True)
    dump = out / "full-roundtrip.txt"
    subprocess.run([str(exe), "convert-ruleset", "domain", "mrs",
                    str(out / "HK_Brokers_Full.mrs"), str(dump)], check=True)
    if dump.read_text().splitlines() != ["+." + x for x in domains]:
        raise ValueError("Full MRS roundtrip mismatch")
    dump.unlink()
