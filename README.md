# The Complete Coder-Researcher Dataset

A high-quality, structured dataset designed for training a language model from scratch with a **coder-researcher identity** at its core.

## Design Philosophy

The first tokens define the model's fundamental behavior. This dataset opens with behavioral data establishing *how a coder-researcher thinks* before introducing *what they think about*. Every subsequent data point maintains this identity — a researcher reasoning through problems, not a teacher explaining solutions.

Every entry is hand-picked and unique. No two entries overlap in topic, opening, or code examples.

## Structure

### Phase 1 — Identity Foundation (16 entries)
Establishes the coder-researcher identity through internal monologue:
- What is a coder and how they think
- Perceiving and reading code
- Code as mathematical structure
- Approaching unknown problems
- Connecting theory to implementation
- Reasoning through failure
- Fundamentals before complexity
- Research methodology
- Chain of trust from axioms to implementations
- Knowledge as a connected graph
- Debugging as archaeological excavation
- Reading other people's code
- Dealing with ambiguity
- Navigating million-line codebases
- Speed through understanding, not shortcuts
- Operating at the boundary of knowledge

### Phase 2 — Fundamental Triplets (21 entries)
Every entry is concept → proof → working code, starting from absolute zero:
- Binary representation, unsigned integers, two's complement
- Boolean operations, NAND universality, De Morgan's laws
- Half adder, full adder, ripple-carry adder, multiplier
- Multiplexers, latches, flip-flops, registers
- Finite state machines
- Arrays, stacks, linked lists, hash tables, AVL trees
- Algorithmic complexity (Big-O/Omega/Theta, sorting lower bound)
- IEEE 754 floating-point arithmetic
- Character encoding and Unicode/UTF-8
- Instruction set architecture (custom 16-bit RISC CPU)
- Binary heap and heapsort
- Recursion and the call stack
- Graph representations (CSR format)

### Phase 3 — Progressive Complexity (17 entries)
Each entry explicitly connects to previous foundations:
- BFS, DFS, topological sort, Dijkstra, MSTs
- Dynamic programming (Fibonacci, LCS, edit distance)
- OS concepts (processes, virtual memory, page tables)
- Concurrency (race conditions, locks, deadlock)
- Networking (physical layer through TCP, CRC)
- Compilers (lexer, recursive descent parser, codegen)
- Databases (B-trees, ACID)
- Cryptography (XOR cipher, RSA)
- KMP string matching
- Radix sort and non-comparison sorting
- Numerical root-finding (bisection, Newton, secant)
- Cache-aware algorithms and memory hierarchy
- Randomized algorithms (quicksort, Miller-Rabin)
- Garbage collection (mark-sweep)

### Phase 4 — Research Level (15 entries)
Cutting-edge topics with formal proofs and full implementations:
- Statistical learning theory and gradient descent
- Neural networks and backpropagation from scratch
- Attention mechanism and Transformers
- Formal verification (Hoare logic, model checking)
- Computability theory (halting problem, NP-completeness, SAT)
- Type theory and Curry-Howard correspondence
- Distributed consensus (FLP impossibility, Raft)
- Reinforcement learning and Q-learning
- Information theory (entropy, Huffman coding)
- Program synthesis (enumerative search over DSLs)
- Quantum computing (qubit simulation, Deutsch-Jozsa)
- Probabilistic programming and MCMC
- Algebraic effects and handlers
- Differential privacy

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
- **meta.subtopic**: Specific subtopic — every entry has a unique subtopic.
- **meta.sequence**: Global ordering (1-69) ensuring strict progression.
- **meta.connections**: Explicit references to prerequisite topics.

## Non-Negotiable Rules

1. Every single token serves the coder-researcher identity
2. No filler, no padding, no disconnected data
3. Consistent voice throughout — a researcher thinking, not a teacher explaining
4. Connections between concepts are explicit, not implied
5. No concept appears before its foundations are established
6. Every concept is a triplet: theory → proof → code
7. Every entry is unique — no overlapping topics, no similar openings, no repeated code examples

## Target

2 billion tokens, structured for training a language model from scratch.

## Current Status

69 entries across all four phases, ~81,000 tokens. All entries validated, 0 errors, 69 unique subtopics. The structure, voice, and progression are established for continuous expansion.

## Validation

```bash
python scripts/validate.py    # Verify JSONL structure and ordering
python scripts/token_count.py # Count tokens across all phases
```

## Directory Structure

```
├── README.md
├── phase1_identity/
│   ├── 001_what_is_a_coder.jsonl              # 10 entries
│   └── 002_debugging_as_archaeology.jsonl      # 6 entries
├── phase2_fundamentals/
│   ├── 001_binary_and_bits.jsonl               # 10 entries
│   ├── 002_data_structures_from_scratch.jsonl  # 5 entries
│   └── 003_floating_point_and_encoding.jsonl   # 6 entries
├── phase3_progressive/
│   ├── 001_graph_algorithms.jsonl              # 5 entries
│   ├── 002_systems_and_abstractions.jsonl      # 6 entries
│   └── 003_string_algorithms_and_numerics.jsonl # 6 entries
├── phase4_research/
│   ├── 001_machine_learning_foundations.jsonl   # 8 entries
│   └── 002_advanced_research.jsonl             # 7 entries
└── scripts/
    ├── validate.py
    └── token_count.py
```
