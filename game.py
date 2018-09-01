import cmd
import sys
import os
import time
import json
import random
import textwrap

# TESTING controls how the game acts and will speed things certain things up for testing purposes.
TESTING = True

# Sets the maximum width that the text can go.
SCREEN_WIDTH = 100

# Sets how fast the text is written on the screen when there is the one letter at a time effect.
DEFAULT_DELAY = [0.1, 0.2]

# Controls if the user should have to hit enter at the end of every line of written text.
DEFAULT_INPUT = False

# Speeds up/slows down all wait times to make gameplay faster. 2 = twice as fast, 0.5 = double speed.
SPEED_MODIFIER = 1

# Defines wether to use the command prompt commands to clear the screen, or just print a bunch of times. Useful for when testing the code using IDLE. The first value is whether to do so, and the second value is the amount of times.
CLEAR_PRINT = [True, 100]

### GENERAL NOTES ###
# To Do:
# - Implement a way of saving the game and loading up the save easily.
# - Implement luck as part of the player and what choices they make affects this.
# - Implement the lottery on Saturdays.
# - Implement a way that the Dictator's mood controls causes random events/fines.

### PROGRAM FUNCTIONS ###


def sleep(wait_time, force=False):
    if TESTING and force is False:
        return

    elif force is True or TESTING is False:
        time.sleep(wait_time / SPEED_MODIFIER)


def display(text, width=SCREEN_WIDTH, end="\r\n"):
    text = textwrap.dedent(text).strip()
    print(textwrap.fill(text, width=width), end=end)


def write_text(string, letter_by_letter=True, should_input=DEFAULT_INPUT, input_end=" ", width=SCREEN_WIDTH, end="\r\n", delay_settings=DEFAULT_DELAY):
    per_character_delay = delay_settings[0]
    per_newline_delay = delay_settings[1]

    if letter_by_letter and not should_input:
        for char in string:
            sys.stdout.write(char)
            sys.stdout.flush()

            sleep(per_character_delay)

        sys.stdout.write(" ")

        sleep(per_newline_delay)
        sys.stdout.write(end)

        sys.stdout.flush()

    elif letter_by_letter and should_input:
        for char in string:
            sys.stdout.write(char)
            sys.stdout.flush()

            sleep(per_character_delay)

        sys.stdout.write(input_end)

        sleep(per_newline_delay)

        input()

        sys.stdout.flush()

    else:
        display(string, end=end)


def clear():
    if not CLEAR_PRINT[0]:
        try:
            if os.name == "nt":
                # For windows.
                os.system("cls")

            elif os.name == "posix":
                # For mac/linux.
                os.system("clear")

            else:
                # Unknown operating system, just print a newline a bunch of times.
                print("\n" * CLEAR_PRINT[1])

        except:
            # Can't figure out the operating system, safest bet is to just print a newline a bunch of times.
            print("\n" * CLEAR_PRINT[1])

    else:
        # The clearing of screen is overriden, so we just print a newline CLEAR_PRINT[1] times.
        print("\n" * CLEAR_PRINT[1])


def super_input(initial, initial_input, input_type, reprompt, reprompt_input, accepted=[], length=0):
    print(initial)
    given_input = input(initial_input)

    while True:
        try:
            # Try convert it into specified type.
            print("")
            given_input = input_type(given_input)

        except:
            # Oops, there was an error.
            print("")

            print(reprompt)
            given_input = input(reprompt_input)

            continue

        if type(given_input) == str:
            if given_input.lower() not in accepted and accepted != []:
                print("")

                print(reprompt)
                given_input = input(reprompt_input)

                continue

        try:
            if len(str(given_input)) != length and length != 0:
                print("")

                print(reprompt)
                given_input = input(reprompt_input)

                continue

        except:
            print("")

            print(reprompt)
            given_input = input(reprompt_input)

            continue

        break

    return given_input


def ordinal(num):
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}

    if 10 <= num % 100 <= 20:
        suffix = 'th'

    else:
        suffix = suffixes.get(num % 10, 'th')

    return str(num) + suffix

# =================== #


class Player():
    def __init__(self, name, cash, luck):
        self.name = name
        self.cash = cash
        self.luck = luck
        self.has_boat=True

    def summarise(self):
        return "{} Information: You have {} in cash.".format(self.name, money(self.cash))


class Game():
    def __init__(self, weather, date, payments, fees, dictator):
        self.weather = weather
        self.date = date

        self.payments = payments
        self.fees = fees

        self.dictator = dictator


