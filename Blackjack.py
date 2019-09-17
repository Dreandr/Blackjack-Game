### Final version!

import random
from IPython.display import clear_output

## A function we will need later to draw random cards from our deck

def which(obj,condition):
    index = []
    for i in range(0,len(obj)):
        if obj[i] == condition:
            index.append(i)
    return index

## Deck class

class deck():
    
    ## generating the basic line-up of cards
    card_list = [i for i in range(2,11)]
    for i in ["Ace", "Jack", "Queen", "King"]:
        card_list.append(i)

    ## generating the deck
    list_1 = []
    for i in ["Clubs", "Diamonds", "Hearts", "Spades"]:
        for y in card_list:
            list_1.append(f"{y} of {i}")
        
    def __str__(self):
        return(f"This is a deck of cards. It currently has {len(self.list_1)} cards in it.")
    
    def draw(self, hand, num):
        for i in range(0,num):
            x = self.list_1.pop(which(self.list_1,random.sample(self.list_1,1)[0])[0])
            hand.current.append(x)
    
    def reshuffle(self):
        self.list_1 = []
        for i in ["Clubs", "Diamons", "Hearts", "Spades"]:
            for y in self.card_list:
                self.list_1.append(f"{y} of {i}")

## Hand class

class hand():
        
    def __init__(self, dealer = False):
        self.dealer = dealer
        self.ace = []
        self.current = []
    
    def pointcount(self):
        counter = 0
        for i in self.current:
            if i.split()[0] == "Ace" and self.dealer == False:
                if len(self.ace) < sum(list(map(lambda x: "Ace" in x, self.current))):
                    choice = ""
                    while choice != "1" or choice != "11":
                        choice = input("Do you want to count the ace as 1 or 11? Print 1 or 11!")
                        if choice == "11":
                            self.ace.append(11)
                            counter = counter + sum(self.ace)
                            break
                        elif choice == "1":
                            self.ace.append(1)
                            counter = counter + sum(self.ace)
                            break
                else:
                    counter = counter + sum(self.ace)
                
            elif i.split()[0] == "Ace" and self.dealer == True:
                if counter < 11:
                    counter = counter + 11
                else:
                    counter = counter + 1
            elif i.split()[0] in ["Jack", "Queen", "King"]:
                counter = counter + 10
            else:
                counter = counter + int(i.split()[0])
        return(counter)
    
    def __str__(self):
        if self.dealer == False:
            return(f"\nYou have the following cards: {self.current}. This is a hand worth {self.pointcount()} points!")
        else:
            return(f"\nThe dealer has one card closed and the following cards open: {[x for i, x in enumerate(self.current) if i != 1]}.")
## generating deck and setting up cash pool    
game_on = True 
game_deck = deck()
choice_legit = False
while choice_legit == False: 
    clear_output()
    player_cash = int(input("Welcome to the casino! How many greenbacks you got on you? You gotta have at least $100!"))
    if player_cash >= 100:
        choice_legit = True
        print("You hella rich, partner!")
        break
    else:
        player_cash = int(input("Welcome to the casino! How many greenbacks you got on you? You gotta have at least $100!"))

player_cash_start = player_cash

while game_on == True:
    ## checking cash
    if player_cash < 10:
        print("Looks like you to too little cash to play! Better luck next time!")
        game_on = False
        break
        
    ## Player betting            
    choice_legit = False
    while choice_legit == False: 
        try:
            player_bet = int(input("How much you bettin', partner? You gotta bet at least $10!"))
        
        except:
            print("Don't joke around with me, partner, that's not a number!")
        
        else:
            if player_bet >= 10 and player_bet <= player_cash:
                choice_legit = True
                player_cash = player_cash - player_bet
                print(f"You bettin' ${player_bet}, got ${player_cash} left!")
                break
            elif player_bet < 10:
                print("Nah, that's too cheap! Try again!")
            elif player_bet >= 10 and player_bet > player_cash:
                print(f"You ain't got this many, only ${player_cash} on yerself!")
       
    #clear_output()
    player_hand = hand()
    dealer_hand = hand(dealer = True)
    game_deck.draw(player_hand, 2)
    game_deck.draw(dealer_hand, 2)
    print(player_hand)
    print(dealer_hand)
    
    #clear_output()       
    player_stalls = False
    dealer_stalls = False   
    ## Main part of the game starts
    while player_hand.pointcount() < 21 and dealer_hand.pointcount() <21:
        
        if player_hand.pointcount() == 21:
            print("You won!")
            player_cash = player_cash + (player_bet*2)
            break
        if dealer_hand.pointcount() == 21:
            print(f"Dealer has the following cards:{dealer_hand.current}. Dealer wins!")
            break
                
        if player_stalls == False:
            choice_legit = False
            while choice_legit == False:
                try:
                    
                    player_choice = input("You wanna hit or stay, partner? Print H or S!")
                    
                except:
                    print("Stop foolin' around, partner, you gotta pring H or S!")
                else:
                    if player_choice == "H":
                        choice_legit = True
                        game_deck.draw(player_hand, 1)
                        print(player_hand)
                        break
                    elif player_choice == "S":
                        choice_legit = True
                        player_stalls = True
                        print("You stand!")
                        break
        else:
            print("You stand and don't draw!")
            
        if player_hand.pointcount() == 21:
            break
        if player_hand.pointcount() > 21:
            print("You bust! Too bad!")
            break
        
        ##dealer's turn
        if dealer_stalls == True:
            print("The dealer stands and doesn't draw!")
        elif dealer_hand.pointcount() < 17 or dealer_hand.pointcount() < player_hand.pointcount() < 21 and dealer_stalls == False:
            print("The dealer hits!")
            game_deck.draw(dealer_hand, 1)
            print(dealer_hand)
        else:
            dealer_stalls = True
            print("The dealer stands!")
        
        if dealer_hand.pointcount() == 21:
            break
        if dealer_hand.pointcount() > 21:
            print(f"The dealer busts with the following cards:{dealer_hand.current}. You win!")
            player_cash = player_cash + (player_bet*2)
            break
        
        if player_stalls == dealer_stalls == True:
            if player_hand.pointcount() >= dealer_hand.pointcount():
                print(f"The dealer has the following cards: {dealer_hand.current}. You win!")
                player_cash = player_cash + (player_bet*2)
                break
            else:
                print(f"The dealer has the following cards: {dealer_hand.current}. You lose!")
                break
                
    if player_hand.pointcount() == 21:
            print("You won!")
            player_cash = player_cash + (player_bet*2)
            
    if dealer_hand.pointcount() == 21:
            print(f"The dealer has the following cards:{dealer_hand.current}. The house won!")
            
    choice = (input("Play another round? Y/N"))
    if choice == "N":
        print(f"You came with ${player_cash_start} and leave the casino with ${player_cash} on you!")
        game_on = False
        break
    else:
        if player_cash < 10:
            print("Looks like you're all outta cash! Come back next time, partner!")
            game_on = False
            break
        else:
            clear_output()
            print("Game on!")