import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

parity_languages = ctrl.Antecedent(np.arange(0, 6, 1), 'Parity across languages')
transparency_contact_options = ctrl.Antecedent(np.arange(0, 6, 1), 'Transparency of contact options')
equal_service= ctrl.Antecedent(np.arange(0, 6, 1), 'Equal service access')
inclusiv_imag_ton = ctrl.Antecedent(np.arange(0, 6, 1), 'Inclusive imagery and tone')
fairness = ctrl.Consequent(np.arange(0, 101, 1), 'fairness')

parity_languages.automf(3)
transparency_contact_options.automf(3)
equal_service.automf(3)
inclusiv_imag_ton.automf(3)

fairness['Not fair enough'] = fuzz.trimf(fairness.universe, [0, 0, 50])
fairness['Fair enough'] = fuzz.trimf(fairness.universe, [50, 75, 100])
fairness['Really fair'] = fuzz.trimf(fairness.universe, [80, 100, 100])

# really fair rule
rule1 = ctrl.Rule((parity_languages['good'] | parity_languages['average']) & (transparency_contact_options['good'] | transparency_contact_options['average']) & (equal_service['good'] | equal_service['average'] ) & (inclusiv_imag_ton['good']|inclusiv_imag_ton['average']) & ~(parity_languages['good'] & transparency_contact_options['average'] & equal_service['average'] & inclusiv_imag_ton['average']) & ~(parity_languages['average'] & transparency_contact_options['good'] & equal_service['average'] & inclusiv_imag_ton['average']) & ~(parity_languages['average'] & transparency_contact_options['average'] & equal_service['good'] & inclusiv_imag_ton['average']) & ~(parity_languages['average'] & transparency_contact_options['average'] & equal_service['average'] & inclusiv_imag_ton['good']) & ~(parity_languages['average'] & transparency_contact_options['average'] & equal_service['average'] & inclusiv_imag_ton['average']), fairness['Really fair'])

# fair enough
rule2 = ctrl.Rule((parity_languages['good'] & transparency_contact_options['average'] & equal_service['average'] & inclusiv_imag_ton['average']) | (parity_languages['average'] & transparency_contact_options['good'] & equal_service['average'] & inclusiv_imag_ton['average']) | (parity_languages['average'] & transparency_contact_options['average'] & equal_service['good'] & inclusiv_imag_ton['average']) | (parity_languages['average'] & transparency_contact_options['average'] & equal_service['average'] & inclusiv_imag_ton['good']), fairness['Fair enough'])
rule3 = ctrl.Rule((parity_languages['good']| parity_languages['poor']) &  (transparency_contact_options['good'] | transparency_contact_options['poor']) & (equal_service['good']| equal_service['poor']) & (inclusiv_imag_ton['good'] | inclusiv_imag_ton['poor']) & ~(parity_languages['good'] & transparency_contact_options['good'] & equal_service['good'] & inclusiv_imag_ton['good']) & ~((transparency_contact_options['poor'] & equal_service['poor'] & inclusiv_imag_ton['poor']) | (parity_languages['poor'] & equal_service['poor'] & inclusiv_imag_ton['poor']) | (parity_languages['poor'] & transparency_contact_options['poor'] &  inclusiv_imag_ton['poor']) | (parity_languages['poor'] & transparency_contact_options['poor'] & equal_service['poor'])), fairness['Fair enough'])
rule4 = ctrl.Rule((parity_languages['poor'] | parity_languages['average']) & (transparency_contact_options['poor'] | transparency_contact_options['average']) & (equal_service['poor'] | equal_service['average'] ) & (inclusiv_imag_ton['poor']|inclusiv_imag_ton['average']) & ~(parity_languages['average'] & transparency_contact_options['poor'] & equal_service['poor'] & inclusiv_imag_ton['poor']) & ~(parity_languages['poor'] & transparency_contact_options['average'] & equal_service['poor'] & inclusiv_imag_ton['poor']) & ~(parity_languages['poor'] & transparency_contact_options['poor'] & equal_service['average'] & inclusiv_imag_ton['poor']) & ~(parity_languages['poor'] & transparency_contact_options['poor'] & equal_service['poor'] & inclusiv_imag_ton['average']) & ~(parity_languages['poor'] & transparency_contact_options['poor'] & equal_service['poor'] & inclusiv_imag_ton['poor']), fairness['Fair enough'])

# not fair enough
rule5 = ctrl.Rule((transparency_contact_options['poor'] & equal_service['poor'] & inclusiv_imag_ton['poor']) | (parity_languages['poor'] & equal_service['poor'] & inclusiv_imag_ton['poor']) | (parity_languages['poor'] & transparency_contact_options['poor'] &  inclusiv_imag_ton['poor']) | (parity_languages['poor'] & transparency_contact_options['poor'] & equal_service['poor']), fairness['Not fair enough'])

calculate_fairness_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])

def compute_fairness(answer_parity_languages, answer_transparency_contact_opt, answer_equal_service, answer_inclusive_image_ton):
    calculating_fairness_ctrl = ctrl.ControlSystemSimulation(calculate_fairness_ctrl)

    calculating_fairness_ctrl.input['Parity across languages'] = answer_parity_languages
    calculating_fairness_ctrl.input['Transparency of contact options'] = answer_transparency_contact_opt
    calculating_fairness_ctrl.input['Equal service access'] = answer_equal_service
    calculating_fairness_ctrl.input['Inclusive imagery and tone'] = answer_inclusive_image_ton

    calculating_fairness_ctrl.compute()

    return calculating_fairness_ctrl.output['fairness']

if __name__== "__main__":
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

    result = compute_fairness(answer_parity, answer_transparency,  answer_equal, answer_inclusive)
    print(result)