class Weather():
    def __init__(self, current, history, chance, special):
        #  A string, either "good", "bad", "storm" or "hurricane"
        self.current = current

        # A list of strings of "good", "bad", "storm" or "hurricane"
        self.history = history

        #  A string that represents a probaility. For example "2/6".
        self.chance = chance

        # Special rules about what might happen
        self.special = special

    def storm(self):
        chance_num = [int(x) for x in self.chance.split("/")]
        for i in range(chance_num[0]):
            rand = random.randint(1, chance_num[1])

            if rand == 1:
                return "bad"

        return "good"

    def set_weather(self, condition):
        self.current = condition
        self.history.append(condition)

class Date():
    def __init__(self, day_count, day_name):
        # A number which represents the amount of days the player has been going for.
        self.day_count = day_count

        # A string which is the current day name.
        self.day_name = day_name

        self.days = "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday".split(
            ",")

    def increment(self):
        self.day_count += 1

        day_index = self.days.index(self.day_name)

        self.day_name = self.days[(day_index + 1) % 7]

    def decrement(self):
        self.day_count -= 1

        day_index = self.days.index(self.day_name)

        self.day_name = self.days[(day_index - 1) % 7]

    def get_day_string(self):
        return "{}, {} Day.".format(self.day_name, ordinal(self.day_count))


class Payments():
    def __init__(self, inshore_pots, offshore_pots, hotel):
        self.inshore = inshore_pots
        self.offshore = offshore_pots
        self.hotel = hotel


class Fees():
    def __init__(self, inshore_pots, offshore_pots, boat, rent):
        self.inshore = inshore_pots
        self.offshore = offshore_pots
        self.boat = boat
        self.rent = rent


class Dictator():
    def __init__(self, name, mood):
        self.name = name
        self.mood = mood


# Main Game Functions
#=====================#

GAME = Game(
    weather=Weather(
        "sunny",
        [],
        "1/6",
        None
    ),
    date=Date(
        1,
        "Monday"
    ),
    payments=Payments(
        inshore_pots=3,
        offshore_pots=5,
        hotel=15
    ),
    fees=Fees(
        inshore_pots=5,
        offshore_pots=-6,
        boat=-150,
        rent=80
    ),
    dictator=Dictator(
        name="Holy Colonel Adolf Mussolini the Malevolent",
        mood="neutral"
    )
)

PLAYER = Player(
    name="",
    cash=0,
    luck=0
)


def intro():
    while True:
        clear()

        print("Welcome to the Lobster Game! ")
        print("In this game, you play the roll of a lonely fisherman, living on an totalitarian, authoritarian island, governed by a tyranical dictator. Sounds fun!\n")

        start_query = super_input(
            "Would you like to start [yes, no]? ",
            ">>> ", str, "I'm sorry, I don't understand.", ">>> ", [
                "y", "n", "yes", "no"
            ]
        )[0].lower()

        if start_query == "y":
            input("Let's get started! (Press <ENTER> to proceed) ")
            break

        elif start_query == "n":
            exit_confirm_query = super_input(
                "Are you sure [yes, no]? ",
                ">>> ", str, "I'm sorry, I don't understand.", ">>> ", [
                    "y", "n", "yes", "no"]
            )[0].lower()

            if exit_confirm_query == "y":
                quit()

            else:
                continue

    welcome_message()

def welcome_message():
    clear()

    print("Type 'skip' to skip through this message at any time or press <ENTER> to proceed.\n")

    starting_messages = [
        f"As has already been said, you play the role of a lonely fisherman who has to try to think smartly about where to place his fishing pots in order to get enough money to live.",
        f"Every morning, on weekdays, you can choose what you want to do. You can either:\n\n\t- 1. Go Lobster fishing.\n\t- 2. Go to the Hotel, or \n\t- 3. Go Back to Sleep.\n",
        f"Hotel work involves doing various work at the hotel on the island that nobody can ever afford to go to. By doing this, you save yourself the chore of Lobster Fishing and earn {money(GAME.payments.hotel)}, but you cannot go Lobster Fishing.",
        f"Going back to bed involves, well... going back to bed. It doesn't do much at all.",
        f"Finally, the main option is lobster fishing. You make your way out of the shack you live in to your boat. You then need to decide where to place your pots.",
        f"There are two options: inshore and offshore. On a normal, clear day, you will get {money(GAME.payments.inshore)} from any inshore pots you place and {money(GAME.payments.offshore)} from any offshore pots.",
        f"However, if there is a storm (which there is a {GAME.weather.chance} of happening), all offshore pots are destroyed and you will have to pay {money(GAME.fees.offshore, is_fee=True)}. Since there is no offshore pots, supply and demand mean that you will now recieve {money(GAME.fees.inshore, is_fee=True)} for each pot you placed.\n\n"
        f"Finally, there is one final situation. If you get bad weather three times in a row, there is a HURRICANE, which destroys your boat. New ones cost {money(GAME.fees.boat, is_fee=True)}. Eek.",
        f"At the end of the week, you have to pay {money(GAME.fees.rent)} as rent for your shack. If you can't pay this much, you lose."
    ]

    for message in starting_messages:
        enter_or_skip = input(message + " ")

        if enter_or_skip == "skip":
            return

        else:
            print("")

    print("Here is the loss/gains in each situation summarized:")
    payment_table(boat=True)

    input("\nGood luck! ")

