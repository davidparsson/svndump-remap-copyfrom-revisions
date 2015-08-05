Usage
-----

This script modifies filtered Subversion dump files by replacing `Node-copyfrom-rev` revisions that are not in the dump file

If [`p4convert`](https://swarm.workshop.perforce.com/projects/perforce-software-p4convert/) logs 
`From node is missing from dataset; skipping!` when importing a partial filtered Subversion repository into Perforce, copy/branch history may be lost. This script can fix this.

First generate your filtered Subversion dump file, then run it though the script:

    ./remap_copyfrom_revisions.py subversion_repo.dmp > remapped_subversion_repo.dmp
    
Finally import the resulting dump file into Perforce.

License
-------

[MIT](LICENSE)
