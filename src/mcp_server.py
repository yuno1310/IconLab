"""Minimal MCP 2025-06-18 stdio server. Process ownership is the trust boundary."""
import json
import os
import sys
import time

RECORDS={'case-a':{'owner':'analyst-a','summary':'Synthetic Anchor return inquiry','private_note':'internal-a'},
         'case-b':{'owner':'analyst-b','summary':'Synthetic Beacon return inquiry','private_note':'internal-b'}}
SCHEMA={'type':'object','properties':{'case_id':{'type':'string','maxLength':40}},'required':['case_id'],'additionalProperties':False}

class ToolService:
    def __init__(self,principal,clock=time.monotonic):
        if principal not in ('analyst-a','analyst-b'): raise ValueError('Known local principal required')
        self.principal=principal; self.clock=clock; self.calls=[]
    def call(self,name,args):
        now=self.clock(); self.calls=[x for x in self.calls if now-x<60]
        if len(self.calls)>=20: raise ValueError('Rate limit: 20 calls per minute per process')
        self.calls.append(now)
        if name!='read_case': raise ValueError('Unknown tool')
        if not isinstance(args,dict) or set(args)!={'case_id'}: raise ValueError('Only case_id is accepted')
        cid=args['case_id']
        if not isinstance(cid,str) or not 1<=len(cid)<=40: raise ValueError('Invalid case_id')
        record=RECORDS.get(cid)
        if record is None or record['owner']!=self.principal: raise ValueError('Case unavailable')
        return {'case_id':cid,'summary':record['summary']}

def dispatch(request,service,state):
    id=request.get('id')
    if request.get('jsonrpc')!='2.0' or not isinstance(request.get('method'),str):
        return {'jsonrpc':'2.0','id':id,'error':{'code':-32600,'message':'Invalid Request'}}
    method=request['method']
    if method=='notifications/initialized': state['initialized']=True; return None
    if id is None: return None
    result={}
    if method=='initialize':
        state['negotiated']=True
        result={'protocolVersion':'2025-06-18','capabilities':{'tools':{'listChanged':False}},'serverInfo':{'name':'harbor-evidence','version':'1.0.0'}}
    elif not state.get('initialized') or not state.get('negotiated'):
        return {'jsonrpc':'2.0','id':id,'error':{'code':-32600,'message':'Initialize first'}}
    elif method=='ping': pass
    elif method=='tools/list': result={'tools':[{'name':'read_case','description':'Read the current process principal\'s synthetic support case','inputSchema':SCHEMA}]}
    elif method=='tools/call':
        params=request.get('params',{})
        try:
            data=service.call(params.get('name'),params.get('arguments'))
            result={'content':[{'type':'text','text':json.dumps(data)}],'isError':False}
        except (ValueError,AttributeError) as exc:
            result={'content':[{'type':'text','text':str(exc)}],'isError':True}
    else: return {'jsonrpc':'2.0','id':id,'error':{'code':-32601,'message':'Method not found'}}
    return {'jsonrpc':'2.0','id':id,'result':result}

def main():
    service=ToolService(os.environ.get('LAB_PRINCIPAL','')); state={}
    while True:
        line=sys.stdin.buffer.readline(16385)
        if not line: break
        if len(line)>16384:
            # Exit rather than allocating an unbounded request or desynchronizing frames.
            print(json.dumps({'jsonrpc':'2.0','id':None,'error':{'code':-32600,'message':'Request exceeds 16384 bytes'}}),flush=True)
            break
        try:
            req=json.loads(line)
            if not isinstance(req,dict): raise ValueError('Object required')
            response=dispatch(req,service,state)
        except (ValueError,TypeError): response={'jsonrpc':'2.0','id':None,'error':{'code':-32700,'message':'Parse error'}}
        if response is not None: print(json.dumps(response),flush=True)

if __name__=='__main__': main()
