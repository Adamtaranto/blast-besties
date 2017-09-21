# Blast-Besties

Rapid discovery of reciprocal best blast pairs from BLAST output files.  


# Table of contents

* [Example usage](#example-usage)
  * [Input requirements](#input-requirements)
* [Standard options](#standard-options)
* [License](#license) 

# Example usage

Run BLASTp for each protein set AvsB and BvsA.
Require vaild alignments to cover 95% of the query sequence and with an e-value of < 0.001.

```bash
blastp -qcov_hsp_perc 95 -query A_prot.fa -subject B_prot.fa -out AvB.tab -evalue 0.001 -outfmt 6 -use_sw_tback
blastp -qcov_hsp_perc 95 -query B_prot.fa -subject A_prot.fa -out BVA.tab -evalue 0.001 -outfmt 6 -use_sw_tback
```

Report reciprocal best match pairs where each hit meets criteria e-value 
<= 0.001, hit-length >= 100, bitscore >= 100.  

```bash
./blastBesties.py -e 0.001 -l 100 -s 100 -a *blastAvB.tab* -b *blastBvA.tab
```

## Input requirements

  - Takes two BLAST output files as input. SetA vs SetB, and SetB vs SetA.
  - BLAST output format 6 (tabular)
  - Hits must be sorted by query name then descending match quality - this is default BLAST behaviour.

# Standard options

```
Usage: BLAST-Besties [-h] [-v] -a BLASTAVB -b BLASTBVA [-l MINLEN] [-e EVAL]
                     [-s BITSCORE] [-o OUTFILE] [-d OUTDIR]

Options:

  # Info
  -h, --help        Show this help message and exit.
  -v, --version     Show program's version number and exit.
  
  # Input 
  -a, --blastAvB    Blast tab result file for fastaA query against fastaB
                    subject.
  -b, --blastBvA    Blast tab result file for fastaB query against fastaA
                    subject.
  
  # Settings
  -l, --minLen      Minimum length of hit to consider valid.
  -e, --eVal        Maximum e-value to consider valid pair.
  -s, --bitScore    Minimum bitscore to consider valid pair.

  # Output
  -o, --outFile     Write reciprocal blast pairs to this file.
  -d, --outDir      Directory for new sequence files to be written to.
```

# License

Software provided under MIT license.

