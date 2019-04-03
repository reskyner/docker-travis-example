import argparse
from dna_ops import DnaOperations

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Perform some operations on a DNA sequence (A,T,C,G only)")
    # set command-line options
    parser.add_argument('-v', '--verbose', action='store_true', help='Print mistakes when checking sequence')
    parser.add_argument('-c', '--check', action='store_true', help='Check the sequence is valid')
    parser.add_argument('-r', '--reverse', action='store_true', help='Reverse-complement the sequence')
    parser.add_argument('-os', '--orfs', action='store_true', help='Find longest open reading frame of input sequence')
    parser.add_argument('-or', '--orfr', action='store_true', help='Find longest open reading frame of '
                                                                   'reverse-complemented sequence')
    # set a group for sequence - either file or string
    sequence_group = parser.add_mutually_exclusive_group()
    sequence_group.add_argument('-s', '--sequence', help='String containing DNA sequence')
    sequence_group.add_argument('-f', '--file', help='File containing DNA sequence')

    args = parser.parse_args()

    # initiate a DnaOperations instance with the input sequence
    if args.sequence:
        seq = DnaOperations(args.sequence)
    elif args.file:
        seq = DnaOperations(''.join(open(args.file, 'r').read().rsplit()))
    # raise exception if no sequence input
    else:
        raise Exception('No input sequence provided - check help for info (--help)')

    # all of the calculations that can be run
    calc_ops = [args.check, args.reverse, args.orfs, args.orfr]
    # if a calculation option not specified, raise an exception
    if not any(calc_ops):
        raise Exception('No calculation option provided!')

    # check the sequence is valid
    if args.check:
        if seq.is_valid(verbose=args.verbose):
            print('Input DNA sequence is valid' + '\n')
        else:
            print('Input DNA sequence is not valid' + '\n')

    # reverse-complement the sequence
    if args.reverse:
        reverse = seq.reverse_complement()
        print('Reverse complemented sequence:\n' + reverse + '\n')

    # get the longest open reading frame of the input sequence
    if args.orfs:
        orfs = seq.open_reading_frame()
        print('Longest open reading frame/s (input sequence):\n' + str(orfs) + '\n')

    # get the longest open reading frame of the reverse-complemented input sequence
    if args.orfr:
        reverse = seq.reverse_complement()
        reverse_sequence = DnaOperations(reverse)
        orfr = reverse_sequence.open_reading_frame()
        print('Longest open reading frame/s (reverse-complemented sequence):\n' + str(orfr) + '\n')

