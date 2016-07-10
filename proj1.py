import random

TOTAL_DAYS = 31
INITIAL_WILLPOWER = 5
EVIL_MODE = False

"""Utility Functions"""

def input_loop(input_function, input_message):
    """repeated requesting input and test with input_function, 
    until the input_fucntion returns True."""
    def input_check():
        input_space = "\n>> "
        user_input = input(input_message + input_space)
        while (not input_function(user_input)) :
            print("invalid input, please try again\n")
            user_input = input(input_message + input_space)
        return user_input
    return input_check
    
def check_float_input(threshold = 0):
    """"check if input is a float that is greater or equal to threshold"""
    def check_float(input_):
        try:
            return float(input_) >= threshold
        except ValueError:
            return False
    return check_float
        
    
def check_int_input(threshold = 0):
    """check if input is an integer that is greater or equal to the threshold."""
    def check_int(input_):
        try:
            return int(input_) >= threshold
        except ValueError:
            return False
    return check_int
        
    
class runiform:
    """random factor for all activities, based on a uniform distribution
    with different parameters."""
    def __init__(self, a, b):
        self._a = a / 100.0
        self._b = b / 100.0

    def toss_value(self):
        """returns a random value if the distribution"""
        return random.random() * self._a + self._b

    def toss_bool(self, threhold):
        """takes a percentile as threhold, if the generated value is above the
        percentile, return 1 else return 0."""
        return random.random() >= (threhold / 100.0)
    
class Activity:
    INITIAL_WP_COST = 0.0
    CONVERSION_RATE = 0.0
    RANDOM_FACTOR = runiform(1, 0)
    
    def __init__(self, person):
        self.performer = person
        
    def perform(self, wp_input):
        return None

    def get_wp_cost(self):
        return self.INITIAL_WP_COST
    

class Do_hw(Activity):
    INITIAL_WP_COST = 3.0
    CONVERSION_RATE = 0.5
    RANDOM_FACTOR = runiform(40, 70)
    HARD_QUESTION_RATE = 1.5
    
    def perform(self, wp_input):
        progress = round(wp_input * (Do_hw.CONVERSION_RATE + self.performer.get_competitiveness() / 100.0) * \
        Do_hw.RANDOM_FACTOR.toss_value(), 2) + self.hard_question()
        self.performer.boost_hw(progress)
        print("You have successfully finished " + str(progress) + " of your hw")
        
    def hard_question(self):
        if Do_hw.RANDOM_FACTOR.toss_bool(0):
            input_message = "You haven enountered a very difficult question,\
            \nwould you invest 1 unit of willpower to ask for help?\
            \nif so, type any number > 0, otherwise type 0." 
            check_wp = check_float_input(0)
            check_input = input_loop(check_wp, input_message)
            user_input = check_input()
            if user_input == '0':
                return 0
            else:
                if self.performer.spend_wp(1):
                    progress = 1 * Do_hw.HARD_QUESTION_RATE
                    self.performer.boost_hw(progress)
                    return progress
                else:
                    return 0
        
class Gaming(Activity):
    """increase competiveness more willpower investment 
    increases competivenss on a diminishing marginal return"""
    INITIAL_WP_COST = 2.0
    CONVERSION_RATE = 3
    RANDOM_FACTOR = runiform(30, 80)
    COMPETITIVE_RATE = 4.5
    
    def perform(self, wp_input):
        progress = round(Gaming.CONVERSION_RATE * wp_input * Gaming.RANDOM_FACTOR.toss_value() + self.ranked(), 2)
        self.performer._competitiveness += progress
        print("Your competitiveness has increase to {0}".format(self.performer.get_competitiveness()))
        
    def ranked(self):
        input_message = "Would you like to spent extra will power(minimum 1) to play ranked games\
        \nenter the amount of willpower you want to spend to play more competitively"
        check_input = input_loop(check_float_input(1), input_message) 
        user_input = float(check_input())
        if user_input == 0:
            return 0
        else:
            if self.performer.spend_wp(user_input):
                progress = user_input * Gaming.COMPETITIVE_RATE
                self.performer._competitiveness += progress
                return progress        
            
class Exercise(Activity):
    INITIAL_WP_COST = 2.0
    CONVERSION_RATE = 4
    RANDOM_FACTOR = runiform(30, 80)
    
    def perform(self, wp_input):
        progress = round(Exercise.CONVERSION_RATE * wp_input)
        if self.performer._health < 30:
            print("Because your health condition is too bad, \
            \nyou have experienced fatigued, willpower minus 2.")
            self.performer.spend_wp_exhaust(2)
        self.performer._health += progress
        print("Your health has increased to {0}".format(self.performer._health))
        
class Sleep_early(Activity):
    CONVERTION_RATE = 3
    
    def perform(self, wp_input):
        progress = round(Sleep_early.CONVERTION_RATE *wp_input)
        self.performer._sleep_quality += progress
        print("Your sleep quality has increased to {0}".format(self.performer._sleep_quality))
        
        
