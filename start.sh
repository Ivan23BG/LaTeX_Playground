#!/usr/bin/env bash
# Initial setup
# python3 -m venv .venv
source .venv/bin/activate
# pip install -r requirements.txt > /dev/null 2>&1
# pip freeze > requirements.txt
# pip install -r requirements.txt > /dev/null 2>&1


# Menu system
case "$1" in
  python)
    python Python/main.py
    ;;
  test)
    echo "Running tests..."
    echo "to fill in"
    ;;
  latex)
    cd LaTeX && python run.py
    ;;
  clean)
    rm -rf __pycache__ .pytest_cache
    ;;
  *)
    echo "Usage:"
    echo "./start.sh python     ->   run project"
    echo "./start.sh test    ->   run tests"
    echo "./start.sh latex   ->   compile LaTeX"
    echo "./start.sh clean   ->   clean files"
    ;;
esac