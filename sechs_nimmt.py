"""
# Description

6 Nimmt is a German game invented in 1994. This program is a simulation of that game. The simulation is run N number of times to determine the best strategy among a combination of strategies.

So far, only simple strategies were simulated, namely RND (the player chooses a random card), LARG (the player always chooses the largest card), SMA (the player always chooses the smallest card).


# Results
Even with these simple strategies, the chance of winning is not always straightforward to deduce. With only 2 players, it looks like a random strategy is the best of the three. With 3 or more players, it seems that LARG often takes the upper hand, provided another player is also playing LARG, thus the strategies reinforce each other. Otherwise, SMA takes the upper hand. Not all possible number of players and combinations have been simulated.

# Future development
It is not my intention to recreate the game for the purpose of playing, an endeavor that would require building a GUI, and potentially hosting the game app on a server. Someone has already beat me to it anyway. Instead, I am merely interested in different strategies and how they fair against each other. I would be also interested to learn about the underlying mathematics that could explain the results.

Next, I will be working on simulating more elaborate strategies that are closer to how real players would approach the game.
"""

from random import randint
import sys

#Constants
MAX_VALUE = 104 #maximum value of a card

MAX_PLAYERS = 10 #maximum number of players

GAME_LENGTH = 10 #maximum number of cards each player gets, which determines the length of the game (one card is played per round)

STACK_NUM = 4 #number of cards in the middle stack

STRATS = ['SMA','LARG','CL_SMA','SMA_LARG','LARG_SMA','RND','PNT_LARG'] #list of strategies


def get_player_card(stack,player_k_cards,strategy):
    """
    Returns a card from a player's deck, based on his strategy,
    and what is available in the stack (if the strategy takes
    the stack into consideration).
    """
    if strategy == 'SMA':
        
        card = min(player_k_cards)
        
    elif strategy == 'LARG':
        
        card = max(player_k_cards)
        
    elif strategy == 'LARG_SMA':
        
        if len(player_k_cards) <= GAME_LENGTH//2:
            
            card = max(player_k_cards)
            
        else:
            
            card = min(player_k_cards)
            
    elif strategy == 'SMA_LARG':
        
        if len(player_k_cards) <= GAME_LENGTH//2:
            
            card = min(player_k_cards)
            
        else:
            
            card = max(player_k_cards)
    else: #RND
        
        card = player_k_cards[randint(0,len(player_k_cards)-1)]

    player_k_cards.remove(card)

    return card

def get_stack_index(stack,card):
    """
    Get the placement index on the stack
    where the next card has to be added.

    Returns None if no such placement is
    found.
    """
    min_diff = 200
    stack_index = -1
    for i in range(len(stack)):
        if stack[i][-1] < card:
            diff = card - stack[i][-1]
            if diff < min_diff:
                min_diff = diff
                stack_index = i

    if min_diff == 200:
        return None

    return stack_index

def get_point_sum(cards,card_list):
    """
    Returns the sum of the points in a card list.
    """
    point_sum = 0
    for card in card_list:
        point_sum += cards[card]

    return point_sum

def get_lowest_point_stack(cards,stack):
    """
    Returns the placement index on the stack
    where the sum of points is the lowest.
    """
    lowest_points = 100
    lowest_point_index = -1
    for i in range(len(stack)):
        point_sum = get_point_sum(cards,stack[i])
        """
        for card in stack[i]:
            point_sum += cards[card]
        """
        if point_sum < lowest_points:
            lowest_points = point_sum
            lowest_point_index = i

    return lowest_point_index

def stack_print(stack):
    """
    Prints the stack in a proper way.
    """
    for sta in stack:
        for card in sta:
            print(str(card).ljust(5,' '),end="")
        print()
    
#create the game
def create_game():
    """
    Returns a MAX_VALUE number of cards each with points
    ranging between 1 and 5, with different proportions
    The points for each specific card are chosen randomly.
    """
    cards = {}
    for i in range(1,MAX_VALUE+1):
        rnd = randint(1,800)
        if rnd <= 400:

            points = 1
            
        elif rnd <= 600:
            
            points = 2

        elif rnd <= 700:

            points = 3

        elif rnd <= 750:

            points = 4

        else:

            points = 5

        cards[i] = points
            
        
    #print(cards)
    return cards


