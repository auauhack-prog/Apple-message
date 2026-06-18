#!/bin/bash
cd "$(dirname "$0")"
python3 graph.py
echo ""
echo "按任意键关闭窗口..."
read -n 1
