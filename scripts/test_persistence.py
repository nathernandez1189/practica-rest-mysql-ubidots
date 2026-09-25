"""Guardar/validar marcadores antes y después de apagar una VM de práctica."""
import argparse,json
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from pathlib import Path
from datetime import datetime,timezone
p=argparse.ArgumentParser();p.add_argument('phase',choices=['before','after']);p.add_argument('--host',default='192.168.100.3');p.add_argument('--file',default='evidencias/persistencia.json');a=p.parse_args()
def request(port,method,path,data=None):
    req=Request(f'http://{a.host}:{port}'+path,method=method,data=json.dumps(data).encode() if data else None,headers={'Content-Type':'application/json'})
    try:r=urlopen(req,timeout=20)
    except HTTPError as e:r=e
    return r.status,json.loads(r.read())
f=Path(a.file)
if a.phase=='before':
    result={'before_utc':datetime.now(timezone.utc).isoformat(),'markers':{}}
    for label,port in [('memory',5000),('mysql',5001),('javascript',5002)]:
        title='Persistencia - '+label+' - '+result['before_utc']
        status,body=request(port,'POST','/books',{'title':title,'author':'Natalia, Miguel y Juan Ospina'})
        assert status==201
        result['markers'][label]={'port':port,'book':body['book']}
else:
    result=json.loads(f.read_text()); result['after_utc']=datetime.now(timezone.utc).isoformat()
    for label,marker in result['markers'].items():
        status,body=request(marker['port'],'GET',f"/books/{marker['book']['id']}")
        expected=404 if label=='memory' else 200
        marker['after_status']=status
        marker['passed']=status==expected and (label=='memory' or body['book']==marker['book'])
        assert marker['passed'],marker
    result['conclusion']='Memoria pierde el registro; MySQL conserva íntegros los registros creados desde Python y JavaScript.'
f.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(f.read_text())
