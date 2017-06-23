#!/usr/bin/env python

#TODO: .key/Data/... exclude

import sys
import os
import hashlib

def printArray(a):
	for e in a:
		print e
		
def printDict(d):
	for k in d:
		print "%s > %s" % (k, d[k])	
		
def printResults(res):
	for k in res:
		print "%s" % k
		for e in res[k]:
			print "   %s" % e
				
		
def scanDir(directory, filter):
	files = []
	if not os.path.isdir(directory):
		print "is not dir"
		return False
	content = os.listdir(directory)	
	for entryName in content:
		fullPath = os.path.join(directory, entryName)
		if ".key/Data/" in fullPath:
			continue
		if os.path.isfile(fullPath) and fullPath.lower().endswith(filter):
			files.append(fullPath)
		if os.path.isdir(fullPath):
			files.extend(scanDir(fullPath, filter))			
	return files
	
def makeMd5(fullPath):
	hash = None
	if not os.path.isfile(fullPath):
		print "is not file"
		return hash
	m = hashlib.md5()
	m.update(open(fullPath).read())
	hash = m.hexdigest()
	return hash	
	
def findMultiples(files):
	multiples = {}
	tmp = {}	
	for fullPath in files:
		md5 = makeMd5(fullPath)
		if md5 in tmp.keys():
			entry = [fullPath, tmp[md5]]
			if md5 in multiples.keys():
				entry.extend(multiples[md5])
			multiples.update({md5 : entry})
		else:
			tmp.update({md5 : fullPath})
	return multiples

def main():
	filter = ""
	directory = os.getcwd()
	filteredFiles = []
	if len(sys.argv) > 1:
		filter = sys.argv[1]
	print "filter = %s" % filter
	print "working directory = %s" % directory
	filteredFiles = scanDir(directory, filter)
	print "number of files found: %s" % len(filteredFiles)
	multiples = findMultiples(filteredFiles)
	printResults(multiples)
	print "number of multiples found: %s" % len(multiples)
	

main()
