#!/usr/bin/env python
import blastbesties as bb
import argparse

def mainArgs():
	### Argument handling.
	parser = argparse.ArgumentParser(description='Finds reciprocal best blast pairs from BLAST output format 6 (tabular). Where hits are sorted by query name then descending match quality.')
	parser.add_argument('-v', '--version', action='version', version='1.1.1')
	parser.add_argument("-a", "--blastAvB", required=True, default=None, help="Blast tab result file for fastaA query against fastaB subject")
	parser.add_argument("-b", "--blastBvA", required=True, default=None, help="Blast tab result file for fastaB query against fastaA subject")
	parser.add_argument("-l","--minLen", default=1, help="Minimum length of hit to consider valid.")
	parser.add_argument("-e","--eVal", default=0.001, type=float, help="Maximum e-value to consider valid pair.")
	parser.add_argument("-s","--bitScore", default=1.0, type=float, help="Minimum bitscore to consider valid pair.")
	parser.add_argument("-o", "--outFile", default=None, help="Write reciprocal blast pairs to this file.")
	parser.add_argument("-d", "--outDir", type=str, default=None, help="Directory for new sequence files to be written to.")
	# Parse arguments
	args = parser.parse_args()
	# Call main function
	return args

def main():
	# Get cmd line args
	args = mainArgs()
	# Check for output directories
	outFilePath = bb.outPathCheck(args)
	# Screen BLAST input files for reciprocal pairs
	recipPairs = bb.getPairs(args.blastAvB, args.blastBvA, args.minLen, args.eVal, args.bitScore)
	# Write reciprical best BLAST pairs to output
	bb.writePairs(recipPairs,outFilePath)
