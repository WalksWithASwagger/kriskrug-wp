#!/bin/bash

# Real-time agent swarm monitor for kriskrug.co

clear
echo "🤖 KRISKRUG.CO AGENT SWARM MONITOR"
echo "=================================="
echo ""

while true; do
    # Get workflow runs
    echo "📊 Latest Agent Activity (Last 10 workflows):"
    gh run list --limit 10 --json status,conclusion,displayTitle,createdAt \
        --jq '.[] | "\(.status | ascii_upcase): \(.displayTitle) (\(.createdAt | split("T")[1] | split(".")[0]))"'
    
    echo ""
    echo "📈 Issue Status:"
    
    # Count by status
    total=$(gh issue list --limit 100 | wc -l | xargs)
    auto=$(gh issue list --label "auto-implement" --limit 100 | wc -l | xargs)
    open=$(gh issue list --state open --limit 100 | wc -l | xargs)
    
    echo "  Total Issues: $total"
    echo "  Auto-Implement: $auto"
    echo "  Still Open: $open"
    
    # Progress bar
    if [ $total -gt 0 ]; then
        completed=$((total - open))
        percent=$((completed * 100 / total))
        filled=$((percent / 2))
        empty=$((50 - filled))
        
        echo ""
        echo -n "  Progress: ["
        for ((i=0; i<filled; i++)); do echo -n "█"; done
        for ((i=0; i<empty; i++)); do echo -n "░"; done
        echo "] $percent%"
    fi
    
    echo ""
    echo "🔄 Refreshing in 30 seconds... (Ctrl+C to stop)"
    echo ""
    
    sleep 30
    clear
    echo "🤖 KRISKRUG.CO AGENT SWARM MONITOR"
    echo "=================================="
    echo ""
done
