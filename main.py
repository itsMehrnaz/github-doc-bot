import sys
import io
import zipfile
import requests
from pathlib import Path

IGNORE = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".idea"}

def parse_repo_url(url):

    parts = url.rstrip("/").replace("https://github.com/", "").split("/")
    return parts[0], parts[1]

def download_repo(owner, repo, dest="downloaded_repo"):

    for branch in ["main", "master"]:
        url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
        print(f"Trying to download from branch: {branch} ...")
        r = requests.get(url)
        if r.status_code == 200:
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(dest)
            print(f"Download successful. Files saved to '{dest}'.")
            return dest
    raise Exception("Download failed. Check the URL or branch name.")

def print_tree(root):
    print("\n--- Project structure ---")
    for path in sorted(Path(root).rglob("*")):
        if any(part in IGNORE for part in path.parts):
            continue
        depth = len(path.relative_to(root).parts) - 1
        indent = "    " * depth
        print(f"{indent}{path.name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <github-repo-url>")
        sys.exit(1)

    repo_url = sys.argv[1]
    owner, repo = parse_repo_url(repo_url)
    dest = download_repo(owner, repo)
    print_tree(dest)
