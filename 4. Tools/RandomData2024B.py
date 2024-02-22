# This is the first version of the requested random test data creator for 2024s
# game.  It is a simple update to the RandomData3.py file and still should be
# considered a Less Quick & Dirty Python script as it still does NOT try to
# make data values that match when adding up things.
#
# This is an updated version of RandomData2024A.py which uses the 'encoded'
# key values instead of the MongoDB keys.  That way the data can be piped into
# the scouting script that checks data and puts it into the database.
# In addition I fixed a the default compLevel value to be 'qm', not 'q'
#
# The script DOES use some weighting to generate score increases/decreases
# between matches so we can see likely trends in Tableau or Plotly.

from random import randint, uniform, shuffle

# 2024 Scouting Data item indexes.  The first 5 will NEVER change because they
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
AMP = 7                     # Amp score count
AMPMISS = 8                 # Amp miss count
SPEAKERCLOSE = 9            # Speaker close score count
SPEAKERNOTCLOSE = 10        # Speaker not close score count
SPEAKERMISS = 11            # Speaker miss count

# The actual team array
a_Teams = [
    # num  name                  ASCF    ARF     TSCF    TRF     MATCH...
    [60,   "Bulldogs",           -0.2,   0.1,    0.3,    0.4,    1, 0, 0, 0, 0, 0],
    [498,  "Cobra Commanders",   0.7,    0.5,    2.1,    1.5,    1, 0, 0, 0, 0, 0],
    [698,  "Hamilton Microbots", 2,      6,      -0.2,   0.3,    1, 0, 0, 0, 0, 0],
    [991,  "BroncoBots",         -1,     0,      -1,     3,      1, 0, 0, 0, 0, 0],
    [1165, "Team Paradise",      0.8,    2,      0.8,    1.1,    1, 0, 0, 0, 0, 0],
    [1212, "Sentinels",          -2,     1.5,    0.5,    1.6,    1, 0, 0, 0, 0, 0],
    [1726, "N.E.R.D.S.",         0.5,    2.1,    0.9,    4,      1, 0, 0, 0, 0, 0],
    [2262, "RoboKrew",           0.4,    0.5,    0.76,   0.8,    1, 0, 0, 0, 0, 0],
    [2403, "Plasma",             0.5,    0.3,    1.8,    1.1,    1, 0, 0, 0, 0, 0],
    [2478, "Westwood",           1.2,    1,      1.2,    0.8,    1, 0, 0, 0, 0, 0],
    [2486, "CocoNuts",           1,      0,      2,      1.3,    1, 0, 0, 0, 0, 0],
    [3944, "All Knights",        0,      1,      0,      1.9,    1, 0, 0, 0, 0, 0],
    [4146, "Sabercats",          0.1,    4,      0.1,    0.7,    1, 0, 0, 0, 0, 0],
    [4183, "Bit Buckets",        0.2,    3,      0.2,    1.1,    1, 0, 0, 0, 0, 0],
    [5539, "DVHS Cyborgs",       0.2,    0.8,    -0.2,   0.8,    1, 0, 0, 0, 0, 0],
    [6352, "LAUNCH TEAM",        0.5,    0.2,    0.5,    0.2,    1, 0, 0, 0, 0, 0],
    [6413, "Degrees of Freedom", 2,      1,      1.8,    2,      1, 0, 0, 0, 0, 0],
    [6479, "AZTECH",             0.5,    0.6,    1.5,    0.6,    1, 0, 0, 0, 0, 0],
    [6656, "Ryu Botics",         0.76,   1.2,    0.75,   1,      1, 0, 0, 0, 0, 0],
    [6833, "Phoenix",            -0.5,   0,      -0.5,   0.4,    1, 0, 0, 0, 0, 0],
    [8021, "Panther Robotics",   0.4,    2,      0.4,    0.8,    1, 0, 0, 0, 0, 0],
    [8087, "Cougar Pride",       0,      1,      0,      1,      1, 0, 0, 0, 0, 0],
    [8848, "Blu CREW",           0.8,    2,      0.8,    0.7,    1, 0, 0, 0, 0, 0],
    [9059, "COLTech",            0.6,    0.4,    0.7,    1,      1, 0, 0, 0, 0, 0]
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
    # print(f"scf:{scoreChangeFactor}, rf:{randomizeFactor}")
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
    a_Teams[team][AMP] = randint(0, 10)
    a_Teams[team][AMPMISS] = randint(0, 5)
    a_Teams[team][SPEAKERCLOSE] = randint(0, 10)
    a_Teams[team][SPEAKERNOTCLOSE] = randint(0, 10)
    a_Teams[team][SPEAKERMISS] = randint(0, 5)

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
        # Bump the teams completed match / round count.
        a_Teams[team][MATCHCOUNT] += 1

        # Autonomous phase values (NOT saved in the team array)
        autoMove            = randint(0, 1)

        autoAmp             = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoAmpMiss         = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])

        autoSpeakerClose    = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoSpeakerNotClose = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])
        autoSpeakerMiss     = calcNewScore(randint(0, 1), a_Teams[team][AUTOSCORECHANGEFACTOR], a_Teams[team][AUTORANDOMIZEFACTOR])

        # Teleop phase values (SAVED in the team array)
        a_Teams[team][AMP]     = calcNewScore(a_Teams[team][AMP], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][AMPMISS] = calcNewScore(a_Teams[team][AMPMISS], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])

        a_Teams[team][SPEAKERCLOSE]    = calcNewScore(a_Teams[team][SPEAKERCLOSE], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][SPEAKERNOTCLOSE] = calcNewScore(a_Teams[team][SPEAKERNOTCLOSE], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])
        a_Teams[team][SPEAKERMISS]     = calcNewScore(a_Teams[team][SPEAKERMISS], a_Teams[team][TELESCORECHANGEFACTOR], a_Teams[team][TELERANDOMIZEFACTOR])

        # End game phase values (NOT saved in the team array)
        telePark        = randint(0, 1)
        teleClimb       = 0 if telePark else randint(0, 4)
        teleTrap        = 0 if telePark else randint(0, 3)
        teleTrapMiss    = 0 if telePark else randint(0, 4)
        teleMic         = randint(0, 3)
        teleMicMiss     = randint(0, 3)
        teleDriverSkill = randint(0, 5)

        comments = "There were " + str(randint(0, 20)) + " people yelling this round."
        # NOT going to try and get fancy with random secondary stats like carding, stopping, no show, etc

        matchResults = (
            f'"key":{a_Teams[team][TEAMNUM]},"mn":{matchNum},"cl":"qm","i":"Python","l":{autoMove},'
            f'"a1":{autoSpeakerClose},"a2":{autoSpeakerNotClose},"a3":{autoSpeakerMiss},'
            f'"a4":{autoAmp},"a5":{autoAmpMiss},'
            f'"t1":{a_Teams[team][SPEAKERCLOSE]},"t2":{a_Teams[team][SPEAKERNOTCLOSE]},"t3":{a_Teams[team][SPEAKERMISS]},'
            f'"t4":{a_Teams[team][AMP]},"t5":{a_Teams[team][AMPMISS]},'
            f'"p":{telePark},"t6":{teleClimb},"t7":{teleTrap},"t8":{teleTrapMiss},'
            f'"m":{teleMic},"mm":{teleMicMiss},'
            f'"c":0,"ns":0,"d":0,"do":0,"ds":{teleDriverSkill},'
            f'"co":"{comments}"'
            )

        # Output the record as a JSON object
        print("{")
        print(matchResults)
        print("},")

# Finish the bounding JSON container
print("]")
