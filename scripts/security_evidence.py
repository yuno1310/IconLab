"""Bounded testing of our local tool implementation and its stdio transport only."""
import json
import os
import subprocess
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.mcp_server import ToolService, RECORDS

class VulnerableFixture:
    """Archived before-fix design, intentionally available only inside this test script."""
    def call(self,name,args): return RECORDS[args['case_id']]

def main():
    out=Path('evidence/security.json')
    before=VulnerableFixture().call('read_case',{'case_id':'case-b'})
    events={'scope':'owned local synthetic process; no remote target','before_cross_owner':before,'before_1000_calls':sum(bool(VulnerableFixture().call('read_case',{'case_id':'case-a'})) for _ in range(1000))}
    s=ToolService('analyst-a',lambda:0)
    try: s.call('read_case',{'case_id':'case-b'})
    except ValueError as e: events['after_cross_owner']=str(e)
    s=ToolService('analyst-a',lambda:0); accepted=blocked=0
    for _ in range(1000):
        try: s.call('read_case',{'case_id':'case-a'}); accepted+=1
        except ValueError: blocked+=1
    events['after_1000_calls']={'accepted':accepted,'blocked':blocked}
    requests=[{'jsonrpc':'2.0','id':0,'method':'initialize'}, {'jsonrpc':'2.0','method':'notifications/initialized'}]
    for i,(name,args) in enumerate([('read_case',{'case_id':'case-a'}),('read_case',{'case_id':'case-b'}),('delete_case',{'case_id':'case-a'}),('read_case',{'case_id':'https://example.invalid'}),('read_case',{'case_id':'case-a','principal':'analyst-b'}),('read_case',{'case_id':"x' OR 1=1 --"})],1):
        requests.append({'jsonrpc':'2.0','id':i,'method':'tools/call','params':{'name':name,'arguments':args}})
    r=subprocess.run([sys.executable,'-m','src.mcp_server'],input='\n'.join(map(json.dumps,requests))+'\n',text=True,capture_output=True,env={**os.environ,'LAB_PRINCIPAL':'analyst-a'},timeout=10,check=True)
    events['transport_responses']=[json.loads(x) for x in r.stdout.splitlines()]
    out.write_text(json.dumps(events,indent=2)+'\n',encoding='utf-8'); print(json.dumps(events,indent=2))

if __name__=='__main__': main()
