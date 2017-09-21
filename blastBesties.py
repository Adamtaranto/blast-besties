#!/usr/bin/env python
#python 2.7.5
#blastBesties.py
#Version 1.1.1 Adam Taranto, May 2017
#Contact, Adam Taranto, adam.taranto@anu.edu.au
# .-. .-')               ('-.      .-')    .-') _          .-. .-')    ('-.    .-')    .-') _             ('-.    .-')    
# \  ( OO )             ( OO ).-. ( OO ). (  OO) )         \  ( OO ) _(  OO)  ( OO ). (  OO) )          _(  OO)  ( OO ).  
#  ;-----.\  ,--.       / . --. /(_)---\_)/     '._         ;-----.\(,------.(_)---\_)/     '._ ,-.-') (,------.(_)---\_) 
#  | .-.  |  |  |.-')   | \-.  \ /    _ | |'--...__)  .-')  | .-.  | |  .---'/    _ | |'--...__)|  |OO) |  .---'/    _ |  
#  | '-' /_) |  | OO ).-'-'  |  |\  :` `. '--.  .--'_(  OO) | '-' /_)|  |    \  :` `. '--.  .--'|  |  \ |  |    \  :` `.  
#  | .-. `.  |  |`-' | \| |_.'  | '..`''.)   |  |  (,------.| .-. `.(|  '--.  '..`''.)   |  |   |  |(_/(|  '--.  '..`''.) 
#  | |  \  |(|  '---.'  |  .-.  |.-._)   \   |  |   '------'| |  \  ||  .--' .-._)   \   |  |  ,|  |_.' |  .--' .-._)   \ 
#  | '--'  / |      |   |  | |  |\       /   |  |           | '--'  /|  `---.\       /   |  | (_|  |    |  `---.\       / 
#  `------'  `------'   `--' `--' `-----'    `--'           `------' `------' `-----'    `--'   `--'    `------' `-----'  

import os
import argparse
from collections import Counter
from os.path import basename

def outPathCheck(args):
	""" Create path to output file."""
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

def getPairs(blastAvB, blastBvA, minLen=1, eVal=0.001, bitScore=0):
	""" Reads in two blast tab output files and returns a list of pairs which are reciprocal best blast hits."""
	pairs = list()
	# Find best A-B pairs
	with open(blastAvB) as src:
		data = [rec.rstrip().split('\t') for rec in src]
		cleaned_data = [map(str.strip, line) for line in data]
		lastQuery = None
		for line in cleaned_data:
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
		data = [rec.rstrip().split('\t') for rec in src]
		cleaned_data = [map(str.strip, line) for line in data]
		lastQuery = None
		for line in cleaned_data:
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
				flipPair = (line[1],line[0])
				pairs.append(flipPair)
			# Update previous query ID
			lastQuery = line[0]
	# Generator which returns list items that occur more than once
	recipPairs = [k for (k,v) in Counter(pairs).iteritems() if v > 1]
	return recipPairs

def writePairs(recipPairs,outFilePath):
	""" Write best batch pairs which occur in both BLAST tab files to output file. """
	# Open handle
	outFile = open(outFilePath,'w')
	# Write file header
	header = "\t".join(['#SetA','SetB'])
	outFile.write(header + "\n")
	# Write pairs
	for a,b in recipPairs:
		abPair = "\t".join([a,b])
		outFile.write(abPair+ "\n")
	# Close handle
	outFile.close()

def main(args):
	# Check for output directories
	outFilePath = outPathCheck(args)
	# Screen BLAST input files for reciprocal pairs
	recipPairs = getPairs(args.blastAvB, args.blastBvA, args.minLen, args.eVal, args.bitScore)
	# Write reciprical best BLAST pairs to output
	writePairs(recipPairs,outFilePath)

if __name__== '__main__':
	### Argument handling.
	parser = argparse.ArgumentParser(description='Finds reciprocal best blast pairs from BLAST output format 6 (tabular). Where hits are sorted by query name then descending match quality.',
									 prog='BLAST-Besties')
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
	main(args)