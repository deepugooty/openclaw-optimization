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
     """Task: Print Hello World
Requirement:
- Create a Python file
- Print exactly: Hello World
Output:
- Complete Python code""",
     "hello.py"),

    ("task2_two_sum",
     """Task: Two Sum
Requirement: Create a Python file
Input:
  nums: list[int]
  target: int
Output:
  indices of two numbers such that nums[i] + nums[j] = target
Constraints:
  exactly one solution
  cannot use same element twice
  return indices in any order
Example: nums = [2,7,11,15], target = 9 → [0,1]""",
     "two_sum.py"),

    ("task3_refactor",
     """Task: Refactor, Optimize, and Test Python Function
Objectives:
1. Fix logical bugs
2. Prevent using the same index twice
3. Handle edge cases
4. Improve readability and structure
5. Optimize time complexity (target: O(n))
6. Add unit tests

Input Code:
def find_pair(nums, target):
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[i] + nums[j] == target:
                return i, j

Requirements:
- Return tuple (i, j) where i != j
- Return None if no valid pair exists
- Handle edge cases: empty list, list with one element, duplicate values, negative numbers
- Use efficient approach (hash map preferred)

Testing:
- Use pytest
- Include at least 5 test cases: normal case, no solution, duplicate numbers, negative numbers, small input edge case

Output Format:
1. Refactored function
2. Explanation (brief, max 5 lines)
3. Test cases (pytest)""",
     "find_pair.py")
]

baseline = {"task1_hello": 0, "task2_two_sum": 0, "task3_refactor": 0}

def run_benchmark(think_mode, output_subdir, log_subdir):
    OUTPUT_DIR = os.path.expanduser(f"~/Desktop/saideepi/openclaw-optimization/output/{output_subdir}")
    LOG_DIR = f"logs/{log_subdir}"
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    label = "WITH Thinking" if think_mode else "WITHOUT Thinking"
    print(f"\n{'='*55}")
    print(f"ITERATION 1 — Optimized Prompts — {label}")
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

    with open(f"{LOG_DIR}/results.json", "w") as f:
        json.dump(results, f, indent=2)

    return results

# Run both modes
print("\n🔵 Running WITHOUT thinking mode...")
results_no_think = run_benchmark(False, "iter1/no_thinking", "iter1/no_thinking")

print("\n\n🟡 Running WITH thinking mode...")
results_think = run_benchmark(True, "iter1/thinking", "iter1/thinking")

# Comparison
print(f"\n{'='*65}")
print("ITER1 — THINKING vs NON-THINKING")
print(f"{'='*65}")
print(f"{'Task':<20} {'No Think (s)':<15} {'Think (s)':<15} {'Overhead'}")
print("-"*65)
for r1, r2 in zip(results_no_think, results_think):
    overhead = ((r2['median_s'] - r1['median_s']) / r1['median_s']) * 100
    sign = "+" if overhead > 0 else ""
    print(f"{r1['task']:<20} {r1['median_s']:<15} {r2['median_s']:<15} {sign}{overhead:.1f}%")
