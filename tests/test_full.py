import ipaddress
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build import collect
from full import collect_full, classical_yaml, check_domain


class FullBuildTests(unittest.TestCase):
    def test_full_counts_and_core_preserved(self):
        _, core, original = collect()
        self.assertEqual(len(original), 24)
        groups, domains, cidrs = collect_full(ROOT, core)
        self.assertEqual(len(domains), 132)
        self.assertEqual(len(cidrs), 94)
        self.assertEqual([len(groups[k]) for k in core], [51, 42, 15, 7, 11, 6])
        self.assertEqual(len(classical_yaml(domains, cidrs).splitlines()), 1 + 132 + 94)
        self.assertEqual(len(set(domains)), 132)
        self.assertEqual(len(set(cidrs)), 94)

    def test_covers_observed_futu_ip_examples(self):
        _, core, _ = collect()
        _, _, cidrs = collect_full(ROOT, core)
        networks = [ipaddress.ip_network(x) for x in cidrs]
        for addr in ["183.60.225.225", "106.55.66.56", "119.91.245.125", "119.29.48.17"]:
            self.assertTrue(any(ipaddress.ip_address(addr) in net for net in networks), addr)

    def test_rejects_third_party_main_domains(self):
        for d in ["qcloud.com", "appsflyersdk.com", "schwab.com", "tradingview.com"]:
            with self.subTest(d=d), self.assertRaises(ValueError):
                check_domain(d)


if __name__ == "__main__":
    unittest.main()
