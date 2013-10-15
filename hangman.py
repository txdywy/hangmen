import sys
import urllib
import urllib2
import httplib
import json
import re
import time
import socket

#'wordsEN.txt'
#'words'
#'am'
def read_dict(filename='words'):
    "Read the file into global variables _wordList and _wordListByLength."
    global _wordList, _wordListByLength
    _wordList, _wordListByLength = [], {}
    for word in open(filename).read().splitlines():
        w = word.upper()
        flag = True
        for x in w:
        	if x not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        		flag = False
        		break
       	if flag:
        	_wordList.append(w)
    _wordList.sort(key = lambda s: len(s))
    index = 0
    length = len(_wordList[index])
    _wordListByLength[length] = []
    for word in _wordList:
    	if len(word)>length:
    		length = len(word)
    		_wordListByLength[length] = [word]
    	else:
    		_wordListByLength[length].append(word)
    	index += 1
    return _wordList, _wordListByLength

def sendRequest(url, values):
	#print values
	#time.sleep(0.5)
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	error = True
	while(error):
		#To handle Threading the Global Interpreter Lock issue with python urllib2
		#Without this, the http request may get blocked(actually always).
		time.sleep(0.05)
		try:
			#print '='
			response = urllib2.urlopen(req, timeout=1)
			the_page = response.read()
			response.close()
			data_response = json.loads(the_page)
			error = False
			#print data_response
			return data_response
		except urllib2.URLError,e:
			#print '???', e.reason
			error = True
			if str(e.reason)=='Bad Request':
				#print req, data, values
				error = False
				return None
		except socket.timeout as e:
			#print '!!!', type(e)
			error = True
	

def guessOneLetter(word, availableLetters, candidatesList):
	for letter in availableLetters:
		for wd in candidatesList:
			if letter in wd:
				return letter 
	return availableLetters[0]

def test_submit():
	url = u'http://strikingly-interview-test.herokuapp.com/guess/process'
	secret = u'H4K8U99LT8OLXRSWKOGCV55SFKO6RU'
	userId = u'genius.ron@gmail.com'
	#Get Test Results
	action = u'getTestResults'
	values = {u'action' : action,
	          u'userId' : userId,
	          u'secret' : secret,
			 }
	response_data = sendRequest(url, values)
	print response_data

	#Submit Test Results
	action = u'submitTestResults'
	values = {u'action' : action,
	          u'userId' : userId,
	          u'secret' : secret,
			 }
	response_data = sendRequest(url, values)
	print response_data

def main():
	#Initite Game
	url = u'http://strikingly-interview-test.herokuapp.com/guess/process'
	action = u'initiateGame'
	userId = u'genius.ron@gmail.com'
	values = {u'action' : action,
	          u'userId' : userId,
			 }
	#secret = u'H4K8U99LT8OLXRSWKOGCV55SFKO6RU'
	response_data = sendRequest(url, values)
	secret = response_data[u'secret']
	print 'Secret key:', secret
	#print response_data
	numberOfWordsToGuess = int(response_data[u'data'][u'numberOfWordsToGuess'])
	numberOfGuessAllowedForEachWord = int(response_data[u'data'][u'numberOfGuessAllowedForEachWord'])

	#Initite my dictionary
	read_dict()
	#print _wordListByLength
	numberOfWordsTried = 0
	while(numberOfWordsTried<80):
		#Give Me A Word
		
		action = u'nextWord'
		userId = u'genius.ron@gmail.com'
		values = {u'action' : action,
		          u'userId' : userId,
		          u'secret' : secret,
				 }
		response_data = sendRequest(url, values)
		#print response_data
		if not response_data:
			continue
		status = int(response_data[u'status'])
		word = response_data[u'word']
		numberOfGuessAllowedForThisWord = int(response_data[u'data'][u'numberOfGuessAllowedForThisWord'])
		numberOfWordsTried = int(response_data[u'data'][u'numberOfWordsTried'])
	
		print ''
		print 'I am guessing word No.' + str(numberOfWordsTried) + ':'
		numberOfGuessToThisWord = 0
		while(numberOfGuessAllowedForThisWord>0):
			#print '.',
			if (numberOfGuessToThisWord==0):
				#Letter frequency from http://en.wikipedia.org/wiki/Letter_frequency
				availableLetters = u'ETAOINSHRDLCUMWFGYPBVKJXQZ'
				usedLetters = u''
			rx = word.replace(u'*', u'.')
			pattern = re.compile(rx)
			length = len(word)
			candidatesList = []
			for w in _wordListByLength[length]:
				if pattern.match(w):
					i, right, wd = 0, True, unicode(w)
					for x in word:
						if x==u'*':
							if unicode(wd[i]) in usedLetters:
								right = False	
								break
						i += 1
					if right:
						candidatesList.append(w)

			#if len(candidatesList)<50:
			#	print candidatesList
			
			if len(candidatesList)==0:
				print 'skip, ',
				break

			#Make A Guess

			action = u'guessWord'
			guess = guessOneLetter(word, availableLetters, candidatesList)
			availableLetters = availableLetters.replace(guess, u'')
			usedLetters += guess
			values = {u'action' : action,
			          u'userId' : userId,
			          u'secret' : secret,
			          u'guess' : guess,
					 }
			response_data = sendRequest(url, values)
			#print '[Guess]', response_data 
			if not response_data:
				#Bad Request
				break
			numberOfWordsTried = int(response_data[u'data'][u'numberOfWordsTried'])
			numberOfGuessAllowedForThisWord = int(response_data[u'data'][u'numberOfGuessAllowedForThisWord'])
			print numberOfGuessAllowedForThisWord,
			word = response_data[u'word']
			print usedLetters, word
			if u'*' not in word:
				print 'hit, ',
				break
			

			#sys.stdin.read(1)
			numberOfGuessToThisWord += 1

		print 'done'

	#Get Test Results
	action = u'getTestResults'
	values = {u'action' : action,
	          u'userId' : userId,
	          u'secret' : secret,
			 }
	response_data = sendRequest(url, values)
	print response_data

	print 'Submit result? Any key to do so, close this window if not.'
	sys.stdin.read(1)

	#Submit Test Results
	action = u'submitTestResults'
	values = {u'action' : action,
	          u'userId' : userId,
	          u'secret' : secret,
			 }
	response_data = sendRequest(url, values)
	print response_data
		
if __name__ == "__main__":
    main()