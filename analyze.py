from pathlib import Path

IGNORE = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".idea"}

# Manifest file -> language mapping
MANIFESTS = {
    "Cargo.toml": "Rust",
    "package.json": "JavaScript/TypeScript",
    "pyproject.toml": "Python",
    "requirements.txt": "Python",
    "setup.py": "Python",
    "go.mod": "Go",
    "pom.xml": "Java",
    "build.gradle": "Java/Kotlin",
    "Gemfile": "Ruby",
    "composer.json": "PHP",
}

# Common entry point filenames
ENTRY_POINTS = {"main.py", "app.py", "__init__.py", "index.js", "main.js",
                "main.rs", "lib.rs", "main.go", "Main.java", "index.ts"}

# Files worth reading in full
KEY_FILES = {"README.md", "README.rst", "README.txt"} | set(MANIFESTS.keys())

def find_project_root(dest):
    # The zip extracts into a single subfolder like "requests-main"
    subdirs = [p for p in Path(dest).iterdir() if p.is_dir()]
    return subdirs[0] if len(subdirs) == 1 else Path(dest)

def detect_language(root):
    found = []
    for path in root.rglob("*"):
        if any(part in IGNORE for part in path.parts):
            continue
        if path.name in MANIFESTS:
            found.append((path.name, MANIFESTS[path.name]))
    return found

def collect_key_files(root, max_chars=3000):
    collected = {}
    for path in root.rglob("*"):
        if any(part in IGNORE for part in path.parts):
            continue
        if path.name in KEY_FILES and path.is_file():
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
                collected[path.name] = content[:max_chars]
            except Exception:
                pass
    return collected

def find_entry_points(root):
    entries = []
    for path in root.rglob("*"):
        if any(part in IGNORE for part in path.parts):
            continue
        if path.name in ENTRY_POINTS and path.is_file():
            entries.append(str(path.relative_to(root)))
    return entries

def build_summary(dest):
    root = find_project_root(dest)

    print("\n=== ANALYSIS ===\n")

    langs = detect_language(root)
    print("Detected languages / manifests:")
    if langs:
        for name, lang in langs:
            print(f"  - {name} -> {lang}")
    else:
        print("  (none detected)")

    entries = find_entry_points(root)
    print("\nEntry points found:")
    for e in entries:
        print(f"  - {e}")

    key_files = collect_key_files(root)
    print(f"\nKey files collected: {list(key_files.keys())}")

    return root, langs, entries, key_files

if __name__ == "__main__":
    build_summary("downloaded_repo")
