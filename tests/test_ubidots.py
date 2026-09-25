from unittest.mock import Mock, patch
import pytest
from testUbidots import build_payload, post_request

def test_five_variables():
    p=build_payload()
    assert set(p)=={'temperature','humidity','position','luminosity','pressure'}
    assert 18<=p['temperature']<=35
    assert 35<=p['humidity']<=85
    assert -90<=p['position']['context']['lat']<=90
    assert -180<=p['position']['context']['lng']<=180
    assert 100<=p['luminosity']<=1000
    assert 745<=p['pressure']<=755

@patch('testUbidots.requests.post')
def test_request_contract(post):
    post.return_value=Mock(status_code=200, json=lambda:{'temperature':[{'status_code':201}]})
    code,_=post_request({'temperature':23},'test-token','equipo-rest')
    assert code==200
    _,kw=post.call_args
    assert kw['timeout']==20 and not kw['allow_redirects']
    assert kw['headers']['X-Auth-Token']=='test-token'

@pytest.mark.parametrize('code',[301,400,401,403,429,500])
@patch('testUbidots.requests.post')
def test_reject_http_errors(post,code):
    post.return_value=Mock(status_code=code)
    with pytest.raises(RuntimeError): post_request({},'test-token')

@patch('testUbidots.requests.post')
def test_reject_partial_failure(post):
    post.return_value=Mock(status_code=200,json=lambda:{'humidity':[{'status_code':400}]})
    with pytest.raises(RuntimeError): post_request({},'test-token')

@pytest.mark.parametrize('url',['http://industrial.api.ubidots.com','https://example.com'])
def test_no_token_to_untrusted_destination(url):
    with pytest.raises(ValueError): post_request({},'test-token',base_url=url)

def test_invalid_device():
    with pytest.raises(ValueError): post_request({},'test-token','../other')
