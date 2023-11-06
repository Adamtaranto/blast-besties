from collections import Counter


def getPairs(blastAvB, blastBvA, minLen=1, eVal=0.001, bitScore=0):
    """Reads in two blast tab output files and returns a list of pairs which are reciprocal best blast hits."""
    pairs = list()
    # Find best A-B pairs
    with open(blastAvB) as src:
        data = [rec.rstrip().split("\t") for rec in src]
        cleaned_data = [map(str.strip, line) for line in data]
        lastQuery = None
        for line in cleaned_data:
            # Map yield generator in Py3
            line = list(line)
            # Ignore lines begining with '#'
            if line[0][0] == "#":
                continue
            # Ignore if eVal is above threshold or bitscore is below threshold
            if float(line[10]) >= eVal or float(line[11]) <= bitScore:
                continue
            # Ignore if hit length is less than threshold
            if line[3] <= minLen:
                continue
            # If first record for this query, store the query:target pair
            if line[0] != lastQuery:
                pairs.append(tuple(line[0:2]))
            # Update previous query ID
            lastQuery = line[0]
    # Append best B-A pairs as A-B
    with open(blastBvA) as src:
        data = [rec.rstrip().split("\t") for rec in src]
        cleaned_data = [map(str.strip, line) for line in data]
        lastQuery = None
        for line in cleaned_data:
            # Map yield generator in Py3
            line = list(line)
            # Ignore lines begining with '#'
            if line[0][0] == "#":
                continue
            # Ignore if eVal is above threshold or bitscore is below threshold
            if float(line[10]) >= eVal or float(line[11]) <= bitScore:
                continue
            # Ignore if hit length is less than threshold
            if line[3] <= minLen:
                continue
            # If first record for this query, flip query:target pair and store as target:query.
            if line[0] != lastQuery:
                flipPair = (line[1], line[0])
                pairs.append(flipPair)
            # Update previous query ID
            lastQuery = line[0]
    # Generator which returns list items that occur more than once
    recipPairs = [k for (k, v) in Counter(pairs).items() if v > 1]
    return recipPairs


def writePairs(recipPairs, outFilePath):
    """Write best batch pairs which occur in both BLAST tab files to output file."""
    # Open handle
    outFile = open(outFilePath, "w")
    # Write file header
    header = "\t".join(["#SetA", "SetB"])
    outFile.write(header + "\n")
    # Write pairs
    for a, b in recipPairs:
        abPair = "\t".join([a, b])
        outFile.write(abPair + "\n")
    # Close handle
    outFile.close()
