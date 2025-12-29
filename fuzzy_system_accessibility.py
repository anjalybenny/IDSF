import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

language_availability = ctrl.Antecedent(np.arange(0, 6, 1), 'Language availability')
screen_reader_compliance = ctrl.Antecedent(np.arange(0, 6, 1), 'Screen-reader compliance')
mobile_responsiveness= ctrl.Antecedent(np.arange(0, 6, 1), 'Mobile responsiveness')
form_accessibility = ctrl.Antecedent(np.arange(0, 6, 1), 'Form accessibility')
accessibility = ctrl.Consequent(np.arange(0, 101, 1), 'accessibility')

language_availability.automf(3)
screen_reader_compliance.automf(3)
mobile_responsiveness.automf(3)
form_accessibility.automf(3)

accessibility['Not accessible enough'] = fuzz.trimf(accessibility.universe, [0, 0, 50])
accessibility['Accessible enough'] = fuzz.trimf(accessibility.universe, [50, 75, 100])
accessibility['Really accessible'] = fuzz.trimf(accessibility.universe, [80, 100, 100])

# really accessible rule
rule1 = ctrl.Rule((language_availability['good'] | language_availability['average']) & (screen_reader_compliance['good'] | screen_reader_compliance['average']) & (mobile_responsiveness['good'] | mobile_responsiveness['average'] ) & (form_accessibility['good']|form_accessibility['average']) & ~(language_availability['good'] & screen_reader_compliance['average'] & mobile_responsiveness['average'] & form_accessibility['average']) & ~(language_availability['average'] & screen_reader_compliance['good'] & mobile_responsiveness['average'] & form_accessibility['average']) & ~(language_availability['average'] & screen_reader_compliance['average'] & mobile_responsiveness['good'] & form_accessibility['average']) & ~(language_availability['average'] & screen_reader_compliance['average'] & mobile_responsiveness['average'] & form_accessibility['good']) & ~(language_availability['average'] & screen_reader_compliance['average'] & mobile_responsiveness['average'] & form_accessibility['average']), accessibility['Really accessible'])

# Accessible enough
rule2 = ctrl.Rule((language_availability['good'] & screen_reader_compliance['average'] & mobile_responsiveness['average'] & form_accessibility['average']) | (language_availability['average'] & screen_reader_compliance['good'] & mobile_responsiveness['average'] & form_accessibility['average']) | (language_availability['average'] & screen_reader_compliance['average'] & mobile_responsiveness['good'] & form_accessibility['average']) | (language_availability['average'] & screen_reader_compliance['average'] & mobile_responsiveness['average'] & form_accessibility['good']), accessibility['Accessible enough'])
rule3 = ctrl.Rule((language_availability['good']| language_availability['poor']) &  (screen_reader_compliance['good'] | screen_reader_compliance['poor']) & (mobile_responsiveness['good']| mobile_responsiveness['poor']) & (form_accessibility['good'] | form_accessibility['poor']) & ~(language_availability['good'] & screen_reader_compliance['good'] & mobile_responsiveness['good'] & form_accessibility['good']) & ~((screen_reader_compliance['poor'] & mobile_responsiveness['poor'] & form_accessibility['poor']) | (language_availability['poor'] & mobile_responsiveness['poor'] & form_accessibility['poor']) | (language_availability['poor'] & screen_reader_compliance['poor'] &  form_accessibility['poor']) | (language_availability['poor'] & screen_reader_compliance['poor'] & mobile_responsiveness['poor'])), accessibility['Accessible enough'])
rule4 = ctrl.Rule((language_availability['poor'] | language_availability['average']) & (screen_reader_compliance['poor'] | screen_reader_compliance['average']) & (mobile_responsiveness['poor'] | mobile_responsiveness['average'] ) & (form_accessibility['poor']|form_accessibility['average']) & ~(language_availability['average'] & screen_reader_compliance['poor'] & mobile_responsiveness['poor'] & form_accessibility['poor']) & ~(language_availability['poor'] & screen_reader_compliance['average'] & mobile_responsiveness['poor'] & form_accessibility['poor']) & ~(language_availability['poor'] & screen_reader_compliance['poor'] & mobile_responsiveness['average'] & form_accessibility['poor']) & ~(language_availability['poor'] & screen_reader_compliance['poor'] & mobile_responsiveness['poor'] & form_accessibility['average']) & ~(language_availability['poor'] & screen_reader_compliance['poor'] & mobile_responsiveness['poor'] & form_accessibility['poor']), accessibility['Accessible enough'])

# not accessible enough
rule5 = ctrl.Rule((screen_reader_compliance['poor'] & mobile_responsiveness['poor'] & form_accessibility['poor']) | (language_availability['poor'] & mobile_responsiveness['poor'] & form_accessibility['poor']) | (language_availability['poor'] & screen_reader_compliance['poor'] &  form_accessibility['poor']) | (language_availability['poor'] & screen_reader_compliance['poor'] & mobile_responsiveness['poor']), accessibility['Not accessible enough'])

calculate_accessibility_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])

def compute_accessibility(answer_language_avail, answer_screen_read, answer_mobile_resp, answer_form_access):
    calculating_accessibility_ctrl = ctrl.ControlSystemSimulation(calculate_accessibility_ctrl)
    

    calculating_accessibility_ctrl.input['Language availability'] = answer_language_avail
    calculating_accessibility_ctrl.input['Screen-reader compliance'] = answer_screen_read
    calculating_accessibility_ctrl.input['Mobile responsiveness'] = answer_mobile_resp
    calculating_accessibility_ctrl.input['Form accessibility'] = answer_form_access

    calculating_accessibility_ctrl.compute()

    return calculating_accessibility_ctrl.output['accessibility']

if __name__== "__main__":
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

    result = compute_accessibility(answer_lang, answer_screen,  answer_mobile, answer_form)
    print(result)


