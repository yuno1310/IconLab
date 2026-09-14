"""Validate source/evidence consistency and produce a secret-free portable archive."""
import hashlib
import json
import re
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ALLOWED=['src','tests','scripts','docs','posts','corpus','evidence','output/decks','output/videos']
FILES=['README.md','START-HERE.md','SETUP.md','.gitignore','.python-version','requirements.txt','compose.yaml','golden-set.yaml','output/evidence-review.html']
def main():
    files=[ROOT/f for f in FILES]
    for folder in ALLOWED:
        files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
    files=sorted(set(files))
    secrets=[l.split('=',1)[1].encode() for l in (ROOT/'.env').read_text().splitlines() if '=' in l] if (ROOT/'.env').exists() else []
    for p in files:
        data=p.read_bytes()
        if any(secret in data for secret in secrets if len(secret)>12):raise ValueError('Local secret detected in '+str(p.relative_to(ROOT)))
        if p.suffix=='.json':json.loads(data)
    for mode in ['final-baseline','final-improved']:
        data=json.loads((ROOT/f'evidence/{mode}/results.json').read_text())
        assert len(data['rows'])==50
        assert sum(r['retrieval_pass'] for r in data['rows'])==data['summary']['retrieval_passes']
        assert sum(r['generation_pass'] for r in data['rows'])==data['summary']['generation_passes']
        exported=[json.loads(l) for l in (ROOT/f'evidence/{mode}/langfuse-export.jsonl').read_text().splitlines()]
        assert len(exported)==50 and all(len(t['observations'])==2 for t in exported)
    decks=list((ROOT/'output/decks').glob('*.pptx')); videos=list((ROOT/'output/videos').glob('*.mp4'))
    assert len(decks)==6 and len(videos)==6
    for deck in decks:
        with zipfile.ZipFile(deck) as z:
            slides=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
            assert len(slides)==8
            for n in slides:
                assert b'Lorem ipsum' not in z.read(n) and b'Title here' not in z.read(n)
    manifest={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    (ROOT/'output/file-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    archive=ROOT/'output/harbor-track-d-submission-pack.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,'harbor-track-d/'+str(p.relative_to(ROOT)))
        z.write(ROOT/'output/file-manifest.json','harbor-track-d/file-manifest.json')
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert not any('/.env' in n or '/tmp/' in n or '/.git/' in n for n in z.namelist())
    print(json.dumps({'files':len(files),'decks':len(decks),'videos':len(videos),'archive_bytes':archive.stat().st_size,'secret_scan':'passed'},indent=2))
if __name__=='__main__': main()
