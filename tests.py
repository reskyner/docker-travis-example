import unittest
import json
from dna_ops import *

test_data = json.load(open('test_data.json', 'r'))


class TestValid(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data = test_data['test_valid_seqs']

    def test_valid(self):
        sequence = DnaOperations(self.test_data['valid_sequence'])
        self.assertTrue(sequence.is_valid())

    def test_valid_mixed(self):
        sequence = DnaOperations(self.test_data['valid_sequence_mixed'])
        self.assertTrue(sequence.is_valid())

    def test_invalid(self):
        sequence = DnaOperations(self.test_data['invalid_sequence'])
        self.assertFalse(sequence.is_valid())

    def test_invalid_mixed(self):
        sequence = DnaOperations(self.test_data['invalid_sequence_mixed'])
        self.assertFalse(sequence.is_valid())


class TestReverse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data = test_data['test_reverse_seqs']

    def test_simple_reverse(self):
        sequence = DnaOperations(self.test_data['seq_in'])
        self.assertEqual(self.test_data['seq_out'], sequence.reverse_complement())

    def test_junk_reverse(self):
        sequence = DnaOperations(self.test_data['junk_in'])
        self.assertRaises(Exception, lambda: sequence.reverse_complement())


class TestOpenReadingFrame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data = test_data['test_orf_seqs']

    def test_normal_sequence(self):
        sequence = DnaOperations(self.test_data['seq_in'])
        self.assertEqual(self.test_data['longest'], sequence.open_reading_frame())

    def test_reverse_complement(self):
        reverse_sequence = DnaOperations(self.test_data['seq_in']).reverse_complement()
        self.assertEqual(reverse_sequence, self.test_data['reverse_complement'])
        self.assertEqual(DnaOperations(reverse_sequence).open_reading_frame(), self.test_data['reverse_matches'])

    def test_junk_reverse_complement(self):
        sequence = DnaOperations(self.test_data['junk_in'])
        self.assertRaises(Exception, lambda: sequence.open_reading_frame())


if __name__ == '__main__':
    unittest.main()