def wakeup_menu(help=False):
    print("You stand beside your bed with a feeling of uncertantity. What do you want to do today?")

    print("")

    print("\t1. Go Lobster Fishing")
    print("\t2. Go to the Hotel")
    print("\t3. Go back to sleep, I'm too tired.")

    print("")

    if not help:
        selected_query = super_input(
            "What would you like to do?",
            ">>> ",
            str,
            "I'm sorry, I don't understand:",
            ">>> ",
            ["1", "2", "3"]
        )

    else:
        selected_query = super_input(
            "What would you like to do?",
            ">>> ",
            str,
            "During the tutorial you're only allowed to go Lobster fishing. Try again:",
            ">>> ",
            ["1"]
        )

    if selected_query == "1":
        return "lobster_fishing"

    elif selected_query == "2":
        return "hotel_work"

    elif selected_query == "3":
        return "sleep_in"


def afternoon_menu(help=False):
    print("You look up the beach and gaze upon your residence. What do you want to do?")

    print("")

    print("\t1. Go back to your house.")

    print("")

    if not help:
        selected_query = super_input(
            "What would you like to do?",
            ">>> ",
            str,
            "I'm sorry, I don't understand:",
            ">>> ",
            ["1"]
        )

    else:
        selected_query = super_input(
            "What would you like to do?",
            ">>> ",
            str,
            "I'm sorry, I don't understand:",
            ">>> ",
            ["1"]
        )

    if selected_query == "1":
        return "house"

def name():
    clear()

    while True:
        print("What would you like to be called?")
        name = input(">>> ").title()

        confirm = input(f"\nAre you sure you want to be called '{name}'? [Y,n] ").lower()

        if confirm == "y" or confirm == "":
            break

        print("")

    print("")

    input("That's a bit of a stupid name. Press <ENTER> to continue. ")

    PLAYER.name = name

def money(value, sign="£", is_fee=False):
    # Converts a
    if value >= 0:
        return sign + str(value)

    elif value < 0 and is_fee:
        return sign + str(value * -1)

    else:
        return f"-{sign}" + str(value)[1:]


def payment_table(boat=False):
    # Prints a table which contains information on the price of pots and boats.
    if not boat:
        print("Weather | Inshore | Offshore")
        print("----------------------------")
        print(f"Good    | {money(GAME.payments.inshore)}      | {money(GAME.payments.offshore)}    ")
        print(f"Bad     | {money(GAME.fees.inshore)}      | {money(GAME.fees.offshore)}     ")

    else:
        print("Weather  | Inshore | Offshore | Boat")
        print("------------------------------------")
        print(f"Good     | {money(GAME.payments.inshore)}      | {money(GAME.payments.offshore)}       | £0  ")
        print(f"Bad      | {money(GAME.fees.inshore)}      | {money(GAME.fees.offshore)}      | £0  ")

        print("Huricane | {}      | {}      | {}  ".format(
            money(GAME.fees.inshore),
            money(GAME.fees.offshore),
            money(GAME.fees.boat)
        ))

def calculate_revenue(pot_choices):
    inshore, offshore = pot_choices[0], pot_choices[1]

    if GAME.weather.current == "good":
        return [inshore * GAME.payments.inshore, offshore * GAME.payments.offshore]

    elif GAME.weather.current == "bad" or GAME.weather.current == "hurricane":
        return [inshore * GAME.fees.inshore, offshore * GAME.fees.offshore]

