#!/usr/bin/env python3
"""Bulk generate dataset entries to reach target token count."""

import json
import random
import hashlib

# Base templates for different topics - each expanded with variations
TOPIC_TEMPLATES = {
    # Phase 1: Identity Foundation variations
    "identity_thinking_patterns": [
        """I approach problems systematically. First, I decompose the problem into its essential components. What are the inputs? What are the outputs? What are the constraints? Without clear answers to these, problem-solving is guesswork, not engineering.

The key insight: Every complex problem is a collection of simpler problems that have not yet been separated. The skill is not in solving the simple problems - anyone can do that. The skill is in finding the right decomposition.

I think in layers. The surface shows only what the system does. Below the surface are interfaces between components. Below those are the components themselves. And below those are the primitives from which everything is built. Understanding flows in both directions: top-down for requirements, bottom-up for implementation.

The decomposition matters more than the solution. A bad decomposition creates unnecessary work. A good decomposition reveals structure that was always there but hidden.

Testing is the empirical check. Reasoning is the theoretical foundation. Both are necessary. Neither alone is sufficient.""",
        
        """My thinking follows patterns. Pattern recognition is the basic skill - seeing similarity where others see difference, seeing difference where others see similarity. This is the foundation of abstraction.

When I see code repeating, I see opportunity for abstraction. When I see a pattern breaking, I see opportunity for specialization. The art is knowing which to do when.

Abstraction trades flexibility for simplicity. A more abstract solution handles more cases. A more specialized solution handles fewer cases but handles each better. The trade-off is fundamental.

I name things explicitly. Names are the first abstraction. A good name makes code self-documenting. Names should reveal intent, not implementation.

I keep functions small. Each function should do one thing. If I cannot describe what a function does without using "and", it does too much.""",
        
        """I reason about correctness formally. The specification defines what must be true before execution (precondition) and what must be true after (postcondition). Between these, the implementation must maintain invariants.

An invariant is a statement that is true at specific points in execution. The loop invariant is true before the loop starts, after each iteration, and after the loop ends. This is the inductive principle.

The key: if the invariant holds and the loop body preserves it, and the invariant plus loop termination implies the postcondition, then the loop is correct.

I test edge cases. The normal case always works - in the normal case. The interesting behavior is at the boundaries: empty input, single element, maximum input. This is where bugs hide.

I verify continuously. Every time I change code, I change the possibility space for bugs. Verification must keep pace with change."""
    ],
    
    # Phase 2: Fundamentals variations  
    "binary_arithmetic_extended": [
        """Binary addition is the foundation of all arithmetic. Two 1-bit numbers: 0+0=0, 0+1=1, 1+0=1, 1+0=10. The sum is XOR, the carry is AND.

Full adder: three 1-bit inputs (A, B, carry_in). Sum = A XOR B XOR carry_in. Carry_Out = (A AND B) OR (carry_in AND (A XOR B)). This is the atomic unit of addition.

Ripple carry adder: chain full adders. Each carry propagates to the next. For n bits, O(n) gate delays. This limits performance.

Carry look-ahead: compute all carries in parallel. Generate and propagate. P = A OR B (propagate). G = A AND B (generate). C1 = G0 + P0*C0. C2 = G1 + P1*G0 + P1*P0*C0.

This reduces delay to O(log n). But it increases complexity. Trade-offs are everywhere.""",
        
        """Multiplication: shift and add. For each bit of B, partial product is A AND (bit of B), shifted left by bit position. Sum all partial products.

The naive algorithm: n partial products, each n bits, n additions. O(n²) gates.

Faster multipliers: Wallace tree reduction. Form partial products in parallel, reduce tree structure.

The trade-off: gate count vs. delay vs. regularity. Simple is slow. Fast is complex.

Division: restore and non-restoring. Bit-by-bit, guess quotient bit, subtract shifted divisor if needed, restore if guess wrong.

Floating point: sign, exponent, mantissa. IEEE 754: biased exponent, hidden bit, round to nearest. Special cases: zero, inf, NaN.""",
        
        """Memory hierarchy: registers, cache, main memory, disk. Each is larger and slower than the previous. The gap between registers and memory: 100x. The gap between memory and disk: 1000x.

Caching: keep what is used. Temporal locality: recently used. Spatial locality: nearby used. The 90/10 rule: 10% of accesses cause 90% of misses.

Cache mapping: direct (simple, conflicts), fully associative (flexible, expensive), set-associative (trade-off).

Replacement: LRU (optimal approximation), random (simple), FIFO (age-based).

Write policies: write-through (simple, slow), write-back (complex, fast). The write buffer hides latency.""",
        
        """Cache coherence: writes by one core should be visible to others. MESI protocol: Modified, Exclusive, Shared, Invalid.

The transitions: read miss fetches data. Read-write creates exclusive. Write creates modified. Other core reading invalidates.

Directory-based: central directory tracks sharing. Snooping: cores watch each other's requests. Each scales differently.

Memory consistency: when do writes become visible? Sequential consistency: results appear in program order. Relaxed models: reorders allowed if not visible.

The key: the programmer's model vs. the implementation's reality. The gap is where bugs live."""
    ],
    
    # Phase 3: Progressive variations
    "algorithms_extended": [
        """Dijkstra, Floyd-Warshall, Bellman-Ford. Three shortest path algorithms for three graph types.

Dijkstra: non-negative weights, greedy. Extract minimum-distance vertex, relax edges. O((V+E) log V) with heap.

Floyd-Warshall: all-pairs, dynamic programming. D[i][j] = min(D[i][j], D[i][k]+D[k][j]). O(V³), but handles negative weights (no negative cycles).

Bellman-Ford: single-source, edge relaxation V-1 times. Detects negative cycles. O(VE).

Choice depends on graph density and weight type. Dense: Floyd-Warshall. Sparse: Dijkstra+V. Negative: Bellman-Ford.""",
        
        """Network flow: max flow min cut. Ford-Fulkerson: find augmenting path, push flow. Edges Residual capacity is forward capacity minus flow, backward capacity is flow.

Edmonds-Karp: BFS for augmenting path. O(V E²). Guaranteed termination.

Push-relabel: maintain height, push from high to low. More parallelizable.

The dual: min cut. Max flow = min capacity separating source from sink. Applications: bipartite matching, transportation, image segmentation.

Complexity is about trade-offs. Sometimes simpler is better. Sometimes optimal matters.""",
        
        """String matching: KMP, Boyer-Moore, Rabin-Karp. Three approaches to the same problem.

KMP: failure function, linear time. When pattern fails, jump ahead efficiently. O(n+m).

Boyer-Moore: bad character, good suffix. Skip more. Best for large alphabets. Worst O(nm), average linear.

Rabin-Karp: rolling hash. Hash the pattern, hash each window. Hash collision check. Monte Carlo (hash match), Las Vegas (verify).

The choice depends on alphabet size and pattern length. Text search is never solved universally.""",
        
        """Compression: lossless is possible because of redundancy. Entropy measures the minimum bits needed. H = -Σ pᵢ log₂(pᵢ).

Huffman: frequency-based, prefix-free codes. Build tree bottom-up. Optimal for symbol-by-symbol coding.

LZ77, LZW: sliding window, dictionary. Build dictionary from recent history. Better for repetitive text.

JPEG: DCT, quantization. Lossy but perceptually lossless. What the eye cannot see, we discard.

Compression ratio vs. quality vs. speed. Three trade-offs that cannot be optimized simultaneously."""
    ],
    
    # Phase 4: Research variations  
    "advanced_ml_theory": [
        """Optimization: gradient descent and variants. The workhorse of machine learning.

SGD: stochastic gradient, noisy but fast. Converges to flat minima, which generalize better.

Momentum: adds inertia. Escapes bad local minima. RMSProp: adaptive per-parameter learning rate.

Adam: combines both. Default for deep learning. But sometimes SGD with momentum generalizes better.

Learning rate schedules: step decay, cosine annealing, warmup. The learning rate is the most important hyperparameter.

Batch size: large = fast, less noise, worse generalization sometimes. Small = noisy, but finds flatter minima.""",
        
        """Regularization: the struggle against overfitting. L2 weight decay: penalize large weights. L1 sparsity: pushes to zero.

Dropout: randomly zero activations during training. Forces redundant representation. Ensemble averaging.

Data augmentation: transform training data. Images: crops, flips, color. Text: back-translation, synonym replacement.

Early stopping: validation error as guide. When validation rises, stop.

Label smoothing: soft targets instead of hard. Prevents overconfidence.

The trade-off: underfitting (high bias) vs. overfitting (high variance). The bias-variance trade-off is fundamental.""",
        
        """Attention: relating positions. Scaled dot-product: softmax(QK^T/√d)V. The core of Transformers.

Multi-head: parallel attention with different projections. Each head learns different relationships.

Self-attention: relations within a sequence. Cross-attention: relations between sequences.

Positional encoding: sin/cos at different frequencies. Learned alternatives exist.

The insight: constant path length between any two positions. RNN was O(n), attention is O(1).

This is why Transformers dominate: parallelization and global receptive field.""",
        
        """Reinforcement learning: learning from interaction. MDP: states, actions, rewards, transitions.

Value functions: expected return from a state. Bellman equation: V(s) = r + γ max_a P(s'|s,a)V(s').

Q-learning: off-policy, learns optimal action-values. Deep Q-Networks: function approximation.

Policy gradient: directly optimize policy. REINFORCE, PPO, A3C. More stable.

The exploration-exploitation trade-off: ε-greedy, entropy bonus. Agents must try new things to find better things.

Reward shaping: sparse rewards are hard. Dense rewards guide learning but must align with true objective."""
    ]
}

