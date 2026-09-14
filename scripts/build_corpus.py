"""Generate owned synthetic source documents and an auditable 50-case development set."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANS = [
    ('Anchor', '24 hours', '48 hours', 'Mira', 'receipt', '30 days', '45 days'),
    ('Beacon', '4 hours', '8 hours', 'Noah', 'serial number', '14 days', '21 days'),
    ('Cedar', '12 hours', '24 hours', 'Iris', 'purchase order', '60 days', '90 days'),
    ('Delta', '2 hours', '6 hours', 'Omar', 'device photograph', '7 days', '10 days'),
    ('Ember', '36 hours', '72 hours', 'Lina', 'warranty card', '20 days', '25 days'),
    ('Fjord', '6 hours', '12 hours', 'Theo', 'error log', '40 days', '50 days'),
    ('Grove', '8 hours', '16 hours', 'Ada', 'delivery note', '15 days', '18 days'),
    ('Haven', '1 hour', '3 hours', 'Zara', 'case number', '10 days', '12 days'),
    ('Indigo', '18 hours', '36 hours', 'Eli', 'activation date', '28 days', '35 days'),
    ('Juniper', '3 hours', '9 hours', 'Ravi', 'service report', '5 days', '8 days'),
]

def main():
    docs, cases = [], []
    def doc(id, title, date, family, content):
        row = dict(id=id, title=title, date=date, family=family, text=content)
        docs.append(row)
        (ROOT/'corpus'/f'{id}.md').write_text(f'# {title}\n\nDate: {date}\nSynthetic: true\n\n{content}\n', encoding='utf-8')
    def case(category, question, answer, sources, terms, forbidden=None):
        cases.append(dict(id=f'Q{len(cases)+1:02}', category=category, question=question,
                          expected_answer=answer, expected_sources=sources,
                          required_terms=terms, forbidden_terms=forbidden or [],
                          must_refuse=category=='must_refuse'))
    for name, current, old, owner, proof, east, west in PLANS:
        slug=name.lower()
        doc(slug+'-old', name+' retired response policy', '2025-01-01', slug+'-response',
            f'{name} response deadline is {old}. This historical response policy is superseded by the 2026 response policy.')
        doc(slug+'-current', name+' current response policy', '2026-08-01', slug+'-response',
            f'{name} response deadline is {current}. This policy supersedes the 2025 response policy. Coverage applies to staffed business hours only.')
        doc(slug+'-routing', name+' escalation procedure', '2026-08-01', slug+'-routing',
            f'{name} escalation owner is {owner}. Required escalation evidence is {proof}. Escalation requires human approval.')
        doc(slug+'-east', name+' East returns bulletin', '2026-08-15', slug+'-returns-east',
            f'{name} returns window is {east} in the East bulletin. The East and West bulletins both claim company-wide coverage. Neither establishes precedence. A support lead must resolve the conflict.')
        doc(slug+'-west', name+' West returns bulletin', '2026-08-15', slug+'-returns-west',
            f'{name} returns window is {west} in the West bulletin. The East and West bulletins both claim company-wide coverage. Neither establishes precedence. A support lead must resolve the conflict.')
    for name, current, old, owner, proof, east, west in PLANS:
        s=name.lower()
        case('easy', f'Who is the {name} escalation owner?', owner, [s+'-routing'], [owner])
    for name, current, old, owner, proof, east, west in PLANS:
        s=name.lower()
        case('synthesis', f'What is the current {name} response deadline and required escalation evidence?',
             f'{current}; {proof}', [s+'-current', s+'-routing'], [current, proof], [old])
    for name, current, old, owner, proof, east, west in PLANS:
        s=name.lower()
        case('conflict', f'What is the {name} returns window when East and West bulletins disagree?',
             f'Conflict: East says {east}; West says {west}. Ask a support lead; neither has precedence.',
             [s+'-east',s+'-west'], [east,west,'conflict','support lead'])
    for name, current, old, owner, proof, east, west in PLANS:
        s=name.lower()
        case('stale', f'What is the current {name} response deadline?', current, [s+'-current'], [current], [old])
    missing = [('Anchor','annual revenue'),('Beacon','administrator password'),('Cedar','CEO salary'),
               ('Delta','next year pricing'),('Ember','customer bank account'),('Fjord','encryption key'),
               ('Grove','live inventory count'),('Haven','legal liability cap'),('Indigo','outage root cause'),
               ('Juniper','private customer address')]
    for name, topic in missing:
        case('must_refuse',f'What is the {name} {topic}?', 'I do not know from the provided sources.', [], [])
    (ROOT/'corpus/index.json').write_text(json.dumps(docs,indent=2)+'\n',encoding='utf-8')
    # JSON is a YAML 1.2 subset, avoiding a runtime parser dependency.
    (ROOT/'golden-set.yaml').write_text(json.dumps({'schema_version':1,'provenance':'synthetic, jointly authored with corpus; development benchmark', 'questions':cases},indent=2)+'\n',encoding='utf-8')
    print(f'Wrote {len(docs)} documents and {len(cases)} cases')

if __name__=='__main__': main()
