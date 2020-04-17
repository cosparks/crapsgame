import random
import time

# come_dict is a global dictionary for storing multiple bets and odds.  every time a new value is stored,
# an old one is popped off so dictionary doesn't become bloated
come_dict = {0: [0]}
explanation = []


def start():  # ask user if they'd like to play
    play_game = False
    question_answered = False
    greeting = get_greeting()
    while not question_answered:
        play = input(greeting + ' Fancy playing a game of craps? (yes/no) ')
        if 'yes' in play:
            play_game = True
            question_answered = True
        elif 'no' in play:
            print("Alright, come back when you're feeling lucky!")
            question_answered = True
        else:
            print("Speak up!  I can't hear you.")
    return play_game


def get_greeting():  # returns 'good morning', 'good afternoon', etc. depending on current time
    current_time = time.localtime()
    if 12 > current_time[3] >= 3:
        greeting = 'Good morning!'
    elif 17 > current_time[3] >= 12:
        greeting = 'Good afternoon!'
    else:
        greeting = 'Good evening!'
    return greeting


def get_name():  # prompts user to enter a name
    name = input("Excellent!  I don't think I've seen you around here before.  What is your name? ")
    return name


def setup_game(name):  # asks user if they would like instructions on how to play
    print("Please have a seat, " + name + ".")
    question_answered = False
    while not question_answered:
        answer = input("Have you played craps before? (yes/no) ")
        if 'yes' in answer:
            want_rules = input("Very good.  Would you care for me to explain the rules as we play? (yes/no) ")
            question_answered = True
        elif 'no' in answer:
            print("Alright, I'll explain the rules as we go along.")
            want_rules = 'yes'
            question_answered = True
        else:
            print("I'm sorry, could you speak more clearly?")

    money = buy_chips()  # runs function for user to buy chips

    if 'yes' in want_rules:  # returns starting wallet value and True if user wants rules explained
        print("Very good, let's play!")
        return True, money
    else:                    # returns starting wallet value and False if user doesn't want rules explained
        print("Very good, let's begin!")
        return False, money


def buy_chips():  # prompts user to enter how much money they'd like to start with
    question_answered = False
    while not question_answered:
        money_str = input("How much money's worth of chips can I put you in for?  $")
        if money_str.isdigit():
            money = int(money_str)
            question_answered = True
        else:
            print("Please enter a numerical value with digits (ie. 1, 2, 3..)")
    return money


def come_out_phase(name, balance, rules):  # first of the two mai phases of the game
    point = 0
    if rules and "a" not in explanation:
        print("~~ This first bet you can make is called a pass bet, it's minimum $5 and maximum $20, and pays out")
        print("even money if you roll a 7 or 11.  However, if you roll a 2, 3 or 12 you lose your bet. ~~")
        explanation.append("a")
    pass_bet = make_pass_bet(name, balance)
    balance = balance - pass_bet
    
    roll = roll_dice()
    
    if roll == 7 or roll == 11:
        balance = balance + (pass_bet * 2)
        print("You win $" + str(pass_bet) + "!  Well done, " + name)
    elif roll == 2 or roll == 3 or roll == 12:
        print("Sorry, " + name + ", you've lost your $" + str(pass_bet))
    else:
        print(str(roll) + "!  The point is now set at " + str(roll))
        point = roll
        if rules and "b" not in explanation:  # prints rules if user has specified
            print("~~ Your bet is now set to the point, so if you roll " + str(point) + ", then you win,")
            print("but if you roll a seven, your bet loses. ~~")
            explanation.append("b")
        balance = check_come_bets(balance, roll, rules)

    if roll == 7 and max(come_dict.keys()) != 0:   # separate condition for any come bets which have been set to a point
        balance = check_come_bets(balance, roll, rules)

    return balance, pass_bet, point


