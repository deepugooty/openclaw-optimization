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
    ("task1_hello", "Task: Print Hello World\nRequirement:\n- Create a Python file\n- Print exactly: Hello World\nOutput:\n- Complete Python code", "hello.py"),
    ("task2_two_sum", "Task: Two Sum\nRequirement: Create a Python file\nInput:\n  nums: list[int]\n  target: int\nOutput:\n  indices of two numbers such that nums[i] + nums[j] = target\nConstraints:\n  exactly one solution\n  cannot use same element twice\n  return indices in any order\nExample: nums = [2,7,11,15], target = 9 → [0,1]", "two_sum.py"),
    ("task3_refactor", "Task: Refactor, Optimize, and Test Python Function\nObjectives:\n1. Fix logical bugs\n2. Prevent using the same index twice\n3. Handle edge cases\n4. Optimize time complexity (target: O(n))\n5. Add unit tests\n\nInput Code:\ndef find_pair(nums, target):\n    for i in range(len(nums)):\n        for j in range(len(nums)):\n            if nums[i] + nums[j] == target:\n                return i, j\n\nRequirements:\n- Return tuple (i, j) where i != j\n- Return None if no valid pair exists\n- Handle edge cases: empty list, single element, duplicates, negatives\n- Use hash map (O(n))\n\nTesting:\n- pytest, at least 5 test cases", "find_pair.py")
]

OUTPUT_DIR = os.path.expanduser("~/Desktop/saideepi/openclaw-optimization/output/iter2/ollama")
LOG_DIR = "logs/iter2"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

baseline = {"task1_hello": 15.68, "task2_two_sum": 79.47, "task3_refactor": 356.28}
iter1 = {"task1_hello": 3.49, "task2_two_sum": 8.20, "task3_refactor": 20.49}

print(f"\n{'='*55}")
print(f"ITERATION 2 — Hardware Tuning")
print(f"Model: {MODEL}")
print(f"Changes: num_thread=8, top_p=0.8, top_k=20, repeat_penalty=1.1")
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
            "think": False,
            "options": {"temperature": 0.1}
        })
        d = resp.json()
        total = d["total_duration"] / 1e9
        tps = d["eval_count"] / (d["eval_duration"] / 1e9)
        tokens = d["eval_count"]
        prompt_tokens = d["prompt_eval_count"]
        times.append(total)
        last_response = d["message"]["content"]
        last_tps, last_tokens, last_prompt_tokens = tps, tokens, prompt_tokens
        print(f"  Run {run+1}: {total:.2f}s | {tps:.1f} tok/s | {tokens} out tokens | {prompt_tokens} prompt tokens")

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
    i1 = iter1.get(name, 0)
    imp = ((b - median) / b) * 100 if b else 0

    print(f"  MEDIAN: {median:.2f}s")
    print(f"  Saved:  {output_path}")
    print(f"  Quality: {quality}")
    print(f"  vs Baseline: {imp:.1f}%")

    results.append({
        "task": name,
        "median_s": round(median, 2),
        "baseline_s": b,
        "iter1_s": i1,
        "improvement_pct": round(imp, 1),
        "tok_per_sec": round(last_tps, 1),
        "output_tokens": last_tokens,
        "prompt_tokens": last_prompt_tokens,
        "quality": quality
    })

print(f"\n{'='*55}")
print("BASELINE vs ITER1 vs ITER2")
print(f"{'='*55}")
print(f"{'Task':<20} {'Baseline':<12} {'Iter1':<12} {'Iter2':<12} {'vs Baseline'}")
print("-"*68)
for r in results:
    print(f"{r['task']:<20} {r['baseline_s']:<12} {r['iter1_s']:<12} {r['median_s']:<12} {r['improvement_pct']}%")

with open(f"{LOG_DIR}/results.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"\nSaved to {LOG_DIR}/results.json")
