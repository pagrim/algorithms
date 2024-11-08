from heapq import heapify, heappush, heappop
import logging
logger = logging.getLogger(__name__)

class HuffmanEncoder:
    """
    This class implements the Huffman encoding algorithm for lossless encoding
    """

    def __init__(self, frequencies):
        self.frequencies = frequencies
        self.nodes = {}
        self.node_idx = 0
        self.root = self._build_tree()
        self._encode_tree(self.root, "")
        logger.info('Built tree, nodes %s', self.nodes)
        logger.info('Node encodings %s', {char: node.encoding for char, node in self.nodes.items()})

    def _build_tree(self):
        """
        Initialise MinHeap and build the tree, finally returning the root
        """

        heap = []
        for char, freq in self.frequencies.items():
            hn = HuffmanNode(char, freq)
            heappush(heap, hn)
            self.nodes[char] = hn
        logger.debug('Init min heap %s', heap)

        while len(heap)>1:
            ln = heappop(heap)
            rn = heappop(heap)
            sum_node_index = self._get_sum_index()
            sn = HuffmanNode(sum_node_index,
                ln.freq + rn.freq,
                left=ln,
                right=rn
            )
            heappush(heap, sn)

        root = heappop(heap)
        root_index = self._get_sum_index(increment=False)
        self.nodes[root_index] = root
        return root

    def _encode_tree(self, node, encoding):
        """
        Encode the tree nodes with the encoding path from the root
        """
        if node.left:
            enc = encoding + "0"
            node.left.encoding = enc
            self._encode_tree(node.left, enc)
        if node.right:
            enc = encoding + "1"
            node.right.encoding = enc
            self._encode_tree(node.right, enc)

    def _get_sum_index(self, increment=True):
        if increment:
            self.node_idx += 1
        idx = f"n{self.node_idx}"
        return idx

    def encode(self, instr):
        """
        Encode an input string by referencing nodes in the tree
        """
        return "".join(self.nodes[char].encoding for char in instr)

    def decode(self, instr):
        """
        Decode an input by traversing the tree
        """
        decoded = ""
        char_index = 0
        while char_index < len(instr):
            node = self.root
            while node.left or node.right:
                curr_char = instr[char_index]
                logger.debug('At index %d, char %s', char_index, curr_char)
                if curr_char == '0':
                    node = node.left
                else:
                    node = node.right
                char_index += 1
            decoded += node.char
            logger.debug('Appended %s, index %d', node.char, char_index)
        return decoded

class HuffmanNode:
    """
    Class representing each node in the tree
    """

    def __init__(self, char, freq, left=None, right=None, encoding=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
        self.encoding = "" if encoding is None else encoding

    def __lt__(self, other):
        return self.freq < other.freq

    def __repr__(self):
        return f"HN({self.char}, {self.freq})"
