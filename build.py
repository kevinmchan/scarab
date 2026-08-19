#!/usr/bin/env python3
"""Build index.html (the deployable game) from the source template plus content/.

The source keeps placeholders so the 185KB of inlined font and dialogue data stays
out of the file you actually edit. Everything needed is in content/ — no network.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / 'content'

src = (ROOT / 'scarab.src.html').read_text()

b64 = (CONTENT / 'cinzel.b64').read_text().replace('\n', '')
assert '/*@CINZEL@*/' in src, 'font placeholder missing'
src = src.replace('/*@CINZEL@*/', b64)

personas = json.loads((CONTENT / 'personas.json').read_text())
copy = json.loads((CONTENT / 'copy.json').read_text())
assert len(personas) == 6, f'expected 6 personas, got {len(personas)}'
assert '__PERSONAS__' in src and '__COPY__' in src, 'content placeholders missing'
src = src.replace('__PERSONAS__', json.dumps(personas, ensure_ascii=False, separators=(',', ':')))
src = src.replace('__COPY__', json.dumps(copy, ensure_ascii=False, separators=(',', ':')))

# The artifact host injects the document skeleton; a plain web server does not.
page = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="description" content="A social deduction game at a 1926 Egyptian tomb excavation. '
        'Two of the seven are cultists. Share the link and find out which.">\n'
        + src + '\n</body></html>\n')

(ROOT / 'index.html').write_text(page)          # deployed to the web
(ROOT / 'scarab.html').write_text(src)           # bare fragment, for publishing as an artifact
print(f'built index.html: {len(page)} bytes · {len(personas)} personas')
