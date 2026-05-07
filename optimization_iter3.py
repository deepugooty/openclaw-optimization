import requests, json, os, re, subprocess

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3.5-hw-optimized"

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

OUTPUT_DIR = os.path.expanduser("~/Desktop/saideepi/openclaw-optimization/output/iter3/ollama")
LOG_DIR = "output/iter3/ollama"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

baseline = {"task1_hello": 15.68, "task2_two_sum": 79.47, "task3_refactor": 356.28}

print(f"\n{'='*55}")
print(f"ITERATION 3 — Hardware-specific Tuning")
print(f"Model: {MODEL}")
print(f"Changes: num_thread=8, num_ctx=64000, top_p=0.8, top_k=20, repeat_penalty=1.1")
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
            "think": True,
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

    b = baseline.get(name, 0)
    imp = ((b - median) / b) * 100 if b else 0

    print(f"  MEDIAN: {median:.2f}s")
    print(f"  Saved:  {output_path}")
    print(f"  Quality: {quality}")
    print(f"  vs Baseline: {imp:.1f}%")

    results.append({
        "task": name,
        "median_s": round(median, 2),
        "baseline_s": b,
        "improvement_pct": round(imp, 1),
        "tok_per_sec": round(last_tps, 1),
        "output_tokens": last_tokens,
        "prompt_tokens": last_prompt_tokens,
        "quality": quality
    })

print(f"\n{'='*55}")
print("BASELINE vs ITER 3")
print(f"{'='*55}")
print(f"{'Task':<20} {'Baseline':<12} {'Iter3':<12} {'Tok/s':<10} {'vs Baseline'}")
print("-"*60)
for r in results:
    print(f"{r['task']:<20} {r['baseline_s']:<12} {r['median_s']:<12} {r['tok_per_sec']:<10} {r['improvement_pct']}%")

with open(f"{LOG_DIR}/results.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved to {LOG_DIR}/results.json")
