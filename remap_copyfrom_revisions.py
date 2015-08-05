#!/usr/bin/env python
import re
import sys
import argparse


def renumber(input_filename, output_filename):
    with open(input_filename, 'r') as input_file:
        with open(output_filename, 'w') as output_file:
            renumber_file(input_file, output_file)


def renumber_file(input_file, output_file):
    revision_number_regex = re.compile("^Revision-number: (\d+)$")
    node_copyfrom_rev_regex = re.compile("^Node-copyfrom-rev: (\d+)$")
    known_revisions = []

    for line in input_file:
        revision_match = revision_number_regex.match(line)
        if revision_match:
            known_revisions.append(int(revision_match.group(1)))

        copyfrom_match = node_copyfrom_rev_regex.match(line)
        if copyfrom_match:
            copyfrom_revision = int(copyfrom_match.group(1))
            if not copyfrom_revision in known_revisions:
                existing_revision = max(filter(lambda item: item < copyfrom_revision, known_revisions))
                sys.stderr.write("Remapping: %d -> %d\n" % (copyfrom_revision, existing_revision))
                output_file.write(line.replace(str(copyfrom_revision), str(existing_revision)))
                continue

        output_file.write(line)


def main():
    parser = argparse.ArgumentParser(description="Modifies Node-copyfrom-revision to existing revisions in Subversion dumps")

    try:
        parser.add_argument("--input", "-i", type=str, required=True, metavar='FILE',
            help='existing svn dump file to process')
        parser.add_argument("--output", "-o", type=str, required=True, metavar='FILE',
            help='output file')
        options = parser.parse_args()
    except ValueError:
        parser.print_help()
        return 1

    return renumber(options.input, options.output)

if __name__ == '__main__':
    sys.exit(main())
