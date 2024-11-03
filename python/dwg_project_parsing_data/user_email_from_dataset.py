import pandas as pd

gcp = pd.read_csv('csv/user_audit.csv')
dataset = pd.read_csv('csv/dataset_access_audit_2024_09_03_12_12.csv')

unique_email_in_dataset = dataset.email.unique()

user = gcp[gcp['gcp'].isin(unique_email_in_dataset)]

user.to_csv('csv/user_audit_satu_data_dat_dataset_2024_09_03_12_50.csv')

# user_in_dataset

print(user.head())
