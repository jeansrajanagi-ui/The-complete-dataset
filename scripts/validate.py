#!/usr/bin/env python3
"""Validate the dataset structure, ordering, and connections."""

import json
import os
import sys
from pathlib import Path

def validate_entry(entry, filename, line_num):
    """Validate a single JSONL entry."""
    errors = []
    
    # Check required fields
    if 'text' not in entry:
        errors.append(f"Missing 'text' field")
    elif not isinstance(entry['text'], str) or len(entry['text']) < 100:
        errors.append(f"'text' too short ({len(entry.get('text', ''))} chars)")
    
    if 'meta' not in entry:
        errors.append(f"Missing 'meta' field")
    else:
        meta = entry['meta']
        for field in ['phase', 'topic', 'subtopic', 'sequence']:
            if field not in meta:
                errors.append(f"Missing 'meta.{field}'")
        
        if 'phase' in meta and meta['phase'] not in [1, 2, 3, 4]:
            errors.append(f"Invalid phase: {meta['phase']}")
        
        if 'sequence' in meta and not isinstance(meta['sequence'], int):
            errors.append(f"Sequence must be integer, got {type(meta['sequence'])}")
    
    return errors

def validate_dataset(root_dir):
    """Validate the entire dataset."""
    root = Path(root_dir)
    all_entries = []
    total_errors = 0
    
    phase_dirs = ['phase1_identity', 'phase2_fundamentals', 'phase3_progressive', 'phase4_research']
    
    for phase_dir in phase_dirs:
        phase_path = root / phase_dir
        if not phase_path.exists():
            print(f"WARNING: {phase_dir}/ not found")
            continue
        
        for jsonl_file in sorted(phase_path.glob('*.jsonl')):
            with open(jsonl_file) as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError as e:
                        print(f"ERROR: {jsonl_file}:{line_num}: Invalid JSON: {e}")
                        total_errors += 1
                        continue
                    
                    errors = validate_entry(entry, str(jsonl_file), line_num)
                    for error in errors:
                        print(f"ERROR: {jsonl_file}:{line_num}: {error}")
                        total_errors += 1
                    
                    all_entries.append((str(jsonl_file), line_num, entry))
    
    # Check sequence ordering
    sequences = [(e['meta']['sequence'], f, ln) for f, ln, e in all_entries if 'meta' in e and 'sequence' in e['meta']]
    sequences.sort()
    
    seen_sequences = set()
    for seq, f, ln in sequences:
        if seq in seen_sequences:
            print(f"WARNING: Duplicate sequence number {seq} at {f}:{ln}")
        seen_sequences.add(seq)
    
    # Check phase ordering matches sequence ordering
    for f, ln, e in all_entries:
        if 'meta' in e and 'phase' in e['meta'] and 'sequence' in e['meta']:
            phase = e['meta']['phase']
            seq = e['meta']['sequence']
            # Entries in later phases should have higher sequence numbers
            for f2, ln2, e2 in all_entries:
                if 'meta' in e2 and 'phase' in e2['meta'] and 'sequence' in e2['meta']:
                    if e2['meta']['phase'] < phase and e2['meta']['sequence'] > seq:
                        print(f"WARNING: Phase ordering violation: phase {e2['meta']['phase']} seq {e2['meta']['sequence']} > phase {phase} seq {seq}")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Total entries: {len(all_entries)}")
    print(f"Total errors: {total_errors}")
    
    phase_counts = {}
    for _, _, e in all_entries:
        p = e.get('meta', {}).get('phase', '?')
        phase_counts[p] = phase_counts.get(p, 0) + 1
    
    for p in sorted(phase_counts.keys()):
        print(f"  Phase {p}: {phase_counts[p]} entries")
    
    # Check connections reference valid topics
    all_subtopics = set()
    for _, _, e in all_entries:
        if 'meta' in e and 'subtopic' in e['meta']:
            all_subtopics.add(e['meta']['subtopic'])
    
    print(f"\nUnique subtopics: {len(all_subtopics)}")
    print(f"Sequence range: {min(s for s, _, _ in sequences)} to {max(s for s, _, _ in sequences)}")
    
    if total_errors == 0:
        print("\nValidation PASSED")
    else:
        print(f"\nValidation FAILED with {total_errors} errors")
    
    return total_errors == 0

if __name__ == '__main__':
    root_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    success = validate_dataset(root_dir)
    sys.exit(0 if success else 1)
