import unittest
import os
import json
import subprocess
from rjo import convert
from logging import getLogger


_log = getLogger(__name__)


def json_loads_iter(s: str):
    dec = json.JSONDecoder()
    ptr = 0
    while True:
        ptr = json.decoder.WHITESPACE.match(s, pos=ptr).end()
        if ptr >= len(s):
            break
        d, ptr = dec.raw_decode(s, ptr)
        yield d


def jo(s: str):
    r = subprocess.run("echo " + s, shell=True, capture_output=True)
    assert r.returncode == 0
    return json.loads(r.stdout)


class TestByData(unittest.TestCase):
    testdata = []

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__), "testdata.json")) as ifp:
            cls.testdata = [x for x in json_loads_iter(ifp.read())]

    def test1(self):
        for i in self.testdata:
            _log.debug("data: %s", i)
            jostr = convert(i)
            _log.debug("jostr: %s", jostr)
            res = jo(jostr)
            _log.debug("jo: %s", res)
            self.assertEquals(i, res)
