"""
Regression eval harness for pod-ft RAG quality.

Measures:
- Citation precision, recall, F1
- Fragments retrieved per query
- Answer relevance (LLM-as-judge placeholder)

Usage:
    uv run python data-pipelines/eval/run_eval.py --api-url https://vectornode.ru
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, field

import httpx

GOLDEN_QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), "golden-questions.json")
GOLDEN_CITATIONS_PATH = os.path.join(os.path.dirname(__file__), "golden-citations.json")


@dataclass
class EvalResult:
    case_id: str
    question: str
    expected_citations: list[str]
    actual_citations: list[str]
    precision: float
    recall: float
    f1: float
    fragments_retrieved: int
    latency_ms: int
    errors: list[str] = field(default_factory=list)


def load_cases(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["cases"]


def compute_metrics(
    expected: list[str],
    actual: list[str],
) -> tuple[float, float, float]:
    expected_set = set(expected)
    actual_set = set(actual)
    true_positives = len(expected_set & actual_set)
    precision = 0.0 if not actual_set else true_positives / len(actual_set)
    recall = 0.0 if not expected_set else true_positives / len(expected_set)
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    return precision, recall, f1


async def run_answer_eval(api_url: str, api_key: str | None = None) -> list[EvalResult]:
    questions = load_cases(GOLDEN_QUESTIONS_PATH)
    results: list[EvalResult] = []
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    async with httpx.AsyncClient(base_url=api_url, headers=headers, timeout=30) as client:
        for case in questions:
            start = __import__("time").time()
            actual_citations: list[str] = []
            errors: list[str] = []
            fragments_count = 0

            try:
                resp = await client.post("/api/v1/answer", json={
                    "question": case["question"],
                    "subject_type": case.get("subject_type"),
                })
                if resp.status_code == 200:
                    data = resp.json()
                    actual_citations = [
                        e.get("citation_label", "")
                        for e in data.get("evidence", [])
                        if e.get("citation_label")
                    ]
                    fragments_count = len(data.get("evidence", []))
                else:
                    errors.append(f"HTTP {resp.status_code}: {resp.text[:200]}")
            except Exception as exc:
                errors.append(str(exc))

            elapsed_ms = int((__import__("time").time() - start) * 1000)
            precision, recall, f1 = compute_metrics(case["expected_citations"], actual_citations)

            results.append(EvalResult(
                case_id=case["id"],
                question=case["question"],
                expected_citations=case["expected_citations"],
                actual_citations=actual_citations,
                precision=precision,
                recall=recall,
                f1=f1,
                fragments_retrieved=fragments_count,
                latency_ms=elapsed_ms,
                errors=errors,
            ))

    return results


async def run_doc_check_eval(api_url: str, api_key: str | None = None) -> list[EvalResult]:
    cases = load_cases(GOLDEN_CITATIONS_PATH)
    results: list[EvalResult] = []
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    async with httpx.AsyncClient(base_url=api_url, headers=headers, timeout=60) as client:
        for case in cases:
            start = __import__("time").time()
            errors: list[str] = []
            fragments_count = 0

            try:
                resp = await client.post("/api/v1/check", json={
                    "tenant_id": "eval",
                    "document_text": case["document_title"],
                    "document_title": case["document_title"],
                    "document_type": case["document_type"],
                    "subject_type": case.get("subject_type"),
                })
                if resp.status_code == 200:
                    data = resp.json()
                    job_id = data.get("job_id")
                    if job_id:
                        for _ in range(30):
                            poll = await client.get(f"/api/v1/check/{job_id}")
                            if poll.status_code == 200:
                                poll_data = poll.json()
                                if poll_data["status"] == "completed":
                                    result = poll_data.get("result", {})
                                    fragments_count = result.get("total_fragments_found", 0)
                                    break
                                elif poll_data["status"] == "failed":
                                    errors.append(f"Job failed: {poll_data.get('error_message')}")
                                    break
                            await __import__("asyncio").sleep(0.5)
                    else:
                        errors.append("No job_id in response")
                else:
                    errors.append(f"HTTP {resp.status_code}: {resp.text[:200]}")
            except Exception as exc:
                errors.append(str(exc))

            elapsed_ms = int((__import__("time").time() - start) * 1000)
            min_frags = case.get("minimum_fragments", 1)
            passed = fragments_count >= min_frags and not errors

            results.append(EvalResult(
                case_id=case["id"],
                question=case["document_title"],
                expected_citations=[f"min_{min_frags}_fragments"],
                actual_citations=[str(fragments_count)],
                precision=1.0 if passed else 0.0,
                recall=1.0 if passed else 0.0,
                f1=1.0 if passed else 0.0,
                fragments_retrieved=fragments_count,
                latency_ms=elapsed_ms,
                errors=errors,
            ))

    return results


def print_report(answer_results: list[EvalResult], doc_check_results: list[EvalResult]) -> None:
    all_results = answer_results + doc_check_results
    if not all_results:
        print("No results to report.")
        return

    avg_precision = sum(r.precision for r in all_results) / len(all_results)
    avg_recall = sum(r.recall for r in all_results) / len(all_results)
    avg_f1 = sum(r.f1 for r in all_results) / len(all_results)
    avg_latency = sum(r.latency_ms for r in all_results) / len(all_results)
    passed = sum(1 for r in all_results if r.f1 >= 0.5 and not r.errors)

    print(f"\n{'='*60}")
    print(f"  EVAL REPORT — {len(all_results)} cases")
    print(f"{'='*60}")
    print(f"  Average Precision: {avg_precision:.3f}")
    print(f"  Average Recall:    {avg_recall:.3f}")
    print(f"  Average F1:        {avg_f1:.3f}")
    print(f"  Average Latency:   {avg_latency:.0f}ms")
    print(f"  Passed:            {passed}/{len(all_results)}")
    print(f"{'='*60}\n")

    header = f"{'Case':<16} {'F1':<8} {'Prec':<8} {'Recall':<8}"
    header += f" {'Frags':<8} {'Latency':<8} {'Status':<10}"
    print(header)
    print("-" * 68)
    for r in all_results:
        status = "PASS" if r.f1 >= 0.5 and not r.errors else "FAIL"
        line = f"{r.case_id:<16} {r.f1:<8.3f} {r.precision:<8.3f}"
        line += f" {r.recall:<8.3f} {r.fragments_retrieved:<8} {r.latency_ms:<8} {status:<10}"
        print(line)
        for e in r.errors:
            print(f"  └─ ERROR: {e}")

    if answer_results:
        print("\n--- Answer Cases ---")
        for r in answer_results:
            print(f"  {r.case_id}: expected={r.expected_citations}, actual={r.actual_citations}")

    print()


async def main() -> None:
    parser = argparse.ArgumentParser(description="pod-ft regression eval harness")
    parser.add_argument(
        "--api-url", default="http://localhost:8000",
        help="Base URL of the gateway",
    )
    parser.add_argument("--api-key", default=None, help="Optional API key")
    args = parser.parse_args()

    print(f"Running eval against {args.api_url} ...")
    answer_results = await run_answer_eval(args.api_url, args.api_key)
    doc_check_results = await run_doc_check_eval(args.api_url, args.api_key)
    print_report(answer_results, doc_check_results)
    all_ok = all(r.f1 >= 0.5 and not r.errors for r in answer_results + doc_check_results)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