class Person:
    # the person class for the main character
        def __init__(self, name):
            self._name = name
            self._willpower = INITIAL_WILLPOWER
            self._daily_wp = self._willpower
            self._sleep_quality = 5.0
            self._health = 5.0
            self.day = 1.0
            self._competitiveness = 0.0
            self._hw_progress = 0.0
            # initializing activity class
            self._activities = {"hw":Do_hw(self), 'gaming':Gaming(self),
                                'exercise':Exercise(self), 'sleep early':Sleep_early(self)}
            
        def perform_activity(self, activity, wp_input):
            """assumer ACTIVITY is a valid string which specifies which activity to perform"""
            selected_activity = self._activities[activity]
            if wp_input < selected_activity.get_wp_cost():
                print("Do not meet minimum willpower for this activity")
            elif self.spend_wp(wp_input):
                selected_activity.perform(wp_input)
            return False


        def rest(self):
            # reset the daily willpower based on health and sleep_quality
            self.day += 1
            sleep_random = runiform(30, 80)
            self._daily_wp = round((1 + self._health / 100.0 + self._sleep_quality / 100.0) * self._willpower *
                                   sleep_random.toss_value())
            print("You are now resting, ZZZZZZZ", "\n\n")
            self.status()
        
        def sleep_early(self):
            """will increase sleeping quality, which is a factor of the nextday's will power regneration"""
            pass
        
        def get_daily_wp(self):
            return self._daily_wp
        
        def get_day(self):
            return self.day 
        
        def set_day(self, num):
            """set the current day to num"""
            self.day = num
        
        def get_competitiveness(self):
            return self._competitiveness
        
        def get_daily_wp(self):
            return self._daily_wp

        def get_hw(self):
            return self._hw_progress

        def boost_hw(self, num):
            self._hw_progress += num
            
        def spend_wp(self, num):
            """spend NUM units of willpower, if the character does not have
            enough willpower, return False and print a warning message."""
            if self._daily_wp >= num:
                self._daily_wp -= num
                return True
            else:
                print("Insufficient Willpower")
                return False
                         
        def spend_wp_exhaust(self, num):
            """spend NUM units of willpower, if the character does not have enough
            willpower, spend all the rest of will power and return NUM."""
            if self._daily_wp >= num:
                self._daily_wp -= num
            else:
                temp = self._daily_wp
                self._daily_wp = 0
                return temp
                         
        def status(self): 
            print("Hello, {3}, This is day {0}   \
                  \nYour current willpower is {1} \
                  \nYour current homework progress is {2}."
                  .format(self.day, self._daily_wp, self._hw_progress, self._name))

        def stat(self):
            print("competitiveness: " + str(self._competitiveness))
            print("health index   : " + str(self._health))
            print("sleep quality  : " + str(self_sleep_quality))

def select_activity(input_):
    """return whether input is an integer between 1 to 5"""
    options = {'hw', 'gaming', 'exercise', 'sleep early', 'rest', 'status', 'q', 'help', 'stat'}
    return input_ in options


check_input_command = input_loop(select_activity, "What would you like to do?")
check_input_wp = input_loop(check_float_input(), "How much will power do you want to invest?")

def evil_mode(player):
    """under evil mode, players have to answer QUESTION_TO_WP questions per will \
    \nregenerated each day."""
    QUESTION_TO_WP = 2
    print("Please answer the following questions to regenerate your daily will power \
    \n {0} questions for each will power regenerated by your character.".format(QUESTION_TO_WP))
    def check_answer(answer):
        """higher order function for checking if player input the right ans"""
        def is_answer(input_):
            try:
                if input_ == 'q' or int(input_) == answer :
                    return True
                else:
                    return False
            except ValueError:
                return False
        return is_answer
    
    wp_regenerated = 0
    for i in range(1, player.get_daily_wp() * QUESTION_TO_WP + 1):
        a, b = random.randint(0, 1000), random.randint(0, 1000)
        answer_check = input_loop(check_answer(a + b), 
                                  "What is the sum of {0} and {1}"
                                  .format(a, b))
        if answer_check() == 'q':
            break
        if int(i / QUESTION_TO_WP) > wp_regenerated:
            wp_regenerated = int(i / QUESTION_TO_WP)
            print("\nYou have regenerated {0} willpower, \
                \nyou can still regenerated {1} willpower.\n"
                .format(wp_regenerated, player.get_daily_wp() - wp_regenerated))
    player._daily_wp = wp_regenerated

def main():
        player_name = input("What would you like to be called?\n")
        player = Person(player_name)
        is_evil_mode = input("\n\nWould you like to play evil mode? \
        \nif so, please input 'y', otherwise input anything else. \
        \nevil mode is strongly recommended for people who have completed this game at least once. \
        \nif this is your first time, please do not activate evil mode.\n")
        if is_evil_mode == 'y':
            EVIL_MODE = True
        while (player.get_day() < 31) :
            temp_day = player.get_day()
            if EVIL_MODE:
              evil_mode(player)
            while (player.get_day() == temp_day):
                print()
                user_command = check_input_command()
                if user_command == 'rest':
                    player.rest()
                elif user_command == 'status':
                    player.status()
                elif user_command == 'q':
                    player.set_day(70)
                elif user_command == 'help':
                    print("Here are the commands: \
                    \nq          : quit the game \
                    \nstat       : display your character's different status \
                    \nstatus     : display your character's current day progress \
                    \nrest       : let your character to rest and move to the next day \
                    \nhw         : do homework activity, mini willpower cost:3\
                    \ngaming     : do gaming activity, mini willpower cost:2\
                    \nexercise   : do exercise activity, mini willpower cost:2\
                    \nsleep early: do sleep early activity, mini willpower cost:0")
                else:
                    activity_wp = float(check_input_wp())
                    player.perform_activity(user_command, activity_wp)
                    print("You now have {0} will power.\n".format(player.get_daily_wp()))
                
            temp_day += 1
            if (player.get_hw() >= 100):
                print("Congraz, {0}, you have completed the game!!".format(player._name))
                break

if __name__ == '__main__':
        main()
