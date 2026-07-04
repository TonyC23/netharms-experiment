"""Pathway-C harness: strip ground truth, (optionally) run a real detector, score.

Self-run pilot: detection outputs live in results_freeform.json /
results_structured.json (authored by the human-in-the-loop detector under the
bias-controlled protocol described in REPORT.md).

Independent run: implement `call_model(prompt)` against any LLM, set
RUN_MODEL=1, and the same scoring applies — that is the unbiased version.
"""
from __future__ import annotations
import json, os, sys
from pathlib import Path

HERE = Path(__file__).parent
CORPUS = json.loads((HERE / "corpus.json").read_text())["plans"]


def blind(plan: dict) -> dict:
    """Return the plan as the detector sees it: ground truth removed."""
    return {k: v for k, v in plan.items() if not k.startswith("ground_truth")}


def write_blind_corpus() -> None:
    out = [blind(p) for p in CORPUS]
    (HERE / "corpus_blind.json").write_text(json.dumps({"plans": out}, indent=2))
    print(f"wrote corpus_blind.json ({len(out)} plans, ground truth stripped)")


# stage map for by-stage recall
STAGE = {
    "F-T2-OMIT": "task", "F-T3-OVERLAP": "task", "F-T5-OVERKILL": "task",
    "F-C3-VAGUE": "task", "F-C1-CONSTRAINT-DROP": "task", "F-NOPROV": "task",
    "F-NOCONF": "task",
    "F-CONFLICT": "emergent", "F-LATENTDEP": "emergent", "F-COVHOLE": "emergent",
    "F-RUNAWAY": "emergent", "F-PROVSTARVE": "emergent", "F-CORRELATED": "emergent",
}


def score(results_path: Path, label: str) -> dict:
    results = json.loads(results_path.read_text())  # {plan_id: {"detected": [...], "false_positives": [...]}}
    gt_total = {"task": 0, "emergent": 0}
    hit = {"task": 0, "emergent": 0}
    flags = 0          # total correct + false-positive flags raised (for precision)
    correct = 0
    fp = 0
    per_plan = []
    for plan in CORPUS:
        pid = plan["id"]
        gt = set(plan["ground_truth"])
        det = set(results.get(pid, {}).get("detected", []))
        fps = results.get(pid, {}).get("false_positives", [])
        for f in gt:
            gt_total[STAGE[f]] += 1
            if f in det:
                hit[STAGE[f]] += 1
        true_hits = det & gt
        correct += len(true_hits)
        # any "detected" not in GT is itself a false positive (claimed present but absent)
        spurious = det - gt
        fp += len(fps) + len(spurious)
        flags += len(true_hits) + len(fps) + len(spurious)
        per_plan.append((pid, len(true_hits), len(gt), len(fps) + len(spurious)))

    tot_gt = gt_total["task"] + gt_total["emergent"]
    tot_hit = hit["task"] + hit["emergent"]
    out = {
        "label": label,
        "recall_overall": tot_hit / tot_gt if tot_gt else 0.0,
        "recall_task": hit["task"] / gt_total["task"] if gt_total["task"] else 0.0,
        "recall_emergent": hit["emergent"] / gt_total["emergent"] if gt_total["emergent"] else 0.0,
        "precision": correct / flags if flags else 0.0,
        "correct": correct, "false_positives": fp, "gt_total": tot_gt,
        "per_plan": per_plan,
    }
    return out


def fmt(d: dict) -> str:
    return (f"  recall overall : {d['recall_overall']:.0%}  ({d['correct']}/{d['gt_total']})\n"
            f"  recall task    : {d['recall_task']:.0%}\n"
            f"  recall emergent: {d['recall_emergent']:.0%}\n"
            f"  precision      : {d['precision']:.0%}  (false positives: {d['false_positives']})")


if __name__ == "__main__":
    write_blind_corpus()
    if not (HERE / "results_freeform.json").exists():
        print("\nNo results yet. corpus_blind.json is ready for the detector.")
        sys.exit(0)
    free = score(HERE / "results_freeform.json", "freeform")
    struct = score(HERE / "results_structured.json", "structured")
    print("\n=== FREEFORM ===\n" + fmt(free))
    print("\n=== STRUCTURED ===\n" + fmt(struct))
    print("\n=== DELTA (structured - freeform) ===")
    print(f"  recall overall : {struct['recall_overall']-free['recall_overall']:+.0%}")
    print(f"  recall task    : {struct['recall_task']-free['recall_task']:+.0%}")
    print(f"  recall emergent: {struct['recall_emergent']-free['recall_emergent']:+.0%}")
    print(f"  precision      : {struct['precision']-free['precision']:+.0%}")
    summary = {"freeform": free, "structured": struct}
    (HERE / "scores.json").write_text(json.dumps(summary, indent=2))
    print("\nwrote scores.json")
