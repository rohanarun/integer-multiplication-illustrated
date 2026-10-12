"""Check artifact structure and render every page for visual inspection."""
from pathlib import Path
import fitz,json,re,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
report={'documents':{},'scope':'Document integrity and pedagogical examples; not a theorem validation.'}
for name,short in [('illustrated-guide','guide'),('expanded-paper','expanded')]:
 doc=fitz.open(ROOT/'output/pdf'/f'{name}.pdf');thumbs=[];problems=[];texts=[]
 for i,p in enumerate(doc):
  text=p.get_text();texts.append(text)
  assert len(text.strip())>80,(name,i,'unexpected empty page')
  for block in p.get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    for span in line['spans']:
     x0,y0,x1,y1=span['bbox']
     if x0<0 or y0<0 or x1>p.rect.width or y1>p.rect.height:problems.append({'page':i+1,'text':span['text']})
  pix=p.get_pixmap(matrix=fitz.Matrix(1,1));fn=ROOT/'preview'/f'{short}-{i+1:03}.png';pix.save(str(fn))
  im=Image.open(fn).convert('RGB');im.thumbnail((306,396))
  tile=Image.new('RGB',(326,430),'#e7ebee');tile.paste(im,((326-im.width)//2,15))
  ImageDraw.Draw(tile).text((10,412),str(i+1),fill='black');thumbs.append(tile)
 for start in range(0,len(thumbs),12):
  batch=thumbs[start:start+12];sheet=Image.new('RGB',(1304,430*((len(batch)+3)//4)),'white')
  for j,t in enumerate(batch):sheet.paste(t,((j%4)*326,(j//4)*430))
  sheet.save(ROOT/'preview'/f'{short}-contact-{start//12+1}.png')
 fulltext='\n'.join(texts)
 assert not problems,problems
 assert '??' not in fulltext,'Unresolved-reference marker'
 for i in range(1,11):assert f'Figure E{i}.' in fulltext,(name,i)
 log=(ROOT/'output/pdf'/f'{name}.log').read_text()
 assert 'Overfull' not in log and 'undefined' not in log.lower(),name
 report['documents'][name]={'pages':len(doc),'added_figures':10,'out_of_page_text':problems,
   'sha256':hashlib.sha256((ROOT/'output/pdf'/f'{name}.pdf').read_bytes()).hexdigest(),
   'all_pages_rendered':True,'unresolved_references':False,'overfull_boxes':False}
manifest=json.loads((ROOT/'source-manifest.json').read_text());count=0
for name,meta in manifest['files'].items():
 if name.startswith('build/'):
  assert hashlib.sha256((ROOT/'original'/name[6:]).read_bytes()).hexdigest()==meta['sha256'],name
  count+=1
report['original_build_files_hash_verified']=count
report['example_checks']=json.loads((ROOT/'example-checks.json').read_text())
(ROOT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({n:{'pages':v['pages'],'figures':v['added_figures']} for n,v in report['documents'].items()},indent=2))
