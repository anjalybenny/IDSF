import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from fuzzy_system_clarity import compute_clarity
from fuzzy_system_accessibility import compute_accessibility
from fuzzy_system_navigation import compute_navigation
from fuzzy_system_fairness import compute_fairness

clarity = ctrl.Antecedent(np.arange(0, 101, 1), 'clarity')
accessibility = ctrl.Antecedent(np.arange(0, 101, 1), 'accessibility')
navigation = ctrl.Antecedent(np.arange(0, 101, 1), 'navigation')
fairness = ctrl.Antecedent(np.arange(0, 101, 1), 'fairness')
inclusivity = ctrl.Consequent(np.arange(0, 101, 1), 'inclusivity')

clarity.automf(3)
accessibility.automf(3)
navigation.automf(3)
fairness.automf(3)

inclusivity['Not inclusive enough'] = fuzz.trimf(inclusivity.universe, [0, 0, 70])
inclusivity['Inclusive enough'] = fuzz.trimf(inclusivity.universe, [50, 75, 100])
inclusivity['Really inclusive'] = fuzz.trimf(inclusivity.universe, [80, 100, 100])

# really inclusive rule
rule1 = ctrl.Rule(clarity['good'] & accessibility['good'] & navigation['good'] & fairness['good'], inclusivity['Really inclusive'])
# fair enough
rule2 = ctrl.Rule((clarity['good']| clarity['average']) & (accessibility['good'] | accessibility['average']) & (navigation['good'] | navigation['average']) & (fairness['good'] | fairness['average']) & ~(clarity['good'] & accessibility['good'] & navigation['good'] & fairness['good']), inclusivity['Inclusive enough'])
# not clear enough2
rule3 = ctrl.Rule(clarity['poor'] | accessibility['poor']| navigation['poor'] | fairness['poor'], inclusivity['Not inclusive enough'])
calculate_inclusivity_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
def compute_inclusivity(answer_clarity, answer_accessibility, answer_navigation, answer_fairness):
    calculating_inclusivity_ctrl = ctrl.ControlSystemSimulation(calculate_inclusivity_ctrl)

    calculating_inclusivity_ctrl.input['clarity'] = answer_clarity
    calculating_inclusivity_ctrl.input['accessibility'] = answer_accessibility
    calculating_inclusivity_ctrl.input['navigation'] = answer_navigation
    calculating_inclusivity_ctrl.input['fairness'] = answer_fairness

    calculating_inclusivity_ctrl.compute()

    return calculating_inclusivity_ctrl.output['inclusivity']

if __name__== "__main__":
    while True:
        try:
            answer_read = float(input("How was the readability of this digital public service on a scale from 0 to 5?: "))
            if 0 <= answer_read <= 5:
                break
            else:
                print("This number is not between 0 and 5")
            
        except ValueError:
            print("Your input was not a number.")

    while True:
        try:       
            answer_guid= float(input("How was the guidance of this digital public service on a scale from 0 to 5?: "))
            if 0 <= answer_guid <= 5:
                break
            else:
                print("This number is not between 0 and 5")
            
        except ValueError:
            print("Your input is not a number.")
    
    while True:
        try:
            answer_termin = float(input("How were is the terminologies explained of this digital public service on a scale from 0 to 5?: "))
            if 0 <= answer_termin <= 5:
                break
            else:
                print("This number is not between 0 and 5")

        except ValueError:
            print("Your input was not a number.")

    while True:
        try:
            answer_ton = float(input("How was the tone consistency of this digital public service on a scale from 0 to 5?: "))
            if 0 <= answer_ton <= 5:
                break
            else:
                print("This number is not between 0 and 5")

        except ValueError:
            print("Your input was not a number.")

    answer_clar = compute_clarity(answer_read, answer_guid, answer_termin, answer_ton)

    while True:
        try:
            answer_lang = float(input("How was the language availability of this digital public service on a scale from 0 to 5?: "))
            if 0 <= answer_lang <= 5:
                break
            else:
                print("This number is not between 0 and 5")
            
        except ValueError:
            print("Your input was not a number.")

    while True:
        try:
            answer_screen= float(input("How was the screen reader compliance of this digital public service on a scale from 0 to 5?: "))
            if 0 <= answer_screen <= 5:
                break
            else:
                print("This number is not between 0 and 5")
            
        except ValueError:
            print("Your input was not a number.")

    while True:
        try:
            answer_mobile = float(input("How was the mobile responsiveness is the terminologies explained of this digital public service on a scale from 0 to 5?: "))
            if 0 <= answer_mobile  <= 5:
                break
            else:
                print("This number is not between 0 and 5")
        except ValueError:
            print("Your input was not a number.")

    while True:
        try:
            answer_form = float(input("How was the form accessibility of this digital public service on a scale from 0 to 5?: "))
            if 0 <= answer_form <= 5:
                break
            else:
                print("This number is not between 0 and 5")
        except ValueError:
            print("Your input was not a number.")
    
    answer_access = compute_accessibility(answer_lang, answer_screen, answer_mobile, answer_form)

    while True:
        try:
            answer_search = float(input("How was the search effectiveness of this digital public service on a scale from 0 to 5?: "))
            if 0 <=  answer_search <= 5:
                break
            else:
                print("This number is not between 0 and 5")
            
        except ValueError:
            print("Your input was not a number.")

    while True:
        try:
            answer_error= float(input("How was the error feedback of this digital public service on a scale from 0 to 5?: "))
            if 0 <=  answer_error <= 5:
                break
            else:
                print("This number is not between 0 and 5")
        except ValueError:
            print("Your input was not a number.")

    while True:
        try:    
            answer_menu = float(input("How was the menu consistency of this digital public service on a scale from 0 to 5?: "))
            if 0 <=  answer_menu <= 5:
                break
            else:
                print("This number is not between 0 and 5")
        except ValueError:
            print("Your input was not a number.")

    while True:
        try:    
            answer_task = float(input("How was the task completion of this digital public service on a scale from 0 to 5?: "))
            if 0 <=  answer_task <= 5:
                break
            else:
                print("This number is not between 0 and 5")
        except ValueError:
            print("Your input was not a number.")

    answer_nav = compute_navigation(answer_search, answer_error, answer_menu, answer_task)

    while True:
        try:
            answer_parity = float(input("How was the language availability of this digital public service on a scale from 0 to 5?: "))
            if 0 <=  answer_parity <= 5:
                break
            else:
                print("This number is not between 0 and 5")
            
        except ValueError:
            print("Your input was not a number.")

    while True:
        try:
            answer_transparency = float(input("How was the screen reader compliance of this digital public service on a scale from 0 to 5?: "))
            if 0 <=  answer_transparency <= 5:
                break
            else:
                print("This number is not between 0 and 5")
            
        except ValueError:
            print("Your input was not a number.")

    while True:
        try:
            answer_equal = float(input("How was the mobile responsiveness is the terminologies explained of this digital public service on a scale from 0 to 5?: "))
            if 0 <=  answer_equal <= 5:
                break
            else:
                print("This number is not between 0 and 5")

        except ValueError:
            print("Your input was not a number.")

    while True:
        try:
            answer_inclusive = float(input("How was the form fairness of this digital public service on a scale from 0 to 5?: "))
            if 0 <=  answer_inclusive <= 5:
                break
            else:
                print("This number is not between 0 and 5")

        except ValueError:
            print("Your input was not a number.")

    answer_fair = compute_fairness(answer_parity, answer_transparency, answer_equal, answer_inclusive)
    
    result = compute_inclusivity(answer_clar, answer_access, answer_nav, answer_fair)
    print('The inclusivity is', result)


