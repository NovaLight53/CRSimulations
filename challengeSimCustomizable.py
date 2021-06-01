#A way to simulate challenges and special challenges with and without pass royale
import random
import math
def createSkillList(sampleSize):
    skill = []
    while len(skill) < sampleSize:
        s = random.gauss(0.5, 0.1667) #Creates a normal distribution of player skill levels
        if s < 0 or s > 1:
            pass
        else:
            skill.append(s)    
    return skill

def createSkillListEven(sampleSize):
    skill = []
    while len(skill) < sampleSize:
        s = random.random() #Creates an even distribution of player skill levels
        if s < 0 or s > 1:
            pass
        else:
            skill.append(s)    
    return skill

def createPlayers(sampleSize, passPercent, distribution):
    """ creates a player pool of sampleSize players with distributed skill levels. 
    Each player is represented by a list in the form [Skill lvl, # of wins, # of losses, passRoyale(T/F)]"""
    if distribution == 'gauss':
        skill = createSkillList(sampleSize)
    elif distribution == 'even':
        skill = createSkillListEven(sampleSize)
    else:
        return 'Incorrect Distribution'
    cutoff = int(sampleSize - sampleSize*passPercent)
    playerD = {}#this will be a dict with sampleSize keys
    for i in range(cutoff): #players without the pass
        playerD[i] = [skill[i], 0, 0, False]
    for j in list(range(cutoff, sampleSize)): # players who have the pass
        playerD[j] = [skill[j], 0, 0, True]
    return playerD
    
def createLowPlayers(sampleSize, passPercent, meanskill):
    """creates a list of players with meanSkill as the average skill of a pass royale player"""
    numPasses = int(0.5*sampleSize * passPercent) 
    playerD = {}
    skill = sorted(createSkillList(sampleSize))
    for i in range(sampleSize):
        playerD[i] = [skill[i], 0, 0, False] #nobody gets the pass initially
    skillFromMean = [abs(i - meanskill)for i in skill ]
    closest = min(skillFromMean)
    avgPass = skillFromMean.index(closest)
    for player in range(avgPass-numPasses, avgPass + numPasses):
        playerD[player][3] = True
        
    return playerD

def getSkillPass(playerD, numPasses):
    skill = 0
    for i in playerD:
        if playerD[i][3] == True:
            skill += playerD[i][0]

    return skill/numPasses
def updateDicts(a, b, playerD, winner):
    if winner == a:
        playerD[a][1] += 1
        playerD[b][2] += 1
    else:
        playerD[a][2] +=1
        playerD[b][1] += 1

def match(a, b, playerD):
    """takes in two players in the form of numbers and updates the player dictionary. """
    if abs(a-b) < 0.1: #if the players are close in skill, the game is a 50/50 
        if random.random < 0.5:
            updateDicts(a, b, playerD, a)
        else:
            updateDicts(a, b, playerD, b)
    chanceOfA = (playerD[a][0]**2)/((playerD[a][0])**2+ (playerD[b][0])**2) #how I determine who wins the match
    if random.random() < chanceOfA:
        updateDicts(a, b, playerD, a)
    else:
        updateDicts(a, b, playerD, b)

def matchmaking(a, b, playerD):
    if abs(playerD[a][1] - playerD[b][1]) <3: #The players have to be somewhat close in wins to be matched with each other
        return True
    else:
        return False
def simulation(sampleSize, passPercent, numWins, distribution):
    """performs a simulation of a challenge with a specific sample size, a percentage of players with a pass and the number of wins required to finish."""
    playerD = createPlayers(sampleSize, passPercent, distribution)
    playersLeft = list(range(sampleSize))
    matches = 0 
    while len(playersLeft) > numWins//3 + 1:     
        a = random.sample(playersLeft, 2)
        if matchmaking(a[0], a[1], playerD) == True:
            matches += 1
            match(a[0], a[1], playerD)
            if playerD[a[0]][1] == numWins or (playerD[a[0]][2] == 3 and playerD[a[0]][3] == False): #if they have 3 losses and no pass == out. If they have enough wins, also out
                playersLeft.remove(a[0])
            if playerD[a[1]][1] == numWins or (playerD[a[1]][2] == 3 and playerD[a[1]][3] == False): #the number of losses can be changed to 5 to simulate global tournaments
                playersLeft.remove(a[1])
            pass
        else:
            pass 
    winsDict = {}
    for i in range(numWins+1):
        winsDict[i] =  len([playerD[player][0] for player in playerD if (playerD[player][1] == i and playerD[player][3] == False)])
    withPass = [playerD[player][0] for player in playerD if playerD[player][1] == numWins]
    withoutPass = [playerD[player][0] for player in playerD if (playerD[player][1] == numWins and playerD[player][3] == False)]
    #print("Matches Played:", matches) #Displays the total number of matches that were played
    #print(winsDict) # this prints out the number of players who finish with a certain amount of wins
    #return sum(withoutPass)/len(withoutPass),len(withoutPass)/sampleSize*(1-passPercent)
    try: 
        results = 100*(sum(withoutPass)/len(withoutPass)), len(withoutPass), 100*(len(withoutPass)/(sampleSize*(1-passPercent))) #Tuple with skill level of players who completed the challenge with and without the pass. 
        return results
    except  ZeroDivisionError as error:
        return 'No Completions'


def simPassSkill(sampleSize, passPercent, numWins, meanSkill):
    """Adjusting the skill level of pass players. Mean skill is the avg skill of a pass royale player. """
    playerD = createLowPlayers(sampleSize, passPercent, meanSkill)
    playersLeft = list(range(sampleSize))
    matches = 0 
    while len(playersLeft) > numWins//3 + 1:     
        a = random.sample(playersLeft, 2)
        if matchmaking(a[0], a[1], playerD) == True:
            matches += 1
            match(a[0], a[1], playerD)
            if playerD[a[0]][1] == numWins or (playerD[a[0]][2] == 3 and playerD[a[0]][3] == False): #if they have 3 losses and no pass == out. If they have enough wins, also out
                playersLeft.remove(a[0])
            if playerD[a[1]][1] == numWins or (playerD[a[1]][2] == 3 and playerD[a[1]][3] == False): #the number of losses can be changed to 5 to simulate global tournaments
                playersLeft.remove(a[1])
            pass
        else:
            pass 
    #winsDict = {}
    #for i in range(numWins+1):
    #    winsDict[i] =  len([playerD[player][0] for player in playerD if (playerD[player][1] == i and playerD[player][3] == False)])
    #withPass = [playerD[player][0] for player in playerD if playerD[player][1] == numWins]
    withoutPass = [playerD[player][0] for player in playerD if (playerD[player][1] == numWins and playerD[player][3] == False)]
    #print("Matches Played:", matches) #Displays the total number of matches that were played
    #print(winsDict) # this prints out the number of players who finish with a certain amount of wins
    return sum(withoutPass)/len(withoutPass),len(withoutPass)/(sampleSize*(1-passPercent))
    
