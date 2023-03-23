import pandas as pd
from mappings import ACCEPTED_REJECTED_MAPPING, GRADES_MAPPING, SUB_GRADE_MAPPING

def predict_accepted_rejected(model, loans): 
    results = {}
    i = 0

    for loan in loans:
        new_entry = pd.DataFrame.from_dict(loan.get_entry_dict())
    
        prediction = model.predict(new_entry)
        predicted_proba = model.predict_proba(new_entry)
    
        results[i] = {
            "Loan_Acceptance": ACCEPTED_REJECTED_MAPPING[prediction[0]],
            "accepted_proba": predicted_proba[:, 1][0],
            "rejected_proba": predicted_proba[:, 0][0]
        }
        i+=1

    return results


def predict_grade(model, loans): 
    results = {}
    i = 0

    for loan in loans:
        new_entry = pd.DataFrame.from_dict(loan.get_entry_dict())
        
        predicted_proba = model.predict_proba(new_entry)
 
        grades = list(GRADES_MAPPING.values())
        probs = predicted_proba.tolist()[0]
        
        grades_res = {grades[i]: probs[i] for i in range(len(grades))} 
        if max(probs) < 0.7:
            sorted_items = sorted(grades_res.items(), key=lambda x: x[1], reverse=True)
            res_grades = [sorted_items[0][0], sorted_items[1][0]]
        else:
            res_grades = max(grades_res, key=grades_res.get)

        res_grades = sorted(res_grades, reverse=False)
         
        if len(res_grades) == 1:
            res_str = f"{res_grades[0]}"
        else:
            res_str = f"{res_grades[0]}-{res_grades[1]}"

        results[i] = res_str
        i+=1 
    
    return results

def predict_subgrade(model, loans): 
    results = {}
    i = 0

    for loan in loans:
        new_entry = pd.DataFrame.from_dict(loan.get_entry_dict())
        
        predicted_proba = model.predict_proba(new_entry)
 
        subgrades = list(SUB_GRADE_MAPPING.values())
        probs = predicted_proba.tolist()[0]
        
        subgrades_res = {subgrades[i]: probs[i] for i in range(len(subgrades))} 

        sorted_items = sorted(subgrades_res.items(), key=lambda x: x[1], reverse=True)
        res_subrades = [sorted_items[i][0] for i in range(5)]

        res_str = f"{res_subrades[0]}-{res_subrades[len(res_subrades)-1]}"
        results[i] = res_str
        
        i+=1 
    
    return results