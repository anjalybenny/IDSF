import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


readability_text = ctrl.Antecedent(np.arange(0, 6, 1), 'Readability of text')
guidance = ctrl.Antecedent(np.arange(0, 6, 1), 'Step-by-step guidance')
terminology_explained = ctrl.Antecedent(np.arange(0, 6, 1), 'Terminology explained')
tone_consistency = ctrl.Antecedent(np.arange(0, 6, 1), 'Tone consistency')
clarity = ctrl.Consequent(np.arange(0, 101, 1), 'clarity')

readability_text.automf(3)
guidance.automf(3)
terminology_explained.automf(3)
tone_consistency.automf(3)

clarity ['Not clear enough'] = fuzz.trimf(clarity.universe, [0, 0, 50])
clarity ['Clear enough'] = fuzz.trimf(clarity.universe, [50, 75, 100])
clarity ['Really clear'] = fuzz.trimf(clarity.universe, [80, 100, 100])

# really clear rule
rule1 = ctrl.Rule((readability_text['good'] | readability_text['average']) & (guidance['good'] | guidance['average']) & (terminology_explained['good'] | terminology_explained['average'] ) & (tone_consistency['good']|tone_consistency['average']) & ~(readability_text['good'] & guidance['average'] & terminology_explained['average'] & tone_consistency['average']) & ~(readability_text['average'] & guidance['good'] & terminology_explained['average'] & tone_consistency['average']) & ~(readability_text['average'] & guidance['average'] & terminology_explained['good'] & tone_consistency['average']) & ~(readability_text['average'] & guidance['average'] & terminology_explained['average'] & tone_consistency['good']) & ~(readability_text['average'] & guidance['average'] & terminology_explained['average'] & tone_consistency['average']), clarity['Really clear'])

# clear enough
rule2 = ctrl.Rule((readability_text['good'] & guidance['average'] & terminology_explained['average'] & tone_consistency['average']) | (readability_text['average'] & guidance['good'] & terminology_explained['average'] & tone_consistency['average']) | (readability_text['average'] & guidance['average'] & terminology_explained['good'] & tone_consistency['average']) | (readability_text['average'] & guidance['average'] & terminology_explained['average'] & tone_consistency['good']), clarity['Clear enough'])
rule3 = ctrl.Rule((readability_text['good']| readability_text['poor']) &  (guidance['good'] | guidance['poor']) & (terminology_explained['good']| terminology_explained['poor']) & (tone_consistency['good'] | tone_consistency['poor']) & ~(readability_text['good'] & guidance['good'] & terminology_explained['good'] & tone_consistency['good']) & ~((guidance['poor'] & terminology_explained['poor'] & tone_consistency['poor']) | (readability_text['poor'] & terminology_explained['poor'] & tone_consistency['poor']) | (readability_text['poor'] & guidance['poor'] &  tone_consistency['poor']) | (readability_text['poor'] & guidance['poor'] & terminology_explained['poor'])), clarity['Clear enough'])
rule4 = ctrl.Rule((readability_text['poor'] | readability_text['average']) & (guidance['poor'] | guidance['average']) & (terminology_explained['poor'] | terminology_explained['average'] ) & (tone_consistency['poor']|tone_consistency['average']) & ~(readability_text['average'] & guidance['poor'] & terminology_explained['poor'] & tone_consistency['poor']) & ~(readability_text['poor'] & guidance['average'] & terminology_explained['poor'] & tone_consistency['poor']) & ~(readability_text['poor'] & guidance['poor'] & terminology_explained['average'] & tone_consistency['poor']) & ~(readability_text['poor'] & guidance['poor'] & terminology_explained['poor'] & tone_consistency['average']) & ~(readability_text['poor'] & guidance['poor'] & terminology_explained['poor'] & tone_consistency['poor']), clarity['Clear enough'])

# not clear enough
rule5 = ctrl.Rule((guidance['poor'] & terminology_explained['poor'] & tone_consistency['poor']) | (readability_text['poor'] & terminology_explained['poor'] & tone_consistency['poor']) | (readability_text['poor'] & guidance['poor'] &  tone_consistency['poor']) | (readability_text['poor'] & guidance['poor'] & terminology_explained['poor']), clarity['Not clear enough'])

calculate_clarity_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])

def compute_clarity(answer_readability, answer_guidance, answer_terminology, answer_tone):
    calculating_clarity_ctrl = ctrl.ControlSystemSimulation(calculate_clarity_ctrl)
    

    calculating_clarity_ctrl.input['Readability of text'] = answer_readability
    calculating_clarity_ctrl.input['Step-by-step guidance'] = answer_guidance
    calculating_clarity_ctrl.input['Terminology explained'] = answer_terminology
    calculating_clarity_ctrl.input['Tone consistency'] = answer_tone

    calculating_clarity_ctrl.compute()

    return calculating_clarity_ctrl.output['clarity']

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

    result = compute_clarity(answer_read, answer_guid, answer_termin, answer_ton)
    print(result)


