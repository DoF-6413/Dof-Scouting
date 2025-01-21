# This is the first version of the random scouting  data creator for 2025s
# game.  It was based on RandomData2024C.  It still does NOT try to
# make data values that match when adding up things.
#
# The script DOES use some weighting to generate score increases/decreases
# between matches so we can see likely trends in Tableau or Plotly.

from random import randint, uniform, shuffle

# 2025 Scouting Data item indexes.  The first 5 will NEVER change because they
# are NOT game dependent.  Game specific values start at 6.  I'm using names
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
MATCHCOUNT = 6              # The number of matches we have created data for
PROCESSOR = 7               # (Teleop) Processor score count
PROCESSORMISS = 8           # (Teleop) Processor miss count
NET = 9                     # (Teleop) Net score count
NETMISS = 10                # (Teleop) Net miss count
L4 = 11                     # (Teleop) L4 score count
L4MISS = 12                 # (Teleop) L4 miss count
L3 = 13                     # (Teleop) L3 score count
L3MISS = 14                 # (Teleop) L3 miss count
L2 = 15                     # (Teleop) L2 score count
L2MISS = 16                 # (Teleop) L2 miss count
L1 = 17                     # (Teleop) L1 score count
L1MISS = 18                 # (Teleop) L1 miss count

# The actual team array
a_Teams = [
    # num  name                  ASCF    ARF     TSCF    TRF     MATCH...
    [60,   "Bulldogs",           -0.2,   0.1,    0.3,    0.4,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [498,  "Cobra Commanders",   0.7,    0.5,    2.1,    1.5,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [698,  "Hamilton Microbots", 2,      6,      -0.2,   0.3,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [991,  "BroncoBots",         -1,     0,      -1,     3,      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1165, "Team Paradise",      0.8,    2,      0.8,    1.1,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1212, "Sentinels",          -2,     1.5,    0.5,    1.6,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1726, "N.E.R.D.S.",         0.5,    2.1,    0.9,    4,      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2262, "RoboKrew",           0.4,    0.5,    0.76,   0.8,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2403, "Plasma",             0.5,    0.3,    1.8,    1.1,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2478, "Westwood",           1.2,    1,      1.2,    0.8,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2486, "CocoNuts",           1,      0,      2,      1.3,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3944, "All Knights",        0,      1,      0,      1.9,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4146, "Sabercats",          0.1,    4,      0.1,    0.7,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4183, "Bit Buckets",        0.2,    3,      0.2,    1.1,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [5539, "DVHS Cyborgs",       0.2,    0.8,    -0.2,   0.8,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6352, "LAUNCH TEAM",        0.5,    0.2,    0.5,    0.2,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6413, "Degrees of Freedom", 2,      1,      1.8,    2,      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6479, "AZTECH",             0.5,    0.6,    1.5,    0.6,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6656, "Ryu Botics",         0.76,   1.2,    0.75,   1,      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6833, "Phoenix",            -0.5,   0,      -0.5,   0.4,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8021, "Panther Robotics",   0.4,    2,      0.4,    0.8,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8087, "Cougar Pride",       0,      1,      0,      1,      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8848, "Blu CREW",           0.8,    2,      0.8,    0.7,    1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [9059, "COLTech",            0.6,    0.4,    0.7,    1,      1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
    a_Teams[team][PROCESSOR] = gamePieces
    a_Teams[team][PROCESSORMISS] = randint(0, 10 - gamePieces)
    gamePieces = randint(0, 9)
    a_Teams[team][NET] = gamePieces
    a_Teams[team][NETMISS] = randint(0, 10 - gamePieces)
    gamePieces = randint(0, 12)
    a_Teams[team][L4] = gamePieces
    a_Teams[team][L4MISS] = randint(0, 15 - gamePieces)
    gamePieces = randint(0, 12)
    a_Teams[team][L3] = gamePieces
    a_Teams[team][L3MISS] = randint(0, 15 - gamePieces)
    gamePieces = randint(0, 12)
    a_Teams[team][L2] = gamePieces
    a_Teams[team][L2MISS] = randint(0, 15 - gamePieces)
    gamePieces = randint(0, 20)
    a_Teams[team][L1] = gamePieces
    a_Teams[team][L1MISS] = randint(0, 25 - gamePieces)
    
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

        autoProcessor       = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoProcessorMiss   = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])

        autoNet             = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoNetMiss         = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])

        autoL4              = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoL4Miss          = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoL3              = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoL3Miss          = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoL2              = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoL2Miss          = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoL1              = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoL1Miss          = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])

        # Teleop phase values (SAVED in the team array)

        a_Teams[team][PROCESSOR]     = calcNewScore(a_Teams[team][PROCESSOR], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][PROCESSORMISS] = calcNewScore(a_Teams[team][PROCESSORMISS], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])

        a_Teams[team][NET]     = calcNewScore(a_Teams[team][NET], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][NETMISS] = calcNewScore(a_Teams[team][NETMISS], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])

        a_Teams[team][L4]      = calcNewScore(a_Teams[team][L4], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][L4MISS]  = calcNewScore(a_Teams[team][L4MISS], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][L3]      = calcNewScore(a_Teams[team][L3], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][L3MISS]  = calcNewScore(a_Teams[team][L3MISS], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][L2]      = calcNewScore(a_Teams[team][L2], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][L2MISS]  = calcNewScore(a_Teams[team][L2MISS], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][L1]      = calcNewScore(a_Teams[team][L1], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][L1MISS]  = calcNewScore(a_Teams[team][L1MISS], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])

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
