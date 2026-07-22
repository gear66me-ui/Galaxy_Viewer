from __future__ import annotations

import base64
import subprocess
import sys
from pathlib import Path

try:
    from github import Auth, Github
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "PyGithub"], check=True)
    from github import Auth, Github


def upload_bridge_file(
    local_path: Path,
    token: str,
    owner: str = "gear66me-ui",
    repository: str = "Galaxy_Viewer",
    branch: str = "sandbox",
    folder: str = "bridge-search",
) -> str:
    client = Github(auth=Auth.Token(token))
    repo = client.get_repo(f"{owner}/{repository}")
    remote_path = f"{folder}/{local_path.name}"
    content = local_path.read_bytes()

    try:
        existing = repo.get_contents(remote_path, ref=branch)
        repo.update_file(
            remote_path,
            f"Update {local_path.name}",
            content,
            existing.sha,
            branch=branch,
        )
    except Exception as exc:
        if "404" not in str(exc):
            raise
        repo.create_file(
            remote_path,
            f"Upload {local_path.name}",
            content,
            branch=branch,
        )

    client.close()
    return f"https://raw.githubusercontent.com/{owner}/{repository}/{branch}/{remote_path}"
