import requests, json, time, sys

MODEL = "qwen3.5:0.8b"
URL = "http://localhost:11434/api/generate"

TASKS = [
    ("task1_hello", "Create a Python file called hello.py that prints Hello World."),
    ("task2_two_sum", "Write a function that finds two numbers in a list that sum to a target."),
    ("task3_refactor", "Refactor this function to handle edge cases and add unit tests:\n\ndef find_max(numbers):\n    max_val = numbers[0]\n    return max_val")
]

results = []

for name, prompt in TASKS:
    print(f"\n{'='*50}")
    print(f"Task: {name}")
    print(f"{'='*50}")
    
    # Run 3 times, take median
    times = []
    for run in range(3):
        resp = requests.post(URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1}
        })
        d = resp.json()
        total = d["total_duration"] / 1e9
        toks = d["eval_count"]
        tps = d["eval_count"] / (d["eval_duration"] / 1e9)
        load = d["load_duration"] / 1e9
        prompt_toks = d["prompt_eval_count"]
        times.append(total)
        print(f"  Run {run+1}: {total:.2f}s | {tps:.1f} tok/s | {toks} output tokens")
    
    median = sorted(times)[1]
    results.append({
        "task": name,
        "median_s": round(median, 2),
        "tok_per_sec": round(tps, 1),
        "output_tokens": toks,
        "prompt_tokens": prompt_toks,
        "load_duration_s": round(load, 2)
    })
    print(f"  MEDIAN: {median:.2f}s")

print("\n" + "="*50)
print("BASELINE SUMMARY")
print("="*50)
for r in results:
    print(f"{r['task']}: {r['median_s']}s | {r['tok_per_sec']} tok/s | {r['output_tokens']} tokens")

with open("logs/baseline/results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nSaved to logs/baseline/results.json")
