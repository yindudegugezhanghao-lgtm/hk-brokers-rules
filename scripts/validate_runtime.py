"""Exercise the actual Mihomo parser and router on a GitHub Actions runner.

All target names resolve to a loopback fixture. No brokerage accounts, APIs,
quotes or trades are contacted by these routing tests.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import http.client
import json
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import threading
import time
import urllib.request

from build import ROOT, cloud_only

MARKER = b"HK_BROKERS_ROUTING_TEST_OK"
NEGATIVES = ["example.com", "hsbc.com.hk", "schwab.com", "htisec.com",
             "amazonaws.com", "myqcloud.com", "tradingview.com",
             "appsflyersdk.com", "googletagmanager.com"]


def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def validate_all(exe, out, domains):
    cloud_only()
    fixture_hits = []

    class Fixture(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path.startswith("/rules/"):
                filename = self.path.removeprefix("/rules/")
                if filename not in {"HK_Brokers.mrs", "HK_Brokers.yaml", "HK_Brokers.list", "HK_Brokers_classical.yaml"}:
                    self.send_error(404)
                    return
                body = (out / filename).read_bytes()
            else:
                fixture_hits.append(self.path)
                body = MARKER
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_):
            pass

    fixture = ThreadingHTTPServer(("127.0.0.1", 0), Fixture)
    thread = threading.Thread(target=fixture.serve_forever, daemon=True)
    thread.start()
    fixture_port = fixture.server_address[1]
    positives = [h for d in domains for h in (d, "api." + d, "quote.deep." + d)]
    negatives = NEGATIVES + [h for d in domains for h in ("not" + d, d + ".example.invalid")]
    all_hosts = {h: "127.0.0.1" for h in positives + negatives}
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    results = {"roundtrip": "passed", "providers": []}
    cases = [("HK_Brokers.list", "text", "classical", "file"),
             ("HK_Brokers.yaml", "yaml", "domain", "file"),
             ("HK_Brokers_classical.yaml", "yaml", "classical", "file"),
             ("HK_Brokers.mrs", "mrs", "domain", "file"),
             ("HK_Brokers.mrs", "mrs", "domain", "http"),
             ("HK_Brokers_classical.yaml", "yaml", "classical", "http")]
    try:
        for filename, format_, behavior, type_ in cases:
            with tempfile.TemporaryDirectory(dir=ROOT / ".build") as tmp:
                home = Path(tmp)
                (home / "rules").mkdir()
                proxy_port, api_port = free_port(), free_port()
                provider = {"type": type_, "behavior": behavior, "format": format_,
                            "path": "./rules/" + filename}
                if type_ == "file":
                    shutil.copyfile(out / filename, home / "rules" / filename)
                else:
                    provider.update(url=f"http://127.0.0.1:{fixture_port}/rules/{filename}",
                                    interval=86400, proxy="DIRECT")
                config = {
                    "mixed-port": proxy_port, "allow-lan": False, "mode": "rule",
                    "log-level": "info", "ipv6": False, "find-process-mode": "off",
                    "external-controller": f"127.0.0.1:{api_port}",
                    "hosts": all_hosts, "dns": {"enable": False},
                    "proxy-groups": [{"name": "BROKER_TEST", "type": "select", "proxies": ["DIRECT"]}],
                    "rule-providers": {"HK_Brokers": provider},
                    "rules": ["RULE-SET,HK_Brokers,BROKER_TEST", "MATCH,REJECT"],
                }
                config_path = home / "config.yaml"
                # JSON is a YAML-compatible serialization; no third-party writer.
                config_path.write_text(json.dumps(config), encoding="utf-8")
                command = [str(exe), "-d", str(home), "-f", str(config_path)]
                subprocess.run(command + ["-t"], check=True, timeout=30)
                with (home / "mihomo.log").open("w+") as log:
                    process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
                    try:
                        loaded = None
                        for _ in range(100):
                            if process.poll() is not None:
                                raise RuntimeError("Mihomo exited before provider initialization")
                            try:
                                with opener.open(f"http://127.0.0.1:{api_port}/providers/rules", timeout=1) as r:
                                    loaded = json.load(r).get("providers", {}).get("HK_Brokers", {})
                                if loaded.get("ruleCount") == len(domains):
                                    break
                            except (OSError, ValueError):
                                pass
                            time.sleep(0.1)
                        else:
                            raise AssertionError(f"Provider not loaded: {loaded}")
                        for n, host in enumerate(positives + negatives):
                            should_match = n < len(positives)
                            before = len(fixture_hits)
                            conn = http.client.HTTPConnection("127.0.0.1", proxy_port, timeout=3)
                            body = b""
                            try:
                                conn.request("GET", f"http://{host}:{fixture_port}/routing-test/{n}",
                                             headers={"Connection": "close"})
                                response = conn.getresponse()
                                body = response.read()
                            except (OSError, http.client.HTTPException):
                                if should_match:
                                    raise
                            finally:
                                conn.close()
                            reached = len(fixture_hits) == before + 1 and body == MARKER
                            if reached != should_match or (not should_match and len(fixture_hits) != before):
                                raise AssertionError(f"{type_}/{format_}: unexpected match for {host}")
                        results["providers"].append({
                            "type": type_, "format": format_, "behavior": behavior,
                            "rule_count": loaded["ruleCount"],
                            "positive_tests": len(positives), "negative_tests": len(negatives),
                            "result": "passed",
                        })
                    finally:
                        process.terminate()
                        try:
                            process.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            process.kill()
                            process.wait()
                        log.seek(0)
                        output = log.read()
                        print(output[-1600:], flush=True)
    finally:
        fixture.shutdown()
        fixture.server_close()
        thread.join(timeout=5)
    # An invalid/truncated MRS must not pass the official parser.
    with tempfile.TemporaryDirectory(dir=ROOT / ".build") as tmp:
        broken = Path(tmp) / "broken.mrs"
        broken.write_bytes((out / "HK_Brokers.mrs").read_bytes()[:8])
        attempt = subprocess.run([str(exe), "convert-ruleset", "domain", "mrs",
                                  str(broken), str(Path(tmp) / "dump.txt")], capture_output=True)
        if attempt.returncode == 0:
            raise AssertionError("Official parser accepted truncated MRS")
    results["corrupt_mrs_rejected"] = True
    results["scope"] = "GitHub-hosted runner; real Mihomo routing against loopback fixtures; no iPhone or authenticated brokerage tests"
    print(json.dumps(results, indent=2), flush=True)
    return results

