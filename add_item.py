#!/usr/bin/env python3
"""Usage: python3 add_item.py DATE "NAME" "PRICE" LINK [IMAGE_PATH] [--no-push]
Prepends item to items.json, copies image into img/, regenerates index.html, commits & pushes.
Run with no args (or --build) to only rebuild index.html."""
import json,sys,os,shutil,subprocess,html
D=os.path.dirname(os.path.abspath(__file__));os.chdir(D)
def build():
    items=json.load(open('items.json'))
    rows=[]
    for it in items:
        e=lambda k:html.escape(it.get(k,''))
        img=f'<img src="{e("image")}" alt="" loading="lazy">' if it.get('image') else '<div class="ph"></div>'
        rows.append(f'<a class="item" href="{e("link")}" target="_blank" rel="noopener">{img}<div class="t"><span class="d">{e("date")}</span><span class="n">{e("name")}</span><span class="p">{e("price")}</span></div><span class="b">선물하기</span></a>')
    page=open('template.html').read().replace('{{ITEMS}}','\n'.join(rows))
    open('index.html','w').write(page)
a=[x for x in sys.argv[1:] if x!='--no-push']
if a and a[0]!='--build':
    date,name,price,link=a[:4];image=''
    if len(a)>4:
        os.makedirs('img',exist_ok=True);dst='img/'+date+'-'+os.path.basename(a[4]);shutil.copy(a[4],dst);image=dst
    items=json.load(open('items.json'));items.insert(0,dict(date=date,name=name,price=price,link=link,image=image))
    json.dump(items,open('items.json','w'),ensure_ascii=False,indent=1)
build()
if a and a[0]!='--build' and '--no-push' not in sys.argv:
    subprocess.run(['git','add','-A'],check=True);subprocess.run(['git','commit','-m','add '+a[1]],check=True);subprocess.run(['git','push'],check=True)