def summarize_revenue(revenue):
    clear()

    inshore, offshore = revenue[0], revenue[1]

    if inshore < 0:
        print(f"You lost {money(inshore, is_fee=True)} due to the bad weather conditions from your inshore pots.")

    elif inshore == 0:
        print(f"Since you didn't have any inshore pots, you made nothing from them.")

    elif inshore > 0:
        print(f"From your inshore pots, you made {money(inshore)} due to the weather conditions. Well done!")

    print("")

    if offshore < 0:
        print(f"You lost {money(offshore, is_fee=True)} due to the bad weather conditions from your offshore pots.")

    elif offshore == 0:
        print(f"Since you didn't have any offshore pots, you made nothing from them.")

    elif offshore > 0:
        print(f"From your offshore pots, you made {money(offshore)} due to the good weather conditions. Well done!")

    print("")

    if inshore + offshore < 0:
        print(f"This means you lost a total of {money(inshore + offshore, is_fee=True)}.")

    elif inshore + offshore == 0:
        print("In total, you made nothing. The losses/gains counter-acted themselves.")

    else:
        print(f"This means that you made a toal of {money(inshore + offshore)}. Congrats!")

    print("")

    new_player_cash = PLAYER.cash + sum(revenue)

    if new_player_cash < 0:
        print(f"All of this means that you are now indebted {money(new_player_cash, is_fee = True)} to the state, so we will say you have '{money(new_player_cash)}' in cash. You previously had {money(PLAYER.cash)} in cash. If you still are in debt by next Sunday, you will be executed.")

    elif new_player_cash == 0:
        print(f"You now have {money(new_player_cash)} in total, which may be problamatic due to the fact you have to pay {money(GAME.fees.rent, is_fee=True)} for rent on Sunday. You previously had {money(PLAYER.cash)} in cash.")

    elif sum(revenue) < 0 and new_player_cash > 0:
        # The player lost money but still has a positive monetary value.
        print(f"All of this means that at the end of the day you're left with {money(new_player_cash)}. You previously had {money(PLAYER.cash)} in cash.")

    else:
        print(f"Now you've gained {money(sum(revenue))}, you've got {money(new_player_cash)}! You previously had {money(PLAYER.cash)} in cash.")

    input("(Press <ENTER> to continue) ")

    clear()

def pot_amount(pot_type, previous=None):
    previous_type = list(
        filter(lambda x: x != pot_type, ["inshore", "offshore"]))[0]

    if previous == None:
        pot_range = list("123456")

    elif previous == 6:
        print(f"Since you've chosen all {previous_type} pots, you cannot choose any more {pot_type} pots.")

        return 0

    else:
        pot_range = 6 - previous
        pot_range = "".join(list(map(lambda x: str(x + 1), range(pot_range))))

    pots = input(f"How many {pot_type} pots would you like [{pot_range[0]}-{pot_range[-1]}, help] >>> ").lower()

    while pots == "" or pots not in pot_range:
        if pots == "help":
            print("\nYou are currently deciding many pots you would like to place inshore and offshore for lobster fishing. Here is the reward/loss in different situations summarized:")

            print("")

            payment_table()

            print("")

            print("Please try again: ")
            pots = input(f"How many {pot_type} pots would you like [{pot_range[0]}-{pot_range[-1]}, help] >>> ").lower()

            print("")

        else:
            print(f"\nI'm sorry, I don't understand what you mean by '{pots}'. Please try again:")
            pots = input(f"How many {pot_type} pots would you like [{pot_range[0]}-{pot_range[-1]}, help] >>> ").lower()

            print("")

    print("")

    return int(pots)

def inshore_offshore():
    while True:
        inshore = pot_amount("inshore")
        offshore = pot_amount("offshore", previous=inshore)

        print(f"You've chosen {inshore} inshore pots and {offshore} offshore pots.\n")
        happy = super_input(
            "Are you happy with this choice?",
            "[Y,n] >>> ",
            str,
            "Sorry, I don't understand what you mean. Please try again:",
            "[Y,n] >>> ",
            ["yes","no","y","n",""]
        )

        if happy == "yes" or happy == "y" or happy == "":
            break

        else:
            print("Ok, you can reselect:\n")


    return [inshore, offshore]

def test():
    while True:
        exec(input(">>> "))

