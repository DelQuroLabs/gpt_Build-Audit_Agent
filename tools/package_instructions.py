"""Assemble deterministic, complete installation prompts from reviewed sources."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTRUCTION_BUDGET = 7500  # Package budget, not a claim about a host's current limit.


def assemble() -> dict[Path, str]:
    config = json.loads((ROOT / "gpt-config.json").read_text(encoding="utf-8"))
    profiles = [config["builder"], config["auditor"], *config["optional_specialists"]["profiles"]]
    outputs = {}
    for profile in profiles:
        chunks = []
        for source in profile["instruction_sources"]:
            text = (ROOT / source).read_text(encoding="utf-8")
            if text.startswith("<!--"):
                text = text.split("-->", 1)[1]
            chunks.append(text.strip())
        content = "\n\n".join(chunks) + "\n"
        if len(content) > INSTRUCTION_BUDGET:
            raise ValueError(f"{profile['name']}: {len(content)} characters exceeds package budget {INSTRUCTION_BUDGET}")
        outputs[ROOT / profile["instructions_file"]] = content
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify generated files without changing them")
    args = parser.parse_args()
    try:
        outputs = assemble()
        for path, content in outputs.items():
            if args.check:
                if not path.exists() or path.read_text(encoding="utf-8") != content:
                    raise ValueError(f"Stale or missing generated prompt: {path.relative_to(ROOT)}")
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8", newline="\n")
            print(f"{path.relative_to(ROOT)}: {len(content)} characters")
    except (OSError, ValueError) as exc:
        print(str(exc))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
