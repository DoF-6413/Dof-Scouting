from random import *

# NOTE: This Less Quick & Dirty Python script still does NOT try to make data values that match when
# adding up things like pieces scored & movement vs "match score" that CoConuts tracked
# The script does use some weighting to generate score increases/decreases between matches so we can
# see likely trends in Tableau.

# Index names to make the code easier to follow

TEAMNUM = 0
TEAMNAME = 1
SCORECHANGEFACTOR = 2
RANDOMIZEFACTOR = 3
MATCHCOUNT = 4
CONEHIGH = 5
CONEMED  = 6
CONELOW  = 7
CONEMISS = 8
CUBEHIGH = 9
CUBEMED  = 10
CUBELOW  = 11
CUBEMISS = 12

# The teams array is made up of several lists that encode match data and other info we need to create 
# trending data to visualize.  Each list looks like this:
#
# [ team_number, team_name, high_goal_score_change_over_time, randomize, last_score, rounds ]
#
# That is because the CoConuts only track a final match score per match and NOTHING else!  If we want
# more later, we have to make adjustments.  That is why I at least use index names to make the script
# readable and more flexible.
a_Teams = [
    [1234, "lions",     0.1,    0,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2345, "tigers",    1.2,    0.5,    0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3456, "bears",     -0.2,   0.5,    0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4567, "wizards",   2,      1,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5678, "eagles",    0.5,    0.2,    0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6789, "falcons",   0.1,    4,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7890, "cheese",    -0.5,   1,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1324, "lime",      -0.5,   0,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2435, "orange",    -1,     0,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3546, "oregano",   1,      0,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4657, "newbies",   0,      3,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5768, "gears",     0.4,    5,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6879, "wires",     -2,     3,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7980, "cogs",      1.2,    1,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1345, "sprockets", 0.8,    2,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2456, "squirrels", 0.5,    8,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3567, "dogs",      2,      6,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4678, "cats",      0.8,    2,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5555, "pigs",      0.2,    3,      0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6666, "parrots",   0.76,   1.2,    0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7777, "seeds",     0,      1,      0, 0, 0, 0, 0, 0, 0, 0, 0] 
    ]

def calcNewScore( currentScore, scoreChangeFactor, randomizeFactor ):
        # Calculate a random decrease or increase amount for adjusting the score
        # using previous value as a starting point.
        # print(f"scf:{scoreChangeFactor}, rf:{randomizeFactor}")
        increase = scoreChangeFactor + uniform( randomizeFactor * -1, randomizeFactor )

        # Update the score with the random increase/decrease amount
        newScore = round( currentScore + increase, 0 )

        # Make sure there is no negative score
        if newScore < 0:
            newScore = 0
        
        return newScore

# Preassign random scores to each team so we have a starting point for increases/decreases
for team in range(21):
	a_Teams[team][CONEHIGH] = randint(0, 10)
	a_Teams[team][CONEMED]  = randint(0, 10)
	a_Teams[team][CONELOW]  = randint(0, 10)
	a_Teams[team][CONEMISS] = randint(0, 10)
	a_Teams[team][CUBEHIGH] = randint(0, 10)
	a_Teams[team][CUBEMED]  = randint(0, 10)
	a_Teams[team][CUBELOW]  = randint(0, 10)
	a_Teams[team][CUBEMISS] = randint(0, 10)

# Output the starting bounding JSON container
print("[")

