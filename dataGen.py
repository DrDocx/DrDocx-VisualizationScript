import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import sys
from colorama import init, Fore
from PIL import Image
import matplotlib.image as mpimg
import random	
import math

_data = []
_tests = []
_testGroups =[]

_localDir = ""

def main():
	pullNamesFromFile()
	pullTestsFromFile()
	#generateTestGroups()

	process()


def pullNamesFromFile(): 
	global _localDir
	print("Intaking Data File")

	_localDir = os.getcwd()
	_dataFilePath = _localDir + "\\names.txt"
	_dataFile = open(_dataFilePath, "r") #read only access of the data file

	_iter = _dataFile.readlines()
	for _line in _iter:
		_data.append(_line[0:-1])


	_dataFile.close()

def pullTestsFromFile(): 
	global _localDir
	print("Intaking Tests File")

	_localDir = os.getcwd()
	_dataFilePath = _localDir + "\\tests.txt"
	_dataFile = open(_dataFilePath, "r") #read only access of the data file

	_iter = _dataFile.readlines()
	for _line in _iter:
		_tests.append(_line[0:-1])


	_dataFile.close()

def generateTestGroups():
	print("Generating Test Groups")
	global _tests

	_groupA = []
	_groupB = []
	_groupC = []
	for i in range(0, 11):
		_groupA.append(generateTest(_tests[i]))
	for i in range(11, 21):
		_groupB.append(generateTest(_tests[i]))
	for i in range(21, 29):
		_groupC.append(generateTest(_tests[i]))

	# _testGroups.append(_groupA)
	# _testGroups.append(_groupB)
	# _testGroups.append(_groupC)

	_testGroups = {"Primary Tests": _groupA, "Secondary Tests": _groupB, "Tertiary Tests":_groupC}

	return _testGroups

def generateTest(name):
	_zscaledScore = random.uniform(-4, 4)
	
	_relTest = {'Name': name, "Description": "abc", "Id": 2}
	_test = {"RawSore": 1, "ScaledScore": 1, "ZScore": _zscaledScore, "Percentile": 50, "RelatedTest": _relTest}
	return _test

def process():

	for patient in _data:
		generatePatients(patient)


def generatePatients(name):
	global _localDir

	with open(_localDir + "/patients/" + name + ".json", "w") as write_file:
		json.dump(generateTestGroups(), write_file)

if __name__ == "__main__":
    main()