import unittest
from pathlib import Path

import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SCRIPTS_DIR))

import mimecast_toolkit
from registry import SCRIPT_REGISTRY


class LauncherTests(unittest.TestCase):
    def test_registry_entries_point_to_existing_scripts(self):
        for entry in SCRIPT_REGISTRY:
            with self.subTest(script=entry.filename):
                self.assertTrue((SCRIPTS_DIR / entry.filename).is_file())

    def test_find_script_accepts_extensionless_and_python_names(self):
        self.assertEqual(
            mimecast_toolkit.find_script("get_account").filename,
            "get_account.py",
        )
        self.assertEqual(
            mimecast_toolkit.find_script("get_account.py").filename,
            "get_account.py",
        )

    def test_child_environment_passes_token_and_removes_client_secret(self):
        env = mimecast_toolkit.build_child_env(
            "token-123",
            "account-123",
            base_env={
                "MIMECAST_CLIENT_ID": "client",
                "MIMECAST_CLIENT_SECRET": "secret",
                "CLIENT_SECRET": "legacy-secret",
                "PATH": "/bin",
            },
        )

        self.assertEqual(env["MIMECAST_ACCESS_TOKEN"], "token-123")
        self.assertEqual(env["MIMECAST_ACCOUNT_CODE"], "account-123")
        self.assertEqual(env["PATH"], "/bin")
        self.assertNotIn("MIMECAST_CLIENT_ID", env)
        self.assertNotIn("MIMECAST_CLIENT_SECRET", env)
        self.assertNotIn("CLIENT_SECRET", env)


if __name__ == "__main__":
    unittest.main()
