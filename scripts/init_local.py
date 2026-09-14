"""Generate lab-only credentials without printing them or overwriting existing secrets."""
import secrets
from pathlib import Path
p=Path('.env')
with p.open('x',encoding='utf-8') as f:
    for key in ['POSTGRES_PASSWORD','NEXTAUTH_SECRET','SALT','LANGFUSE_USER_PASSWORD']:
        f.write(key+'='+secrets.token_hex(24)+'\n')
    f.write('LANGFUSE_PUBLIC_KEY=pk-lf-'+secrets.token_hex(16)+'\n')
    f.write('LANGFUSE_SECRET_KEY=sk-lf-'+secrets.token_hex(24)+'\n')
print('Created ignored .env with local-only credentials')