def point_phase(balance, point, bet, odds_bet, odds, rules):  # this phase begins once a point is set

    if rules and "e" not in explanation:
        print("~~ You can also place another bet called a 'come bet'.  It works pretty much the same as a pass")
        print("bet: 7 or 11 wins; 2, 3 or 12 loses; and otherwise it gets set to a point.  You could win big money! ~~")
        explanation.append("e")

    balance = come_bet_prompt(balance)  # asks the player if they wish to place a come bet

    if len(come_dict) == 1 and come_dict[0][0] == 0:  # if user only has point bets, show how much is on table
        print("You have $" + str(bet + odds_bet) + " on the table and $" + str(balance) +
              " worth of chips in your wallet.")
    else:                                             # if user has come and point bets, show how much is on table
        come_bets = 0
        for key in come_dict:
            come_list = come_dict[key]
            if len(come_list) > 1:
                come_bets = come_bets + (come_list[0] + come_list[1])
            elif len(come_list) == 1:
                come_bets = come_bets + come_list[0]
        print("On the table you have $" + str(bet + odds_bet) + " in pass bets, $" + str(come_bets) +
              " in come bets and $" + str(balance) + " worth of chips in your wallet.")
    finished = False
    turn = 0
    while not finished:                               # run loop until player hits their point or sevens out
        if turn > 0:
            balance = come_bet_prompt(balance)
        roll = roll_dice()
        if roll == point:
            winnings = (bet * 2) + odds_bet + (odds_bet * odds)  # if bet is 5
            balance = balance + winnings
            print("You win!! You got your money back and won $" + str(bet + (odds_bet * odds)) + " you lucky duck!")
            balance = check_come_bets(balance, roll, rules)
            finished = True
        elif roll == 7:
            print("Sorry, you sevened out and lost your point bets.")
            balance = check_come_bets(balance, roll, rules)
            finished = True
        else:
            print("You didn't hit your point!")
            balance = check_come_bets(balance, roll, rules)
        turn += 1
    return balance


def roll_dice():  # prints roll statement and returns roll values
    dice_sides = ['[ . ]', '[ : ]', '[ :. ]', '[ :: ]', '[:.:]', '[:::]']
    dice_list = []
    dice_value = 0
    question_answered = False
    while not question_answered:
        ready = input("Are you ready to roll? (yes/no) ")
        if 'yes' in ready:
            question_answered = True
        elif 'no' in ready:
            print("A bit of sarcasm.  Very funny!")
            question_answered = True
        else:
            print("Are you alright? You haven't had too much to drink, have you?")
    for i in range(2):
        dice_list.append(dice_sides[random.randrange(0, 6)])
    for die in dice_list:
        dice_value = dice_value + (dice_sides.index(die) + 1)
    print("You rolled " + dice_list[0] + dice_list[1] + "!!!  " + str(dice_value) + "!")
    return dice_value


def make_pass_bet(name, balance):  # intial pass bet prompt
    bet_within_limit = False
    while not bet_within_limit:
        pass_bet_str = input("How much would you like to bet? ")
        if pass_bet_str.isdigit():  # check if string only contains digits
            pass_bet = int(pass_bet_str)  # convert str to int
            if 5 <= pass_bet <= 20 and check_wallet(balance, pass_bet) == 'clear':
                bet_within_limit = True
            elif 5 > pass_bet or 20 < pass_bet:
                print("I'm sorry, " + name + ", your bet must be between 5 and 20 dollars.")
                bet_within_limit = False
            elif check_wallet(balance, pass_bet) == 'broke':
                pass_bet = 0
                return pass_bet
            elif check_wallet(balance, pass_bet) == 'redo':
                bet_within_limit = False
        else:
            print("Please enter a numerical value with digits (ie. 5, 10, 15..)")
    return pass_bet


def place_odds(balance, name, bet, point, rules):  # asks player whether they want to place odds on pass bets
    odds, odds_str = lookup_odds(point)
    if rules and "c" not in explanation:
        print("~~ Now, if you like, you can place an odds bet.  Odds bets are extra money you put down on your point.")
        print("You can either bet the same amount as your pass bet or you can double it.  These are the best odds in")
        print("the casino, so maybe give it a try!  The odds on " + str(point) + " are " + odds_str + ". ~~")
        explanation.append("c")
    question_answered = False
    if check_wallet(balance, bet) != 'broke':  # don't ask player unless they have enough money to place odds
        while not question_answered:
            odds_answer = input("Would you like to place odds on your bet? (yes/no) ")

            if 'yes' in odds_answer:
                single_or_double = odds_selection_prompt()
                odds_bet = bet * single_or_double
                if check_wallet(balance, odds_bet) != 'redo':
                    balance = balance - odds_bet
                    question_answered = True
                else:
                    print("You do not have enough money to place double odds.  You can go for single if you'd like.")
            elif 'no' in odds_answer:
                print("It seems you like to keep it safe, " + name)
                odds_bet = 0
                question_answered = True
            else:
                print("Oh dear I must be losing my hearing.  One more time?")
    else:
        odds_bet = 0
    return odds_bet, odds, balance


def odds_selection_prompt():  # prompts user to select single or double odds
    question_answered = False
    while not question_answered:
        single_or_double = input("Would you like single or double odds? ")
        if 'single' in single_or_double:
            odds = 1
            return odds
        elif 'double' in single_or_double:
            odds = 2
            return odds
        else:
            print("It's quite loud in here, can you say that again?")


