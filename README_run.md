# Running the independent detector (on your machine)

The sandbox where this was authored is network-isolated, so the truly
independent run happens on your machine, against any OpenAI-compatible endpoint.
Detection is blind (the model sees `corpus_blind.json`, never the labels), and
findings are mapped to catalogue IDs by a separate step so the freeform
condition isn't penalised for not naming codes.

## Option 1 — Ollama (local, free, real model diversity vs Claude)

```bash
ollama serve            # if not already running
ollama pull llama3.1:8b # or qwen2.5, mistral-nemo, etc.

cd experiments/pathway-c
DET_BASE_URL=http://localhost:11434/v1 DET_MODEL=llama3.1:8b \
python run_model.py
python harness.py        # prints recall / precision / delta, writes scores.json
```

## Option 2 — LM Studio

Start the local server (default port 1234), load a model, then:

```bash
DET_BASE_URL=http://localhost:1234/v1 DET_MODEL=<loaded-model-name> \
python run_model.py && python harness.py
```

## Option 3 — a cloud API (e.g. OpenAI) for a strong non-Claude detector

```bash
DET_BASE_URL=https://api.openai.com/v1 DET_API_KEY=sk-... DET_MODEL=gpt-4o-mini \
python run_model.py && python harness.py
```

## Hardening knobs (recommended for a citable result)

- **Different mapper model.** Set `MAP_MODEL` (and `MAP_BASE_URL`/`MAP_API_KEY`)
  to a model different from the detector, so the free-text→ID mapping isn't done
  by the same model that produced the findings.
- **Audit the mapping.** `results_raw.json` holds every raw review; spot-check
  that the mapper assigned IDs faithfully.
- **Scale + relabel.** Expand `corpus.json` toward ~25–30 plans and have a second
  person check the `ground_truth` labels. The delta surviving that is the bar.
- **Repeat.** Run 3–5 times (temperature is 0.2) to see run-to-run variance on
  the borderline cases (P6 needle; freeform's salient-emergent catches).

The self-run pilot's numbers live in `scores.json` / `REPORT.md`. Re-running the
steps above overwrites `results_*.json` with the independent model's findings, so
`harness.py` then reports the independent delta for direct comparison.
