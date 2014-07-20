## A program to play Blackjack 
## By BlueHat GURU
## Written in Python 3.4.1


# Assumption: players already know how to play blackjack, and do not require educating.




# This is just defining a deck of cards, returning it as a list in numerical_suit order.
card_values = ('ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king')
deck_suits = ('_clubs', '_diamonds', '_hearts', '_spades')
deckofcards = [ value+suit for value in card_values for suit in deck_suits]

#build a dictionary of card values for the handvalue calculation
card_value_dictionary = {}
card_value_counter = 0
for card in card_values:
    card_value_counter = card_value_counter + 1
    if card_value_counter > 10:
        card_value_counter = 10
    card_value_dictionary[card[:3]] = card_value_counter

#import a couple of packages that blackjack won't run without
import random 
import math

#A string which will be used in several places.
failuretocomply = """
Local laws forbid us from taking money from people
who can't understand our instructions.

I'm going to have to ask you to leave."""






def playgame(playerchips=100, quittracker = False):
    #loops until the player looses all chips or quits
    
    print('Welcome to our casino. You have ' + str(playerchips) + ' chips to play with.')
    numberdecks, quittracker = get_number_decks(quittracker)
    tabledeck= bigdeckmaker(numberdecks)
    random.shuffle(tabledeck)
    random.shuffle(tabledeck) # seems to work better with two
    useddeck = []
    
    while (playerchips > 0 and quittracker == False):
        playerbet, quittracker = get_number_bet(playerchips, quittracker)
        if quittracker: # make sure the player just leaves if they give a bad answer
            break
        bet_result, tabledeck, useddeck, quittracker = playhand(playerbet, playerchips, tabledeck, useddeck, quittracker)
        playerchips = playerchips + bet_result
        print('You now have ' + str(playerchips) + ' chips.')
        if quittracker == False:
            quittracker = quit_query()
        
    print('You leave the casino with ' + str(playerchips) + ' chips.')





def playhand(bet_valueph, playerchipsph, deckatthetable, usedcards, quittrackerph):
    #function to actually play through a hand
    playerhandph=[]
    dealerhandph=[]
    playerhandvalue = 0
    dealerhandvalue = 0
    playerstand = False
    
    deckatthetable, playerhandph, usedcards = dealto(deckatthetable, playerhandph, usedcards)
    handstatement(playerhandph, 'Your')
    deckatthetable, dealerhandph, usedcards = dealto(deckatthetable, dealerhandph, usedcards)
    handstatement(dealerhandph, 'The dealer\'s')
    deckatthetable, playerhandph, usedcards = dealto(deckatthetable, playerhandph, usedcards)
    handstatement(playerhandph, 'Your')
    
    while ( (playerhandvalue < 21) and (playerstand != True)):  
        bet_valueph, playerstand, playerhandph, deckatthetable, usedcards, quittrackerph = \
        playerdecision_dialog(bet_valueph, playerchipsph, playerstand, playerhandph, deckatthetable, usedcards, quittrackerph)
        if quittrackerph: # make sure the player just leaves if they give a bad answer
            break
        playerhandvalue = handvalue(playerhandph)
        handstatement(playerhandph, 'Your')
    
    while ( dealerhandvalue < 17) and (quittrackerph == False):
        deckatthetable, dealerhandph, usedcards = dealto(deckatthetable, dealerhandph, usedcards)
        dealerhandvalue = handvalue(dealerhandph)
        handstatement(dealerhandph, 'The dealer\'s')

    #int(bet_valueph)
    bet_resultph = bet_result(bet_valueph, playerhandph, dealerhandph)
    usedcards = usedcards + playerhandph + dealerhandph
    return bet_resultph, deckatthetable, usedcards, quittrackerph





def dealto(deckdealtfrom, deckdealtto, sparedeck):
    #dealing a card, and altering appropriate decks/hands; also to reincorporate used cards if we run out
    if len(deckdealtfrom)<=0:
        deckdealtfrom.extend(sparedeck)
        random.shuffle(deckdealtfrom)
        del sparedeck[:]
    deckdealtto.append(deckdealtfrom.pop())
    return deckdealtfrom, deckdealtto, sparedeck




def handstatement(handtoprint, userflag):
    handstring = ''
    for card in range(len(handtoprint)):
        handstring = handstring + ' ' + handtoprint[card] + ','#try to incorporate proper english at some point
    handvaluestring = str(handvalue(handtoprint))
    #print(userflag + ' hand is ' + handstring + '.')
    print(userflag + ' hand is ' + handstring + ' worth '+ handvaluestring + '.')
        



    
def playerdecision_dialog(bet_valuepd, playerchipspd, playerstandpd, playerhandpd, deckdealtfromph, usedcardspd, quittrackerpd, retries=6, decideflag = False):
    #dialog asking the player what action they want this hand.
    while (retries > 0) and (decideflag == False):
        playeraction = input('Do you want to hit, stand, or double? ')
            
        if playeraction in ('h', 'hi', 'ht', 'hit'):
            deckdealtfromph, playerhandpd, usedcardspd = dealto(deckdealtfromph, playerhandpd, usedcardspd)
            decideflag = True
            
        elif playeraction in ('s', 'st', 'sta', 'stan', 'stand'):
            playerstandpd = True
            decideflag = True
            
        elif playeraction in ('d', 'do', 'dou', 'doub', 'doubl', 'double' ):
            if 2*bet_valuepd > playerchipspd:
                print('I\'m sorry, you can\'t bet more chips than you have.')
                retries = retries - 1
            else:
                bet_valuepd = 2*bet_valuepd
                deckdealtfromph, playerhandpd, usedcardspd = dealto(deckdealtfromph, playerhandpd, usedcardspd)
                playerstandpd = True
                decideflag = True
                
        #will need to add 'surrender' and 'split' here, if implemented
        #elif playeraction in ('surren', 'surrender'): # supposed to only be available on first decision of hand, and results in quit game -> complicated
        #    playerstandpd = True
        #    bet_valuepd = bet_valuepd - int(bet_valuepd/2)
        #    decideflag = True
        #elif playeraction in ('sp', 'spl', 'spli', 'split'):
            # supposed to only be available on first decision of hand, and results in two player hands -> complicated
            #decideflag = True
            
        else:
            retries = retries - 1
            print('I am sorry, I did not understand what you said. Could you repeat it, please?')
    if retries <= 0:
        quittrackerpd = True
        print(failuretocomply)
        bet_valuepd = 0
    return bet_valuepd, playerstandpd, playerhandpd, deckdealtfromph, usedcardspd, quittrackerpd
    




