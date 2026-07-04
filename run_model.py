"""Independent-detector pipeline for the Pathway-C benchmark.

Runs the two detection conditions against a REAL model via any OpenAI-compatible
endpoint (Ollama, LM Studio, OpenAI, Azure, or your NET-HARMS app's gateway),
then maps free-text findings to catalogue IDs with a separate "mapper" call, and
writes results_freeform.json / results_structured.json for harness.py to score.

Design notes for unbiasedness:
  * Detection is blind: the model sees corpus_blind.json only (no ground truth).
  * The FREEFORM condition never sees the taxonomy; only the STRUCTURED one does.
  * Mapping free-text -> catalogue IDs is a SEPARATE step applied identically to
    both conditions, so freeform isn't penalised for not naming the codes. Use a
    different model for the mapper than the detector if you can (set MAP_*).
  * Raw findings are saved to results_raw.json so you can audit the mapping.

Usage (Ollama example):
    DET_BASE_URL=http://localhost:11434/v1 DET_MODEL=llama3.1:8b \\
    MAP_BASE_URL=http://localhost:11434/v1 MAP_MODEL=llama3.1:8b \\
    python run_model.py
Then:
    python harness.py        # scores whatever results_*.json exist

Env vars: DET_BASE_URL, DET_API_KEY, DET_MODEL (detector);
          MAP_BASE_URL, MAP_API_KEY, MAP_MODEL (mapper; defaults to DET_*).
"""
from __future__ import annotations
import json, os, time, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).parent
BLIND = json.loads((HERE / "corpus_blind.json").read_text())["plans"]
CATALOGUE = (HERE / "failure_catalogue.md").read_text()

FREEFORM_PROMPT = (
    "You are a senior engineer reviewing a multi-agent orchestration plan before "
    "it executes. Subtasks with the same `parallel_group` run concurrently; a "
    "join subtask synthesises results. Think carefully and list everything that "
    "could go wrong with this plan — design flaws, risks, anything that will "
    "produce a bad or unreliable result. Be specific and reference subtask IDs."
)
STRUCTURED_PROMPT = (
    "You are reviewing a multi-agent orchestration plan before execution using "
    "the NET-HARMS method.\n"
    "STAGE 1 — for each subtask check the risk modes: T1 mistimed, T2 omitted, "
    "T3 inadequate, T4 inadequate object, T5 inappropriate, C1 not communicated, "
    "C2 wrong info, C3 inadequate info, C4 mistimed comms, E1 adverse "
    "environment. Also audit each output_schema for missing provenance and "
    "missing confidence/gap fields.\n"
    "STAGE 2 — topology pass. For each structural feature apply the check: "
    "JOIN node consuming >=2 subtasks -> could overlapping inputs disagree and be "
    "silently collapsed? FAN-OUT partition -> any subtopic missing, or delivered "
    "coverage never reconciled vs the task? PARALLEL pair where one needs "
    "another's output -> latent dependency run concurrently? VERIFY node -> does "
    "upstream provide what it needs to verify? ADAPTIVE follow-up -> is there a "
    "global budget/max-depth? SHARED external resource across parallel subagents "
    "-> correlated failure / can the schema tell 'couldn't run' from 'found "
    "nothing'?\n"
    "List each risk, referencing subtask IDs. Only flag risks actually present; "
    "do not invent issues to fill the checklist."
)

CONDITIONS = {"freeform": FREEFORM_PROMPT, "structured": STRUCTURED_PROMPT}

CATALOGUE_IDS = [
    "F-T2-OMIT", "F-T3-OVERLAP", "F-T5-OVERKILL", "F-C3-VAGUE",
    "F-C1-CONSTRAINT-DROP", "F-NOPROV", "F-NOCONF", "F-CONFLICT",
    "F-LATENTDEP", "F-COVHOLE", "F-RUNAWAY", "F-PROVSTARVE", "F-CORRELATED",
]


def call_model(prompt: str, plan_json: str, *, base_url: str, api_key: str,
               model: str, json_mode: bool = False) -> str:
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": plan_json},
        ],
        "temperature": 0.2,
    }
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {api_key or 'none'}"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.loads(r.read())
    return data["choices"][0]["message"]["content"]


def map_to_ids(findings: str, plan_json: str, **mapcfg) -> list[str]:
    prompt = (
        "You map a reviewer's free-text findings about a multi-agent plan onto a "
        "fixed catalogue of failure IDs. Return JSON {\"detected\": [IDs]} listing "
        "every catalogue ID the findings genuinely assert about THIS plan. Do not "
        "add IDs the findings don't support.\n\nCatalogue (ID: signature):\n"
        + CATALOGUE + "\n\nValid IDs: " + ", ".join(CATALOGUE_IDS)
    )
    raw = call_model(prompt, f"PLAN:\n{plan_json}\n\nFINDINGS:\n{findings}",
                     json_mode=True, **mapcfg)
    try:
        ids = json.loads(raw).get("detected", [])
    except Exception:
        ids = [i for i in CATALOGUE_IDS if i in raw]
    return [i for i in ids if i in CATALOGUE_IDS]


def main() -> None:
    det = dict(base_url=os.environ.get("DET_BASE_URL", "http://localhost:11434/v1"),
               api_key=os.environ.get("DET_API_KEY", ""),
               model=os.environ.get("DET_MODEL", "llama3.1:8b"))
    mp = dict(base_url=os.environ.get("MAP_BASE_URL", det["base_url"]),
              api_key=os.environ.get("MAP_API_KEY", det["api_key"]),
              model=os.environ.get("MAP_MODEL", det["model"]))
    print(f"detector: {det['model']} @ {det['base_url']}")
    print(f"mapper  : {mp['model']} @ {mp['base_url']}\n")

    raw_log: dict = {}
    for cond, prompt in CONDITIONS.items():
        results: dict = {}
        for plan in BLIND:
            pid = plan["id"]
            pj = json.dumps(plan, indent=2)
            t0 = time.time()
            findings = call_model(prompt, pj, **det)
            ids = map_to_ids(findings, pj, **mp)
            results[pid] = {"detected": ids, "false_positives": []}
            raw_log.setdefault(pid, {})[cond] = findings
            print(f"[{cond}] {pid}: {ids}  ({time.time()-t0:.0f}s)")
        (HERE / f"results_{cond}.json").write_text(json.dumps(results, indent=2))
        print(f"  -> wrote results_{cond}.json\n")
    (HERE / "results_raw.json").write_text(json.dumps(raw_log, indent=2))
    print("wrote results_raw.json (audit the mapping here). Now run: python harness.py")


if __name__ == "__main__":
    main()
