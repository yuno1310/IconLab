import json
import os
import subprocess
import sys
import unittest
from src.agent import ROOT, ask
from src.evaluate import score
from src.mcp_server import ToolService

class LabTests(unittest.TestCase):
    def test_golden_integrity(self):
        cases=json.loads((ROOT/'golden-set.yaml').read_text())['questions']
        self.assertEqual(len(cases),50)
        docs={d['id'] for d in json.loads((ROOT/'corpus/index.json').read_text())}
        for category in ('easy','synthesis','conflict','stale','must_refuse'):
            self.assertEqual(sum(c['category']==category for c in cases),10)
        for c in cases: self.assertTrue(set(c['expected_sources'])<=docs)
    def test_grader_rejects_wrong_refusal(self):
        c={'expected_sources':['a'],'must_refuse':False,'required_terms':['24 hours']}
        r={'answer':'24 hours','refused':True,'citations':['a'],'retrieved_sources':['a']}
        self.assertFalse(score(c,r)['generation_pass'])
    def test_grader_separates_failure_types(self):
        c={'expected_sources':['a'],'must_refuse':False,'required_terms':['24 hours']}
        r={'answer':'48 hours','refused':False,'citations':['a'],'retrieved_sources':['a']}
        self.assertTrue(score(c,r)['retrieval_pass']); self.assertFalse(score(c,r)['generation_pass'])
    def test_refusal_not_masked_by_execution_error(self):
        c={'expected_sources':[],'must_refuse':True}
        self.assertFalse(score(c,{'refused':True,'error':'timeout'})['generation_pass'])
    def test_naive_remains_distinct(self):
        q='What is the current Anchor response deadline?'
        self.assertNotEqual(ask(q,'naive')['answer'],ask(q,'improved')['answer'])
    def test_ownership_and_projection(self):
        s=ToolService('analyst-a')
        self.assertNotIn('private_note',s.call('read_case',{'case_id':'case-a'}))
        with self.assertRaisesRegex(ValueError,'unavailable'): s.call('read_case',{'case_id':'case-b'})
    def test_injection_and_principal_override(self):
        s=ToolService('analyst-a')
        for args in ({'case_id':'../../etc/passwd'},{'case_id':"case-a' OR 1=1 --"},{'case_id':'case-b','principal':'analyst-b'},{'case_id':['case-a']}):
            with self.assertRaises(ValueError): s.call('read_case',args)
    def test_rate_window(self):
        now=[0]; s=ToolService('analyst-a',lambda:now[0])
        for _ in range(20): s.call('read_case',{'case_id':'case-a'})
        with self.assertRaisesRegex(ValueError,'Rate limit'): s.call('read_case',{'case_id':'case-a'})
        now[0]=61; self.assertIn('summary',s.call('read_case',{'case_id':'case-a'}))
    def test_mcp_actual_transport(self):
        requests=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18'}},
                  {'jsonrpc':'2.0','method':'notifications/initialized'},
                  {'jsonrpc':'2.0','id':2,'method':'tools/list'},
                  {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'read_case','arguments':{'case_id':'case-b'}}}]
        run=subprocess.run([sys.executable,'-m','src.mcp_server'],input='\n'.join(map(json.dumps,requests))+'\n',capture_output=True,text=True,env={**os.environ,'LAB_PRINCIPAL':'analyst-a'},timeout=10)
        self.assertEqual(run.returncode,0,run.stderr)
        rows=[json.loads(x) for x in run.stdout.splitlines()]
        self.assertEqual(len(rows),3); self.assertTrue(rows[-1]['result']['isError'])
    def test_invalid_and_oversized_transport(self):
        for line in ('not json\n','x'*17000+'\n'):
            r=subprocess.run([sys.executable,'-m','src.mcp_server'],input=line,capture_output=True,text=True,env={**os.environ,'LAB_PRINCIPAL':'analyst-a'},timeout=10)
            self.assertIn('error',json.loads(r.stdout))

if __name__=='__main__': unittest.main()
