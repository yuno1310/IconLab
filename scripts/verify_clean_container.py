"""Reproduce the fixture suite in an isolated, network-disabled Linux container."""
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE = 'python:3.12.14-slim'
PROGRAM = '''
import json, os, platform, subprocess, sys, zipfile
with zipfile.ZipFile('/input/pack.zip') as z: z.extractall('/tmp/work')
os.chdir('/tmp/work/harbor-track-d')
test=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],capture_output=True,text=True)
report={'python':platform.python_version(),'system':platform.system(),'tests':{'exit_code':test.returncode,'output':test.stdout+test.stderr},'scores':{}}
assert test.returncode==0, report
for mode, expected in [('naive',(30,10)),('improved',(50,48))]:
 run=subprocess.run([sys.executable,'-m','src.evaluate','--mode',mode,'--out','/tmp/'+mode],capture_output=True,text=True)
 assert run.returncode==0, run.stderr
 summary=json.load(open('/tmp/'+mode+'/results.json'))['summary']
 assert (summary['retrieval_passes'],summary['generation_passes'])==expected, summary
 report['scores'][mode]=summary
demo=subprocess.run([sys.executable,'-m','src.chat','--backend','fixture','--question','What is Anchor annual revenue?'],capture_output=True,text=True)
assert demo.returncode==0 and json.loads(demo.stdout)['refused'] is True
report['demo_cli']='passed'
print(json.dumps(report))
'''

def main():
    inspected = subprocess.run(['docker','image','inspect',IMAGE,'--format','{{json .RepoDigests}}'], check=True,capture_output=True,text=True)
    digest = json.loads(inspected.stdout)[0]
    archive = ROOT / 'output/harbor-track-d-submission-pack.zip'
    run = subprocess.run(['docker','run','--rm','--network','none','--read-only','--cap-drop','ALL',
        '--security-opt','no-new-privileges','--tmpfs','/tmp:rw,size=256m',
        '--mount',f'type=bind,source={archive},target=/input/pack.zip,readonly',
        '-e','PYTHONDONTWRITEBYTECODE=1',digest,'python','-c',PROGRAM],check=True,capture_output=True,text=True,timeout=180)
    report = {'recorded_at':datetime.now(timezone.utc).isoformat(),'image_digest':digest,
        'scope':'Fresh disposable Linux runtime with network disabled and no host Python packages. Fixture suite and CLI only; not another person or fresh full model/DB deployment.',**json.loads(run.stdout)}
    (ROOT/'evidence/clean-container-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('tests','scores')},indent=2))

if __name__ == '__main__':
    main()
