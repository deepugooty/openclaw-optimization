# Command Reference — OpenClaw + Qwen 3.5 0.8B Optimization

## Docker — Container Management

# Start OpenClaw containers
export OPENCLAW_IMAGE=ghcr.io/openclaw/openclaw:latest
docker compose up -d --no-build

# Stop all containers
docker compose down

# Restart gateway
docker restart openclaw-openclaw-gateway-1

# Check running containers
docker ps

# View logs
docker logs openclaw-openclaw-gateway-1 2>&1 | tail -20

# Follow logs live
docker logs -f openclaw-openclaw-gateway-1 2>&1

# Filter logs
docker logs openclaw-openclaw-gateway-1 2>&1 | grep -i "error\|agent model\|tool"

# Run command inside container as root
docker exec -u root openclaw-openclaw-gateway-1 sh -c "command"

# Copy file from container to Mac
docker cp openclaw-openclaw-gateway-1:/path/inside ~/Desktop/file.py

# Copy file from Mac to container
docker cp ~/Desktop/file.py openclaw-openclaw-gateway-1:/path/inside/

# Build sandbox image
docker build -f Dockerfile.sandbox -t openclaw-sandbox:bookworm-slim .

## Docker — Install Docker CLI Inside Container (Run After Every Restart)

docker exec -u root openclaw-openclaw-gateway-1 sh -c "
curl -fsSL https://download.docker.com/linux/static/stable/aarch64/docker-27.3.1.tgz \
  | tar xz --strip-components=1 -C /usr/local/bin/ docker/docker
chmod +x /usr/local/bin/docker
chmod 666 /var/run/docker.sock
"

## OpenClaw — Config Management

# Read main config
docker exec openclaw-openclaw-gateway-1 \
  python3 -c "import json; print(json.dumps(json.load(open('/home/node/.openclaw/openclaw.json')), indent=2))"

# Read agent models config
docker exec openclaw-openclaw-gateway-1 \
  python3 -c "import json; print(json.dumps(json.load(open('/home/node/.openclaw/agents/main/agent/models.json')), indent=2))"

# Disable sandbox
docker exec openclaw-openclaw-gateway-1 \
  python3 -c "
import json
p='/home/node/.openclaw/openclaw.json'
c=json.load(open(p))
c['agents']['defaults']['sandbox']['mode']='off'
json.dump(c,open(p,'w'),indent=2)
print('done')
"

# Set primary model
docker exec openclaw-openclaw-gateway-1 \
  python3 -c "
import json
p='/home/node/.openclaw/openclaw.json'
c=json.load(open(p))
c['agents']['defaults']['model']['primary'] = 'ollama/qwen3.5:0.8b'
json.dump(c,open(p,'w'),indent=2)
print('done')
"

# Disable thinking mode + enable caching (Iteration 2)
docker exec openclaw-openclaw-gateway-1 \
  python3 -c "
import json
p='/home/node/.openclaw/agents/main/agent/models.json'
c=json.load(open(p))
c['providers']['ollama']['options'] = {'think': False, 'num_keep': 48}
json.dump(c,open(p,'w'),indent=2)
print('done')
"

# Clear all sessions
docker exec openclaw-openclaw-gateway-1 \
  python3 -c "
import json
json.dump({}, open('/home/node/.openclaw/agents/main/sessions/sessions.json','w'))
print('cleared')
"

# Delete BOOTSTRAP.md
docker exec openclaw-openclaw-gateway-1 rm -f /home/node/.openclaw/workspace/BOOTSTRAP.md

# Run openclaw doctor to disable unused skills
docker exec -it openclaw-openclaw-gateway-1 openclaw doctor --fix

# Check what model OpenClaw is using
docker logs openclaw-openclaw-gateway-1 2>&1 | grep "agent model" | tail -3

# Check workspace files
docker exec openclaw-openclaw-gateway-1 ls /home/node/.openclaw/workspace/

## Ollama — Model Management

# Start Ollama server
ollama serve &

# Check running models
ollama ps

# List installed models
ollama list

# Pull model
ollama pull qwen3.5:0.8b

# Show model details
ollama show qwen3.5:0.8b

# Create custom model from Modelfile
ollama create qwen3.5-hw-optimized -f modelfiles/Modelfile.iter3_final

# Stop a running model
ollama stop qwen3.5:0.8b

# Test model directly
ollama run qwen3.5:0.8b "say hello"

## Ollama — API Testing

# Test via chat API (supports thinking mode)
curl -s http://localhost:11434/api/chat \
  -d '{"model":"qwen3.5:0.8b","messages":[{"role":"user","content":"say hello"}],"stream":false,"think":false}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['message']['content'][:100])"

# Test tool calling capability
curl -s http://localhost:11434/api/chat -d '{
  "model": "qwen3.5:0.8b",
  "messages": [{"role": "user", "content": "Use the get_date tool"}],
  "tools": [{"type":"function","function":{"name":"get_date","description":"Get date","parameters":{}}}],
  "stream": false
}' | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d['message'], indent=2))"

## Benchmarking

# Run baseline benchmark
python3 benchmark.py

# Run Iteration 1 benchmark (prompt optimization)
python3 benchmark_iter1.py

# Run Iteration 2 benchmark (hardware tuning via Ollama direct)
python3 benchmark_iter2.py

# Run Iteration 3 benchmark (hardware tuning)
python3 benchmark_iter3.py

# Quick single task measurement
python3 -c "
import requests
resp = requests.post('http://localhost:11434/api/chat', json={
    'model': 'qwen3.5:0.8b',
    'messages': [{'role': 'user', 'content': 'Create a Python file that prints Hello World'}],
    'stream': False,
    'think': False,
    'options': {'temperature': 0.1}
})
d = resp.json()
print(f'total: {d[\"total_duration\"]/1e9:.2f}s')
print(f'tok/s: {d[\"eval_count\"]/(d[\"eval_duration\"]/1e9):.1f}')
print(f'tokens: {d[\"eval_count\"]}')
"

## Wall-Clock Timing (OpenClaw Chat)

# Record start time before sending prompt
date +"%H:%M:%S"

# Record end time after agent finishes
date +"%H:%M:%S"

# Verify output files were created
cat ~/.openclaw/workspace/hello.py
cat ~/.openclaw/workspace/two_sum.py
cat ~/.openclaw/workspace/find_pair.py

# Run generated files to verify correctness
python3 ~/.openclaw/workspace/hello.py

# Run pytest on generated tests
docker exec openclaw-openclaw-gateway-1 sh -c "
cd /home/node/.openclaw/workspace && python3 -m pytest test_find_pair.py -v
"

## Git — Repository Management

# Add and commit
git add .
git commit -m "message"
git push

# Pull before push if rejected
git pull origin main --rebase
git push

# Check status
git status
git log --oneline | head -10

## macOS — System Commands

# Check physical CPU cores
sysctl -n hw.physicalcpu

# Find Docker binary location
which docker
readlink -f $(which docker)

# Force quit Docker Desktop
sudo killall -9 "Docker Desktop"
open /Applications/Docker.app
