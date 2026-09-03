"""Supplemental structured quality scoring for Phase 2 specialist output.

This module does not replace the rubric-required EvaluationAgent. It adds a
small deterministic scoring layer so a reviewer can see quality dimensions
beyond the required PASS/FAIL evaluator verdict.
"""

from __future__ import annotations

import re
from typing import Dict, List


_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "for",
    "from",
    "i",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "so",
    "that",
    "the",
    "this",
    "to",
    "we",
    "with",
}


def _strip_prefix(text: str) -> str:
    """Remove optional Markdown/list prefixes from a user-story line."""
    return re.sub(r"^\s*(?:[-*•]+\s*|\d+[.)]\s*)", "", text).strip()


def extract_user_stories(text: str) -> List[str]:
    """Extract story-shaped lines from Product Manager output."""
    stories: List[str] = []
    for raw_line in text.splitlines():
        line = _strip_prefix(raw_line)
        if line.startswith(("As a ", "As an ")):
            stories.append(line)
    return stories


def _content_tokens(text: str) -> set[str]:
    """Return lowercase content tokens suitable for lightweight traceability checks."""
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9-]{2,}", text.lower())
    return {token for token in tokens if token not in _STOP_WORDS}


def score_product_manager_output(user_stories_text: str, product_spec: str) -> Dict[str, object]:
    """Score Product Manager output across four transparent dimensions.

    Dimensions are intentionally deterministic and easy to audit:
    - format_compliance: every story follows As a/an ..., I want ..., so that ...
    - completeness: rewards a useful set of at least five stories
    - traceability: stories reuse substantive concepts found in the product spec
    - clarity: stories are concise, single-sentence statements of practical length

    The supplemental decision is PASS only when the total is at least 75/100 and
    format compliance receives the full 25 points. The mandatory EvaluationAgent
    still runs independently in ``agentic_workflow.py`` and retains its required
    return fields and correction loop.
    """
    stories = extract_user_stories(user_stories_text)
    if not stories:
        return {
            "format_compliance": 0,
            "completeness": 0,
            "traceability": 0,
            "clarity": 0,
            "total": 0,
            "decision": "FAIL",
            "story_count": 0,
        }

    valid_format = sum(
        1
        for story in stories
        if story.startswith(("As a ", "As an "))
        and ", I want " in story
        and " so that " in story
    )
    format_score = round(25 * valid_format / len(stories))

    # Five or more substantive stories earns full completeness credit.
    completeness_score = min(25, len(stories) * 5)

    spec_tokens = _content_tokens(product_spec)
    traceable = 0
    for story in stories:
        overlap = _content_tokens(story) & spec_tokens
        if len(overlap) >= 3:
            traceable += 1
    traceability_score = round(25 * traceable / len(stories))

    clear = 0
    for story in stories:
        word_count = len(story.split())
        sentence_endings = len(re.findall(r"[.!?](?:\s|$)", story))
        if 12 <= word_count <= 60 and sentence_endings <= 1:
            clear += 1
    clarity_score = round(25 * clear / len(stories))

    total = format_score + completeness_score + traceability_score + clarity_score
    decision = "PASS" if total >= 75 and format_score == 25 else "FAIL"

    return {
        "format_compliance": format_score,
        "completeness": completeness_score,
        "traceability": traceability_score,
        "clarity": clarity_score,
        "total": total,
        "decision": decision,
        "story_count": len(stories),
    }


def format_quality_score(score: Dict[str, object]) -> str:
    """Render the structured score in a reviewer-friendly form."""
    return "\n".join(
        [
            "=== PRODUCT MANAGER SUPPLEMENTAL QUALITY SCORE ===",
            f"Format Compliance: {score['format_compliance']}/25",
            f"Completeness: {score['completeness']}/25",
            f"Traceability to Product Specification: {score['traceability']}/25",
            f"Clarity: {score['clarity']}/25",
            f"Total: {score['total']}/100",
            f"Story Count: {score['story_count']}",
            f"Supplemental Decision: {score['decision']}",
            "Note: This score supplements, and does not replace, the required EvaluationAgent PASS/FAIL loop.",
        ]
    )
