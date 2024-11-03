from os import listdir
from os.path import join
import re
import json
import pandas as pd

mypath = 'groups'
list_paths = [join(mypath, x) for x in listdir(mypath)]
gcp = []
list_email = []
result_json = {}

for path in list_paths:
    open_path = open(path, 'r')
    read_file = open_path.read()

    group_email = re.findall(r"email:\s*(.*)", read_file)
    group_email = [r.strip() for r in group_email]
    emails = re.findall(r"\n\-\s*(.*)", read_file)
    if emails == []:
        emails = re.findall(r"\s\-\s*(.*)", read_file)
        emails = [r.replace("-", "").strip() for r in emails]

    for x in range(len(emails)-1):
        group_email.append(group_email[0])

    for x, y in zip(group_email, emails):
        gcp.append(x)
        list_email.append(y)

dct = {'gcp':gcp, 'list_email':list_email}
data = pd.DataFrame(dct)
data.to_csv('csv/user_audit.csv', index = 0)
