import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


search_effectiveness = ctrl.Antecedent(np.arange(0, 6, 1), 'Search effectiveness')
error_feedback = ctrl.Antecedent(np.arange(0, 6, 1), 'Error feedback')
menu_consistency = ctrl.Antecedent(np.arange(0, 6, 1), 'Menu consistency')
task_completion = ctrl.Antecedent(np.arange(0, 6, 1), 'Task completion')
navigation = ctrl.Consequent(np.arange(0, 101, 1), 'navigation')

search_effectiveness.automf(3)
error_feedback.automf(3)
menu_consistency.automf(3)
task_completion.automf(3)

navigation['Not navigatable enough'] = fuzz.trimf(navigation.universe, [0, 0, 50])
navigation['Navigatable enough'] = fuzz.trimf(navigation.universe, [50, 75, 100])
navigation['Really navigatable'] = fuzz.trimf(navigation.universe, [80, 100, 100])

# really navigatable rule
rule1 = ctrl.Rule((search_effectiveness['good'] | search_effectiveness['average']) & (error_feedback['good'] | error_feedback['average']) & (menu_consistency['good'] | menu_consistency['average'] ) & (task_completion['good']|task_completion['average']) & ~(search_effectiveness['good'] & error_feedback['average'] & menu_consistency['average'] & task_completion['average']) & ~(search_effectiveness['average'] & error_feedback['good'] & menu_consistency['average'] & task_completion['average']) & ~(search_effectiveness['average'] & error_feedback['average'] & menu_consistency['good'] & task_completion['average']) & ~(search_effectiveness['average'] & error_feedback['average'] & menu_consistency['average'] & task_completion['good']) & ~(search_effectiveness['average'] & error_feedback['average'] & menu_consistency['average'] & task_completion['average']), navigation['Really navigatable'])

# navigatable enough
rule2 = ctrl.Rule((search_effectiveness['good'] & error_feedback['average'] & menu_consistency['average'] & task_completion['average']) | (search_effectiveness['average'] & error_feedback['good'] & menu_consistency['average'] & task_completion['average']) | (search_effectiveness['average'] & error_feedback['average'] & menu_consistency['good'] & task_completion['average']) | (search_effectiveness['average'] & error_feedback['average'] & menu_consistency['average'] & task_completion['good']), navigation['Navigatable enough'])
rule3 = ctrl.Rule((search_effectiveness['good']| search_effectiveness['poor']) &  (error_feedback['good'] | error_feedback['poor']) & (menu_consistency['good']| menu_consistency['poor']) & (task_completion['good'] | task_completion['poor']) & ~(search_effectiveness['good'] & error_feedback['good'] & menu_consistency['good'] & task_completion['good']) & ~((error_feedback['poor'] & menu_consistency['poor'] & task_completion['poor']) | (search_effectiveness['poor'] & menu_consistency['poor'] & task_completion['poor']) | (search_effectiveness['poor'] & error_feedback['poor'] &  task_completion['poor']) | (search_effectiveness['poor'] & error_feedback['poor'] & menu_consistency['poor'])), navigation['Navigatable enough'])
rule4 = ctrl.Rule((search_effectiveness['poor'] | search_effectiveness['average']) & (error_feedback['poor'] | error_feedback['average']) & (menu_consistency['poor'] | menu_consistency['average'] ) & (task_completion['poor']|task_completion['average']) & ~(search_effectiveness['average'] & error_feedback['poor'] & menu_consistency['poor'] & task_completion['poor']) & ~(search_effectiveness['poor'] & error_feedback['average'] & menu_consistency['poor'] & task_completion['poor']) & ~(search_effectiveness['poor'] & error_feedback['poor'] & menu_consistency['average'] & task_completion['poor']) & ~(search_effectiveness['poor'] & error_feedback['poor'] & menu_consistency['poor'] & task_completion['average']) & ~(search_effectiveness['poor'] & error_feedback['poor'] & menu_consistency['poor'] & task_completion['poor']), navigation['Navigatable enough'])

# not navigatable enough
rule5 = ctrl.Rule((error_feedback['poor'] & menu_consistency['poor'] & task_completion['poor']) | (search_effectiveness['poor'] & menu_consistency['poor'] & task_completion['poor']) | (search_effectiveness['poor'] & error_feedback['poor'] &  task_completion['poor']) | (search_effectiveness['poor'] & error_feedback['poor'] & menu_consistency['poor']), navigation['Not navigatable enough'])

calculate_navigation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])

def compute_navigation(answer_search_effect, answer_error_feedback, answer_menu_constant, answer_task_complete):
    calculating_navigation_ctrl = ctrl.ControlSystemSimulation(calculate_navigation_ctrl)

    calculating_navigation_ctrl.input['Search effectiveness'] = answer_search_effect
    calculating_navigation_ctrl.input['Error feedback'] = answer_error_feedback
    calculating_navigation_ctrl.input['Menu consistency'] = answer_menu_constant
    calculating_navigation_ctrl.input['Task completion'] = answer_task_complete

    calculating_navigation_ctrl.compute()

    return calculating_navigation_ctrl.output['navigation']

if __name__== "__main__":
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

    result = compute_navigation(answer_search, answer_error, answer_menu, answer_task)
    print(result)


