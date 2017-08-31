import requests
import sys
from bs4 import BeautifulSoup as BS

def getMatches(team = ''):

	url = "http://www.espncricinfo.com/ci/engine/match/index.html?view=live"
	r = requests.get(url)
	soup = BS(r.text, "html.parser")
	tableHeads = soup.find_all('div', {'class' : 'match-section-head'})
	tableData = soup.find_all('section', {'class' : 'matches-day-block'})
	team_matches = []
	
	if team == '':
		print "\nHere are the events going on live right now: "
		for ix in range(0, len(tableHeads)):
			print "\t" + str(ix+1) + ". " + str(tableHeads[ix].h2.text)

		try:
			ch = raw_input("\nChoose the event for which you wish to check out the matches (Enter 0 to See All; -1 to exit): ")
			ch = int(ch)
			if ch == -1:
				sys.exit("Hope you had fun. Have a great day ahead!")
			temp = tableData[ch - 1] or (ch == 0)
			
		except (IndexError, ValueError):
			print 'Please enter a valid integer between -1 and ' + str(len(tableData)) + '.'
			askForExit()
	else:
		ch = 0

	if ch > 0:
		matches = tableData[ch-1].find_all('section', {'class' : 'default-match-block'})
	
	else:
		matches = tableData[0].find_all('section', {'class' : 'default-match-block'})
		for ix in range(1, len(tableData)):
			matches = matches + tableData[ix].find_all('section', {'class':'default-match-block'})

	for ix in range(0,len(matches)):
		
		matchDetails = matches[ix].find_all('div')
		
		team1 = str(matchDetails[1].text.split('\n',1)[1].split(' ')[0])
		if len(str(matchDetails[1].text.split('\n',1)[1].split(' ')[1]))>0:
			team1 = team1 + " " + str(matchDetails[1].text.split('\n',1)[1].split(' ')[1])
		score1 = str(matchDetails[1].find('span').text)
		if len(str(matchDetails[1].text.split('\n',1)[1].split(' ')[2]))>0:
			team1 = team1 + " " + str(matchDetails[1].text.split('\n',1)[1].split(' ')[2])
		score2 = str(matchDetails[2].find('span').text)
		
		team2 = str(matchDetails[2].text.split('\n',1)[1].split(' ')[0])
		if len(str(matchDetails[2].text.split('\n',1)[1].split(' ')[1]))>0:
			team2 = team2 + " " + str(matchDetails[2].text.split('\n',1)[1].split(' ')[1])
		if len(str(matchDetails[2].text.split('\n',1)[1].split(' ')[2]))>0:
			team2 = team2 + " " + str(matchDetails[2].text.split('\n',1)[1].split(' ')[2])

		headerline = "Match " + str(ix+1) + ": " + team1 + " vs " + team2
		if len(headerline)<40:
			headerline += (" " * (40 - len(headerline)))
		
		if team in ['', team1.lower(), team2.lower()]:
			team_matches.append(ix+1)
			print "\n" + headerline + "\t\t(" + str(matchDetails[0].find('span', {'class':'bold'}).text) +")"
			print str(matchDetails[0].find('span', class_='match-no').a.text.split('     ',1)[1])
			print "\t" + team1 + ": " + score1 + "\n\t" + team2 + ": " + score2
			print "\n" + matchDetails[3].text.split('\n')[1]
			print "_"*50

	if len(team_matches) == 0 and team != '':
		print 'Sorry! No match found for team ' + team + '.'
		getMatches('')

	try:
		if len(team_matches) == 1:
			ch = team_matches[0]
		else:
			ch = raw_input("\nChoose the event for which you wish to see the whole scorecard (Enter -1 to Exit; 0 for previous menu): ")
			ch = int(ch)
			if ch == -1:
				sys.exit("Hope you had fun. Have a great day ahead!")
			if ch == 0:
				getMatches(' ')
			temp = matches[ch - 1]

	except (IndexError, ValueError):
		print 'Please enter a valid integer between -1 and ' + str(len(matches)) + '.'
		askForExit()

	url2 = "http://www.espncricinfo.com" + matches[ch-1].find_all('div')[4].find_all('a')[0]['href'] + "?view=scorecard"
	matchDetails = matches[ch-1].find_all('div')
	team1 = str(matchDetails[1].text.split('\n',1)[1].split(' ')[0])
	if len(str(matchDetails[1].text.split('\n',1)[1].split(' ')[1]))>0:
		team1 = team1 + " " + str(matchDetails[1].text.split('\n',1)[1].split(' ')[1])
	score1 = str(matchDetails[1].find('span').text)
	if len(str(matchDetails[1].text.split('\n',1)[1].split(' ')[2]))>0:
		team1 = team1 + " " + str(matchDetails[1].text.split('\n',1)[1].split(' ')[2])
	score2 = str(matchDetails[2].find('span').text)

	team2 = str(matchDetails[2].text.split('\n',1)[1].split(' ')[0])
	if len(str(matchDetails[2].text.split('\n',1)[1].split(' ')[1]))>0:
		team2 = team2 + " " + str(matchDetails[2].text.split('\n',1)[1].split(' ')[1])
	if len(str(matchDetails[2].text.split('\n',1)[1].split(' ')[2]))>0:
		team2 = team2 + " " + str(matchDetails[2].text.split('\n',1)[1].split(' ')[2])

	meta = "\t" + team1 + ": " + score1 + "\n\t" + team2 + ": " + score2
	meta += "\n\n" + matchDetails[3].text.split('\n')[1]
		
	






if __name__ == '__main__':
	sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=50, cols=100))
	print "\n" + "*" *100
	#print "Welcome to Live Cricket Scores Terminal App v2.0 by Navjot Singh"
	
	team = ''
	for ix in range(1, len(sys.argv)):
		team = team + str(sys.argv[ix]).lower() + ' '
	team = team.strip()

	getMatches(team)