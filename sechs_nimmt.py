"""

"""

from random import randint
import sys

#Constants

MAX_VALUE = 104

MAX_PLAYERS = 10

GAME_LENGTH = 10

STACK_NUM = 4

STRATS = ['SMA','LARG','CL_SMA','SMA_LARG','LARG_SMA','RND','PNT_LARG']


def get_player_card(stack,player_k_cards,strategy):
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
    point_sum = 0
    for card in card_list:
        point_sum += cards[card]

    return point_sum

def get_lowest_point_stack(cards,stack):
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

    for sta in stack:
        for card in sta:
            print(str(card).ljust(5,' '),end="")
        print()
    
#create the game
def create_game():
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
    player_num = 0
    while player_num == 0 or player_num > MAX_PLAYERS:
        player_num  = int(input("Number of players: "))

    strategies = [s for s in input("Player strategies: ").split()]

    return player_num, strategies

def initialize_game(player_num, strategies):
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