def lookup_odds(point):  # contains dictionary with odds for each point (float is for math, str is for print statements)
    odds_dict = {4: [2/1, '1:2'], 10: [2/1, '1:2'], 5: [3/2, '3:2'], 9: [3/2, '3:2'], 6: [6/5, '6:5'], 8: [6/5, '6:5']}
    odds_list = odds_dict[point]
    odds_math = odds_list[0]
    odds_str = odds_list[1]
    return odds_math, odds_str


def check_wallet(balance, bet):  # check if player has enough money to make a bet
    if (balance - 5) < 0:
        return 'broke'
    elif (balance - bet) < 0:
        return 'redo'
    else:
        return 'clear'


def check_come_bets(balance, roll, rules):        # handles how dice rolls affect come bets
    if roll == 7 and max(come_dict.keys()) != 0:  # if you roll 7 with active come bets, you lose all of them
        come_loss = 0
        key_list = []

        for i in come_dict.keys():  # pops all active come bets with a set point out of dictionary
            if i > 0 and len(come_dict[i]) > 1:
                come_loss = come_loss + (come_dict[i][0] + come_dict[i][1])
                key_list.append(i)
            elif i > 0 and len(come_dict[i]) == 1:
                come_loss = come_loss + (come_dict[i][0])
                key_list.append(i)
        for key in key_list:
            come_dict.pop(key)
        print("You lost all your active come bets!  You're out $" + str(come_loss) + ".")

    if roll in come_dict.keys():  # if you hit a set come point, pay out winnings and pop values out of dictionary
        balance = calculate_come_winnings(roll, balance, rules)
        come_dict.pop(roll)

    if 0 in come_dict.keys() and come_dict[0][0] != 0:  # if you have come bet without a set point
        come_bet = come_dict[0][0]
        if roll == 7 or roll == 11:                     # if roll == 7, 11: your bet wins
            balance = balance + (come_bet * 2)
            if roll == 7:
                print("But your come bet won $" + str(come_bet) + "!!")
            else:
                print("Your come bet won $" + str(come_bet) + "!!")
            come_dict[0] = [0]
        elif roll == 2 or roll == 3 or roll == 12:      # if roll == 2, 3, 12: your bet loses
            print("Sorry, you've lost your come bet :(")
            come_dict[0] = [0]
        else:
            balance = set_come_point(balance, roll, come_bet, rules)  # else: your bet's point is set to the roll
    return balance


def come_bet_prompt(balance):
    question_answered = False
    if len(come_dict.keys()) > 1 or come_dict[0][0] > 0:  # if user already has come bets on the table:
        determiner = "another"                            # ask if they want to make 'another' come bet
    else:                                                 # otherwise:
        determiner = "a"                                  # ask if they want to make 'a' come bet
    if check_wallet(balance, 5) != 'broke':  # only prompt if the player has enough money to make a come bet
        if len(come_dict) <= 6:  # if there are already 6 come bets (max) on the table, no more bets are allowed
            while not question_answered:  # finish loop when question_answered == True
                come_bet_question = input("Would you like to place " + determiner + " come bet? (yes/no) ")
                if 'yes' in come_bet_question:
                    question_answered = True
                    balance = make_come_bet(balance)
                elif 'no' in come_bet_question:
                    question_answered = True
                else:
                    print("Sorry, once again?")
    return balance


def calculate_come_bets():  # adds up stored values in come dictinoary to show how much players have on the table
    come_bets_total = 0
    for i in come_dict.keys():
        if len(come_dict[i]) > 1:
            come_bets_total = come_bets_total + (come_dict[i][0] + come_dict[i][1])
        else:
            come_bets_total = come_bets_total + come_dict[i][0]
    return come_bets_total


def make_come_bet(balance):  # asks player how much they'd like to bet and verifies they have enough
    bet_within_limit = False
    while not bet_within_limit:
        come_bet_str = input("How much would you like to bet? ")
        if come_bet_str.isdigit():              # check if str only contains digits
            come_bet = int(come_bet_str)        # convert str to int
            if 5 <= come_bet <= 20 and check_wallet(balance, come_bet) == 'clear':
                bet_within_limit = True
            elif check_wallet(balance, come_bet) == 'redo':
                print("Sorry, but you don't have enough money to make that bet.  You can bet $" + str(balance)
                      + " at most")
                bet_within_limit = False
            else:
                print("I'm sorry, but your bet must be between 5 and 20 dollars.")
                bet_within_limit = False
        else:
            print("Please enter a numerical value with digits (ie. 5, 10, 15..)")
    come_dict[0] = [come_bet]
    return balance - come_bet


