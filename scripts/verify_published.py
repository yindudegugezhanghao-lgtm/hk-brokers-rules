"""Check public HTTPS assets from the Actions runner after atomic publication."""
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.request
from build import ROOT, cloud_only
from validate_runtime import validate_all

cloud_only()
manifest = json.loads((ROOT / ".build/rules/manifest.json").read_text())
repository = os.environ["GITHUB_REPOSITORY"]
base = f"https://raw.githubusercontent.com/{repository}/release/rules/"
immutable = f"https://raw.githubusercontent.com/{repository}/{os.environ['RELEASE_COMMIT']}/rules/"
remote = ROOT / ".build/downloaded"
remote.mkdir(exist_ok=True)
deadline = time.monotonic() + 360  # GitHub raw can cache a moving branch for 5 minutes.
for name in ["HK_Brokers.list", "HK_Brokers.yaml", "HK_Brokers_classical.yaml", "HK_Brokers.mrs", "HK_Brokers_Full.list", "HK_Brokers_Full.yaml", "HK_Brokers_Full_classical.yaml", "HK_Brokers_Full.mrs", "manifest.json", "validation.json", "SHA256SUMS"]:
    expected = (ROOT / ".build/rules" / name).read_bytes()
    for attempt in range(73):
        try:
            # Verify exact user subscription URLs. Run-specific metadata is
            # checked at the immutable published Git commit, not a cached branch.
            url = (base if name.startswith("HK_Brokers") else immutable) + name
            req = urllib.request.Request(url,
                                         headers={"Cache-Control": "no-cache"})
            with urllib.request.urlopen(req, timeout=20) as response:
                data = response.read()
            if data != expected:
                raise ValueError("Published content differs (possibly stale CDN cache)")
            (remote / name).write_bytes(data)
            print(f"HTTPS 200 and byte comparison passed: {url}", flush=True)
            break
        except (OSError, ValueError) as exc:
            if attempt == 72 or time.monotonic() >= deadline:
                raise
            print(f"Waiting for GitHub raw propagation: {name}: {exc}", flush=True)
            time.sleep(5)
domains = sorted(d for group in manifest["brokers"].values() for d in group)
validate_all(ROOT / ".tools/mihomo", remote, domains,
             sorted(d for group in manifest["full_brokers"].values() for d in group),
             manifest["full_ip_cidrs"])
with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
    summary.write("\nPublic HTTPS downloads matched build bytes. Downloaded MRS passed live routing tests again.\n")
