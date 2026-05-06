#!/bin/bash
TASK=$1
ITER=$2
mkdir -p logs/${ITER}

echo "=== ${ITER} - ${TASK} ===" | tee -a logs/${ITER}/wall_clock.log
echo "START: $(date +"%H:%M:%S")" | tee -a logs/${ITER}/wall_clock.log
echo "Waiting for task to complete..."
read -p "Press ENTER when agent finishes..."
echo "END: $(date +"%H:%M:%S")" | tee -a logs/${ITER}/wall_clock.log

# Capture Ollama metrics
docker logs openclaw-openclaw-gateway-1 2>&1 | grep -i "eval\|token" | tail -3 >> logs/${ITER}/wall_clock.log

# Verify output
echo "Files created:" | tee -a logs/${ITER}/wall_clock.log
ls ~/.openclaw/workspace/*.py 2>/dev/null | tee -a logs/${ITER}/wall_clock.log
echo "---" | tee -a logs/${ITER}/wall_clock.log
