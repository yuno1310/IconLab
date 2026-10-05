"""Ask the lab a question: python -m src.chat --help."""
import argparse
import json
from pathlib import Path
from .agent import ask

def main():
    parser = argparse.ArgumentParser(description='Ask the owned local RAG lab a question.')
    parser.add_argument('--question', required=True, help='Question of 1 to 2000 characters')
    parser.add_argument('--backend', choices=['ollama', 'fixture'], default='ollama')
    parser.add_argument('--mode', choices=['naive', 'improved'], default='improved')
    parser.add_argument('--trace', type=Path, default=Path('tmp/demo/traces.jsonl'))
    args = parser.parse_args()
    if not 1 <= len(args.question) <= 2000:
        parser.error('Question length must be 1..2000')
    result = ask(args.question, args.mode, args.backend, args.trace)
    print(json.dumps({'backend': args.backend, 'mode': args.mode,
        'warning': 'Extractive test double, not an LLM answer.' if args.backend == 'fixture' else 'Local model output; review the cited evidence.',
        **result}, indent=2, ensure_ascii=True))
    if result.get('error'):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
