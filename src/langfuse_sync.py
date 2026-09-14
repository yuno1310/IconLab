"""Replay persisted spans to pinned local Langfuse v2 and export them back."""
import argparse
import base64
import json
import os
import urllib.request
from datetime import datetime,timezone
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument('traces',type=Path); p.add_argument('--export',type=Path,required=True); a=p.parse_args()
    host='http://127.0.0.1:3000'
    auth=base64.b64encode((os.environ['LANGFUSE_PUBLIC_KEY']+':'+os.environ['LANGFUSE_SECRET_KEY']).encode()).decode()
    def request(path,data=None):
        req=urllib.request.Request(host+path,data=json.dumps(data).encode() if data is not None else None,headers={'Authorization':'Basic '+auth,'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=30) as r: return json.load(r)
    def stamp(v): return datetime.fromtimestamp(v,timezone.utc).isoformat()
    rows=[json.loads(l) for l in a.traces.read_text().splitlines() if l]
    for trace in rows:
        batch=[{'id':trace['id']+'-create','type':'trace-create','timestamp':trace['timestamp'],
                'body':{'id':trace['id'],'name':'harbor-rag','input':trace['question'],'output':trace['result'],
                        'tags':[trace['backend'],trace['mode'],'track-d'],'metadata':{'model':trace['model']}}}]
        for o in trace['observations']:
            body={'id':o['id'],'traceId':trace['id'],'name':o['name'],'startTime':stamp(o['start']),'endTime':stamp(o['end']),
                  'metadata':{'backend':trace['backend'],'tokens':o['tokens']}}
            typ='span-create'
            if o['name']=='generation' and trace['backend']=='ollama':
                typ='generation-create'; body['model']=trace['model']
                body['usage']={k:v for k,v in o['tokens'].items() if v is not None}
            batch.append({'id':o['id']+'-create','type':typ,'timestamp':trace['timestamp'],'body':body})
        result=request('/api/public/ingestion',{'batch':batch})
        if result.get('errors'): raise RuntimeError(json.dumps(result['errors']))
    exported=[]
    for trace in rows:
        result=request('/api/public/traces/'+trace['id'])
        obs=result.get('observations',[])
        if len(obs)!=len(trace['observations']): raise RuntimeError('Dashboard observations not yet available; rerun sync')
        exported.append({**trace,'observations':[{'id':o['id'],'trace_id':trace['id'],'name':o['name'],
            'start':datetime.fromisoformat(o['startTime'].replace('Z','+00:00')).timestamp(),
            'end':datetime.fromisoformat(o['endTime'].replace('Z','+00:00')).timestamp(),
            'tokens':o.get('metadata',{}).get('tokens',{'input':None,'output':None})} for o in obs], 'source':'langfuse-api'})
    a.export.write_text(''.join(json.dumps(r)+'\n' for r in exported)); print(f'Exported {len(exported)} dashboard traces')

if __name__=='__main__': main()
