"""Validate human-reviewed sources; compile MRS only on GitHub-hosted Actions."""
import argparse
import datetime as dt
import gzip
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SUFFIXES = {"com", "cn", "hk", "com.hk", "com.cn"}
# Explicit backstop, not an ownership classifier. All additions also need review.
FORBIDDEN = {
    "amazonaws.com", "cloudfront.net", "aliyuncs.com", "qcloud.com",
    "myqcloud.com", "azureedge.net", "akamai.net", "akamaized.net",
    "appsflyersdk.com", "play-analytics.com", "googletagmanager.com",
    "google-analytics.com", "udesk.cn", "tradingview.com", "b-cdn.net",
    "hsbc.com.hk", "hsbc.com", "za.group", "schwab.com", "ibkr.com",
    "htisec.com",  # Haitong, not Huatai International.
}


def cloud_only():
    if (os.environ.get("GITHUB_ACTIONS") != "true"
            or os.environ.get("RUNNER_ENVIRONMENT") != "github-hosted"):
        raise RuntimeError("MRS build/test/publish is restricted to GitHub-hosted Actions")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate_domain(domain):
    if domain in PUBLIC_SUFFIXES:
        raise ValueError(f"Public suffix is not a registrable domain: {domain}")
    if len(domain) > 253 or domain != domain.lower():
        raise ValueError(f"Invalid lowercase domain: {domain}")
    try:
        ipaddress.ip_address(domain)
    except ValueError:
        pass
    else:
        raise ValueError(f"IP address forbidden: {domain}")
    labels = domain.split(".")
    if any(not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", s)
           for s in labels):
        raise ValueError(f"Invalid domain: {domain}")
    suffix = max((s for s in PUBLIC_SUFFIXES if domain.endswith("." + s)),
                 key=len, default=None)
    if suffix is None or len(labels) != len(suffix.split(".")) + 1:
        raise ValueError(f"Only registrable main domains with reviewed suffixes: {domain}")
    if any(domain == d or domain.endswith("." + d) for d in FORBIDDEN):
        raise ValueError(f"Out-of-scope domain: {domain}")


