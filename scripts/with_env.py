"""Run a Python module with local .env variables, without displaying credentials."""
import os
import runpy
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
for line in Path('.env').read_text().splitlines():
    if line and not line.startswith('#'):
        k,v=line.split('=',1); os.environ[k]=v
module=sys.argv[1]; sys.argv=sys.argv[1:]; runpy.run_module(module,run_name='__main__')
