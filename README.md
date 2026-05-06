# OpenClaw + Qwen 3.5 0.8B Optimization

## Setup
1. Install Docker Desktop
2. Install Ollama: `brew install ollama`
3. Pull model: `ollama pull qwen3.5:0.8b`
4. Clone OpenClaw: `git clone https://github.com/openclaw/openclaw`
5. Start OpenClaw: `cd openclaw && export OPENCLAW_IMAGE=ghcr.io/openclaw/openclaw:latest && docker compose up -d --no-build`
6. After every restart run:
```bash
docker exec -u root openclaw-openclaw-gateway-1 sh -c "curl -fsSL https://download.docker.com/linux/static/stable/aarch64/docker-27.3.1.tgz | tar xz --strip-components=1 -C /usr/local/bin/ docker/docker && chmod +x /usr/local/bin/docker && chmod 666 /var/run/docker.sock"
```

## Environment
- macOS Apple Silicon (aarch64), M2, 8 cores
- Qwen 3.5 0.8B Q8_0
- OpenClaw v2026.5.3
- Ollama with Metal GPU

## Running Benchmarks (Ollama Direct)
```bash
pip3 install requests
python3 benchmark.py          # baseline
python3 benchmark_iter1.py    # iteration 1 - prompt optimization
python3 benchmark_iter2.py    # iteration 2 - hardware tuning
```

## Running Tasks Through OpenClaw Chat (Wall-Clock Measurement)

This measures the full agent experience including tool calls, file writing, and code execution.

1. Open `http://localhost:18789` in your browser
2. Type `/new` and press Enter before every task — this resets session history
3. Record the start time in terminal: `date +"%H:%M:%S"`
4. Paste the task prompt in the chat and press Enter
5. Wait for the agent to finish — watch the tool call blocks (Exec/Write) appear
6. Record the end time: `date +"%H:%M:%S"`
7. Count the tool calls — each Exec or Write block = 1 tool call
8. Check if the output file was created: `cat ~/.openclaw/workspace/<filename>.py`

## Optimization Iterations
- **Iter 1:** Structured prompts + token cap
- **Iter 2:** Disable thinking mode + caching + single bash command
- **Iter 3:** CPU threading + decoding params via Modelfile

## Results Summary

### Ollama Direct
| Task | Baseline | Iter 1 | Iter 3 |
|------|----------|--------|--------|
| Task 1 | 15.68s | 0.61s | 1.72s |
| Task 2 | 79.47s | 8.20s | 8.31s |
| Task 3 | 33.77s | 20.49s | 15.64s |

### OpenClaw Wall-Clock
| Task | Baseline | Iter 1 | Iter 2 |
|------|----------|--------|--------|
| Task 1 time | 2m 57s | 1m 47s | 1m 5s |
| Task 1 tool calls | 17 | 8 | 2 |
| Task 2 time | 1m-11m | 2m 5s | 2m 10s |
| Task 2 tool calls | 1-15 | 6 | 2 |
| Task 3 time | ~14 min | 28 min | 6+ min |
| Task 3 tool calls | 14+ | 32 | 15+ |
