import pathlib
import pandas as pd
import patients as pt

insurance_file = pathlib.Path(__file__).parent.parent / 'data' / 'insurance.csv'
insurance_df = pd.read_csv(insurance_file)

patients = pt.Patients(insurance_df)

print(patients.age_analysis())
print(patients.sex_analysis())
print(patients.smoker_analysis())

