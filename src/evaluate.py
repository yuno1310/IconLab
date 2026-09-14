"""Reusable evaluation: python -m src.evaluate --help."""
import argparse
import hashlib
import importlib
import json
import platform
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from .agent import ROOT, ask

def contains(text,term):
    import re
    return re.search(r'(?<!\w)'+re.escape(term.lower())+r'(?!\w)',text.lower()) is not None

def score(case,result):
    expected=set(case['expected_sources']); retrieved=set(result.get('retrieved_sources',[]))
    recall=len(expected&retrieved)/len(expected) if expected else float(not retrieved)
    retrieval=expected<=retrieved if expected else not retrieved
    citations=set(result.get('citations',[]))
    if case['must_refuse']:
        generation=result.get('refused') is True and not citations
    else:
        generation=(result.get('refused') is False and expected<=citations and citations<=retrieved
          and all(contains(result.get('answer',''),t) for t in case['required_terms'])
          and not any(contains(result.get('answer',''),t) for t in case.get('forbidden_terms',[])))
    if result.get('error'): generation=False
    return {'retrieval_pass':bool(retrieval),'source_recall':recall,'generation_pass':bool(generation)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--mode',choices=['naive','improved'],default='improved')
    p.add_argument('--backend',choices=['fixture','ollama'],default='fixture')
    p.add_argument('--golden',type=Path,default=ROOT/'golden-set.yaml')
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--adapter',help='Optional module:function accepting question and returning answer/citations/refused/retrieved_sources')
    args=p.parse_args(); args.out.mkdir(parents=True,exist_ok=True)
    cases=json.loads(args.golden.read_text(encoding='utf-8'))['questions']
    if len({c['id'] for c in cases})!=len(cases): raise ValueError('Duplicate case IDs')
    adapter=None
    if args.adapter:
        module,function=args.adapter.split(':'); adapter=getattr(importlib.import_module(module),function)
    trace=args.out/'traces.jsonl'
    if trace.exists(): raise FileExistsError('Choose a new output folder; evidence must not be silently overwritten')
    rows=[]
    for case in cases:
        try: result=adapter(case['question']) if adapter else ask(case['question'],args.mode,args.backend,trace)
        except Exception as exc: result={'answer':'','citations':[],'retrieved_sources':[],'refused':False,'error':f'{type(exc).__name__}: {exc}'}
        rows.append({**case,**score(case,result),'actual':result})
    n=len(rows)
    summary={'recorded_at':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),
      'backend':args.backend if not adapter else args.adapter,'mode':args.mode,'n':n,
      'golden_sha256':hashlib.sha256(args.golden.read_bytes()).hexdigest(),
      'corpus_sha256':hashlib.sha256((ROOT/'corpus/index.json').read_bytes()).hexdigest(),
      'retrieval_passes':sum(r['retrieval_pass'] for r in rows),'generation_passes':sum(r['generation_pass'] for r in rows),
      'errors':sum(bool(r['actual'].get('error')) for r in rows),'categories':dict(Counter(c['category'] for c in cases)),
      'warning':'Fixture results are deterministic test-double results, not model quality evidence.' if args.backend=='fixture' and not adapter else 'Rule-based grading requires human calibration.'}
    (args.out/'results.json').write_text(json.dumps({'summary':summary,'rows':rows},indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))
    if summary['errors']: raise SystemExit(1)

if __name__=='__main__': main()