#choose number of players and strategies
def game_mode(cards):
    """
    Returns user entered number of players and list of
    strategies.
    """
    player_num = 0
    while player_num == 0 or player_num > MAX_PLAYERS:
        player_num  = int(input("Number of players: "))

    strategies = [s for s in input("Player strategies: ").split()]

    return player_num, strategies

def initialize_game(player_num, strategies):
    """
    Initializes the game by creating and returning
    the card deck for each player, the middle stack, and
    an empty list that would contain the losing cards
    accumulated by each player.
    """
    #distribute cards on each player
    chosen_card_set = set()
    player_cards = {}


    for j in range(player_num):
        player_cards[j+1] = []

    for i in range(GAME_LENGTH):
        for j in range(player_num):
            card_num = randint(1,MAX_VALUE)

            while card_num in chosen_card_set:
                card_num = randint(1,MAX_VALUE)

            
            player_cards[j+1].append(card_num)
            chosen_card_set.add(card_num)

    #print(player_cards)

    

    #place the stack
    stack = [[] for i in range(STACK_NUM)]
    for k in range(STACK_NUM):
        card_num = randint(1,MAX_VALUE)
        while card_num in chosen_card_set:
            card_num = randint(1,MAX_VALUE)

        stack[k].append(card_num)
        chosen_card_set.add(card_num)

    #stack_print(stack)

    

    #create empty losing stack for each player
    player_losing_cards = {}
    for j in range(player_num):
        player_losing_cards[j+1] = []

    return player_cards, stack, player_losing_cards

#play each round
def play_round(round_play, stack, player_losing_cards):
    """
    Returns the new state of the stack and the list of
    player losing cards, using the list of cards chosen
    by the players.
    """
    for i in range(len(round_play)):
        placement_index = get_stack_index(stack,round_play[i][1])
        #print("Player "+str(round_play[i][0])+" playing card "+str(round_play[i][1]))

        if placement_index is None:
            placement_index = get_lowest_point_stack(cards,stack)
            player_losing_cards[round_play[i][0]] += stack[placement_index] #add captured cards to player losing cards list
            stack[placement_index] = [round_play[i][1]]

        else:
            if len(stack[placement_index]) == 5:
                #print("Full stack")
                player_losing_cards[round_play[i][0]] += stack[placement_index]
                stack[placement_index] = [round_play[i][1]]
            elif len(stack[placement_index]) < 5 and len(stack) > 0:
                #print("Stack not yet full")
                stack[placement_index].append(round_play[i][1])
            else:
                #print("invalid number of cards in stack "+str(len(stack[placement_index])))
                stack_print(stack)
                sys.exit()

    return round_play, stack, player_losing_cards



#play all rounds
def run(stack, player_cards, strategies, player_losing_cards):
    """
    Main function. Runs the game loop, and returns the final state
    of the game.
    """
    for r in range(GAME_LENGTH):
        round_play = []

        for k in range(player_num):
            card = get_player_card(stack,player_cards[k+1],strategies[k])
            round_play.append((k+1,card))

        round_play = sorted(round_play,key = lambda x:x[1])

        #print(round_play)

        round_play, stack, player_losing_cards = play_round(round_play, stack, player_losing_cards)
        #print("Stack at round "+str(r+1))
        #stack_print(stack)

    return player_losing_cards
        



#simulate N number of times
if __name__=="__main__":
    cards = create_game()

    player_num, strategies = game_mode(cards)

    #or simluation mode
    N = 10000
    strategy_wins = [0 for i in range(player_num)]
    for x in range(N):

        player_cards, stack, player_losing_cards = initialize_game(player_num, strategies)

        player_losing_cards = run(stack, player_cards, strategies, player_losing_cards)

        #check the winner
        points = []
        for key,value in player_losing_cards.items():
            
            points.append(get_point_sum(cards,value))

        min_index = points.index(min(points))
        strategy_wins[min_index]+=1

    for i in range(player_num):
        print("Player "+str(i+1)+" "+strategies[i]+" "+str(strategy_wins[i]))
        
    #print("Player "+str(key)+": has cards "+str(value)+" with total points -"+str(get_point_sum(cards,value)))
