#!/usr/bin/env python
#python 2.7.5
#blastBesties.py
#Version 1. Adam Taranto, May 2015
#Contact, Adam Taranto, adam.taranto@anu.edu.au
#.-. .-')               ('-.      .-')    .-') _          .-. .-')    ('-.    .-')    .-') _             ('-.    .-')    
#\  ( OO )             ( OO ).-. ( OO ). (  OO) )         \  ( OO ) _(  OO)  ( OO ). (  OO) )          _(  OO)  ( OO ).  
# ;-----.\  ,--.       / . --. /(_)---\_)/     '._         ;-----.\(,------.(_)---\_)/     '._ ,-.-') (,------.(_)---\_) 
# | .-.  |  |  |.-')   | \-.  \ /    _ | |'--...__)  .-')  | .-.  | |  .---'/    _ | |'--...__)|  |OO) |  .---'/    _ |  
# | '-' /_) |  | OO ).-'-'  |  |\  :` `. '--.  .--'_(  OO) | '-' /_)|  |    \  :` `. '--.  .--'|  |  \ |  |    \  :` `.  
# | .-. `.  |  |`-' | \| |_.'  | '..`''.)   |  |  (,------.| .-. `.(|  '--.  '..`''.)   |  |   |  |(_/(|  '--.  '..`''.) 
# | |  \  |(|  '---.'  |  .-.  |.-._)   \   |  |   '------'| |  \  ||  .--' .-._)   \   |  |  ,|  |_.' |  .--' .-._)   \ 
# | '--'  / |      |   |  | |  |\       /   |  |           | '--'  /|  `---.\       /   |  | (_|  |    |  `---.\       / 
# `------'  `------'   `--' `--' `-----'    `--'           `------' `------' `-----'    `--'   `--'    `------' `-----'  

from __future__ import print_function
import os
import sys
import argparse
from collections import Counter
from os.path import basename


def main(minLen=0, eVal=0.001, recipFile=True, blastAvB=None, blastBvA=None):

	#Read pairs in as list of tuples
	if blastAvB and blastBvA:
		readBlast(minLen, eVal, blastAvB, blastBvA, recipFile)
	else:
		sys.exit('Must provide two tabbed blast result files.')


def readBlast(minLen, eVal, blastTabA, blastTabB, recipFile):
	#Reads in two blast tab output files and returns a list of pairs which are reciprocal best blast hits.
	pairs = list()

	#Find best A-B pairs
	with open(blastTabA) as src:
		data = [rec.rstrip().split('\t') for rec in src]
		cleaned_data = [map(str.strip, line) for line in data]
		lastQuery = None
		for line in cleaned_data:
			#Ignore lines begining with '#'
			if line[0][0] == "#":
				continue
			#Ignore if eVal is above threshold
			if float(line[10]) >= eVal:
				continue
			#Ignore in hit length is less than threshold
			if line[3] <= minLen:
				continue
			#If first record for this query, store the query:target pair
			if line[0] != lastQuery:	
				pairs.append(tuple(line[0:2]))
			#Update previous query ID
			lastQuery = line[0]

	#Append best B-A pairs as A-B
	with open(blastTabB) as src:
		data = [rec.rstrip().split('\t') for rec in src]
		cleaned_data = [map(str.strip, line) for line in data]
		lastQuery = None
		for line in cleaned_data:
			if line[0][0] == "#":
				continue
			if line[0] != lastQuery:	
				flipPair = (line[1],line[0])
				pairs.append(flipPair)
			lastQuery = line[0]

	#Retrieve list items that occur more than once
	recipPairs = [k for (k,v) in Counter(pairs).iteritems() if v > 1]

	if recipFile:
		baseA = os.path.splitext(basename(blastTabA))[0]
		baseB = os.path.splitext(basename(blastTabB))[0]
		outName = baseA + "_" + baseB + "_reciprocal_pairs.tab"
		outFile = open(outName,'w')
		header = "\t".join(['#SetA','SetB'])
		outFile.write(header + "\n")
		
		for a,b in recipPairs:
			abPair = "\t".join([a,b])
			outFile.write(abPair+ "\n")

		outFile.close()

	return recipPairs

if __name__== '__main__':
	###Argument handling.
	arg_parser = argparse.ArgumentParser(description='Finds reciprocal best blast pairs, above e-value threshold.')
	arg_parser.add_argument("-a", "--blastAvB", help="Blast tab result file for fastaA query against fastaB subject")
	arg_parser.add_argument("-b", "--blastBvA", help="Blast tab result file for fastaB query against fastaA subject")
	arg_parser.add_argument("-w", "--recipFile", action='store_true', default=True, help="Write reciprocal blast pairs to file. Default True.")
	arg_parser.add_argument("-l","--minLen", help="Minimum length of hit to consider valid.")
	arg_parser.add_argument("-e","--eVal", type=float, help="Minimum eval to consider valid pair.")

	#Parse arguments
	args = arg_parser.parse_args()

	###Variable Definitions
	minLen = args.minLen
	eVal = args.eVal
	blastAvB = args.blastAvB
	blastBvA = args.blastBvA
	recipFile = args.recipFile

	main(minLen, eVal, recipFile, blastAvB, blastBvA)
