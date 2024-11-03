from os import listdir
from os.path import join
import re
import pandas as pd

mypath = 'Terraform/production'
path = []

paths_project = [join(mypath, x) for x in listdir(mypath)]
for project in paths_project:
    for dataset in listdir(project):
        path.append(join(project, dataset))

column_name = pd.Series(path)
paths = column_name[column_name.str.contains('bigquery_')].reset_index(drop=1)

dataset = []
role = []
email = []
projects = []

for path_ind in paths:
    open_file = open(path_ind, 'r')
    read_file = open_file.read()

    dataset_name = re.findall(r'dataset_id\s*(.*)',read_file)
    dataset_name = [r.replace("=", "").replace('"', "").strip() for r in dataset_name]
    roles_matches = re.findall(r'role\s*=\s*"(.*?)"', read_file)
    roles_matches = [r.replace("=", "").replace('"', "").strip() for r in roles_matches]
    email_matches = re.findall(r"by_email\s*(.*)", read_file)
    email_matches = [r.replace("=", "").replace('"', "").strip() for r in email_matches]

    for x, y in zip(roles_matches, email_matches):
        project_find = re.findall(r'production/*(.*)\\',path_ind)
        projects.append(project_find[0])
        dataset.append(dataset_name[0])
        role.append(x)
        email.append(y)

dict = {'project':projects,'dataset':dataset, 'role':role, 'email':email}

data = pd.DataFrame(dict)
data.to_csv('csv/dataset_all.csv', index = 0)
# csv naming need to be automated with date and time retrieval

print(data.head())
