# .-. .-')               ('-.      .-')    .-') _          .-. .-')    ('-.    .-')    .-') _             ('-.    .-')
# \  ( OO )             ( OO ).-. ( OO ). (  OO) )         \  ( OO ) _(  OO)  ( OO ). (  OO) )          _(  OO)  ( OO ).
#  ;-----.\  ,--.       / . --. /(_)---\_)/     '._         ;-----.\(,------.(_)---\_)/     '._ ,-.-') (,------.(_)---\_)
#  | .-.  |  |  |.-')   | \-.  \ /    _ | |'--...__)  .-')  | .-.  | |  .---'/    _ | |'--...__)|  |OO) |  .---'/    _ |
#  | '-' /_) |  | OO ).-'-'  |  |\  :` `. '--.  .--'_(  OO) | '-' /_)|  |    \  :` `. '--.  .--'|  |  \ |  |    \  :` `.
#  | .-. `.  |  |`-' | \| |_.'  | '..`''.)   |  |  (,------.| .-. `.(|  '--.  '..`''.)   |  |   |  |(_/(|  '--.  '..`''.)
#  | |  \  |(|  '---.'  |  .-.  |.-._)   \   |  |   '------'| |  \  ||  .--' .-._)   \   |  |  ,|  |_.' |  .--' .-._)   \
#  | '--'  / |      |   |  | |  |\       /   |  |           | '--'  /|  `---.\       /   |  | (_|  |    |  `---.\       /
#  `------'  `------'   `--' `--' `-----'    `--'           `------' `------' `-----'    `--'   `--'    `------' `-----'

import argparse
import logging

from argparse_tui import add_tui_argument

from blastbesties.blastops import getPairs
from blastbesties.utils import outPathCheck, isfile, writePairs
from blastbesties._version import __version__
from blastbesties.logs import init_logging

def mainArgs():
    """
    Handles command-line arguments for the script.

    Returns:
    argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Finds reciprocal best BLAST pairs from BLAST output format 6 (tabular). Where hits are sorted by query name then descending match quality."
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
        help="Show program's version number and exit."
    )
    parser.add_argument(
        "-a",
        "--blastAvB",
        required=True,
        help="BLAST tab result file for fastaA query against fastaB subject."
    )
    parser.add_argument(
        "-b",
        "--blastBvA",
        required=True,
        help="BLAST tab result file for fastaB query against fastaA subject."
    )
    parser.add_argument(
        "-l",
        "--minLen",
        default=1,
        type=int,
        help="Minimum length of hit to consider valid. Defaults to 1."
    )
    parser.add_argument(
        "-e",
        "--eVal",
        default=0.001,
        type=float,
        help="Maximum e-value to consider valid pair. Defaults to 0.001."
    )
    parser.add_argument(
        "-s",
        "--bitScore",
        default=1.0,
        type=float,
        help="Minimum bitscore to consider valid pair. Defaults to 1.0."
    )
    parser.add_argument(
        "-o",
        "--outFile",
        default=None,
        help="Write reciprocal BLAST pairs to this file."
    )
    parser.add_argument(
        "-d",
        "--outDir",
        type=str,
        default=None,
        help="Directory for new sequence files to be written to."
    )
    parser.add_argument(
        "--loglevel",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set logging level. Defaults to INFO."
    )
    
    add_tui_argument(parser, option_strings=["--tui"])
    
    # Parse arguments
    args = parser.parse_args()
    return args

def main():
    """
    Main function to execute the script.
    """
    # Get command-line arguments
    args = mainArgs()

    # Set up logging
    init_logging(loglevel=args.loglevel)

    # Check if input files exist
    isfile([args.blastAvB, args.blastBvA])

    # Determine output file path
    outFilePath = outPathCheck(args)

    # Find reciprocal best BLAST pairs
    recipPairs = getPairs(
        args.blastAvB, args.blastBvA, args.minLen, args.eVal, args.bitScore
    )

    # Write reciprocal best BLAST pairs to output file
    writePairs(recipPairs, outFilePath)

    logging.info("Finished")

if __name__ == "__main__":
    main()
