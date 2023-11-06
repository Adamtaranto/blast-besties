from os.path import basename
import os


def outPathCheck(args):
    """Create path to output file."""
    if not args.outFile:
        baseA = os.path.splitext(basename(args.blastAvB))[0]
        baseB = os.path.splitext(basename(args.blastBvA))[0]
        outName = baseA + "_" + baseB + "_reciprocal_pairs.tab"
    else:
        outName = args.outFile

    if args.outDir:
        absOutDir = os.path.abspath(args.outDir)
        # Create outDir if does not exist
        if not os.path.isdir(absOutDir):
            os.makedirs(absOutDir)
        outFilePath = os.path.join(args.outDir, outName)
    else:
        outFilePath = outName

    return outFilePath
