import os
from pytest import raises
from dpnclient import util
from dpnclient import const
from datetime import datetime

def test_now_str():
    timestamp = util.now_str()
    assert util.RE_TIMESTAMP.match(timestamp) is not None

def test_looks_like_uuid():
    assert util.looks_like_uuid("e084c014-9ba1-41a3-9eb3-6daef8097bc5") == True
    assert util.looks_like_uuid("This is not a UUID") == False

def test_status_valid():
    for status in const.STATUSES:
        assert util.status_valid(status)
    assert util.status_valid('not a status') == False

def test_protocols_valid():
    for protocol in const.PROTOCOLS:
        assert util.protocol_valid(protocol)
    assert util.protocol_valid('not a protocol') == False

def test_bag_type_valid():
    for bag_type in const.BAG_TYPES:
        assert util.bag_type_valid(bag_type)
    assert util.bag_type_valid('not a bag type') == False

def test_fixity_type_valid():
    for fixity_type in const.FIXITY_TYPES:
        assert util.fixity_type_valid(fixity_type)
    assert util.fixity_type_valid('not a fixity type') == False

def test_username():
    assert util.username('joe') == 'dpn.joe'

def test_xfer_dir():
    assert util.xfer_dir('joe') == '/home/dpn.joe/outbound'

def test_rsync_link():
    link = util.rsync_link('tdr', 'example.com', '/home/dpn.tdr/outbound', 'file.tar')
    assert link == "dpn.tdr@example.com:/home/dpn.tdr/outbound/file.tar"

def test_digest():
    filepath = os.path.abspath(os.path.join(__file__, '..', 'testdata', 'checksum.txt'))
    assert util.digest(filepath, 'md5') == '772bdaf5340fd975bb294806d340f6d9'
    assert util.digest(filepath, 'sha256') == 'c8843be4c9d672ae91542f5539e770c6eadc5465161e4ffa5389ecef460f553f'
    # Should raise exception if we don't implement the requested algorithm.
    with raises(ValueError):
        util.digest(filepath, 'md6')
