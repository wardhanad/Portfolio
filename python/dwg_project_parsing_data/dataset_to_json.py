import json
import re

mypath = 'production/satu-data-production/bigquery_satu_data_master.tf'
f = open(mypath, 'r')
string_example = f.read()

roles_matches = re.findall(r"role\s*(.*)", string_example)
roles_matches = [r.replace("=", "").replace('"', "").strip() for r in roles_matches]
email_matches = re.findall(r"by_email\s*(.*)", string_example)
email_matches = [r.replace("=", "").replace('"', "").strip() for r in email_matches]
usertype_matches = re.findall(r".*(?=\s*_by_email)", string_example)
usertype_matches = [r.strip() for r in usertype_matches if len(r) > 0]

email_matches = [(x, y) for x, y in zip(email_matches, usertype_matches)]

result_json = {}
for x, y in zip(roles_matches, email_matches):
    if x in result_json:
        result_json[x].append(y[0])
    else:
        result_json[x] = [y[0]]

print(result_json)

with open("Json\satu_data_master.json", "w") as fp:
    json.dump(result_json, fp)
