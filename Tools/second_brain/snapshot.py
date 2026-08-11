from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXCLUDED_DIRECTORIES = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".next",
    "dist",
    "build",
}


def snapshot_tree(root: Path) -> list[dict[str, object]]:
    """Return a stable metadata-only file snapshot, omitting generated directories."""
    files = []
    for path in root.rglob("*"):
        relative_path = path.relative_to(root)
        if any(part in EXCLUDED_DIRECTORIES for part in relative_path.parts[:-1]) or not path.is_file():
            continue
        stat = path.stat()
        files.append(
            {
                "path": relative_path.as_posix(),
                "size": stat.st_size,
                "st_mtime_ns": stat.st_mtime_ns,
            }
        )
    return sorted(files, key=lambda entry: str(entry["path"]))


def hash_files(paths: list[Path]) -> dict[str, str]:
    """Map every requested path to its SHA-256 content digest."""
    hashes = {}
    for path in paths:
        digest = hashlib.sha256()
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
        hashes[str(path)] = digest.hexdigest()
    return hashes


def _write_json(output: Path | None, value: object) -> None:
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if output is None:
        print(rendered, end="")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")


def _read_json(snapshot: Path) -> object:
    return json.loads(snapshot.read_text(encoding="utf-8"))


def _verify_trees(snapshot: Path) -> bool:
    expected = _read_json(snapshot)
    if not isinstance(expected, dict):
        raise ValueError("tree snapshot must be an object mapping roots to file entries")
    actual = {root: snapshot_tree(Path(root)) for root in expected}
    if actual == expected:
        return True
    print(f"Tree snapshot differs: {snapshot}")
    return False


def _verify_hashes(snapshot: Path) -> bool:
    expected = _read_json(snapshot)
    if not isinstance(expected, dict) or not all(isinstance(value, str) for value in expected.values()):
        raise ValueError("hash snapshot must be an object mapping paths to hashes")
    actual = hash_files([Path(path) for path in expected])
    if actual == expected:
        return True
    print(f"Hash snapshot differs: {snapshot}")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or verify source snapshots.")
    parser.add_argument("--tree", type=Path, action="append")
    parser.add_argument("--hash", type=Path, action="append")
    parser.add_argument("--verify-tree", type=Path)
    parser.add_argument("--verify-hashes", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    actions = sum(bool(value) for value in (args.tree, args.hash, args.verify_tree, args.verify_hashes))
    if actions != 1:
        parser.error("select exactly one of --tree, --hash, --verify-tree, or --verify-hashes")
    if (args.tree or args.hash) and args.output is None:
        parser.error("--output is required when creating a snapshot")
    if (args.verify_tree or args.verify_hashes) and args.output is not None:
        parser.error("--output cannot be used while verifying a snapshot")

    if args.tree:
        _write_json(args.output, {str(root): snapshot_tree(root) for root in args.tree})
        return 0
    if args.hash:
        _write_json(args.output, hash_files(args.hash))
        return 0
    if args.verify_tree:
        return 0 if _verify_trees(args.verify_tree) else 1
    return 0 if _verify_hashes(args.verify_hashes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