def handvalue(handlist): # to compute what a hand is worth
    handinteger = 0
    ace_present = False
    for card_in_hand in handlist:
        if card_in_hand[:3] in list(card_value_dictionary.keys()):
            handinteger = handinteger + card_value_dictionary[card_in_hand[:3]]
        if card_in_hand[:3] == 'ace':
            ace_present = True

    #The player will never wish to count more than one ace as an 11
    if (ace_present == True) and (handinteger + 10 <= 21):
        handinteger = handinteger + 10
    return handinteger
            





def bet_result(betvaluebr, playerhandbr, dealerhandbr):
    
    playerblackjackbr = black_jack_check(playerhandbr)
    playerhandvalue = handvalue(playerhandbr)
    dealerblackjackbr = black_jack_check(dealerhandbr)
    dealerhandvalue = handvalue(dealerhandbr)
    
    if playerhandvalue > 21:
        betmodifier = -1
        
    elif dealerhandvalue > 21 and playerhandvalue <= 21:
        betmodifier = 1
        
    elif dealerhandvalue <= 21 and playerhandvalue <= 21:
        if playerhandvalue > dealerhandvalue:
            betmodifier = 1
        elif playerhandvalue < dealerhandvalue:
            betmodifier = -1
        elif playerhandvalue == dealerhandvalue:
            if (playerblackjackbr == True) and  (dealerblackjackbr == False):
                betmodifier = 1
            elif (playerblackjackbr == False) and  (dealerblackjackbr == True):
                betmodifier = -1
            else:
                betmodifier = 0

    if playerblackjackbr == True:
        betmodifier = (3/2)*betmodifier
                
    betresultbr = int(betmodifier * betvaluebr)
    return betresultbr





def black_jack_check(handtocheckbjc, isblackjack = False):
    tenfacelist = []
    for cardvaluebjc in card_values[8:12]:
        tenfacelist = tenfacelist + [cardvaluebjc[:3]]
    if len(handtocheckbjc) == 2:
        if (handtocheckbjc[0][:3] in ['ace']) and (handtocheckbjc[1][:3] in tenfacelist):
            isblackjack = True
        elif (handtocheckbjc[1][:3] in ['ace']) and (handtocheckbjc[0][:3] in tenfacelist):
            isblackjack = True                    
    return isblackjack





def bigdeckmaker(numberofdecks, fulldeck=deckofcards):
    #takes an integer number of decks and combines them into one big deck
    loopvar = numberofdecks
    makedeck = []
    loopdeck = fulldeck
    while loopvar > 0:
        makedeck.extend(loopdeck[:])
        loopvar = loopvar -1
    return makedeck






def get_number_from_player(playermaxchoice, maxstring, inputstring, minstring, quittrackergnfp, retries=6):
    #dialog asking player to choose a number, used for both making bets and picking tables.
    while (retries > 0) :
        playerchoice = input(inputstring)
        if len(playerchoice) < 1:
            playerchoice='user input error'
        elif playerchoice[0] in [ str(range(10)[i]) for i in range(10)]:
            playerchoice_int = int(playerchoice)
            if (playerchoice_int <= playermaxchoice) and (playerchoice_int >0):
                return playerchoice_int, quittrackergnfp
            elif playerchoice_int < 1:
                print(minstring+' Try again.')
            else:
                print(maxstring + str(playermaxchoice) + '. Try again.')
        else:            
            print('Please enter an integer.')
        retries = retries - 1
        if retries <= 0:    
            print(failuretocomply)
            quittrackergnfp = True
            return 0, quittrackergnfp
            

def get_number_bet(totalplayerchips, quittrackergnb):
    # written like this for convenience
    betmaxstring = 'You may bet at most '
    betinputstring = 'Please type how many chips would you like to bet: '
    betminstring = 'You must bet at least one.'
    numberofchips, quittrackergnb = get_number_from_player(totalplayerchips, betmaxstring, betinputstring, betminstring, quittrackergnb)
    return numberofchips, quittrackergnb 

def get_number_decks(quittrackergnd):
    # written like this for convenience
    deckmaxstring = 'You may choose at most '
    deckinputstring = 'Please choose how many decks your table is using: '
    deckminstring = 'You can\'t play with less than one deck of cards.'
    numberofdecks, quittrackergnd = get_number_from_player(8, deckmaxstring, deckinputstring, deckminstring, quittrackergnd)
    return numberofdecks, quittrackergnd





def quit_query(retries=4):
    while (retries > 0):
        ok = input('Do you want to keep playing, Yes or No? ')
        if ok in ('y', 'ye', 'yes'):
            return False
        if ok in ('n', 'no', 'nop', 'nope'):
            return True
        retries = retries - 1
        if retries < 0:
            print(failuretocomply)
        print('Yes or no, please!')





if __name__ == "__main__":
    playgame()