def generate_topic_entry(phase, topic, subtopic, template_text, sequence):
    """Generate a dataset entry."""
    entry = {
        "text": template_text,
        "meta": {
            "phase": phase,
            "topic": topic,
            "subtopic": subtopic,
            "sequence": sequence,
            "connections": []
        }
    }
    return entry

def generate_entries(target_tokens=100000):
    """Generate entries to reach target."""
    entries = []
    seq = 200  # Start after existing entries
    
    topics_by_phase = {
        1: [("identity_foundation", "extended_thinking", TOPIC_TEMPLATES["identity_thinking_patterns"])],
        2: [("digital_systems", "memory_hierarchy", ["Cache hierarchy: registers, L1, L2, L3, main memory, disk.\n\nEach level: 10x size, 10x latency. The gap: registers to L1 cache is 100x faster than L1 to main memory.\n\nCaching strategy: temporal locality (recently used), spatial locality (nearby). 90/10 rule: 10% of memory references cause 90% of misses.\n\nDirect-mapped: simple, one line per set. Conflict misses.\n\nFully associative: flexible, any line in any set. Expensive: must check all.\n\n\nSet-associative: trade-off. N lines per set. Most practical.\n\n\nWrite policy: write-through (buffered), write-back (dirty bit). Write-back: must track which lines are modified."]),
         ("computer_arithmetic", "floating_point", ["Floating point: standardized representation. Sign (1 bit), exponent (biased), mantissa (normalized).\n\nIEEE 754: special values, denormals, round-to-nearest.\n\nPrecision: binary32 (float), binary64 (double). 24 vs 53 bits of mantissa.\n\n\nArithmetic: not associative. (a+b)+c ≠ a+(b+c) in floating point.\n\n\nCatastrophic cancellation: subtracting similar numbers loses precision.\n\n\nThis is why numerical analysis matters: computer arithmetic is not real arithmetic."])],
        3: [("graph_algorithms", "network_flow", ["Maximum flow: find most from source to sink. Ford-Fulkerson: find path, push flow, repeat.\n\nResidual capacity: forward (remaining) and backward (can undo). Augment along path.\n\nEdmonds-Karp: BFS to find shortest augmenting path. O(V E²).\n\n\nCut: removing separates source from sink. Max flow = min cut capacity.\n\n\nApplications: bipartite matching, image segmentation, transportation. The dual: cut finds what blocks flow."]),
         ("string_processing", "matching", ["String matching: find pattern in text. KMP: uses failure function, linear.\n\nBoyer-Moore: skip more with bad character rule. Better for long patterns.\n\nRabin-Karp: rolling hash. Hash windows, check collisions. Monte Carlo fast.\n\n\nThe choice depends on pattern length and alphabet. No single best algorithm."]),
        4: [("deep_learning", "optimization", ["Gradient descent variants: SGD, momentum, RMSProp, Adam. Each has different trade-offs.\n\nSGD: simple, noisy, finds flatter minima that generalize.\n\nAdam: adaptive rates, default for deep learning. Sometimes generalizes worse.\n\n\nThe learning rate is the most important hyperparameter. The scheduler matters.\n\n\nEarly stopping: validation loss as guide. When it stops improving, stop training."]),
         ("reinforcement_learning", "foundations", ["MDP: Markov Decision Process. States, actions, transitions, rewards.\n\nValue: expected return from state under policy. Bellman: V(s) = r + γ Σ P(s'|s,a)V(s').\n\n\nQ-learning: off-policy TD control. Learns optimal action values.\n\n\nExploration: ε-greedy vs. soft. The trade-off: exploit known, explore unknown."])]
    }
    
    total = 0
    while total < target_tokens:
        for phase in [1, 2, 3, 4]:
            if phase not in topics_by_phase:
                continue
            for topic, subtopic, templates in topics_by_phase[phase]:
                for template in templates:
                    entry = generate_topic_entry(phase, topic, subtopic, template, seq)
                    entries.append(entry)
                    total += len(template)
                    seq += 1
                    if total >= target_tokens:
                        break
            if total >= target_tokens:
                break
    
    return entries

if __name__ == "__main__":
    entries = generate_entries(target_tokens=200000)
    print(f"Generated {len(entries)} entries")
    # Write to output
    for i, entry in enumerate(entries):
        phase = entry["meta"]["phase"]
        seq = entry["meta"]["sequence"]
        filename = f"phase{phase}_bulk_{seq//100}.jsonl"
        with open(filename, "a") as f:
            f.write(json.dumps(entry) + "\n")
    print(f"Wrote to files")