import json

from versions import *

def test_parse_gh_release_k8s():
    with open('testdata/k8s.json') as t:
        rs = json.load(t)

    a = parse_gh_release(rs, 2, 3)

    assert len(a) == 3
    assert type(a[0]) == dict

    assert a[0]['series'] == "1.17"
    assert a[0]['pre']['ver'] == "1.17.0-alpha.3"
    assert a[0]['ga'] == None

    assert a[1]['series'] == "1.16"
    assert a[1]['pre'] == None
    assert a[1]['ga']['ver'] == "1.16.2"

def test_parse_gh_release_zfs():
    with open('testdata/zfs.json') as t:
        rs = json.load(t)

    a = parse_gh_release(rs, 2, 2)

    assert len(a) == 2
    assert type(a[0]) == dict

    assert a[0]['series'] == "0.8"
    assert a[0]['pre'] == None
    assert a[0]['ga']['ver'] == "0.8.2"

    assert a[1]['series'] == "0.7"
    assert a[1]['pre'] == None
    assert a[1]['ga']['ver'] == "0.7.13"

def test_ver_num():
    assert get_ver_num("1.2.3") == "1.2.3"
    assert get_ver_num("v1.2.3") == "1.2.3"
    assert get_ver_num("1.2.3-0") == "1.2.3-0"
    assert get_ver_num("1.2.3-rc1.beta1") == "1.2.3-rc1.beta1"
