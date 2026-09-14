"""Aggregate persisted observations; never measures latency itself."""
import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from .agent import ROOT

def percentile(values,p):
    return sorted(values)[max(0,math.ceil(len(values)*p)-1)]
def main():
    p=argparse.ArgumentParser(); p.add_argument('traces',type=Path); p.add_argument('--out',type=Path,required=True)
    p.add_argument('--input-usd-per-million',type=float); p.add_argument('--output-usd-per-million',type=float)
    p.add_argument('--price-source',default='Not supplied; cost not estimated')
    a=p.parse_args(); rows=[json.loads(l) for l in a.traces.read_text().splitlines() if l]
    grouped=defaultdict(list)
    for t in rows:
        for o in t['observations']: grouped[(t['backend'],o['name'])].append(o)
    guesses=json.loads((ROOT/'evidence/latency-guesses.json').read_text()); report=[]
    for (backend,node),obs in grouped.items():
        ms=[(o['end']-o['start'])*1000 for o in obs]
        inp=None if any(o['tokens']['input'] is None for o in obs) else sum(o['tokens']['input'] for o in obs)
        out=None if any(o['tokens']['output'] is None for o in obs) else sum(o['tokens']['output'] for o in obs)
        cost=None if inp is None or out is None or a.input_usd_per_million is None or a.output_usd_per_million is None else (inp*a.input_usd_per_million+out*a.output_usd_per_million)/1e6
        guess=guesses[backend][node]
        report.append({'backend':backend,'node':node,'n':len(obs),'p50_ms':percentile(ms,.5),'p95_ms':percentile(ms,.95),
                       'guessed_p50_ms':guess['p50'],'guessed_p95_ms':guess['p95'],
                       'p50_gap_ms':percentile(ms,.5)-guess['p50'],'p95_gap_ms':percentile(ms,.95)-guess['p95'],
                       'input_tokens':inp,'output_tokens':out,'modeled_usd':cost})
    a.out.write_text(json.dumps({'trace_source':str(a.traces),'price_source':a.price_source,'percentile':'nearest rank','rows':report},indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
