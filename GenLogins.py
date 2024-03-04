#!/usr/bin/python3

import sys, itertools

#################
### VARIABLES ###
#################

# Custom names to work with
CUSTOM_NAMES = [("Corinne", "Duval"), ("Pierre", "Gaston")]

# Create variations or not
WITH_VARIATIONS = True

# Wordlist path to work with
# Wordlist format = <Firstname>:<Lastname> per line
WORDLIST = None

# Maximum/Minimum Firstname/Lastname size
MAX_FIRST_SIZE = 8
MAX_LAST_SIZE = 8
MIN_FIRST_SIZE = 4
MIN_LAST_SIZE = 4

# Separators
SEPARATORS = ["."]

# In case there is a specific format to follow
# Formats specification [(<SizeFirst1>, <Separator1>, <SizeLast1>, @<Domain1>), (<SizeFirst2>, <Separator2>, <SizeLast2>, @<Domain2>), ...]
# @<Domain> and <Separator> can be = ""
WITH_FORMATS = True
FORMATS = [("FULL", ".", "FULL", "@domain1.com"), (1, "", "FULL", "")]

#############
### MAIN ####
#############

def generate_variations(list):
    variations = []

    for first, last in list:
        if MAX_FIRST_SIZE > len(first):
            max_first_size = len(first)
        else:
            max_first_size = MAX_FIRST_SIZE
        if MAX_LAST_SIZE > len(last):
            max_last_size = len(last)
        else:
            max_last_size = MAX_LAST_SIZE
        if MIN_FIRST_SIZE > len(first):
            min_first_size = len(first)
        else:
            min_first_size = MIN_FIRST_SIZE
        if MIN_LAST_SIZE > len(last):
            min_last_size = len(last)
        else:
            min_last_size = MIN_LAST_SIZE
        for first_size in range(min_first_size, max_first_size + 1):
            for last_size in range(min_last_size, max_last_size + 1):
                if first[:first_size] != '' or last[:last_size] != '':
                    # <Firstname><Lastname> and <Lastname><Firstname>
                    variations.append(f"{first[:first_size]}{last[:last_size]}")
                    variations.append(f"{last[:last_size]}{first[:first_size]}")
                    for separator in SEPARATORS:
                        if first[:first_size] != '' and last[:last_size] != '':
                            # <Firstname><Separator><Lastname> and <Lastname><Separator><Firstname>
                            variations.append(f"{first[:first_size]}{separator}{last[:last_size]}")
                            variations.append(f"{last[:last_size]}{separator}{first[:first_size]}")

    return variations

def generate_with_formats(list):
    variations = []

    for first, last in list:
        for format in FORMATS:
            format_first, format_separator, format_last, format_domain = format
            if (isinstance(format_first, int)):
                first = first[:format_first]
            if (isinstance(format_last, int)):
                last = last[:format_last]
            variations.append(f"{first}{format_separator}{last}{format_domain}")

    return variations

if __name__ == "__main__":
    if (len (sys.argv) != 2):
        print ("\n[ERROR] Usage : {} <OutputFileName>\n".format (sys.argv[0]))
        exit()

    print ("\n[+] Generating wordlist ...")

    DIC = []

    # Add custom words
    for name in CUSTOM_NAMES:
        first, last = name
        first = first.lower().replace(" ", "")
        last = last.lower().replace(" ", "")
        DIC += [(first, last)]

    # Add words in wordlist
    if (WORDLIST != None):
        with open (WORDLIST, "r") as wd:
            lines = wd.readlines()
            for line in lines:
                line = line.replace ("\n", "")
                first, last = line.split(":")
                first = first.lower().replace(" ", "")
                last = last.lower().replace(" ", "")
                DIC += [(first, last)]

    # Generate variations
    RES = []
    if (WITH_FORMATS):
        RES += generate_with_formats(DIC)
    if (WITH_VARIATIONS):
        RES += generate_variations(DIC)

    with open (sys.argv[1], "w+") as ofile:
        for name in RES:
            ofile.write (name + "\n")

    print ("[OK] Done\n")
