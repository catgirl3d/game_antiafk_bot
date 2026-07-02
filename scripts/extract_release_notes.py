from __future__ import annotations

import argparse
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHANGELOG_PATH = PROJECT_ROOT / "CHANGELOG.md"
SECTION_PREFIX = "## "
UNRELEASED_KEY = "unreleased"


def normalize_section_key(value: str) -> str:
    token = value.strip().strip("[]").lower()
    if token == UNRELEASED_KEY:
        return token
    if token.startswith("v."):
        return token[2:]
    if token.startswith("v"):
        return token[1:]
    return token


def parse_section_key(header_line: str) -> str | None:
    if not header_line.startswith(SECTION_PREFIX):
        return None

    raw_title = header_line[len(SECTION_PREFIX):].strip()
    section_name = raw_title.split(" - ", 1)[0].strip()
    return normalize_section_key(section_name)


def collect_section_lines(changelog_lines: list[str], target_key: str) -> list[str]:
    section_lines: list[str] = []
    is_collecting = False

    for line in changelog_lines:
        section_key = parse_section_key(line)

        if not is_collecting and section_key == target_key:
            is_collecting = True
            section_lines.append(line)
            continue

        if is_collecting and section_key is not None:
            break

        if is_collecting:
            section_lines.append(line)

    return section_lines


def extract_release_notes_from_text(tag_name: str, changelog_text: str) -> str:
    normalized_tag = normalize_section_key(tag_name)
    changelog_lines = changelog_text.splitlines()

    section_lines = collect_section_lines(changelog_lines, normalized_tag)
    if section_lines:
        return "\n".join(section_lines).strip()

    unreleased_lines = collect_section_lines(changelog_lines, UNRELEASED_KEY)
    if unreleased_lines:
        unreleased_lines[0] = f"## [{tag_name}]"
        return "\n".join(unreleased_lines).strip()

    raise ValueError(
        f"Could not find changelog section for '{tag_name}' and no [Unreleased] section exists."
    )


def extract_release_notes(tag_name: str, changelog_path: Path = CHANGELOG_PATH) -> str:
    changelog_text = changelog_path.read_text(encoding="utf-8")
    return extract_release_notes_from_text(tag_name, changelog_text)


def write_release_notes(
    tag_name: str,
    output_path: Path,
    changelog_path: Path = CHANGELOG_PATH,
) -> Path:
    release_notes = extract_release_notes(tag_name, changelog_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(f"{release_notes}\n", encoding="utf-8")
    return output_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract GitHub release notes from CHANGELOG.md.")
    parser.add_argument("tag_name", help="Git tag to extract release notes for")
    parser.add_argument("output_path", nargs="?", help="Optional output file path")
    parser.add_argument(
        "--changelog",
        default=str(CHANGELOG_PATH),
        help="Path to the changelog file",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    changelog_path = Path(args.changelog)

    if args.output_path:
        write_release_notes(args.tag_name, Path(args.output_path), changelog_path)
    else:
        print(extract_release_notes(args.tag_name, changelog_path))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
