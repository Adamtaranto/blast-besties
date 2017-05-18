# Blast-Besties
Rapid discovery of reciprocal best blast pairs from BLAST output files.  

Input: 
  - Takes two BLAST output files as input. SetA vs SetB, and SetB vs SetA.
  - BLAST output format 6 (tabular)
  - Hits must be sorted by query name then descending match quality (Default BLAST behaviour)  

## Usage:
Example:  

**./blastBesties** -e 0.001 -s 100 -a *blastAvB.tab* -b *blastBvA.tab*  

**Required:**
  - **-a, --blastAvB** [BLASTAVB]
    - Blast tab result file for fastaA query against fastaB subject.
  - **-b, --blastBvA** [BLASTBVA]
    - Blast tab result file for fastaB query against fastaA subject.  

**Optional:**
  - **-h, --help**
    - Show this help message and exit.
  - **-v, --version**
    - Show programs version number and exit.
  - **-l, --minLen** [MINLEN]
    - Minimum length of hit to consider valid.
  - **-e, --eVal** [EVAL]  
    - Maximum e-value to consider valid pair.
  - **-s, --bitScore** [BITSCORE]
    - Minimum bitscore to consider valid pair.
  - **-o, --outFile** [OUTFILE]
    - Write reciprocal blast pairs to this file.
  - **-d, --outDir** [OUTDIR]
    - Directory for new sequence files to be written to.