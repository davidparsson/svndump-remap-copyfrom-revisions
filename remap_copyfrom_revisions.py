#!/usr/bin/env python
import re
import sys

def renumber(dump_filename):
    with open(dump_filename, 'r+') as dump_file:
        renumber_file(dump_file)

def renumber_file(dump_file):
    revision_number_regex = re.compile("^Revision-number: (\d+)$")
    node_copyfrom_rev_regex = re.compile("^Node-copyfrom-rev: (\d+)$")
    known_revisions = []

    for line in dump_file:
        revision_match = revision_number_regex.match(line)
        if revision_match:
            known_revisions.append(int(revision_match.group(1)))

        copyfrom_match = node_copyfrom_rev_regex.match(line)
        if copyfrom_match:
            copyfrom_revision = int(copyfrom_match.group(1))
            if not copyfrom_revision in known_revisions:
                existing_revision = max(filter(lambda item: item < copyfrom_revision, known_revisions))
                sys.stderr.write("Remapping: %d -> %d\n" % (copyfrom_revision, existing_revision))
                sys.stdout.write(line.replace(str(copyfrom_revision), str(existing_revision)))
                continue

        sys.stdout.write(line)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        raise Exception("Wrong number of arguments provided")
    elif len(sys.argv) == 2:
        sys.exit(renumber(sys.argv[1]))
    else:
        sys.exit(renumber_file(sys.stdin))