# Lets generate 28 matches worth of random data for randomly selected teams.
# We will shuffle the a_Teams array each round and order them by the number of rounds played to
# try and make every team get the same number of matches.  Once we have that list we can create some
# random results.
for matchNum in range(29):
    # Shuffle the teams...
    shuffle( a_Teams )

    # Order them by the number of rounds...
    a_Teams.sort( key=lambda x: x[MATCHCOUNT] )
    
    # Grab the first 6 teams from the results of all that
    for team in range(6):
        # Bump the teams completed match / round count.
        a_Teams[team][MATCHCOUNT] += 1

        # Autonomous phase values
        autoMove     = randint( 0, 1 )

        autoConeHigh = randint( 0, 1 )
        autoConeMed  = randint( 0, 1 )
        autoConeLow  = randint( 0, 1 )
        autoConeMiss = randint( 0, 1 )

        autoCubeHigh = randint( 0, 1 )
        autoCubeMed  = randint( 0, 1 )
        autoCubeLow  = randint( 0, 1 )
        autoCubeMiss = randint( 0, 1 )

        autoChargeStation = randint( 0, 3 )

        # Teleop phase values
        telePark     = randint( 0, 1 )

        a_Teams[team][CONEHIGH] = calcNewScore( a_Teams[team][CONEHIGH], a_Teams[team][SCORECHANGEFACTOR], a_Teams[team][RANDOMIZEFACTOR] )
        a_Teams[team][CONEMED]  = calcNewScore( a_Teams[team][CONEMED], a_Teams[team][SCORECHANGEFACTOR], a_Teams[team][RANDOMIZEFACTOR] )
        a_Teams[team][CONELOW]  = calcNewScore( a_Teams[team][CONELOW], a_Teams[team][SCORECHANGEFACTOR], a_Teams[team][RANDOMIZEFACTOR] )
        a_Teams[team][CONEMISS] = calcNewScore( a_Teams[team][CONEMISS], a_Teams[team][SCORECHANGEFACTOR], a_Teams[team][RANDOMIZEFACTOR] )

        a_Teams[team][CUBEHIGH] = calcNewScore( a_Teams[team][CUBEHIGH], a_Teams[team][SCORECHANGEFACTOR], a_Teams[team][RANDOMIZEFACTOR] )
        a_Teams[team][CUBEMED]  = calcNewScore( a_Teams[team][CUBEMED], a_Teams[team][SCORECHANGEFACTOR], a_Teams[team][RANDOMIZEFACTOR] )
        a_Teams[team][CUBELOW]  = calcNewScore( a_Teams[team][CUBELOW], a_Teams[team][SCORECHANGEFACTOR], a_Teams[team][RANDOMIZEFACTOR] )
        a_Teams[team][CUBEMISS] = calcNewScore( a_Teams[team][CUBEMISS], a_Teams[team][SCORECHANGEFACTOR], a_Teams[team][RANDOMIZEFACTOR] )

        teleChargeStation = randint( 0, 3 )

        telePlayDefense   = randint( 0, 5 )
        teleHandleDefense = randint( 0, 5 )

        notes = "There were " + str( randint( 0, 20 ) ) + " people yelling this round." 
        # NOT going to try and get fancy with random secondary stats like carding, stopping, no show, etc

        matchResults = (
            f'"teamNumber":{a_Teams[team][TEAMNUM]},"matchNum":{matchNum},"autoMove":{autoMove},"autoChargeStation":{autoChargeStation},'
            f'"autoConeHigh":{autoConeHigh},"autoConeMed":{autoConeMed},"autoConeLow":{autoConeLow},"autoConeMiss":{autoConeMiss},'
            f'"autoCubeHigh":{autoCubeHigh},"autoCubeMed":{autoCubeMed},"autoCubeLow":{autoCubeLow},"autoCubeMiss":{autoCubeMiss},'
            f'"telePark":{telePark},"teleChargeStation":{teleChargeStation},'
            f'"teleConeHigh":{a_Teams[team][CONEHIGH]},"teleConeMed":{a_Teams[team][CONEMED]},"teleConeLow":{a_Teams[team][CONELOW]},"teleConeMiss":{a_Teams[team][CONEMISS]},'
            f'"teleCubeHigh":{a_Teams[team][CUBEHIGH]},"teleCubeMed":{a_Teams[team][CUBEMED]},"teleCubeLow":{a_Teams[team][CUBELOW]},"teleCubeMiss":{a_Teams[team][CUBEMISS]},'
			f'"card":0,"noShow":0,"stopped":0,"tipped":0,"died":0,"handleDefense":{telePlayDefense},"playDefense":{teleHandleDefense},'
			f'"notes":"{notes}"'
		)

        # Output the record as a jason object 
        print( "{" )
        print( matchResults )
        print( "}," )

# Finish the bounding JSON container
print("]")

