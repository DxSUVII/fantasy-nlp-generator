from flask import Flask, request, jsonify
from generate import generate_fantasy_name, ML_AVAILABLE, model, tokenizer
import torch

app = Flask(__name__)

# Preload model to avoid RAM issues
if ML_AVAILABLE and model is None:
    try:
        from transformers import GPT2LMHeadModel, GPT2Tokenizer
        model_name = "distilgpt2"
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        model = GPT2LMHeadModel.from_pretrained(model_name)
        tokenizer.pad_token = tokenizer.eos_token
        print("Model preloaded for API!")
    except Exception as e:
        print(f"Model preload failed: {e}. Using rule-based only.")
        ML_AVAILABLE = False

@app.route('/generate', methods=['GET'])
def generate():
    prompt = request.args.get('prompt', 'Single elf name, no spaces: ')
    temperature = float(request.args.get('temperature', 0.7))
    seed = int(request.args.get('seed', 42))
    use_flare = request.args.get('use_flare', 'true').lower() == 'true'
    try:
        name = generate_fantasy_name(prompt, max_new_tokens=8, temperature=temperature, seed=seed, use_flare=use_flare)
        return jsonify({'name': name})
    except Exception as e:
        print(f"API error: {e}. Using rule-based fallback.")
        name = generate_fantasy_name(prompt, max_new_tokens=8, temperature=temperature, seed=seed, use_flare=use_flare)
        return jsonify({'name': name})

if __name__ == '__main__':
    try:
        app.run(debug=False)  # Disable debug to avoid segfault
    except Exception as e:
        print(f"Flask error: {e}")