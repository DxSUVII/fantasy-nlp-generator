# Fantasy NLP Name Generator

 this is a lightweight fantasy name generator built with DistilGPT-2 for Red Panda Games' NLP assignment. I started with full GPT-2, but my 2GB RAM laptop threw a "paging file too small" (os error 1455) tantrum, so I pivoted to DistilGPT-2 (82M params, ~300MB load)—it’s 97% as good but fits like a glove on low-spec hardware. No GPU, no dataset, just pre-trained magic with tight prompts to spit clean middle names like "Sylvar" or "Eldrin," then I add elvish flair (prefixes like "Zar-", suffixes like "-vax") for that D&D boss energy. If ML flakes (RAM crash, segfault), it falls back to rule-based for reliability—efficiency first, always.

The whole thing runs local or in Colab, generates text assets (names for elves, swords, villages), and shows how params like temperature and seed change outputs. API included for production vibes. This was a grind on 2GB RAM, but it’s stable now—ML-focused, with fallbacks to keep it rolling.

## Setup
- Activate env: `source env/Scripts/activate` (Windows) or `source env/bin/activate` (Mac/Linux).
- Install: `pip install -r requirements.txt`.
- Run: `python generate.py` (script), `python app.py` (API), `python experiments.py` (tests).

## Model/Why DistilGPT-2?
- **Model**: DistilGPT-2 (Hugging Face transformers). It's a distilled version of GPT-2-small—half the params (82M vs 124M), loads in ~300MB, runs on CPU without GPU. Pre-trained on massive English text, so it "knows" fantasy vibes from books/games without fine-tuning.
- **Why?**: Started with full GPT-2 for creativity, but my 2GB laptop choked on download/load (pagefile error 1455, segfaults on Flask restart). Switched to DistilGPT-2 for efficiency—retains 97% performance, fits RAM, no crashes. No dataset needed (pre-trained), but tight prompts ("Single elf name, no spaces: ") guide it to names, not stories.
- **Struggles & Debugging**: 
  - **RAM Hell**: 2GB total RAM meant model load swapped to disk, causing "paging file too small." Fixed by switching models, preloading in API, `gc.collect()` for memory cleanup, and `debug=False` in Flask to avoid reload crashes.
  - **Junk Names**: ML spat non-fantasy BS like "Table," "Class," "Following," "Based" (training data noise). Fixed with expanded blocklist in `fantasy_flare` (50+ words like "table," "class," "following," "player," "quest"), tighter sampling (top_k=3, top_p=0.65, repetition_penalty=1.8), and `max_new_tokens=8` to keep outputs short.
  - **Unicode Crap**: “【curse” or “/ˈk.eɛnhʀ̃” from training data. Fixed with `isalnum()` filter and special char check in `fantasy_flare`.
  - **Raw Mode Bug**: Raw names (`use_flare=False`) kept prefixes/suffixes. Fixed by stripping them explicitly.
  - **Segfaults**: Flask debug mode reloaded model, tanking RAM. Fixed with `debug=False` and fallback.
  - **Efficiency**: All runs in <1s on 2GB RAM. ML for creativity, fallback for stability—shows how to make NLP work on low-spec hardware.

## Features
- **Generation**: ML middle name (e.g., “Sylvar”) + optional flair (prefix/suffix for “Zar-Sylvar-vax”).
- **API**: Flask endpoint `/generate?prompt=...&temperature=1.0&seed=42&use_flare=true` returns JSON `{"name": "Zar-Sylvar-vax"}`.
- **Experiments**: Tests temperature, seed, flare; includes validation (length, fantasy-like regex).
- **Outputs**: Text files in `outputs/` (e.g., “Kor-Zorath-ion”).
- **Fallback**: Rule-based names if ML crashes (e.g., “Sylv-Eldrin-is”).

## Params Tested
- **Temperature**: 0.5 (safe, consistent names), 1.2 (wild, creative but risky).
- **Seed**: 42, 123, 456 (reproducibility and variety).
- **Flare**: On (polished with prefix/suffix), Off (raw ML middle).
- **Observations**: Low temp = reliable (e.g., “Thal-Eldrin-lyn”). High temp = bold (e.g., “Zar-Zephyra-vax”). Seeds vary style. Flare adds game vibe but can amplify junk (fixed with blocklist). Raw middles shorter (8–10 chars) vs. flared (12–14 chars). All pass fantasy regex (capital start, letters/hyphens, letter end).
- **Validation**: Length (8–14 chars), fantasy-like (regex: ^[A-Z][a-zA-Z-]*[a-z]$). All pass—see `experiments.md`.

## Code Breakdown
- **generate.py**: Core script—loads model, generates names, saves outputs. Handles RAM with fallback.
- **app.py**: Flask API—preloads model, endpoints `/generate` for prompt-based names.
- **experiments.py**: Runs parameter tests, validation, prints results.
- **fantasy_flare**: Post-processing—adds prefix/suffix or strips for raw. Blocklist nukes junk.

## Trade-Offs
- **ML vs. Rule-Based**: ML for creativity, but flaky on low RAM (segfaults, junk). Rule-based for reliability, but less "wow." Chose ML main with fallback—balances efficiency.
- **Efficiency**: Tight sampling (top_k=3) cuts junk but reduces variety. `max_new_tokens=8` keeps short names but limits detail.
- **No Fine-Tuning**: Pre-trained for speed, but junk from general text. Trade-off: Fast on 2GB RAM vs. perfect fantasy names.

## Next Steps
- Fine-tune DistilGPT-2 on fantasy dataset (e.g., D&D names from Kaggle) for better middles.
- Add job queue (RQ or Celery) for batch generation.
- Post-processing: Normalize length, style checks (e.g., vowel count for "fantasy feel").

## Notes
- Low-RAM (2GB) optimizations: Fallback, `debug=False`, model preloading, `gc.collect()`.
- Error handling: Try/except for model load, generation, saves, API crashes.
- Tested on Windows/Git Bash, Python 3.10+.

