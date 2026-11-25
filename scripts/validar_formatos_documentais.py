"""Valida arquivos de ingestão sem executar OCR, agente ou Langfuse.
Requer pypdf para verificar camadas textuais de PDF.
"""
import hashlib
import json
import zipfile
from pathlib import Path
from pypdf import PdfReader
from xml.etree import ElementTree as ET

R = Path(__file__).resolve().parents[1]
P = R / 'data/formatos-documentais-v0'
def rows(name):
    return [json.loads(line) for line in (P/name).read_text().splitlines() if line.strip()]
def path(name):
    p=(P/name).resolve()
    assert P.resolve() in p.parents, 'Referência documental fora do lote'
    return p

def main():
    inputs,truth,files=rows('entradas.jsonl'),rows('avaliador/verdade.jsonl'),rows('arquivos/manifesto.jsonl')
    assert len(inputs)==len(truth)==12 and len(files)==42
    assert len({f['arquivo'] for f in files})==42
    assert len({x['metadata']['variante_id'] for x in inputs})==12
    assert {x['metadata']['variante_id'] for x in inputs}=={x['variante_id'] for x in truth}
    originals={cid:json.loads((R/f'data/piloto-multimodal-v0/entradas/{cid}.json').read_text()) for cid in ['FDE-001','FDE-003']}
    reftruth={x['caso_id']:x['expectedOutput'] for x in map(json.loads,(R/'data/piloto-multimodal-v0/avaliador/verdade.jsonl').read_text().splitlines())}
    def semantic(text, source):
        normalized=' '.join(text.split())
        for line in source.splitlines():
            if not line or line.startswith(('DOCUMENTO SINTÉTICO','REGRAS SINTÉTICAS')):
                continue
            required=line.split(': ',1)[1] if ': ' in line else line
            assert ' '.join(required.split()) in normalized, 'Conteúdo material ausente: '+required
    canonical={d['documento_id']:d['texto_referencia'] for t in truth for d in t['expectedOutput']['extracao_documental']}
    for f in files:
        p=path(f['arquivo']);b=p.read_bytes()
        assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
        source=next(d for d in originals[f['caso_origem']]['documentos'] if d['documento_id']==f['documento_id'])
        if p.suffix=='.pdf':
            reader=PdfReader(p);assert len(reader.pages)==1
            text=reader.pages[0].extract_text().strip()
            if p.name.endswith('-escaneado.pdf'):assert not text,'PDF raster não pode conter texto'
            else:
                assert text
                semantic(text,canonical[f['documento_id']])
        elif p.suffix=='.docx':
            with zipfile.ZipFile(p) as z:xml=ET.fromstring(z.read('word/document.xml'))
            ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            paras=[''.join(t.text or '' for t in paragraph.findall('.//w:t',ns)) for paragraph in xml.findall('.//w:p',ns)]
            semantic(' '.join(paras),canonical[f['documento_id']])
        elif p.suffix=='.xlsx':
            with zipfile.ZipFile(p) as z:xml=ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
            ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
            numbers=[float(c.find('s:v',ns).text) for c in xml.findall('.//s:c',ns) if c.get('t') in [None,'n'] and c.find('s:v',ns) is not None]
            assert numbers==[1800.0], numbers
        elif p.suffix=='.png':assert b.startswith(b'\x89PNG\r\n\x1a\n')
        elif p.suffix=='.jpg':assert b.startswith(b'\xff\xd8')
    known={f['arquivo'] for f in files}
    for row in inputs:
        inp=row['input'];m=row['metadata'];cid=m['caso_origem']
        assert m['particao']=='DESENVOLVIMENTO' and m['suporte_agente']=='NAO_CONFIRMADO'
        assert inp['caso_id']==cid and len(inp['documentos'])==4
        assert {d['documento_id'] for d in inp['documentos']}=={d['documento_id'] for d in originals[cid]['documentos']}
        for d in inp['documentos']:
            assert d['arquivo'] in known and 'conteudo' not in d and 'texto_referencia' not in d
        assert not {'expectedOutput','gabarito','texto_referencia'} & inp.keys()
        for im in inp['imagens']:
            assert (R/im['arquivo']).is_file()
        expected=next(x['expectedOutput'] for x in truth if x['variante_id']==m['variante_id'])
        assert expected['comportamento']==reftruth[cid]
        for d in expected['extracao_documental']:
            assert d['texto_referencia']==canonical[d['documento_id']]
            original=next(s['conteudo'] for s in originals[cid]['documentos'] if s['documento_id']==d['documento_id'])
            # IDs, dates and monetary facts remain unchanged by presentation edits.
            import re
            facts=re.findall(r'\b(?:\d{4}-\d{2}-\d{2}|\d+\.\d{2}|(?:AP|SIN|ORC|VEI|SEG|OFI)-\d{3})\b',original)
            assert all(fact in d['texto_referencia'] for fact in facts)
    print('OK: 2 casos, 12 variantes, 42 arquivos; hashes, conteúdo, PDFs raster e gabaritos consistentes. OCR e agente não executados.')

if __name__=='__main__':main()
