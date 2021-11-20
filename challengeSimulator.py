import random

def challengeSim(sampleSize, maxWins, maxLosses):
    playerList = [[i, 0, 0] for i in range(sampleSize)]
    playersLeft = list(range(sampleSize))
    totalMatches = 0
    queue = []
    while len(playersLeft) > maxWins:
        player = random.choice(playersLeft)
        playerStats = playerList[player]
        opponent = findOpponent(playerList[player], queue)
        if opponent == False:
            queue = insert(playerStats, queue)
        elif opponent[0] == player:
            pass #matching against themself
        else: #do a match
            winner = random.choice((player, opponent[0]))
            totalMatches += 1
            queue.remove(opponent)
            if winner == player: #update standings
                playerStats[1] += 1
                opponent[2] += 1
            else:
                opponent[1] += 1
                playerStats[2] +=1 
            if playerStats[1] == maxWins or playerStats[2] == maxLosses: 
                playersLeft.remove(player)
            if opponent[1] == maxWins or opponent[2] == maxLosses:
                playersLeft.remove(opponent[0])
    challengeWinners = [len(list(filter(lambda x: x[1] == i, playerList))) for i in range(maxWins + 1)]
    print(f"Total Matches: {totalMatches}")
    return challengeWinners

def insert(e, L):
    """inserts element e into sorted list L
    Used to add players into the queue"""
    if L == []:
        return [e]
    mid = len(L)//2
    if len(L) == 1:
        if e[1] > L[0][1]:
            return [L[0]] + [e]
        else:
            return [e] + [L[0]]
    if e[1] > L[mid][1]:
        return L[:mid] + insert(e, L[mid:])
    elif e[1] < L[mid][1]:
        return insert(e, L[:mid]) + L[mid:]
    else:
        return L[:mid] + [e] + L[mid:]

        
def findOpponent(player, queue):
    """return an opponent with the same number of wins as player. 
    Uses binary search to speed up the process
    Arguments:
    player: a list of 3 elements
    queue: A list of lists, each element being a player list"""
    if len(queue) == 0:
        return False
    elif len(queue) == 1:
        if player[1] == queue[0][1] or (player[1] > 15 and abs(queue[0][1] - player[1]) < 2): #2nd conditional speeds up mm past 15 wins. 
            return queue[0]
        else:
            return False
    mid = len(queue)//2
    if queue[mid][1] <= player[1]:
        return findOpponent(player, queue[mid:])
    else:
        return findOpponent(player, queue[:mid])

