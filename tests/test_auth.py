import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import auth


class AuthTests(unittest.TestCase):
    def test_get_config_reads_env_file_and_credentials_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            credentials_file = Path(tmpdir) / "credentials.txt"
            env_file.write_text("MIMECAST_CLIENT_ID=env-client\n", encoding="utf-8")
            credentials_file.write_text(
                "client_secret=file-secret\naccount_code=file-account\n",
                encoding="utf-8",
            )

            with mock.patch.object(auth, "ENV_FILE", str(env_file)), mock.patch.object(
                auth, "CREDENTIALS_FILE", str(credentials_file)
            ), mock.patch.dict(os.environ, {}, clear=True):
                config = auth.get_config()

        self.assertEqual(config["client_id"], "env-client")
        self.assertEqual(config["client_secret"], "file-secret")
        self.assertEqual(config["account_code"], "file-account")

    def test_get_token_reuses_access_token_from_environment(self):
        with mock.patch.dict(os.environ, {"MIMECAST_ACCESS_TOKEN": "token-123"}, clear=True):
            with mock.patch.object(auth.requests, "post") as post:
                token = auth.get_token()

        self.assertEqual(token, "token-123")
        post.assert_not_called()

    def test_get_token_accepts_session_overrides_without_writing_credentials(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env_file = Path(tmpdir) / ".env"
            credentials_file = Path(tmpdir) / "credentials.txt"
            response = mock.Mock()
            response.json.return_value = {"access_token": "session-token"}

            with mock.patch.object(auth, "ENV_FILE", str(env_file)), mock.patch.object(
                auth, "CREDENTIALS_FILE", str(credentials_file)
            ), mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(
                auth.requests, "post", return_value=response
            ) as post, mock.patch("sys.stdout", new=io.StringIO()):
                token = auth.get_token(
                    {"client_id": "inline-client", "client_secret": "inline-secret"}
                )

            self.assertEqual(token, "session-token")
            self.assertFalse(env_file.exists())
            self.assertFalse(credentials_file.exists())
            post.assert_called_once()
            self.assertEqual(post.call_args.kwargs["data"]["client_id"], "inline-client")
            self.assertEqual(post.call_args.kwargs["data"]["client_secret"], "inline-secret")


if __name__ == "__main__":
    unittest.main()
