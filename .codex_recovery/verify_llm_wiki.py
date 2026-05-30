from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(r"C:\Obsidian\KnowledgeVault")
KNOWLEDGE = ROOT / "Knowledge"

PERMANENT_REQUIRED = [
    "## 한 줄 정의",
    "## 내 말로 다시 설명",
    "## 언제 쓰는가",
    "## 언제 쓰면 안 되는가",
    "## 자주 헷갈리는 점",
    "## 확인 질문",
]

EXPANDED = {
    "RAG",
    "LLM",
    "LangGraph",
    "Pandas DataFrame",
    "Django ORM Model",
    "useEffect",
    "Django QuerySet",
    "Embedding",
    "Vector Store",
    "React API Fetch",
    "Docker Compose",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def without_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def links_in(text: str) -> list[str]:
    text = without_code(text)
    return [m.split("#", 1)[0].split("|", 1)[0] for m in re.findall(r"\[\[([^\]]+)\]\]", text)]


def status_of(text: str) -> str:
    match = re.search(r'^status:\s*"([^"]+)"', text, re.M)
    return match.group(1) if match else "missing"


def main() -> int:
    md_files = sorted(KNOWLEDGE.rglob("*.md"))
    names = {p.stem for p in md_files}
    names.add("README")

    empty = [str(p.relative_to(ROOT)) for p in md_files if p.stat().st_size == 0]
    missing_frontmatter = [str(p.relative_to(ROOT)) for p in md_files if not read(p).startswith("---\n")]
    status_counts: Counter[str] = Counter()
    broken_links: list[dict[str, str]] = []
    permanent_missing_sections: list[dict[str, object]] = []
    suspicious: list[dict[str, str]] = []
    expanded_status: dict[str, dict[str, object]] = {}

    for path in md_files:
        text = read(path)
        status_counts[status_of(text)] += 1
        clean = without_code(text)

        for target in links_in(text):
            if target and target not in names:
                broken_links.append({"file": str(path.relative_to(ROOT)), "target": target})

        if "Permanent Notes" in path.parts:
            missing = [heading for heading in PERMANENT_REQUIRED if heading not in text]
            if missing:
                permanent_missing_sections.append({
                    "file": str(path.relative_to(ROOT)),
                    "missing": missing,
                })

        for pattern in [r"param\(\$m\)", r"\$title은/는", r"(?m)^/는", r"(?m)^은/는", r"(?m)^태그:.*\n\s+#llm_wiki"]:
            if re.search(pattern, clean):
                suspicious.append({"file": str(path.relative_to(ROOT)), "pattern": pattern})

    for title in sorted(EXPANDED):
        path = KNOWLEDGE / "Permanent Notes" / f"{title}.md"
        text = read(path) if path.exists() else ""
        expanded_status[title] = {
            "exists": path.exists(),
            "status": status_of(text) if text else "missing",
            "bytes": path.stat().st_size if path.exists() else 0,
        }

    report = {
        "markdown_files": len(md_files),
        "empty_files": len(empty),
        "missing_frontmatter": len(missing_frontmatter),
        "broken_links": len(broken_links),
        "permanent_missing_sections": len(permanent_missing_sections),
        "suspicious_patterns": len(suspicious),
        "status_distribution": dict(sorted(status_counts.items())),
        "expanded_status": expanded_status,
        "examples": {
            "empty": empty[:10],
            "missing_frontmatter": missing_frontmatter[:10],
            "broken_links": broken_links[:10],
            "permanent_missing_sections": permanent_missing_sections[:10],
            "suspicious": suspicious[:10],
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

    failures = (
        empty
        or missing_frontmatter
        or broken_links
        or permanent_missing_sections
        or suspicious
        or any(v["status"] != "wiki-expanded" or not v["exists"] or v["bytes"] == 0 for v in expanded_status.values())
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
