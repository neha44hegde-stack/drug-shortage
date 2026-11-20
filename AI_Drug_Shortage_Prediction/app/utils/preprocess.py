import pandas as pd


def preprocess_input(drug_name, quantity, location):
    """
    Preprocess user input before prediction.
    """
    data = pd.DataFrame({
        "Drug_Name": [drug_name],
        "Quantity": [quantity],
        "Location": [location]
    })

    return data