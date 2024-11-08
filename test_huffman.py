import pytest
from huffman import HuffmanEncoder, logger


freq1 = {'a': 5, 'b': 9, 'c': 12, 'd': 13, 'e': 16, 'f': 45}
freq2 = {'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}
freq3 = {' ': 7, 'a': 4, 'e': 4, 'f': 3, 't': 2, 'h': 2, 'i': 2, 's': 2,
    'n': 2, 'm': 2, 'x': 1, 'p': 1, 'l': 1, 'o': 1, 'u': 1, 'r': 1}
freq4 = {'a': 1, 'b': 1, 'c': 1}

@pytest.mark.parametrize(("frequencies", "raw"),
    [
        pytest.param(freq1, 'abc', id='id01'),
        pytest.param(freq1, 'afeb', id='id02'),
        pytest.param(freq2, 'abracadabra', id='id03'),
        pytest.param(freq3, 'huffman', id='id04'),
        pytest.param(freq4, 'ab', id='id05'),
    ])
def test_huffman_encoder(frequencies, raw):
    he = HuffmanEncoder(frequencies)
    calc_encoding = he.encode(raw)
    logger.info('Encoded %s as %s', raw, calc_encoding)
    calc_decoding = he.decode(calc_encoding)
    logger.info('Decoded %s as %s', calc_encoding, calc_decoding)
    assert calc_decoding == raw
