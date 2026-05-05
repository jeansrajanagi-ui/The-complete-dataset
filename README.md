# The Complete Coder-Researcher Dataset

A high-quality, structured dataset designed for training a language model from scratch with a **coder-researcher identity** at its core.

## Design Philosophy

The first tokens define the model's fundamental behavior. This dataset opens with behavioral data establishing *how a coder-researcher thinks* before introducing *what they think about*. Every subsequent data point maintains this identity — a researcher reasoning through problems, not a teacher explaining solutions.

## Structure

### Phase 1 — Identity Foundation (First tokens, most critical)
Establishes the coder-researcher identity through internal monologue:
- What is a coder and how they think
- Approaching unknown problems
- Connecting theory to implementation
- Reasoning through failure
- Fundamentals before complexity
- Research methodology
- Knowledge as a connected graph

**Format:** Behavioral monologues in the voice of an expert coder-researcher.

### Phase 2 — Fundamental Triplets
Every entry is a strictly connected triplet:
1. **Concept or theory** — precise definitions
2. **Mathematical or logical proof** — rigorous derivation
3. **Working code implementation** — verified against the proof

Starting from absolute zero:
- Binary representation and bits
- Boolean logic and gates (AND, OR, NOT, XOR, NAND)
- NAND universality and De Morgan's laws
- Half adder, full adder, ripple-carry adder
- Binary multiplication
- Multiplexers
- Memory: latches, flip-flops, registers
- Finite state machines
- Arrays, stacks, linked lists
- Hash tables
- Binary search trees (AVL)
- Algorithmic complexity (Big-O, Big-Omega, Big-Theta)
- Sorting lower bounds

### Phase 3 — Progressive Complexity
Difficulty increases strictly. Each entry connects to previous entries explicitly.
- Graph algorithms (BFS, DFS, topological sort)
- Shortest paths (Dijkstra)
- Minimum spanning trees (Kruskal, Union-Find)
- Dynamic programming (Fibonacci, LCS, edit distance)
- Operating systems (processes, virtual memory)
- Concurrency (race conditions, locks, deadlock)
- Networking (physical layer to TCP)
- Compilers (lexing, parsing, code generation)
- Databases (B-trees, ACID)
- Cryptography (XOR, RSA, modular arithmetic)

### Phase 4 — Research Level
Cutting-edge topics with formal proofs and full implementations:
- Machine learning foundations (statistical learning theory, gradient descent)
- Neural networks (backpropagation, from scratch)
- Attention mechanism and Transformers
- Formal verification (Hoare logic, model checking)
- Computability theory (halting problem, NP-completeness, SAT solvers)
- Type theory and Curry-Howard correspondence
- Distributed systems (FLP impossibility, Raft consensus)

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

- **text**: The training content. Written as internal monologue of a coder-researcher.
- **meta.phase**: 1-4, corresponding to the four phases.
- **meta.topic**: Major topic area.
- **meta.subtopic**: Specific subtopic.
- **meta.sequence**: Global ordering (1, 2, 3, ...) ensuring strict progression.
- **meta.connections**: Explicit references to prerequisite topics.

## Non-Negotiable Rules

1. Every single token serves the coder-researcher identity
2. No filler, no padding, no disconnected data
3. Consistent voice throughout — a researcher thinking, not a teacher explaining
4. Connections between concepts are explicit, not implied
5. No concept appears before its foundations are established
6. Every concept is a triplet: theory → proof → code

## Target

2 billion tokens, structured for training a language model from scratch.

## Current Status

This is the foundational structure with substantial initial content across all four phases (34 entries, ~80,000 tokens). The structure, voice, and progression are established. Expansion follows the roadmap in the final entry.

## Validation

```bash
python scripts/validate.py    # Verify JSONL structure and ordering
python scripts/token_count.py # Count tokens across all phases
```

## Directory Structure

```
├── README.md
├── phase1_identity/
│   └── 001_what_is_a_coder.jsonl          # 10 entries
├── phase2_fundamentals/
│   ├── 001_binary_and_bits.jsonl           # 10 entries
│   └── 002_data_structures_from_scratch.jsonl  # 5 entries
├── phase3_progressive/
│   ├── 001_graph_algorithms.jsonl          # 5 entries
│   └── 002_systems_and_abstractions.jsonl  # 6 entries
├── phase4_research/
│   └── 001_machine_learning_foundations.jsonl  # 8 entries
└── scripts/
    ├── validate.py
    └── token_count.py
```
