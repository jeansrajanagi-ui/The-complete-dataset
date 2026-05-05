#!/usr/bin/env python3
"""Count tokens across all dataset phases using a simple tokenizer approximation."""

import json
import os
import sys
import re
from pathlib import Path

def approximate_token_count(text):
    """Approximate token count using whitespace + punctuation splitting.
    
    This is a rough approximation. For exact counts, use tiktoken or
    the target model's tokenizer. Rule of thumb: 1 token ≈ 4 characters
    for English text, ~3.5 for code-heavy text.
    """
    # Split on whitespace and common punctuation boundaries
    tokens = re.findall(r'\w+|[^\w\s]', text)
    return len(tokens)

def character_based_estimate(text):
    """Estimate token count based on character count (more reliable for mixed content)."""
    return len(text) / 3.7  # code-heavy text averages ~3.7 chars per token

def count_tokens(root_dir):
    """Count tokens across all dataset files."""
    root = Path(root_dir)
    
    phase_stats = {}
    total_tokens_approx = 0
    total_tokens_char = 0
    total_chars = 0
    total_entries = 0
    
    phase_dirs = ['phase1_identity', 'phase2_fundamentals', 'phase3_progressive', 'phase4_research']
    
    for phase_dir in phase_dirs:
        phase_path = root / phase_dir
        if not phase_path.exists():
            continue
        
        phase_tokens_approx = 0
        phase_tokens_char = 0
        phase_chars = 0
        phase_entries = 0
        
        for jsonl_file in sorted(phase_path.glob('*.jsonl')):
            with open(jsonl_file) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    
                    text = entry.get('text', '')
                    tokens_approx = approximate_token_count(text)
                    tokens_char = character_based_estimate(text)
                    chars = len(text)
                    
                    phase_tokens_approx += tokens_approx
                    phase_tokens_char += tokens_char
                    phase_chars += chars
                    phase_entries += 1
        
        phase_stats[phase_dir] = {
            'entries': phase_entries,
            'tokens_word': phase_tokens_approx,
            'tokens_char': int(phase_tokens_char),
            'characters': phase_chars,
        }
        
        total_tokens_approx += phase_tokens_approx
        total_tokens_char += phase_tokens_char
        total_chars += phase_chars
        total_entries += phase_entries
    
    # Print report
    print("=" * 70)
    print("TOKEN COUNT REPORT")
    print("=" * 70)
    print(f"{'Phase':<30} {'Entries':>8} {'Tokens(word)':>13} {'Tokens(char)':>13} {'Chars':>10}")
    print("-" * 70)
    
    for phase, stats in phase_stats.items():
        print(f"{phase:<30} {stats['entries']:>8} {stats['tokens_word']:>13,} {stats['tokens_char']:>13,} {stats['characters']:>10,}")
    
    print("-" * 70)
    print(f"{'TOTAL':<30} {total_entries:>8} {total_tokens_approx:>13,} {int(total_tokens_char):>13,} {total_chars:>10,}")
    print("=" * 70)
    
    target = 2_000_000_000
    current = int(total_tokens_char)
    print(f"\nTarget: {target:,} tokens")
    print(f"Current: {current:,} tokens (character-based estimate)")
    print(f"Progress: {current / target * 100:.4f}%")
    print(f"Remaining: {target - current:,} tokens")
    
    avg_per_entry = current / total_entries if total_entries > 0 else 0
    entries_needed = int((target - current) / avg_per_entry) if avg_per_entry > 0 else 0
    print(f"\nAverage tokens per entry: {avg_per_entry:,.0f}")
    print(f"Estimated entries needed for target: {entries_needed:,}")

if __name__ == '__main__':
    root_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    count_tokens(root_dir)
