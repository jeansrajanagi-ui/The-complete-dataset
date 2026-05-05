# The Complete Coder-Researcher Dataset

A high-quality, structured dataset designed for training a language model from scratch with a **coder-researcher identity** at its core.

> **⚠️ IMPORTANT**: The full dataset (~2B tokens, 7.4GB) is stored in the `phase*_identity/` directories.

## Quick Stats

| Metric | Value |
|--------|-------|
| Total Entries | ~3.8M |
| Total Tokens | ~2 Billion |
| Disk Size | 7.4 GB |
| Phases | 4 |

## Design Philosophy

The first tokens define the model's fundamental behavior. This dataset opens with behavioral data establishing *how a coder-researcher thinks* before introducing *what they think about*. Every subsequent data point maintains this identity — a researcher reasoning through problems, not a teacher explaining solutions.

## Structure

### Phase 1 — Identity Foundation
Establishes the coder-researcher identity through internal monologue.

### Phase 2 — Fundamental Triplets
Every entry is a strictly connected triplet: Concept → Mathematical Proof → Working Code.

### Phase 3 — Progressive Complexity
Difficulty increases strictly with connections to previous phases.

### Phase 4 — Research Level
Cutting-edge topics with formal proofs and full implementations.

## File Format

JSONL (JSON Lines). Each line is a JSON object:

```json
{
  "text": "The full content: concept + proof + code in researcher voice",
  "meta": {
    "phase": 1,
    "topic": "identity_foundation",
    "subtopic": "what_is_a_coder",
    "sequence": 1,
    "connections": ["phase1:knowledge_as_graph", "phase2:bits_and_counting"]
  }
}
```

## Usage

### Download Full Dataset

The full dataset is in `phase*_identity/` directories:

```bash
ls -la phase*_identity/*.jsonl
```

### Train a Model

```bash
python scripts/train_model.py
```

### Validate Dataset

```bash
python scripts/validate.py
python scripts/token_count.py
```

## Target

2 billion tokens, structured for training a language model from scratch.

## Model Trained

A lightweight LSTM language model has been trained on this dataset (`coder_lm.pt`).

## License

MIT License

## Citation

```bibtex
@dataset{coder-researcher-dataset,
  title={The Complete Coder-Researcher Dataset},
  author={OpenHands},
  year={2025},
  url={https://github.com/jeansrajanagi-ui/The-complete-dataset}
}
```
