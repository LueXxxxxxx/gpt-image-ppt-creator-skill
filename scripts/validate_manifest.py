#!/usr/bin/env python3
"""Validate an image-only PPT slide manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ALLOWED_ROLES = {"cover", "agenda", "transition", "content", "summary", "closing"}
ALLOWED_CONTENT_TITLE_MODES = {"topic-only", "module-plus-topic"}
REQUIRED_DECK_FIELDS = {"title", "slides"}
REQUIRED_SLIDE_FIELDS = {"number", "role", "main_title", "visual_intent"}


def normalize_text(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return " ".join(value.split())


def validate_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"Could not read JSON: {exc}"]

    for field in REQUIRED_DECK_FIELDS:
        if field not in data:
            errors.append(f"Missing deck field: {field}")

    content_title_mode = data.get("content_title_mode", "topic-only")
    if content_title_mode not in ALLOWED_CONTENT_TITLE_MODES:
        errors.append(
            "`content_title_mode` must be one of "
            f"{sorted(ALLOWED_CONTENT_TITLE_MODES)}"
        )

    slides = data.get("slides")
    if not isinstance(slides, list) or not slides:
        errors.append("`slides` must be a non-empty list")
        return errors

    seen_numbers: set[int] = set()
    for index, slide in enumerate(slides, start=1):
        prefix = f"slide[{index}]"
        if not isinstance(slide, dict):
            errors.append(f"{prefix} must be an object")
            continue

        for field in REQUIRED_SLIDE_FIELDS:
            if field not in slide or slide[field] in ("", None):
                errors.append(f"{prefix} missing required field: {field}")

        number = slide.get("number")
        if not isinstance(number, int) or number < 1:
            errors.append(f"{prefix}.number must be a positive integer")
        elif number in seen_numbers:
            errors.append(f"{prefix}.number is duplicated: {number}")
        else:
            seen_numbers.add(number)

        role = slide.get("role")
        if role not in ALLOWED_ROLES:
            errors.append(f"{prefix}.role must be one of {sorted(ALLOWED_ROLES)}")

        body = slide.get("body", [])
        if body is not None and not isinstance(body, list):
            errors.append(f"{prefix}.body must be a list when provided")

    expected_numbers = set(range(1, len(slides) + 1))
    if seen_numbers and seen_numbers != expected_numbers:
        errors.append(f"Slide numbers must be contiguous from 1 to {len(slides)}")

    selected_roles = set(data.get("selected_roles", []))
    if "transition" in selected_roles:
        transition_indices: dict[str, int] = {}
        content_indices: dict[str, int] = {}

        for index, slide in enumerate(slides):
            if not isinstance(slide, dict):
                continue
            role = slide.get("role")
            module = normalize_text(slide.get("module"))
            title = normalize_text(slide.get("main_title"))
            key = module or title
            if not key:
                continue
            if role == "transition":
                transition_indices.setdefault(key, index)
            elif role == "content" and module:
                content_indices.setdefault(module, index)

        for module, first_content_index in content_indices.items():
            transition_index = transition_indices.get(module)
            if transition_index is None:
                errors.append(
                    "Missing transition slide for content module: "
                    f"{module}"
                )
            elif transition_index > first_content_index:
                errors.append(
                    "Transition slide must appear before first content slide "
                    f"for module: {module}"
                )

        for index, slide in enumerate(slides, start=1):
            if not isinstance(slide, dict) or slide.get("role") != "content":
                continue
            module = normalize_text(slide.get("module"))
            title = normalize_text(slide.get("main_title"))
            subtitle = normalize_text(slide.get("subtitle"))
            if module and title and module == title:
                if content_title_mode == "topic-only":
                    errors.append(
                        f"slide[{index}] uses the module title as content "
                        f"main_title while content_title_mode is topic-only; "
                        f"use a specific content topic as main_title: {title}"
                    )
                elif not subtitle:
                    errors.append(
                        f"slide[{index}] content main_title duplicates module "
                        f"title without a specific subtitle; add a specific "
                        f"content subtitle or use the specific content topic "
                        f"as main_title: {title}"
                    )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    errors = validate_manifest(args.manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
