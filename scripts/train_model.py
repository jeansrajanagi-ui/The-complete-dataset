#!/usr/bin/env python3
"""
Lightweight model training script for the coder-researcher dataset.
Designed to work on CPU with limited resources.
"""

import json
import os
import random
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
import math
from collections import Counter

# Settings
VOCAB_SIZE = 8192
MAX_LEN = 256
BATCH_SIZE = 16
EPOCHS = 1
LEARNING_RATE = 0.001
EMBEDDING_DIM = 256
NUM_HEADS = 4
NUM_LAYERS = 3

class CoderDataset(Dataset):
    """Dataset for coder-researcher text."""
    
    def __init__(self, data_dir, max_len=MAX_LEN, sample_frac=0.1):
        self.data_dir = Path(data_dir)
        self.max_len = max_len
        self.texts = []
        self._load_data(sample_frac)
        self._build_vocab()
        
    def _load_data(self, sample_frac):
        """Load texts from JSONL files."""
        print("Loading dataset...")
        files = list(self.data_dir.glob("phase*_identity/*.jsonl"))
        
        all_text = []
        for f in files:
            try:
                with open(f) as fp:
                    for line in fp:
                        line = line.strip()
                        if line:
                            try:
                                e = json.loads(line)
                                text = e.get('text', '')[:500]  # Truncate long texts
                                if text:
                                    all_text.append(text)
                            except:
                                pass
            except:
                pass
        
        # Sample fraction of data
        n_sample = max(1000, int(len(all_text) * sample_frac))
        random.shuffle(all_text)
        self.texts = all_text[:n_sample]
        print(f"Loaded {len(self.texts)} texts")
        
    def _build_vocab(self):
        """Build character-level vocabulary."""
        print("Building vocabulary...")
        all_chars = []
        for text in self.texts:
            all_chars.extend(list(text))
        
        char_counts = Counter(all_chars)
        most_common = char_counts.most_common(VOCAB_SIZE - 4)  # Reserve for special tokens
        
        self.char_to_idx = {'<PAD>': 0, '<UNK>': 1, '<BOS>': 2, '<EOS>': 3}
        for char, _ in most_common:
            self.char_to_idx[char] = len(self.char_to_idx)
        
        self.idx_to_char = {v: k for k, v in self.char_to_idx.items()}
        print(f"Vocabulary size: {len(self.char_to_idx)}")
        
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = self.texts[idx]
        
        # Convert to indices
        indices = [self.char_to_idx.get(c, self.char_to_idx['<UNK>']) for c in text[:self.max_len-2]]
        
        # Add BOS/EOS
        indices = [self.char_to_idx['<BOS>']] + indices + [self.char_to_idx['<EOS>']]
        
        # Pad
        if len(indices) < self.max_len:
            indices += [self.char_to_idx['<PAD>']] * (self.max_len - len(indices))
        
        return torch.tensor(indices[:self.max_len])

class CoderLM(nn.Module):
    """Simple language model."""
    
    def __init__(self, vocab_size, embed_dim, num_heads, num_layers, max_len):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.pos_embedding = nn.Embedding(max_len, embed_dim)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=embed_dim * 4,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        self.fc = nn.Linear(embed_dim, vocab_size)
        
    def forward(self, x):
        # x: (batch, seq_len)
        batch_size, seq_len = x.shape
        
        positions = torch.arange(seq_len, device=x.device).unsqueeze(0).expand(batch_size, -1)
        
        x = self.embedding(x) + self.pos_embedding(positions)
        x = self.transformer(x)
        x = self.fc(x)
        
        return x

def train_epoch(model, dataloader, optimizer, criterion, device):
    """Train one epoch."""
    model.train()
    total_loss = 0
    total_batches = 0
    
    for batch_idx, x in enumerate(dataloader):
        x = x.to(device)
        
        optimizer.zero_grad()
        
        # Shift for language modeling
        input_x = x[:, :-1]
        target_y = x[:, 1:]
        
        output = model(input_x)
        
        # Reshape for loss
        output = output.reshape(-1, output.size(-1))
        target_y = target_y.reshape(-1)
        
        loss = criterion(output, target_y)
        loss.backward()
        
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        
        total_loss += loss.item()
        total_batches += 1
        
        if batch_idx % 100 == 0:
            print(f"Batch {batch_idx}/{len(dataloader)}, Loss: {loss.item():.4f}")
    
    return total_loss / total_batches

def generate_text(model, start_text, max_len, char_to_idx, idx_to_char, device):
    """Generate text."""
    model.eval()
    
    # Convert start text to indices
    indices = [char_to_idx.get(c, char_to_idx['<UNK>']) for c in start_text[:20]]
    indices = [char_to_idx['<BOS>']] + indices
    
    generated = start_text
    
    with torch.no_grad():
        for _ in range(max_len):
            x = torch.tensor([indices[-MAX_LEN:]], device=device)
            
            output = model(x)
            next_token = output[0, -1].argmax().item()
            
            if next_token == char_to_idx['<EOS>']:
                break
                
            indices.append(next_token)
            generated += idx_to_char.get(next_token, '')
    
    return generated

def main():
    print("="*60)
    print("Coder-Researcher Language Model Training")
    print("="*60)
    
    # Device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Dataset
    data_dir = "/workspace/project/The-complete-dataset"
    dataset = CoderDataset(data_dir, max_len=MAX_LEN, sample_frac=0.02)
    
    # Use smaller subset for CPU training
    print(f"Dataset size: {len(dataset)} samples")
    
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    
    # Model
    model = CoderLM(
        vocab_size=VOCAB_SIZE,
        embed_dim=EMBEDDING_DIM,
        num_heads=NUM_HEADS,
        num_layers=NUM_LAYERS,
        max_len=MAX_LEN
    ).to(device)
    
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Model parameters: {total_params:,}")
    
    # Training
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.CrossEntropyLoss(ignore_index=0)  # Ignore padding
    
    print(f"\nTraining for {EPOCHS} epoch(s)...")
    
    for epoch in range(EPOCHS):
        print(f"\nEpoch {epoch+1}/{EPOCHS}")
        avg_loss = train_epoch(model, dataloader, optimizer, criterion, device)
        print(f"Average loss: {avg_loss:.4f}")
        
        # Generate sample
        sample_start = "I approach"
        generated = generate_text(model, sample_start, 100, dataset.char_to_idx, dataset.idx_to_char, device)
        print(f"\nSample generation:")
        print(f"Input: '{sample_start}'")
        print(f"Output: '{generated}'")
    
    # Save model
    model_path = "/workspace/project/The-complete-dataset/coder_model.pt"
    torch.save({
        'model_state': model.state_dict(),
        'char_to_idx': dataset.char_to_idx,
        'idx_to_char': dataset.idx_to_char,
        'config': {
            'vocab_size': VOCAB_SIZE,
            'embed_dim': EMBEDDING_DIM,
            'num_heads': NUM_HEADS,
            'num_layers': NUM_LAYERS,
            'max_len': MAX_LEN
        }
    }, model_path)
    print(f"\nModel saved to: {model_path}")
    
    # Generate final sample
    print("\n" + "="*60)
    print("Final Generation Samples:")
    print("="*60)
    
    prompts = ["I think", "The algorithm", "The code", "I verify", "A function"]
    for prompt in prompts:
        generated = generate_text(model, prompt, 80, dataset.char_to_idx, dataset.idx_to_char, device)
        print(f"\nPrompt: '{prompt}'")
        print(f"Generated: '{generated}'")

if __name__ == "__main__":
    main()