def collect(root=ROOT):
    brokers = json.loads((root / "brokers.json").read_text(encoding="utf-8"))
    if not brokers or any(not re.fullmatch(r"[a-z][a-z0-9_-]*", k) for k in brokers):
        raise ValueError("Invalid broker registry")
    expected = {f"{k}.txt" for k in brokers}
    if {p.name for p in (root / "source").iterdir()} != expected:
        raise ValueError("source/ must exactly match the broker registry")
    by_broker, seen = {}, set()
    for broker in brokers:
        domains = []
        for lineno, raw in enumerate((root / "source" / f"{broker}.txt").read_text(
                encoding="utf-8").splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if not line.startswith("DOMAIN-SUFFIX,") or line.count(",") != 1:
                raise ValueError(f"{broker}:{lineno}: DOMAIN-SUFFIX only")
            domain = line.split(",")[1]
            validate_domain(domain)
            if domain in seen:
                raise ValueError(f"Duplicate rule: {domain}")
            seen.add(domain)
            domains.append(domain)
        if not domains:
            raise ValueError(f"Empty broker source: {broker}")
        by_broker[broker] = sorted(set(domains))
    for domain in seen:
        if any(domain.endswith("." + other) for other in seen if other != domain):
            raise ValueError(f"Redundant covered subdomain: {domain}")
    records = json.loads((root / "docs/domains.json").read_text(encoding="utf-8"))
    if len(records) != len(seen) or {r["domain"] for r in records} != seen:
        raise ValueError("Evidence ledger and enabled sources differ")
    for record in records:
        if record["domain"] not in by_broker.get(record["broker"], []):
            raise ValueError("Evidence broker mismatch")
        dt.date.fromisoformat(record["verified_on"])
        if not record.get("reason") or not record.get("change"):
            raise ValueError("Evidence needs reason and change history")
        official = [s for s in record["sources"] if s["kind"] == "official"]
        if not official or any(not s["url"].startswith("https://") for s in official):
            raise ValueError("Each domain needs an official HTTPS source")
    return brokers, by_broker, sorted(seen)


def install_mihomo():
    cloud_only()
    lock = json.loads((ROOT / "tools.lock.json").read_text())["mihomo"]
    request = urllib.request.Request(lock["url"], headers={"User-Agent": "HK-Broker-Rules-CI"})
    with urllib.request.urlopen(request, timeout=120) as response:
        compressed = response.read()
    if digest(compressed) != lock["sha256"]:
        raise ValueError("Mihomo download SHA256 mismatch")
    exe = ROOT / ".tools/mihomo"
    exe.parent.mkdir(exist_ok=True)
    exe.write_bytes(gzip.decompress(compressed))
    exe.chmod(0o755)
    version = subprocess.check_output([str(exe), "-v"], text=True).strip()
    if f"v{lock['version']}" not in version:
        raise ValueError(f"Unexpected Mihomo version: {version}")
    print(version, flush=True)
    return exe, version


def classical_yaml(domains):
    return "payload:\n" + "".join(f"  - 'DOMAIN-SUFFIX,{d}'\n" for d in domains)


def compile_rules(exe, out, brokers, by_broker, domains):
    cloud_only()
    out.mkdir(parents=True, exist_ok=True)
    lines = ["# Generated; edit source/*.txt and docs/domains.json instead."]
    for key, title in brokers.items():
        lines.extend(["", f"# {title}"])
        lines.extend(f"DOMAIN-SUFFIX,{d}" for d in by_broker[key])
    (out / "HK_Brokers.list").write_text("\n".join(lines) + "\n", encoding="utf-8")
    yaml = "payload:\n" + "".join(f"  - '+.{d}'\n" for d in domains)
    (out / "HK_Brokers.yaml").write_text(yaml, encoding="utf-8")
    (out / "HK_Brokers_classical.yaml").write_text(classical_yaml(domains), encoding="utf-8")
    subprocess.run([str(exe), "convert-ruleset", "domain", "yaml",
                    str(out / "HK_Brokers.yaml"), str(out / "HK_Brokers.mrs")], check=True)
    dump = out / "roundtrip.txt"
    subprocess.run([str(exe), "convert-ruleset", "domain", "mrs",
                    str(out / "HK_Brokers.mrs"), str(dump)], check=True)
    actual = dump.read_text().splitlines()
    if actual != ["+." + d for d in domains]:
        raise ValueError(f"MRS round-trip mismatch: {actual}")
    dump.unlink()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    brokers, by_broker, domains = collect()
    print(f"Validated {len(domains)} domains across {len(brokers)} brokers", flush=True)
    if args.validate_only:
        return
    cloud_only()
    exe, version = install_mihomo()
    out = ROOT / ".build/rules"
    compile_rules(exe, out, brokers, by_broker, domains)
    # Import only after the cloud guard: no local MRS execution.
    from validate_runtime import validate_all
    results = validate_all(exe, out, domains)
    manifest = {
        "domain_count": len(domains), "brokers": by_broker,
        "source_commit": os.environ["GITHUB_SHA"],
        "workflow_run": f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/actions/runs/{os.environ['GITHUB_RUN_ID']}",
        "mihomo": version,
        "built_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "files": {p.name: digest(p.read_bytes()) for p in sorted(out.glob("HK_Brokers*"))},
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "validation.json").write_text(json.dumps(results, indent=2) + "\n")
    (out / "SHA256SUMS").write_text("".join(
        f"{digest(p.read_bytes())}  {p.name}\n" for p in sorted(out.iterdir())
        if p.is_file() and p.name != "SHA256SUMS"))
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(f"## HK Broker Rules\n\n{len(domains)} domains; Mihomo {version}\n\n"
                    "Source validation, MRS round-trip and live routing tests passed.\n\n"
                    "```json\n" + json.dumps(results, indent=2) + "\n```\n")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError) as exc:
        sys.exit(str(exc))
