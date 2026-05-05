#!/usr/bin/env python3
"""
Quick training demo - trains a small model for demonstration.
"""

import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
import random

# Tiny settings for quick demo
VOCAB_SIZE = 256
MAX_LEN = 64
BATCH_SIZE = 32
EPOCHS = 1

class QuickDataset(Dataset):
    def __init__(self, data_dir, max_samples=10000):
        print("Loading data...")
        self.texts = []
        
        # Sample from dataset
        files = list(Path(data_dir).glob("phase*_identity/*.jsonl"))
        
        for f in files[:10]:  # Only first 10 files
            try:
                with open(f) as fp:
                    for line in fp:
                        line = line.strip()
                        if line and len(self.texts) < max_samples:
                            try:
                                e = json.loads(line)
                                text = e.get('text', '')[:200]
                                if text:
                                    self.texts.append(text)
                            except:
                                pass
            except:
                pass
        
        print(f"Loaded {len(self.texts)} texts")
        
        # Build vocab from chars
        chars = set()
        for t in self.texts:
            chars.update(t)
        
        self.char2idx = {c: i+4 for i, c in enumerate(sorted(chars))}
        self.char2idx['<PAD>'] = 0
        self.char2idx['<UNK>'] = 1
        self.char2idx['<BOS>'] = 2
        self.char2idx['<EOS>'] = 3
        self.idx2char = {v: k for k, v in self.char2idx.items()}
        
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        t = self.texts[idx]
        ids = [self.char2idx.get(c, 1) for c in t[:MAX_LEN-2]]
        ids = [2] + ids + [3]  # BOS, EOS
        if len(ids) < MAX_LEN:
            ids += [0] * (MAX_LEN - len(ids))
        return torch.tensor(ids[:MAX_LEN])

class TinyLM(nn.Module):
    def __init__(self, vocab_size, embed_dim=64, hidden=128):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden, 2, batch_first=True)
        self.fc = nn.Linear(hidden, vocab_size)
        
    def forward(self, x):
        x = self.embed(x)
        x, _ = self.lstm(x)
        return self.fc(x)

def main():
    print("="*50)
    print("Quick Training Demo")
    print("="*50)
    
    device = torch.device('cpu')
    
    # Data
    dataset = QuickDataset("/workspace/project/The-complete-dataset", max_samples=5000)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    print(f"Dataset: {len(dataset)} samples")
    
    # Model
    model = TinyLM(VOCAB_SIZE).to(device)
    print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Train
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    print(f"\nTraining {EPOCHS} epoch...")
    
    for epoch in range(EPOCHS):
        total_loss = 0
        for i, x in enumerate(loader):
            x = x.to(device)
            
            optimizer.zero_grad()
            
            # Shift for LM
            out = model(x[:, :-1])
            loss = criterion(out.reshape(-1, VOCAB_SIZE), x[:, 1:].reshape(-1))
            
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            if i % 100 == 0:
                print(f"Batch {i}/{len(loader)}, Loss: {loss.item():.4f}")
        
        print(f"Epoch {epoch+1} complete, Avg Loss: {total_loss/len(loader):.4f}")
    
    # Save
    torch.save({
        'model': model.state_dict(),
        'char2idx': dataset.char2idx,
        'idx2char': dataset.idx2char
    }, '/workspace/project/The-complete-dataset/tiny_model.pt')
    
    # Generate
    model.eval()
    
    print("\n" + "="*50)
    print("Sample Generations:")
    print("="*50)
    
    prompts = ["I think", "The code", "I verify"]
    
    with torch.no_grad():
        for prompt in prompts:
            ids = [dataset.char2idx.get(c, 1) for c in prompt[:10]]
            ids = [2] + ids
            
            for _ in range(30):
                x = torch.tensor([ids[-63:]]).to(device)
                out = model(x)
                next_id = out[0, -1].argmax().item()
                if next_id == 3:
                    break
                ids.append(next_id)
            
            result = ''.join([dataset.idx2char.get(i, '?') for i in ids[1:]])
            print(f"\nPrompt: '{prompt}'")
            print(f"Output: '{result}'")
    
    print("\n✓ Training complete! Model saved.")

if __name__ == "__main__":
    main()