from generate import generate_fantasy_name

def run_experiments():
    prompt = "Single elf name, no spaces: "
    configs = [
        {'temperature': 0.5, 'seed': 42, 'use_flare': True},
        {'temperature': 1.2, 'seed': 123, 'use_flare': True},
        {'temperature': 0.7, 'seed': 456, 'use_flare': True},
        {'temperature': 0.7, 'seed': 42, 'use_flare': False},
    ]
    results = []
    for config in configs:
        name = generate_fantasy_name(
            prompt,
            max_new_tokens=8,
            temperature=config['temperature'],
            seed=config['seed'],
            use_flare=config['use_flare']
        )
        results.append({
            'prompt': prompt,
            'temperature': config['temperature'],
            'seed': config['seed'],
            'use_flare': config['use_flare'],
            'name': name
        })
    return results

if __name__ == '__main__':
    results = run_experiments()
    for r in results:
        print(f"Prompt: {r['prompt']}, Temp: {r['temperature']}, Seed: {r['seed']}, Flare: {r['use_flare']}, Name: {r['name']}")