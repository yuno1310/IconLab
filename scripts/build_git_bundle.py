"""Prepare a standalone tagged repository from the secret-checked submission ZIP."""
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    isolated = Path(tempfile.mkdtemp(prefix='publish-repo-', dir=ROOT / 'tmp'))
    with zipfile.ZipFile(ROOT / 'output/harbor-track-d-submission-pack.zip') as archive:
        archive.extractall(isolated)
    repo = isolated / 'harbor-track-d'
    def git(*args):
        return subprocess.run(['git', *args], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()
    git('init', '-b', 'codex/track-d')
    assert Path(git('rev-parse', '--show-toplevel')).resolve() == repo.resolve()
    git('add', '--all')
    tracked = git('diff', '--cached', '--name-only').splitlines()
    assert not any(p.startswith(('.env', 'tmp/', '.git/')) for p in tracked)
    git('-c', 'user.name=Codex', '-c', 'user.email=codex@localhost', 'commit', '-m', 'Prepare Track D submission evidence and deliverables')
    git('tag', 'submission-ready-v1')
    bundle = ROOT / 'output/harbor-track-d.bundle'
    git('bundle', 'create', str(bundle), '--all')
    git('bundle', 'verify', str(bundle))
    print(f'Verified portable repository: {bundle}\nCommit: {git("rev-parse", "HEAD")}\nTracked files: {len(tracked)}\nTag: submission-ready-v1')

if __name__ == '__main__':
    main()
