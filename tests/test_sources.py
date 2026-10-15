import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build import ROOT, collect, validate_domain, cloud_only


class SourceValidation(unittest.TestCase):
    def test_reviewed_ledger_matches_sources(self):
        brokers, grouped, domains = collect()
        self.assertEqual(set(brokers), set(grouped))
        self.assertEqual(sum(map(len, grouped.values())), len(domains))

    def test_invalid_broad_and_non_main_domains(self):
        for domain in ["127.0.0.1", "::1", "*.futunn.com", "com", "com.hk",
                       "api.futunn.com", "Futunn.com", "futunn.com/path",
                       "futunn.com,PROXY", "futunn..com", "-futu.com",
                       "amazonaws.com", "hsbc.com.hk", "htisec.com"]:
            with self.subTest(domain=domain), self.assertRaises(ValueError):
                validate_domain(domain)

    def test_poisoned_sources_rejected(self):
        for line in ["DOMAIN-SUFFIX,futunn.com", "DOMAIN,api.futunn.com",
                     "IP-CIDR,1.2.3.0/24", "DOMAIN-KEYWORD,futu",
                     "DOMAIN-SUFFIX,unverified-example.com"]:
            with self.subTest(line=line), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                shutil.copytree(ROOT / "source", root / "source")
                shutil.copytree(ROOT / "docs", root / "docs")
                shutil.copyfile(ROOT / "brokers.json", root / "brokers.json")
                with (root / "source/futu.txt").open("a", encoding="utf-8") as f:
                    f.write("\n" + line + "\n")
                with self.assertRaises(ValueError):
                    collect(root)


if __name__ == "__main__":
    unittest.main()
