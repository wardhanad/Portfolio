from os import listdir
from os.path import join
import re
import json

mypath = 'groups'
list_paths = [join(mypath, x) for x in listdir(mypath)]
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
    if x in result_json:
      result_json[x].append(y)
    else:
      result_json[x] = [y]

with open("Json\gcp.json", "w") as fp:
    json.dump(result_json, fp)
