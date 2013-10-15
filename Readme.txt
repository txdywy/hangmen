Files:
hangman.py
words

Run:
Put all files under a same folder, then execute: python hangman.py

Workflow of the hangman solver:
1. Read a Unix dictionary file(words) and sort all words by their length, split the whole list into several ones based on word lengtg.
2. Interact with the REST API to guess 80 words.
2.1. Guess one letter in each round with a priority obtained from wiki(http://en.wikipedia.org/wiki/Letter_frequency) 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
2.2. For each round after guess one letter, user regular expression pattern to filter out words with certain a destined length, either the letter hit or not will eliminate a lot of cadidates.
2.3. If candidates word list is empty then skip this word, otherwise keep going until the last chance.
3. Obtain the result.
4. Submit the score.

P.S. I met some issues when I use python urllib2 to send http POST request and interact with server. Some connection error happens, and it looks there is also an issue related to "Threading the Global Interpreter Lock". Anyway, it looks time.sleep() changes thread scheduling and make it work to get a result finally.
But it is still possible to interupt or block the program, which is also depending on the platform(it went differnt on linux/windows/ironpython).

Submit JSON:
{u'status': 200, u'data': {u'numberOfWrongGuesses': 246, u'userId': u'genius.ron@gmail.com', u'dateTime': u'Mon Sep 09 2013 17:21:40 GMT+0000 (UTC)', u'numberOfCorrectWords': 68, u'secret': u'7FEQ8MMN1ZE0CNMI4AUHJU8FEZIFTJ', u'totalScore': 1114, u'numberOfWordsTried': 80}, u'message': u'Thank You! Please paste this JSON and send to joyce[at]strikingly.com', u'userId': u'genius.ron@gmail.com', u'secret': u'7FEQ8MMN1ZE0CNMI4AUHJU8FEZIFTJ'}