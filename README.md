<a href="https://opensource.org/licenses/MIT">
<img src="https://img.shields.io/badge/License-MIT-yellow.svg" align="left" height="20"/>
</a> 
<br clear="left"/>


# Blast-Besties

Rapid discovery of reciprocal best blast pairs from BLAST output files.  


## Table of contents
- [Blast-Besties](#blast-besties)
  - [Table of contents](#table-of-contents)
  - [Install Blast-Besties](#install-blast-besties)
  - [Example usage](#example-usage)
    - [Input requirements](#input-requirements)
    - [Standard options](#standard-options)
  - [License](#license)

## Install Blast-Besties

There are 3 options available for installing Blast-Besties locally:

1) Install from PyPi.

```bash
pip install blastbesties
```

2) Pip install latest development version directly from this git repository.

```bash
pip install git+https://github.com/Adamtaranto/blast-besties.git
```

3) Clone from this repository and install as a local Python package if you want to edit the code.

```bash
git clone https://github.com/Adamtaranto/blast-besties.git && cd blast-besties && pip install -e ".[tests]"
```


## Example usage

Run BLASTp for each protein set AvsB and BvsA.
Require vaild alignments to cover 90% of the query sequence and with an e-value of < 0.001.

```bash
blastp -qcov_hsp_perc 90 -query A_prot.fa -subject B_prot.fa -out AvB.tab -evalue 0.001 -outfmt 6 -use_sw_tback
blastp -qcov_hsp_perc 90 -query B_prot.fa -subject A_prot.fa -out BvA.tab -evalue 0.001 -outfmt 6 -use_sw_tback
```

Report reciprocal best match pairs where each hit meets criteria e-value 
<= 0.001, hit-length >= 40, bitscore >= 100.  

```bash
blastbesties -e 0.001 -l 40 -s 100 -a AvB.tab -b BvA.tab -o pairs.tab
```

To run in interactive mode use `--tui` to open the terminal user interface.

```bash
blastbesties --tui
```


### Input requirements

  - Takes two BLAST output files as input. SetA vs SetB, and SetB vs SetA.
  - BLAST output format 6 (tabular)
  - Hits must be sorted by query name then descending match quality - this is default BLAST behaviour.

### Standard options

```
Usage: blastbesties [-h] [--version] -a BLASTAVB -b BLASTBVA [-l MINLEN] [-e EVAL] [-s BITSCORE] [-o OUTFILE] [-d OUTDIR] [--loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--tui]

Finds reciprocal best BLAST pairs from BLAST output format 6 (tabular). Where hits are sorted by query name then descending match quality.

options:
  -h, --help            show this help message and exit
  --version             Show program's version number and exit.
  -a BLASTAVB, --blastAvB BLASTAVB
                        BLAST tab result file for fastaA query against fastaB subject.
  -b BLASTBVA, --blastBvA BLASTBVA
                        BLAST tab result file for fastaB query against fastaA subject.
  -l MINLEN, --minLen MINLEN
                        Minimum length of hit to consider valid. Defaults to 1.
  -e EVAL, --eVal EVAL  Maximum e-value to consider valid pair. Defaults to 0.001.
  -s BITSCORE, --bitScore BITSCORE
                        Minimum bitscore to consider valid pair. Defaults to 1.0.
  -o OUTFILE, --outFile OUTFILE
                        Write reciprocal BLAST pairs to this file.
  -d OUTDIR, --outDir OUTDIR
                        Directory for new sequence files to be written to.
  --loglevel {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set logging level. Defaults to INFO.
  --tui                 Open Textual UI.
```

## License

Software provided under MIT license.