def set_come_point(balance, roll, come_bet, rules):  # sets come point and conditionally runs odds_on_come
    if roll not in come_dict.keys():
        come_dict[roll] = [come_bet]
    else:
        come_dict[roll][0] = come_dict[roll][0] + come_bet
    come_dict[0] = [0]
    print('Your come bet has been set to ' + str(roll) + '!')
    if check_wallet(balance, come_bet) != 'broke':
        balance = odds_on_come(balance, come_bet, roll, rules)
    return balance


def odds_on_come(balance, come_bet, roll, rules):  # once a come bet's point is set, ask users if they'd like odds
    odds, odds_str = lookup_odds(roll)
    if rules and "d" not in explanation:                                      # explains the betting process
        print("~~ Odds on come bets work the exact same as odds on pass bets: you can choose single or double and")
        print("if you hit your point, the odds are paid out on top of your primary bet's winnings.  But remember,")
        print("if you roll a seven, then you lose all your bets with a set point! The odds on " + str(roll) + " are "
              + odds_str + ". ~~")
        explanation.append("d")
    question_answered = False
    while not question_answered:                    # works the same as place_odds function
        odds_answer = input("Would you like to place odds on your come bet? (yes/no) ")
        odds_bet = 0
        if 'yes' in odds_answer:
            single_or_double = odds_selection_prompt()
            odds_bet = come_bet * single_or_double
            if check_wallet(balance, odds_bet) != 'redo':
                balance = balance - odds_bet
                question_answered = True
            else:
                print("You do not have enough money to place double odds.  You can go for single if you'd like.")
        elif 'no' in odds_answer:
            print("Ok, but these are great odds, you know?  The best, actually!")
            odds_bet = 0
            question_answered = True
        else:
            print("Oh dear I must be losing my hearing.  One more time?")
    if len(come_dict[roll]) == 1:                   # if no odds bet in list, append odds_bet and odds to list
        come_dict[roll].append(odds_bet)
        come_dict[roll].append(odds)
    elif roll in come_dict.keys() and len(come_dict[roll]) > 1:  # if odds bet already in list, add to existing one
        come_dict[roll][1] = come_dict[roll][1] + odds_bet
    return balance


def calculate_come_winnings(roll, balance, rules):  # adds up stored values in come_bet dictionary and returns winnings
    if rules:
        print("Here's how this works")
    values_list = come_dict[roll]
    if len(values_list) > 1:                        # if bet has odds, do this math
        bet = values_list[0]
        odds_bet = values_list[1]
        odds = values_list[2]
        winnings = (bet * 2) + odds_bet + (odds_bet * odds)
        display_winnings = bet + (odds_bet * odds)
    else:                                           # if bet has no odds, do this math
        bet = values_list[0]
        winnings = bet * 2
        display_winnings = bet
    balance = balance + winnings
    print("You hit your come point and got paid out $" + str(display_winnings) + " on top of your bet!  "
          + "You now have $" + str(balance) + " in your wallet.")
    return balance


def play_again_prompt(start_balance, balance, name):  # display winnings and ask user to play again if not broke
    question_answered = False
    active_bets = calculate_come_bets()
    total_winnings = balance - start_balance
    if total_winnings >= 0:
        word = " up "
    else:
        word = " down "
    if check_wallet(balance, 5) != 'broke':
        while not question_answered:
            if active_bets > 0:
                answer = input("You still have $" + str(active_bets)
                               + " on the table.  Would you like to play again? (yes/no) ")
            else:
                answer = input("You're" + word + "$" + str(abs(total_winnings))
                               + ".  Would you like to play again? (yes/no) ")
            if 'yes' in answer:
                return True
            elif 'no' in answer:
                print("Come back when you're feeling lucky!")
                return False
            else:
                print("I don't understand")
    else:
        print("Sorry, " + name + " but you don't have enough chips left to place any more bets."
              + "  Come play again sometime!")


def main():
    play_game = start()
    turn = 0
    while play_game:
        if turn == 0:
            name = get_name()
            explain_rules, wallet = setup_game(name)
            start_balance = wallet
        elif "a" and "b" and "c" and "d" and "e" in explanation:  # if all rules have been explained, stop explaining
            explain_rules = False
        wallet, pass_bet, point = come_out_phase(name, wallet, explain_rules)
        if point != 0:
            odds_bet, odds, wallet = place_odds(wallet, name, pass_bet, point, explain_rules)
            wallet = point_phase(wallet, point, pass_bet, odds_bet, odds, explain_rules)
            print("You have $" + str(wallet) + " left")
            play_game = play_again_prompt(start_balance, wallet, name)
        elif point == 0:
            print("You have $" + str(wallet) + " left.")
            play_game = play_again_prompt(start_balance, wallet, name)
        turn += 1


if __name__ == "__main__":
    main()
