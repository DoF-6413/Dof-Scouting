from random import *

# NOTE: This Quick & Dirty Python script does NOT try to make data values that match when
# adding up things like pieces scored & movement vs "match score" that CoConuts tracked
# The script does use have some weighting to factor in how to trend scaling of some data
# but it does not try to make it all be consistent.  That can be done later if we really
# need it.

# Index names to make the code easier to follow

TEAMNUM = 0
TEAMNAME = 1
SCORECHANGEFACTOR = 2
RANDOMIZEFACTOR = 3
LASTMATCHSCORE = 4
MATCHCOUNT = 5

# The teams array is made up of several lists that encode match data and other info we need to create 
# trending data to visualize.  Each list looks like this:
#
# [ team_number, team_name, high_goal_score_change_over_time, randomize, last_score, rounds ]
#
# That is because the CoConuts only track a final match score per match and NOTHING else!  If we want
# more later, we have to make adjustments.  That is why I at least use index names to make the script
# readable and more flexible.
a_Teams = [
    [1234, "lions",     0.1,    0,      0, 0],
    [2345, "tigers",    1.2,    0.5,    0, 0],
    [3456, "bears",     -0.2,   0.5,    0, 0],
    [4567, "wizards",   2,      1,      0, 0],
    [5678, "eagles",    0.5,    0.2,    0, 0],
    [6789, "falcons",   0.1,    4,      0, 0],
    [7890, "cheese",    -0.5,   1,      0, 0],
    [1324, "lime",      -0.5,   0,      0, 0],
    [2435, "orange",    -1,     0,      0, 0],
    [3546, "oregano",   1,      0,      0, 0],
    [4657, "newbies",   0,      3,      0, 0],
    [5768, "gears",     0.4,    5,      0, 0],
    [6879, "wires",     -2,     3,      0, 0],
    [7980, "cogs",      1.2,    1,      0, 0],
    [1345, "sprockets", 0.8,    2,      0, 0],
    [2456, "squirrels", 0.5,    8,      0, 0],
    [3567, "dogs",      2,      6,      0, 0],
    [4678, "cats",      0.8,    2,      0, 0],
    [5555, "pigs",      0.2,    3,      0, 0],
    [6666, "parrots",   0.76,   1.2,    0, 0],
    [7777, "seeds",     0,      1,      0, 0] 
    ]

# Assign random "last_score" to each team
# TODO: Do we need to do this so the script later wont die due to a value of 0??
# for team in range(21):
# 	a_Teams[team][LASTMATCHSCORE] = randint(0, 20)

# Output the starting bounding JSON container
print("{")

# Lets generate 28 matches worth of random data for randomly selected teams.
# We will shuffle the a_Teams array each round and order them by the number of rounds played to
# try and make every team get the same number of matches.  Once we have that list we can create some
# random results.
for round in range(29):
    # Shuffle the teams...
    shuffle( a_Teams )

    # Order them by the number of rounds...
    a_Teams.sort( key=lambda x: x[MATCHCOUNT] )
    
    # Grab the first 6 teams from the results of all that
    for team in range(6):
        # Bump the teams completed match / round count.
        a_Teams[team][MATCHCOUNT] += 1

        # Calculate a random decrease or increase amount for adjusting the teams match score
        # using previous matches value as a starting point.
        # increase = a_Teams[team][SCORECHANGEFACTOR] + randint( a_Teams[team][RANDOMIZEFACTOR] * -1, a_Teams[team][RANDOMIZEFACTOR] )

        # # Make the teams current match score based by that factor and their last match score.
        # a_Teams[team][LASTMATCHSCORE] = round( a_Teams[team][LASTMATCHSCORE] + increase, 0 )
        # # Make sure no team gets a negative score
        # if a_Teams[team][LASTMATCHSCORE] < 0:
        #     a_Teams[team][LASTMATCHSCORE] = 0

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

        teleConeHigh = randint( 0, 10 )
        teleConeMed  = randint( 0, 10 )
        teleConeLow  = randint( 0, 10 )
        teleConeMiss = randint( 0, 10 )

        teleCubeHigh = randint( 0, 5 )
        teleCubeMed  = randint( 0, 5 )
        teleCubeLow  = randint( 0, 5 )
        teleCubeMiss = randint( 0, 5 )

        teleChargeStation = randint( 0, 3 )

        telePlayDefense   = randint( 0, 5 )
        teleHandleDefense = randint( 0, 5 )

        notes = "There were " + str( randint( 0, 20 ) ) + " peopole yelling this round." 
        # NOT going to try and get fancy with random secondary stats like carding, stopping, no show, etc

        matchResults = (
            f'teamNumber:{a_Teams[team][TEAMNUM]},matchNum:{round},autoMove:{autoMove},autoChargeStation:{autoChargeStation},'
            f'autoConeHigh:{autoConeHigh},autoConeMed:{autoConeMed},autoConeLow:{autoConeLow},autoConeMiss:{autoConeMiss},'
            f'autoCubeHigh:{autoCubeHigh},autoCubeMed:{autoCubeMed},autoCubeLow:{autoCubeLow},autoCubeMiss:{autoCubeMiss},'
            f'telePark:{telePark},teleChargeStation:{teleChargeStation},'
            f'teleConeHigh:{teleConeHigh},teleConeMed:{teleConeMed},teleConeLow:{teleConeLow},teleConeMiss:{teleConeMiss},'
            f'teleCubeHigh:{teleCubeHigh},teleCubeMed:{teleCubeMed},teleCubeLow:{teleCubeLow},teleCubeMiss:{teleCubeMiss},'
			f'card:0,noShow:0,stopped:0,tipped:0,died:0,handleDefense:0,playDefense:0,'
			f'notes:"{notes}"'
		)

        # Output the record as a jason object 
        print( "{" )
        print( matchResults )
        print( "}," )

# Finish the bounding JSON container
print("}")

