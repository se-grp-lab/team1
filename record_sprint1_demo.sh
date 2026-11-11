#!/usr/bin/env bash
set -e

REPO_DIR="/home/andey/Documents/Sem5/SE/group_project/team1"
OUTPUT_VIDEO="$REPO_DIR/VAMC_Sprint1_Demo.mp4"
ARTIFACT_DIR="/home/andey/.gemini/antigravity-cli/brain/29037a4d-5b2e-4223-8768-a96f6bb7003d"

cd "$REPO_DIR"

# Clean up old file
rm -f "$OUTPUT_VIDEO"

echo "Starting screen recording via wf-recorder..."
wf-recorder -f "$OUTPUT_VIDEO" &
WF_PID=$!

# Give wf-recorder a second to initialize frames
sleep 1.5

echo "Launching interactive demo in Ghostty..."
ghostty --title="VAMC Sprint 1 Feature Demo" -e bash -c "cd $REPO_DIR && PYTHONPATH=. python3 demo_runner.py; sleep 2" &
GHOSTTY_PID=$!

# Focus & maximize/fullscreen in Niri
sleep 0.8
niri msg action fullscreen-window || true

# Wait for ghostty process to exit
wait $GHOSTTY_PID || true

echo "Demo finished. Finalizing recording..."
sleep 1.5

# Un-fullscreen if needed
niri msg action fullscreen-window || true

kill -2 $WF_PID 2>/dev/null || true
wait $WF_PID 2>/dev/null || true

echo "Copying video to artifacts..."
cp "$OUTPUT_VIDEO" "$ARTIFACT_DIR/VAMC_Sprint1_Demo.mp4"

echo "Verifying video properties..."
ffprobe -hide_banner "$OUTPUT_VIDEO" 2>&1 | grep -E "Duration|Stream #0:0"

echo "Recording complete: $OUTPUT_VIDEO"