def main():
    name()
    clear()

    while True:
        clear()

        day_info = GAME.date.get_day_string()
        print(day_info)
        print("="*len(day_info))

        print("")

        print(f"Hello, {PLAYER.name}. You currently have {money(PLAYER.cash)} in cash.\n")

        if GAME.date.day_name == "Saturday":
            print("It's Satuday! If you had a life, you could probably spend your time productively.")
            input("(At this stage of the development of the game, you can't do anything. Once you've accepted this, hit <ENTER>) ")

        elif GAME.date.day_name == "Sunday":
            input("It's Sunday, AKA PAYMENT DAY! (Press <ENTER> to continue) ")
            print("Let's see if you have enough money..\n.")

            sleep(3)

            if PLAYER.cash < 80:
                input(f"Uh-oh. You only have {money(PLAYER.cash)}. Bye! ")
                quit()

            elif PLAYER.cash < 100:
                input(f"You're really scraping the barrel with this one. ")
                input(f"Since you have {money(PLAYER.cash)}, you're left with {money(PLAYER.cash - GAME.fees.rent)}. ")

                print("")

                input("(Press <ENTER> to continue) ")

                PLAYER.cash -= GAME.fees.rent

            else:
                input(f"Since you have {money(PLAYER.cash)}, you're left with {money(PLAYER.cash - GAME.fees.rent)}. ")

                print("")

                input("(Press <ENTER> to continue) ")

                PLAYER.cash -= GAME.fees.rent

        else:
            activity = wakeup_menu()

            print(activity)

            if activity == "lobster_fishing":
                # Lobster Fishing
                clear()
                print("You've chosen: Lobster Fishing\n")

                lobster_fishing()

            elif activity == "hotel_work":
                # Hotel Work
                clear()
                print("You've chosen: Hotel Work\n")

                hotel_work()

            elif activity == "sleep_in":
                # Sleep In
                clear()
                print("You've chosen: Sleeping In?\n")
                
                sleep_in()


        #######
        GAME.date.increment()

def lobster_fishing():
    pots = inshore_offshore()

    weather_current = GAME.weather.storm()

    if len(GAME.weather.history) > 1:
        if weather_current == "bad" and weather_current[-2:] == ["bad", "bad"]:
            GAME.weather.set_weather("hurricane")

    elif weather_current == "bad":
        GAME.weather.set_weather("bad")

    else:
        GAME.weather.set_weather("good")

    if GAME.weather.current == "good":
        print("Watching from the shore you see the weather is...\n")
        sleep(3)

        print("Good!")

        input("\n(Press <ENTER> to continue) ")

        revenues = calculate_revenue(pots)
        summarize_revenue(revenues)

        PLAYER.cash += sum(revenues)

    elif GAME.weather.current == "bad":
        print("Watching from the shore you see the weather is...\n")
        sleep(3)

        print("Bad! Poor luck.")

        input("\n(Press <ENTER> to continue) ")

        revenues = calculate_revenue(pots)
        summarize_revenue(revenues)

        PLAYER.cash += sum(revenues)

    elif GAME.weather.current == "hurricane":
        print("Watching from the shore you see...\n")
        sleep(3)

        print("A swirling torrent of wind causing havoc as it sweeps across the offshore bay, unfortunately destroying your boat!")

        input("\n(Press <ENTER> to continue) ")

        PLAYER.has_boat = False

        revenues = calculate_revenue(pots)
        summarize_revenue(revenues)

        PLAYER.cash += sum(revenues)

        if PLAYER.cash >= GAME.fees.boat:
            purchase_boat = super_input(f"You currently have {money(PLAYER.cash)}, which is enough to purchase a {money(GAME.fees.boat, is_fee=True)} boat. Would you like to do so? ",
            ">>>",
            str,
            "I'm sorry, I don't understand. Please try again:",
            ">>> ",
            ["yes", "no", "y", "n"]).lower()[0]

            if purchase_boat == "y":
                print(f"\nYou have purchased a new boat. You currently have {money(PLAYER.cash)}.")

                input("\n(Press <ENTER> to continue) ")

            else:
                input("\nOk, this does mean you cannot go fishing tomorrow unless you buy a boat.\n\n(Press <ENTER> to continue) ")




def hotel_work():
    clear()
    
    print("You walk to the hotel that nobody can afford to work at and request to work.\n")

    activity = random.choice([
        "dish washing"
    ])

    if activity == "dish washing":
        print(f"You walk to the hotel kitchen and see the great amount of dishes stacked up next to the sink. You are passed some soap and a cloth.")

        print("\nPress the letters that come up on screen.")

        input("(Press <ENTER> to continue) ")

        for i in range(50):
            print("")

            letter = random.choice(list("abcdefghijklmnopqrstuvwxyz"))
            char = input(f"{letter} ({i+1}/50) >>> ")

            while letter[0] != char:
                print("\nTry again:")
                char = input(f"{letter} ({i+1}/50) >>> ")

        print("")

        input("You've finished washing the dishes. Press <ENTER> to wrap up your work at the hotel. ")

    clear()

    PLAYER.cash += GAME.payments.hotel

    print(f"You are given {money(GAME.payments.hotel)} for your services, making your current cash {money(PLAYER.cash)}.")

    print("")

    input("(Press <ENTER> to continue) ")


def sleep_in():
    print("Why have you chosen that? You can't feel tired, this is a game! You've wasted some valuable fishing/working time. I hope you feel really happy.\n")

    input("(Press <ENTER> to sleep) ")

def setup():
    pass

if __name__ == "__main__":
    #intro()
    #main()
    test()
