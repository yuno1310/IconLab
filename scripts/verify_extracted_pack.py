"""Check the delivered archive in a fresh directory, without the working tree."""
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    parent = ROOT / 'tmp'
    parent.mkdir(exist_ok=True)
    isolated = Path(tempfile.mkdtemp(prefix='archive-check-', dir=parent))
    with zipfile.ZipFile(ROOT / 'output/harbor-track-d-submission-pack.zip') as archive:
        archive.extractall(isolated)
    checkout = isolated / 'harbor-track-d'
    subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=checkout, check=True)
    scores = {}
    for mode, expected in [('naive', (30, 10)), ('improved', (50, 48))]:
        destination = f'tmp/extracted-{mode}'
        subprocess.run([sys.executable, '-m', 'src.evaluate', '--mode', mode, '--out', destination], cwd=checkout, check=True)
        summary = json.loads((checkout / destination / 'results.json').read_text())['summary']
        assert (summary['retrieval_passes'], summary['generation_passes']) == expected, summary
        scores[mode] = summary
    report = {'scope': 'Automated extracted archive on the same machine; not independent human reproduction', 'tests': 'passed', 'fixture_scores': scores}
    (ROOT / 'evidence/extracted-pack-check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
