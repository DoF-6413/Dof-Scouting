# This is the second version of the random scouting data creator for 2025s
# game.  It was based on RandomData2025A.  Changes include:
#
# 1: Adding the ability to control which reef levels can be scored in Auto
#        and Teleop.
# 2: Updated index descriptions to be correct.
#
# The script DOES use some weighting to generate score increases/decreases
# between matches so we can see likely trends in Tableau or Plotly.

from random import randint, uniform, shuffle

# 2025 Scouting Data item indexes.  The first 6 will NEVER change because they
# are NOT game dependent.  Game specific values start at 7.  I'm using names
# to make the code easier to follow.
#
# The teams array is made up of several lists that encode match data and other
# info we need to create trending data to visualize.  Each list is made up of
# the following data values:

TEAMNUM = 0                 # The team number
TEAMNAME = 1                # The team name (UNUSED)
AUTOSCORECHANGEFACTOR = 2   # The auto scoring change over time factor
AUTORANDOMIZEFACTOR = 3     # The auto randomization factor for each round
TELESCORECHANGEFACTOR = 4   # The teleop scoring change over time factor
TELERANDOMIZEFACTOR = 5     # The teleop randomization factor for each round
CANAUTOPROCESSOR = 6        # (Auto) The robot can score in the processor
CANTELEPROCESSOR = 7        # (Teleop) The robot can score in the processor
CANAUTONET = 8              # (Auto) The robot can score in the net
CANTELENET = 9              # (Teleop) The robot can score in the net
CANAUTOL4 = 10              # (Auto) The robot can score in L4
CANTELEL4 = 11              # (Teleop) The robot can score in L4
CANAUTOL3 = 12              # (Auto) The robot can score in L3
CANTELEL3 = 13              # (Teleop) The robot can score in L3
CANAUTOL2 = 14              # (Auto) The robot can score in L2
CANTELEL2 = 15              # (Teleop) The robot can score in L2
CANAUTOL1 = 16              # (Auto) The robot can score in L1
CANTELEL1 = 17              # (Teleop) The robot can score in L1
MATCHCOUNT = 18             # The number of matches we have created data for
PROCESSOR = 19              # (Teleop) Processor score count
PROCESSORMISS = 20          # (Teleop) Processor miss count
NET = 21                    # (Teleop) Net score count
NETMISS = 22                # (Teleop) Net miss count
L4 = 23                     # (Teleop) L4 score count
L4MISS = 24                 # (Teleop) L4 miss count
L3 = 25                     # (Teleop) L3 score count
L3MISS = 26                 # (Teleop) L3 miss count
L2 = 27                     # (Teleop) L2 score count
L2MISS = 28                 # (Teleop) L2 miss count
L1 = 29                     # (Teleop) L1 score count
L1MISS = 30                 # (Teleop) L1 miss count


