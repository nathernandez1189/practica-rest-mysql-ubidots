"""Prueba real por HTTP: mismas comprobaciones para las tres implementaciones."""
import argparse
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from datetime import datetime, timezone

def verify(base):
    results=[]
    def req(method,path,status,body=None):
        request=Request(base+path, data=None if body is None else json.dumps(body).encode(),
                        method=method, headers={'Content-Type':'application/json'})
        try: response=urlopen(request,timeout=15)
        except HTTPError as exc: response=exc
        payload=json.loads(response.read())
        result={'method':method,'path':path,'expected':status,'actual':response.status,'passed':response.status==status}
        results.append(result)
        assert result['passed'],result
        return payload
    req('GET','/health',200)
    req('GET','/books',200)
    title="Cien años de soledad 🦋'); DROP TABLE books; --"
    created=req('POST','/books',201,{'title':title,'author':'Equipo'})['book']
    path=f"/books/{created['id']}"
    try:
        assert req('GET',path,200)['book']['title']==title
        assert req('PUT',path,200,{'author':'Natalia, Miguel y Juan Ospina'})['book']['author']=='Natalia, Miguel y Juan Ospina'
        assert req('GET',path,200)['book']['title']==title
        req('PUT',path,400,{'author':5})
        req('POST','/books',400,{'title':''})
        req('POST','/books',400,{'title':'X'*256})
        req('POST','/books',400,{'title':'X','extra':'campo'})
        req('GET','/books/2147483647',404)
        req('DELETE','/books/2147483647',404)
    finally:
        req('DELETE',path,200)
    req('GET',path,404)
    return {'url':base,'checks':results,'passed':len(results)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--host',default='127.0.0.1');p.add_argument('--output');a=p.parse_args()
    report={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'kind':'HTTP real contra servicios activos',
            'results':[verify(f'http://{a.host}:{port}') for port in [5000,5001,5002]]}
    output=json.dumps(report,ensure_ascii=False,indent=2)
    if a.output:
        from pathlib import Path
        Path(a.output).write_text(output+'\n')
    print(output)
