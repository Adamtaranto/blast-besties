from collections import Counter
import logging


def getPairs(blastAvB, blastBvA, minLen=1, eVal=0.001, bitScore=0):
    """
    Reads in two BLAST tabular output files and returns a list of pairs which are reciprocal best BLAST hits.

    Parameters:
    blastAvB (str): Path to the BLAST output file for query A against subject B.
    blastBvA (str): Path to the BLAST output file for query B against subject A.
    minLen (int, optional): Minimum length of hit to consider valid. Defaults to 1.
    eVal (float, optional): Maximum e-value to consider valid pair. Defaults to 0.001.
    bitScore (float, optional): Minimum bitscore to consider valid pair. Defaults to 0.

    Returns:
    list: A list of tuples representing reciprocal best BLAST hit pairs.
    """
    logging.info(f"Retrieving reciprocal best hits between {blastAvB} and {blastBvA}")
    logging.info(
        f"Filtering BLAST hits: minLen={minLen}, eVal={eVal}, bitScore={bitScore}"
    )

    pairs = []

    # Process the first BLAST file (A vs B)
    with open(blastAvB) as src:
        data = [rec.rstrip().split("\t") for rec in src]
        cleaned_data = [map(str.strip, line) for line in data]
        lastQuery = None
        for line in cleaned_data:
            line = list(line)  # Convert map object to list
            # Ignore lines beginning with '#'
            if line[0][0] == "#":
                continue
            # Ignore if e-value is above threshold or bitscore is below threshold
            if float(line[10]) > eVal or float(line[11]) < bitScore:
                continue
            # Ignore if hit length is less than threshold
            if int(line[3]) < minLen:
                continue
            # If first record for this query, store the query:target pair
            if line[0] != lastQuery:
                pairs.append(tuple(line[0:2]))
            # Update previous query ID
            lastQuery = line[0]

    # Process the second BLAST file (B vs A)
    with open(blastBvA) as src:
        data = [rec.rstrip().split("\t") for rec in src]
        cleaned_data = [map(str.strip, line) for line in data]
        lastQuery = None
        for line in cleaned_data:
            line = list(line)  # Convert map object to list
            # Ignore lines beginning with '#'
            if line[0][0] == "#":
                continue
            # Ignore if e-value is above threshold or bitscore is below threshold
            if float(line[10]) > eVal or float(line[11]) < bitScore:
                continue
            # Ignore if hit length is less than threshold
            if int(line[3]) < minLen:
                continue
            # If first record for this query, flip query:target pair and store as target:query
            if line[0] != lastQuery:
                flipPair = (line[1], line[0])
                pairs.append(flipPair)
            # Update previous query ID
            lastQuery = line[0]

    # Identify reciprocal best pairs
    recipPairs = [k for (k, v) in Counter(pairs).items() if v > 1]
    logging.info(
        f"Found {len(recipPairs)} reciprocal best BLAST pairs passing match criteria."
    )

    return recipPairs