# The actual team array
a_Teams = [
    # num  name                  ASCF    ARF     TSCF    TRF     CAP...                                                                             MATCH...
    [60,   "Bulldogs",           -0.2,   0.1,    0.3,    0.4,    False, True, False, False, False, False, False, True, False, True, False, True,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [498,  "Cobra Commanders",   0.7,    0.5,    2.1,    1.5,    True, True, False, True, True, True, True, True, True, True, True, True,           1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [698,  "Hamilton Microbots", 2,      6,      -0.2,   0.3,    False, True, False, False, False, False, False, True, False, True, False, True,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [991,  "BroncoBots",         -1,     0,      -1,     3,      False, True, False, False, False, False, False, False, False, True, False, True,   1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1165, "Team Paradise",      0.8,    2,      0.8,    1.1,    False, False, False, False, False, False, False, False, False, False, False, True, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1212, "Sentinels",          -2,     1.5,    0.5,    1.6,    False, False, False, False, False, False, False, True, False, True, False, True,   1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1726, "N.E.R.D.S.",         0.5,    2.1,    0.9,    4,      False, True, False, False, False, False, False, True, False, True, True, True,     1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2262, "RoboKrew",           0.4,    0.5,    0.76,   0.8,    False, False, False, False, False, False, False, True, False, True, False, True,   1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2403, "Plasma",             0.5,    0.3,    1.8,    1.1,    True, True, False, True, True, True, True, True, True, True, True, True,           1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2478, "Westwood",           1.2,    1,      1.2,    0.8,    False, True, False, True, False, False, False, True, False, True, True, True,      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2486, "CocoNuts",           1,      0,      2,      1.3,    True, True, False, True, True, True, True, True, True, True, True, True,           1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3944, "All Knights",        0,      1,      0,      1.9,    False, False, False, False, False, False, False, True, False, True, False, True,   1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4146, "Sabercats",          0.1,    4,      0.1,    0.7,    False, False, False, False, False, False, False, True, False, True, False, True,   1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4183, "Bit Buckets",        0.2,    3,      0.2,    1.1,    False, True, False, False, False, True, False, True, False, True, True, True,      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5539, "DVHS Cyborgs",       0.2,    0.8,    -0.2,   0.8,    False, False, False, False, False, False, False, True, False, True, False, True,   1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6352, "LAUNCH TEAM",        0.5,    0.2,    0.5,    0.2,    False, True, False, False, False, False, False, True, False, True, False, True,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6413, "Degrees of Freedom", 2,      1,      1.8,    2,      True, True, False, True, True, True, True, True, True, True, True, True,           1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6479, "AZTECH",             0.5,    0.6,    1.5,    0.6,    False, True, False, True, False, True, False, True, False, True, True, True,       1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6656, "Ryu Botics",         0.76,   1.2,    0.75,   1,      False, False, False, False, False, False, False, False, False, True, False, True,  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6833, "Phoenix",            -0.5,   0,      -0.5,   0.4,    False, False, False, False, False, False, False, False, False, True, False, True,  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8021, "Panther Robotics",   0.4,    2,      0.4,    0.8,    False, False, False, False, False, False, False, False, False, False, False, True, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8087, "Cougar Pride",       0,      1,      0,      1,      False, False, False, False, False, False, False, False, False, False, False, True, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8848, "Blu CREW",           0.8,    2,      0.8,    0.7,    False, True, False, False, False, False, False, False, False, False, False, True,  1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [9059, "COLTech",            0.6,    0.4,    0.7,    1,      False, False, False, False, False, False, False, True, False, True, False, True,   1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]


def calcNewScore(currentScore: float, scoreChangeFactor: float, randomizeFactor: float) -> int:
    """
    Calculate a new score based on the current score, score change factor,
    and randomize factor.

    Args:
        currentScore (float): The current score.
        scoreChangeFactor (float): The factor by which the score should change.
        randomizeFactor (float): The factor by which the score change should be randomized.

    Returns:
        float: The new score.
    """
    # Calculate a random decrease or increase amount for adjusting the score
    # using previous value as a starting point.
    increase = scoreChangeFactor + uniform(randomizeFactor * -1, randomizeFactor)

    # Update the score with the random increase/decrease amount
    newScore = round(currentScore + increase, 0)

    # Make sure there is no negative score
    if newScore < 0:
        newScore = 0

    return int(newScore)


# Preassign random scores to each team so we have a starting point for
# increases/decreases
for team in range(len(a_Teams)):
    gamePieces = randint(0, 9)
    a_Teams[team][PROCESSOR] =  0 if not a_Teams[team][CANTELEPROCESSOR] else gamePieces
    a_Teams[team][PROCESSORMISS] = 0 if not a_Teams[team][CANTELEPROCESSOR] else randint(0, 10 - gamePieces)
    gamePieces = randint(0, 9)
    a_Teams[team][NET] =  0 if not a_Teams[team][CANTELENET] else gamePieces
    a_Teams[team][NETMISS] = 0 if not a_Teams[team][CANTELENET] else randint(0, 10 - gamePieces)
    gamePieces = randint(0, 12)
    a_Teams[team][L4] = 0 if not a_Teams[team][CANTELEL4] else gamePieces
    a_Teams[team][L4MISS] = 0 if not a_Teams[team][CANTELEL4] else randint(0, 15 - gamePieces)
    gamePieces = randint(0, 12)
    a_Teams[team][L3] = 0 if not a_Teams[team][CANTELEL3] else gamePieces
    a_Teams[team][L3MISS] = 0 if not a_Teams[team][CANTELEL3] else randint(0, 15 - gamePieces)
    gamePieces = randint(0, 12)
    a_Teams[team][L2] = 0 if not a_Teams[team][CANTELEL2] else gamePieces
    a_Teams[team][L2MISS] = 0 if not a_Teams[team][CANTELEL2] else randint(0, 15 - gamePieces)
    gamePieces = randint(0, 20)
    a_Teams[team][L1] = 0 if not a_Teams[team][CANTELEL1] else gamePieces
    a_Teams[team][L1MISS] = 0 if not a_Teams[team][CANTELEL1] else randint(0, 25 - gamePieces)
    
# Output the starting bounding JSON container
print("[")

# Lets generate 40 matches worth of random data for randomly selected teams.
# We will shuffle the a_Teams array each round and order them by the number of
# rounds played to try and make every team get the same number of matches.
# Once we have that list we can create some random results.
for matchNum in range(1, 41):
    # Shuffle the teams...
    shuffle(a_Teams)

    # Order them by the number of rounds...
    a_Teams.sort(key=lambda x: x[MATCHCOUNT])

    # Grab the first 6 teams from the results of all that
    for team in range(6):
        # Bump the teams completed match count.
        a_Teams[team][MATCHCOUNT] += 1

        # Autonomous phase values (NOT saved in the team array)

        autoProcessor       = 0 if not a_Teams[team][CANAUTOPROCESSOR] else calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoProcessorMiss   = 0 if not a_Teams[team][CANAUTOPROCESSOR] else calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])

        autoNet             = 0 if not a_Teams[team][CANAUTONET] else calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoNetMiss         = 0 if not a_Teams[team][CANAUTONET] else calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])

        autoL4              = 0 if not a_Teams[team][CANAUTOL4] else calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoL4Miss          = 0 if not a_Teams[team][CANAUTOL4] else calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoL3              = 0 if not a_Teams[team][CANAUTOL3] else calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoL3Miss          = 0 if not a_Teams[team][CANAUTOL3] else calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoL2              = 0 if not a_Teams[team][CANAUTOL2] else calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoL2Miss          = 0 if not a_Teams[team][CANAUTOL2] else calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoL1              = 0 if not a_Teams[team][CANAUTOL1] else calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoL1Miss          = 0 if not a_Teams[team][CANAUTOL1] else calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])

        # Teleop phase values (SAVED in the team array)

        a_Teams[team][PROCESSOR]     = 0 if not a_Teams[team][CANTELEPROCESSOR] else calcNewScore(a_Teams[team][PROCESSOR], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][PROCESSORMISS] = 0 if not a_Teams[team][CANTELEPROCESSOR] else calcNewScore(a_Teams[team][PROCESSORMISS], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])

        a_Teams[team][NET]     = 0 if not a_Teams[team][CANTELENET] else calcNewScore(a_Teams[team][NET], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][NETMISS] = 0 if not a_Teams[team][CANTELENET] else calcNewScore(a_Teams[team][NETMISS], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])

        a_Teams[team][L4]      = 0 if not a_Teams[team][CANTELEL4] else calcNewScore(a_Teams[team][L4], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][L4MISS]  = 0 if not a_Teams[team][CANTELEL4] else calcNewScore(a_Teams[team][L4MISS], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][L3]      = 0 if not a_Teams[team][CANTELEL3] else calcNewScore(a_Teams[team][L3], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][L3MISS]  = 0 if not a_Teams[team][CANTELEL3] else calcNewScore(a_Teams[team][L3MISS], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][L2]      = 0 if not a_Teams[team][CANTELEL2] else calcNewScore(a_Teams[team][L2], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][L2MISS]  = 0 if not a_Teams[team][CANTELEL2] else calcNewScore(a_Teams[team][L2MISS], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][L1]      = 0 if not a_Teams[team][CANTELEL1] else calcNewScore(a_Teams[team][L1], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][L1MISS]  = 0 if not a_Teams[team][CANTELEL1] else calcNewScore(a_Teams[team][L1MISS], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])

        # End game phase values (NOT saved in the team array)

        telePark        = randint(0, 1)
        teleClimb       = 0 if telePark else randint(0, 4)

        comments = "There were " + str(randint(0, 20)) + " people yelling this match."

        # NOT going to try and get fancy with random secondary stats like carding, stopping, no show, etc

        matchResults = (
            f'"key":{a_Teams[team][TEAMNUM]},"mn":{matchNum},"cl":"qm","i":"Python",'
            f'"a1":{autoL4},"a2":{autoL4Miss},"a3":{autoL3},"a4":{autoL3Miss},'
            f'"a5":{autoL2},"a6":{autoL2Miss},"a7":{autoL1},"a8":{autoL1Miss},'
            f'"a9":{autoNet},"a10":{autoNetMiss},"a11":{autoProcessor},"a12":{autoProcessorMiss},'
            f'"t1":{a_Teams[team][L4]},"t2":{a_Teams[team][L4MISS]},'
            f'"t3":{a_Teams[team][L3]},"t4":{a_Teams[team][L3MISS]},'
            f'"t5":{a_Teams[team][L2]},"t6":{a_Teams[team][L2MISS]},'
            f'"t7":{a_Teams[team][L1]},"t8":{a_Teams[team][L1MISS]},'
            f'"t9":{a_Teams[team][NET]},"t10":{a_Teams[team][NETMISS]},'
            f'"t11":{a_Teams[team][PROCESSOR]},"t12":{a_Teams[team][PROCESSORMISS]},'
            f'"c":{teleClimb},"ns":0,"d":0,"r":0,'
            f'"co":"{comments}"'
            )

        # Output the record as a JSON object
        print("{")
        print(matchResults)
        print("},")

# Finish the bounding JSON container
print("]")
