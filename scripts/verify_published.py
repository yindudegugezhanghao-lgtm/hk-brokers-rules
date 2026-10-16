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
remote = ROOT / ".build/downloaded"
remote.mkdir(exist_ok=True)
for name in ["HK_Brokers.list", "HK_Brokers.yaml", "HK_Brokers.mrs", "manifest.json", "validation.json", "SHA256SUMS"]:
    expected = (ROOT / ".build/rules" / name).read_bytes()
    for attempt in range(12):
        try:
            # Verify the exact subscription URLs users will enter. Only build
            # metadata uses a cache-busting query when a run republishes it.
            url = base + name
            if not name.startswith("HK_Brokers."):
                url += "?run=" + os.environ["GITHUB_RUN_ID"]
            req = urllib.request.Request(url,
                                         headers={"Cache-Control": "no-cache"})
            with urllib.request.urlopen(req, timeout=20) as response:
                data = response.read()
            if data != expected:
                raise ValueError("Published content differs (possibly stale CDN cache)")
            (remote / name).write_bytes(data)
            print(f"HTTPS 200 and byte comparison passed: {base + name}", flush=True)
            break
        except (OSError, ValueError) as exc:
            if attempt == 11:
                raise
            print(f"Waiting for GitHub raw propagation: {name}: {exc}", flush=True)
            time.sleep(5)
domains = sorted(d for group in manifest["brokers"].values() for d in group)
validate_all(ROOT / ".tools/mihomo", remote, domains)
with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
    summary.write("\nPublic HTTPS downloads matched build bytes. Downloaded MRS passed live routing tests again.\n")
