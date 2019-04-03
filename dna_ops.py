import re


class DnaOperations:
    def __init__(self, sequence):
        self.sequence = sequence.upper()

    def iterate_pattern(self, pattern):
        """Iterate self.sequence (initiated by input to class) and look for patterns matching input
        Args:
            pattern: A string containing a regex pattern
        Returns:
            iterator: A regex iterator object, resulting from finding pattern iteratively from self.sequence
        """
        # make regex pattern from input
        p = re.compile(pattern)
        # iterate to find all occurrences of p in search_string
        iterator = p.finditer(self.sequence)

        return iterator

    def construct_mistakes(self, invalid):
        """Construct a string from self.sequence highlighting where characters with given indices are
        Args:
            invalid: An array containing the indices of the invalid positions to be highlighted
        Returns:
            dna_string: self.sequence with '^' AFTER the characters in positions given by invalid
        """
        dna_string = self.sequence
        # counter to add 1 when marker character added to string
        counter = 0
        # using list of invalid character indices
        for i in range(0, len(invalid)):
            # modify input string to add '^' after (+1) invalid character
            dna_string = dna_string[:invalid[i] + counter + 1] + '^' + dna_string[invalid[i] + counter + 1:]
            # always then add 1 to the counter unless it's the last entry - string becomes longer by 1
            if i != len(invalid) - 1:
                counter += 1

        return dna_string

    def is_valid(self, verbose=False):
        """Check whether self.sequence contains anything that is not A,C,T,G (case-insensitive)
        Args:
            verbose (default=False): True to print mistakes (from self.construct_mistakes)
        Returns:
            True if valid, False if not
        """
        # pattern:
        # 1. case insensitive (?i)
        # 2. search for any single character not matching A, T, C or G [^ATGC]
        iterator = self.iterate_pattern(r"(?i)[^ATGC]")
        # convert spans from iterator to single index values (we know each span has len 1 as looking for single chars)
        invalid = [range(m.span()[0], m.span()[1])[0] for m in iterator]

        # if there are any invalid bits, construct the string with mistakes indicated, and return False
        if invalid:
            if verbose:
                mistakes = self.construct_mistakes(invalid=invalid)
                print('mistake(s) found in string:\n' + mistakes + '\n')

            return False

        # no mistakes returns true
        return True

    def reverse_complement(self):
        """Returns the reverse-complemented sequence of self.sequence
        Returns:
            reverse_string: reverse-complimented sequence
        """
        # make sure not lower-case
        dna_string = self.sequence.upper()
        # dict of translations
        translate = {'A': 'T', 'C': 'G', 'T': 'A', 'G': 'C'}
        # construct string from list of translated characters
        try:
            reverse_string = ''.join([translate[x] for x in dna_string])[::-1]
        except KeyError:
            raise KeyError('A character in the input sequence is not right. Use is_valid() to check')

        return reverse_string

    def open_reading_frame(self):
        """Returns the longest open reading frame/s of self.sequence;
        Returns:
            orf (lst): List of longest open reading frame/s
        """
        if not self.is_valid():
            raise Exception('A character in the input sequence is not right. Use is_valid() to check')
        # pattern:
        # 1. any part of the string beginning with ATG (ATG)
        # 2. any set of 3 characters not containing TAA or TAG or TGA - any number of matches ((?:(?!TAA|TAG|TGA)...)*)
        # 3. ends with TAG or TAA or TGA (TAG|TAA|TGA)
        iterator = self.iterate_pattern(r"(ATG)(?:(?!TAA|TAG|TGA)...)*(TAG|TAA|TGA)")
        # get spans of matches from iterator
        spans = [m.span() for m in iterator if m.span]
        if spans:
            # get the positions(p) and lengths(ln) for each matching string
            enumerated = [(p, ln) for (p, ln) in enumerate([y - x for x, y in spans])]
            # get the max length from enumerated
            m_len = max([ln for (p, ln) in enumerated])
            # get the corresponding positions
            indices = [p for (p, ln) in enumerated if ln == m_len]
            # get all strings corresponding to the maximum length from their indices (spans)
            orf = [self.sequence[spans[i][0]:spans[i][1]] for i in indices]

        else:
            orf = []

        return orf
