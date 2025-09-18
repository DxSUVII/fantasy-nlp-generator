# Stop symlink warning
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Import libs
try:
    from transformers import GPT2LMHeadModel, GPT2Tokenizer
    import torch
    ML_AVAILABLE = True
except Exception as e:
    print(f"ML import failed: {e}. Using rule-based only.")
    ML_AVAILABLE = False
import random

# Load model
model = None
tokenizer = None
if ML_AVAILABLE:
    try:
        model_name = "distilgpt2"
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name)
        tokenizer.pad_token = tokenizer.eos_token
        print("Model loaded – ML available!")
    except Exception as e:
        print(f"Model load failed: {e}. Using rule-based only.")
        ML_AVAILABLE = False

def rule_based_name():  # Minimal backup
    """Random fantasy name, no ML."""
    bases = ["Eldrin", "Sylvar", "Zorath", "Kael", "Liora", "Valthor", "Aeloria", "Draven", "Thalor", "Elyndra", "Zephyra", "Sylvana", "Korvath", "Aelric", "Zyra", "Eldora", "Varn", "Lorien", "Mythra", "Zandor"]
    prefixes = ["Thal-", "Ely-", "Vor-", "Zar-", "Drak-", "Sylv-", "Kor-", "Ael-", "Zyr-"]
    suffixes = ["-dor", "-lyn", "-thar", "-vax", "-mir", "-ion", "-el", "-or", "-is"]
    return random.choice(prefixes) + random.choice(bases) + random.choice(suffixes)

def fantasy_flare(name, prompt, use_flare=True):
    """
    Adds elvish vibe or raw. Falls back if junk.
    """
    prefixes = ["Thal-", "Ely-", "Vor-", "Zar-", "Drak-", "Sylv-", "Kor-", "Ael-", "Zyr-"]
    suffixes = ["-dor", "-lyn", "-thar", "-vax", "-mir", "-ion", "-el", "-or", "-is"]
    if not use_flare:
        if not ML_AVAILABLE:
            return rule_based_name()
        cleaned = name.replace(prompt, "").replace("'", "").replace('"', "").replace("_", "").replace("Blizzard", "").replace("copyright", "").strip()
        return cleaned if cleaned and len(cleaned) > 4 and cleaned.isalnum() else rule_based_name()
    try:
        cleaned = name.replace(prompt, "").replace("'", "").replace('"', "").replace("_", "").replace("Blizzard", "").replace("copyright", "").replace("image", "").replace("rights", "").replace("history", "").replace("sites", "").replace("started", "").replace("building", "").replace("fire", "").replace("curse", "").replace("monster", "").replace("original", "").replace("mantis", "").replace("kodoku", "").strip()
        words = [w for w in cleaned.split() if len(w) > 4 and w.lower() not in ['the', 'a', 'an', 'and', 'is', 'name', 'this', 'have', 'rights', 'important', 'take', 'ground', 'families', 'image', 'history', 'sites', 'started', 'building', 'fire', 'think', 'just', 'journey', 'magic', 'sorcery', 'really', 'simple', 'curse', 'monster', 'original', 'mantis', 'kodoku'] and w.isalnum()]
        if not words or any(c in "_-©[]{}|⁄ˈ" or c.isdigit() for c in cleaned):
            return rule_based_name()
        target_word = random.choice(words).capitalize()
        return random.choice(prefixes) + target_word + random.choice(suffixes)
    except Exception as e:
        print(f"Flare error: {e}")
        return rule_based_name()

def generate_fantasy_name(prompt, max_new_tokens=8, temperature=0.7, seed=42, use_flare=True):
    """
    Generates name, falls back if ML fails.
    """
    if not ML_AVAILABLE or model is None:
        return rule_based_name()
    try:
        torch.manual_seed(seed)
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        attention_mask = (inputs != tokenizer.pad_token_id).long()
        outputs = model.generate(
            inputs,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_k=5,
            top_p=0.75,
            repetition_penalty=1.5,
            num_return_sequences=1,
            no_repeat_ngram_size=3,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
        name = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        return fantasy_flare(name, prompt, use_flare)
    except Exception as e:
        print(f"Generate error: {e}. Using rule-based fallback.")
        return rule_based_name()

# Test it
prompt = "Single elf name, no spaces: "
print("Basic name (flared):")
print(generate_fantasy_name(prompt))

print("\nWilder (temp 1.2, flared):")
print(generate_fantasy_name(prompt, temperature=1.2, seed=123))

print("\nNew seed (456, flared):")
print(generate_fantasy_name(prompt, seed=456))

print("\nRaw name (no flare):")
print(generate_fantasy_name(prompt, use_flare=False))

print("\nRule-based only (no ML):")
print(rule_based_name())

# Save outputs
try:
    os.makedirs("outputs", exist_ok=True)
    test_prompts = [
        "Single elf name, no spaces: ",
        "Single dragon item name, no spaces: ",
        "Single fantasy village name, no spaces: "
    ]
    for i, p in enumerate(test_prompts):
        name = generate_fantasy_name(p, temperature=0.7 + i*0.2, seed=42 + i * 10)
        with open(f"outputs/name{i+1}.txt", "w", encoding="utf-8") as f:
            f.write(name)
        print(f"Saved '{name}' to outputs/name{i+1}.txt")
except Exception as e:
    print(f"Save error: {e}")