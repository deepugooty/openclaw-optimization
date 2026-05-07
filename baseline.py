import requests, json, os, re, subprocess

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3.5:0.8b"

def extract_code(text):
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    matches = re.findall(r'```python\n(.*?)```', text, re.DOTALL)
    if matches:
        return matches[0]
    matches = re.findall(r'```\n(.*?)```', text, re.DOTALL)
    if matches:
        return matches[0]
    return text

TASKS = [
    ("task1_hello",
     "Create a Python file that prints Hello World",
     "hello.py"),
    ("task2_two_sum",
     "Write a function that finds two numbers in a list that sum to a target",
     "two_sum.py"),
    ("task3_refactor",
     "Refactor this function to handle edge cases and add unit tests:\n\ndef find_max(numbers):\n    max_val = numbers[0]\n    return max_val",
     "find_max.py")
]

def run_benchmark(think_mode, output_subdir, log_subdir):
    OUTPUT_DIR = os.path.expanduser(f"~/Desktop/saideepi/openclaw-optimization/output/{output_subdir}")
    LOG_DIR = f"logs/{log_subdir}"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    label = "WITH Thinking" if think_mode else "WITHOUT Thinking"
    print(f"\n{'='*55}")
    print(f"BASELINE — Ollama Direct — {label}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"{'='*55}")

    results = []

    for name, prompt, filename in TASKS:
        print(f"\n=== {name} ===")
        times = []
        last_response = ""
        last_tps, last_tokens, last_prompt_tokens = 0, 0, 0

        for run in range(3):
            resp = requests.post(OLLAMA_URL, json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "think": think_mode,
                "options": {"temperature": 0.1}
            })
            d = resp.json()
            total = d["total_duration"] / 1e9
            tps = d["eval_count"] / (d["eval_duration"] / 1e9)
            tokens = d["eval_count"]
            prompt_tokens = d["prompt_eval_count"]
            times.append(total)
            last_response = d["message"]["content"]
            thinking = d["message"].get("thinking", "")
            last_tps, last_tokens, last_prompt_tokens = tps, tokens, prompt_tokens
            print(f"  Run {run+1}: {total:.2f}s | {tps:.1f} tok/s | {tokens} out tokens | {prompt_tokens} prompt tokens | thinking: {'yes' if thinking else 'no'}")

        median = sorted(times)[1]
        code = extract_code(last_response)
        output_path = os.path.join(OUTPUT_DIR, filename)
        with open(output_path, "w") as f:
            f.write(code)

        try:
            result = subprocess.run(["python3", output_path], capture_output=True, text=True, timeout=10)
            quality = "✅ runs" if result.returncode == 0 else f"❌ {result.stderr[:80]}"
        except Exception as e:
            quality = f"❌ {str(e)[:80]}"

        print(f"  MEDIAN: {median:.2f}s")
        print(f"  Saved:  {output_path}")
        print(f"  Quality: {quality}")

        results.append({
            "task": name,
            "think": think_mode,
            "median_s": round(median, 2),
            "tok_per_sec": round(last_tps, 1),
            "output_tokens": last_tokens,
            "prompt_tokens": last_prompt_tokens,
            "quality": quality
        })

    print(f"\n{'='*55}")
    print(f"SUMMARY — {label}")
    print(f"{'='*55}")
    print(f"{'Task':<20} {'Median':<10} {'Tok/s':<10} {'Out Tok':<10} {'Quality'}")
    print("-"*60)
    for r in results:
        print(f"{r['task']:<20} {r['median_s']:<10} {r['tok_per_sec']:<10} {r['output_tokens']:<10} {r['quality']}")

    with open(f"{LOG_DIR}/results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to {LOG_DIR}/results.json")
    return results

# Run both modes
print("\n🔵 Running WITHOUT thinking mode...")
results_no_think = run_benchmark(False, "baseline_ollama/no_thinking", "baseline_ollama/no_thinking")

print("\n\n🟡 Running WITH thinking mode...")
results_think = run_benchmark(True, "baseline_ollama/thinking", "baseline_ollama/thinking")

# Comparison
print(f"\n{'='*65}")
print("THINKING vs NON-THINKING COMPARISON")
print(f"{'='*65}")
print(f"{'Task':<20} {'No Think (s)':<15} {'Think (s)':<15} {'Overhead'}")
print("-"*65)
for r1, r2 in zip(results_no_think, results_think):
    overhead = ((r2['median_s'] - r1['median_s']) / r1['median_s']) * 100
    sign = "+" if overhead > 0 else ""
    print(f"{r1['task']:<20} {r1['median_s']:<15} {r2['median_s']:<15} {sign}{overhead:.1f}%")
