import pandas as pd

from prediction.mappings import (ACCEPTED_REJECTED_MAPPING, GRADES_MAPPING,
                                 SUB_GRADE_MAPPING)


def predict_accepted_rejected(model, loans):
    """
    Predict loan acceptance or rejection based on a model and loan data.

    Args:
    model: A trained machine learning model.
    loans: A list of Loan objects.

    Returns:
    A dictionary containing predicted acceptance/rejection for each loan.
    """
    results = {}
    i = 0

    for loan in loans:
        new_entry = pd.DataFrame.from_dict(loan.get_entry_dict())

        prediction = model.predict(new_entry)
        predicted_proba = model.predict_proba(new_entry)

        results[i] = {
            "Loan_Acceptance": ACCEPTED_REJECTED_MAPPING[prediction[0]],
            "accepted_proba": predicted_proba[:, 1][0],
            "rejected_proba": predicted_proba[:, 0][0],
        }
        i += 1

    return results


def predict_grade(model, loans):
    """
    Predict loan grades based on a model and loan data.

    Args:
    model: A trained machine learning model.
    loans: A list of Loan objects.

    Returns:
    A dictionary containing predicted grade for each loan.
    """
    results = {}
    i = 0

    for loan in loans:
        new_entry = pd.DataFrame.from_dict(loan.get_entry_dict())

        main_prediction = model.predict(new_entry)
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

        results[i] = {
            "grade_category": res_str,
            "predicted_grade": GRADES_MAPPING[main_prediction[0]],
        }

        i += 1

    return results


def predict_subgrade(model, loans):
    """
    Predict loan subgrades based on a model and loan data.

    Args:
    model: A trained machine learning model.
    loans: A list of Loan objects.

    Returns:
    A dictionary containing predicted subgrade for each loan.
    """
    results = {}
    i = 0

    for loan in loans:
        new_entry = pd.DataFrame.from_dict(loan.get_entry_dict())

        main_prediction = model.predict(new_entry)
        predicted_proba = model.predict_proba(new_entry)

        subgrades = list(SUB_GRADE_MAPPING.values())
        probs = predicted_proba.tolist()[0]

        subgrades_res = {subgrades[i]: probs[i] for i in range(len(subgrades))}
        sorted_items = sorted(subgrades_res.items(), key=lambda x: x[1], reverse=True)

        valid_sub_grades = {}

        for subgrade, score in sorted_items:
            if subgrade[0] == new_entry.grade[0]:
                valid_sub_grades[subgrade] = score

        res_str = (
            f"{list(valid_sub_grades.keys())[0]}-{list(valid_sub_grades.keys())[1]}"
        )
        if int(list(valid_sub_grades.keys())[0][1]) > int(
            list(valid_sub_grades.keys())[1][1]
        ):
            res_str = (
                f"{list(valid_sub_grades.keys())[1]}-{list(valid_sub_grades.keys())[0]}"
            )

        results[i] = {
            "subgrade_category": res_str,
            "predicted_subgrade": SUB_GRADE_MAPPING[main_prediction[0]],
        }
        i += 1

    return results


def predict_int_rate(model, loans):
    """
    Predicts the interest rate for a list of loans using a trained machine learning model.

    Args:
        model: A trained machine learning model with a `predict` method.
        loans: A list of `Loan` objects, each representing a loan.

    Returns:
        A dictionary where the keys are the indices of the loans in the `loans` list
        and the values are the predicted interest rates for each loan.
    """
    results = {}
    for i, loan in enumerate(loans):
        new_entry = pd.DataFrame.from_dict(loan.get_entry_dict())
        main_prediction = model.predict(new_entry)
        results[i] = main_prediction[0]
    return results
