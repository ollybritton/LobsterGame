import cmd
import sys
import os
import time
import json
import random
import textwrap

# TESTING controls how the game acts and will speed things certain things up for testing purposes.
TESTING = False

# Sets the maximum width that the text can go.
SCREEN_WIDTH = 100

# Sets how fast the text is written on the screen when there is the one letter at a time effect.
DEFAULT_DELAY = [0.1, 0.2]

# Controls if the user should have to hit enter at the end of every line of written text.
DEFAULT_INPUT = False

# Speeds up/slows down all wait times to make gameplay faster. 2 = twice as fast, 0.5 = double speed.
SPEED_MODIFIER = 4

# Defines wether to use the command prompt commands to clear the screen, or just print a bunch of times. Useful for when testing the code using IDLE. The first value is whether to do so, and the second value is the amount of times.
CLEAR_PRINT = [False, 100]

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


def super_input(initial, initial_input, input_type, reprompt, reprompt_input, accepted=[]):
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

        if given_input.lower() not in accepted:
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


class Fees():
    def __init__(self, inshore_pots, offshore_pots, boat):
        self.inshore = inshore_pots
        self.offshore = offshore_pots


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
        boat=-150
    ),
    dictator=Dictator(
        name="Holy Colonel Adolf Mussolini the Malevolent",
        mood="neutral"
    )
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
            return

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


def weekday_wakeup_menu(help=False):
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


def payment_table():
    print("Weather | Inshore | Offshore")
    print("----------------------------")
    print("Good    | £{}      | £{}    ".format(
        GAME.payments.inshore, GAME.payments.offshore)
    )
    print("Bad     | £{}      | {}     ".format(
        GAME.fees.inshore, "-£" + str(GAME.fees.offshore)[1:]))


def game_help():
    help_needed_query = super_input(
        "Would you like some help to get you started [y, n]?",
        ">>> ",
        str,
        "I'm sorry, I don't understand. Try again:",
        ">>> ",
        ["y", "n", "yes", "no"]
    )[0].lower()

    if help_needed_query == "y":
        clear()

        # Print the current day.
        print(GAME.date.get_day_string())

        # Add some space in the layout.
        print("")

        write_text("Since this is your first day on this island, the Dictator, who you now know to be named {}, is cutting you off some slack. He's going to give you a chance to prove your skills as a lobster fisherman, and is only going to fine you £40 at the end of the week, instead of the full £80.".format(GAME.dictator.name))

        print("")

        write_text(
            "To go lobster fishing, and thus prove your worth, you need to select 'Go Lobster Fishing' on the Wakeup Menu."
        )

        print("")

        # Print a wakeup menu - a list of things that you can do in the morning.
        weekday_wakeup_menu(help=True)

        print("")

        write_text("You make your way out of your tiny shack, and your eyes gaze upon what is your boat, when in reality it's just a falling apart mess.")

        print("")

        write_text("Here is where you get to make a crucial decision - how many lobsters you want to put where. You can put them in two places: inshore & offshore. When the weather is good, the amount you will be payed is like this:")

        print("")

        print("\tInshore: £{} per lobster inshore.".format(GAME.payments.inshore))
        print("\tOffshore: £{} per lobster offshore.".format(
            GAME.payments.offshore))

        print("")

        input("(Press <ENTER> to continue) ")

        print("")

        write_text("However, that is only when the weather is good. When the weather is bad, if you have any offshore lobster pots, they get swept away into the ocean and broken, and you have to pay for new ones straight away. However, since demand has gone up for lobsters, the ones inshore (which are protected from the storm) pay you more. Or put simply:")

        print("")

        print("\tInshore: £{} per lobster inshore.".format(GAME.fees.inshore))
        print("\tOffshore: {} per lobster offshore.".format(
            "-£" + str(GAME.fees.offshore)[1:])
        )

        print("")

        input("(Press <ENTER> to continue) ")

        print("")

        write_text("So, to recap:")

        print("")

        # Render a payment table.
        payment_table()

        print("")

        write_text(
            "Finally, there is also the very slim chance of a hurricane. This occurs when there is bad weather 3 times in a row.")

    else:
        return


def main():
    while True:
        clear()

        # Print the current day.
        write_text(GAME.date.get_day_string())

        # Add some space in the layout.
        print("")

        # If it's the first time for the user, help them a bit.
        if(GAME.date.day_count == 1):
            game_help()

        GAME.date.increment()


if __name__ == "__main__":
    main()
