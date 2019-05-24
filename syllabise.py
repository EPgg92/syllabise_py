#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""syllabise.py

Package of useful functions to syllabise word in french.

This file needs a constants.yaml file in the same directory as the script 
containing:
    - a list named vowel containing your vowels (V)
    - a list named consonnant containing your consonnants (C)
    - a dictionnary named exeption containing as key some letters and as value
      a V or a C

Usage:
  ./syllabise.py WORD [WORD ...]
  ./syllabise.py (-f | --file) inputfile
  ./syllabise.py (-h | --help)
  ./syllabise.py (-v | --version)

"""
import re
import sys
import yaml
import argparse


def open_yml(path):
    """Return a dict form a yml file.

    :param path: path to a yml file
    :type path: str
    :return: dictionnary corresponding at yml file
    :rtype: dict
    """
    returned_dic = {}
    with open(path, 'r') as stream:
        returned_dic = yaml.load(stream, Loader=yaml.SafeLoader)
    return returned_dic


def create_yml(path, data):
    """Create yml file from a dict.

    :param path: path to a yml file to create
    :type path: str
    :param data: dictionnary of variable
    :type data: dict
    """
    with open(path, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


DICT_CONST = open_yml('./constants.yaml')
VOWEL = DICT_CONST['vowel']
NO_E_VOWEL = VOWEL.copy()
NO_E_VOWEL.remove('e')
EXEPTION = DICT_CONST['exeption']
CONSONNANT = DICT_CONST['consonnant']


def list_letters_and_exceptions(word):
    """Return a transformed word split into letters and exeptions.

    Read constants.yaml where are located exceptions, as entiere words or
    groups like TR, DR, diphtongs, etc.

    :param word: a word
    :type word: str
    :return: list of letters and exeptions
    :rtype: list
    """
    letters_and_exceptions = []
    w = word
    jump = 0
    for j in range(len(w)):
        if jump == 0:
            k = 0
            while True:
                if k != 0:
                    wj = w[j:-k]
                else:
                    wj = w[j:]
                if wj in EXEPTION:
                    jump = len(wj) - 1
                    letters_and_exceptions.append(wj)
                    break
                elif len(wj) == 1:
                    letters_and_exceptions.append(wj)
                    break
                elif wj == '':
                    break
                k += 1
        else:
            jump -= 1
    return letters_and_exceptions


def transform_cv(list_let_exc):
    """Return a list of C and V using list of letters and exeptions.

    :param list_let_exc: list of letters and exeptions
    :type list_let_exc: list
    :return: list of C and V tags
    :rtype: list
    """
    return [EXEPTION[let_exc] if let_exc in EXEPTION else
            'V' if let_exc in VOWEL else
            'C' if let_exc in CONSONNANT else ""
            for let_exc in list_let_exc]


def get_syllabe_cv(list_cv):
    """Return list of grouped C and V tags using list of C and V tags.

    Intend to respect the Maximal Onset Principle without overloading codas
        - VCV > V.CV
        - VCCV > VC.CV (TR and his buddies are already taking in account))

    :param list_cv: list of C and V tags
    :type list_cv: list
    :return: list of grouped C and V tags
    :rtype: list
    """
    temp = [''.join(x) for x in re.findall(r'C*VC*', ''.join(list_cv))]
    syllabe_cv = []
    for i, x in enumerate(temp):
        if i != len(temp) - 1 and x[-1] == "C" and temp[i + 1][0] == "V":
            syllabe_cv.append(x[:-1])
            temp[i + 1] = "{}{}".format("C", temp[i + 1])
        else:
            syllabe_cv.append(x)
    return syllabe_cv


def syllabise_word(word):
    """Return list of syllabe of a word.

    :param word: a word
    :type word: str
    :return: list of syllabe
    :rtype: list()
    """
    list_let_exc = list_letters_and_exceptions(word)
    list_cv = transform_cv(list_let_exc)
    syllabe_cv = get_syllabe_cv(list_cv)
    syllabes = []
    for cv in syllabe_cv:
        syll = []
        for _ in range(len(cv)):
            syll.append(list_let_exc.pop(0))
        syllabes.append("".join(syll))
    return syllabes

def print_syllabise(word):
    """Print the syllabised word

    :param word: a word
    :type word: str
    """
    print('{} => {}'.format(word, str(syllabise_word(word))))


if __name__ == '__main__':
    # Manage args
    parser = argparse.ArgumentParser(usage=__doc__, prog='syllabise.py')
    parser.add_argument('-f', '--file', nargs=1, 
        help="syllabise the text contained in the input file")
    parser.add_argument('--version', action='version',
        version='%(prog)s 1.0')
    parser.add_argument('words', metavar='WORD', type=str, nargs='*',
                   help='words to syllabise')
    args = parser.parse_args()
    print(args)

    if args.file != None:
        for file in args.file:
            print(file)
            with open(file,'r') as f:
                for line in f:
                    for word in line.split():
                        print_syllabise(word)
    else:
        for word in args.words:
            print_syllabise(word)
