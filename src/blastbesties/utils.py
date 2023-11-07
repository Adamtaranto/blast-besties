from os import makedirs
import logging
import os.path as op
import sys


def isfile(fileList: list):
    isMissing = False
    for infile in fileList:
        if not op.exists(infile):
            logging.error(f"Input file not found: {infile}")
            isMissing = True
    if isMissing:
        logging.error(f"Exiting.")
        sys.exit(1)


def outPathCheck(args):
    """Create path to output file."""
    if not args.outFile:
        baseA = op.splitext(op.basename(args.blastAvB))[0]
        baseB = op.splitext(op.basename(args.blastBvA))[0]
        outName = baseA + "_" + baseB + "_reciprocal_pairs.tab"
        # Replace any spaces with "_"
        outName = outName.replace(" ", "_")
    else:
        outName = args.outFile

    if args.outDir:
        absOutDir = op.abspath(args.outDir)
        # Create outDir if does not exist
        if not op.isdir(absOutDir):
            makedirs(absOutDir)
        outFilePath = op.join(args.outDir, outName)
    else:
        outFilePath = outName

    return outFilePath


def writePairs(recipPairs, outFilePath):
    """Write best batch pairs which occur in both BLAST tab files to output file."""
    logging.info(f"Writing pairs to file: {outFilePath}")
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
