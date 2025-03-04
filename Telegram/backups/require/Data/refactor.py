
import json
import re
compile_ = re.compile(r'\d{2}-\d{2}')

__global_refactored_object__ = {
    "Студент": [],
    "Преподаватель": [],
    "Сотрудник": []
}

def parse_json():
    with open('parking_employee.json', 'r', encoding='utf-8') as file_read:
        json_ = json.load(file_read)
        for object_ in json_[-1]['data']:
            parsed_object = {
                "user_id": object_['ID'],
                "initials": object_["INITIALS"],
                "phone_number": object_["PhoneNumber"],
                "group": object_["GROUPS"],
                "state_number": object_["StateNumber"],
                "SQLuser_id": object_["SQLID"],
            }
            if re.fullmatch(compile_, object_['GROUPS']):
                __global_refactored_object__['Студент'].append(parsed_object)
            elif object_['GROUPS'] == 'Преподаватель':
                __global_refactored_object__['Преподаватель'].append(parsed_object)
            else:
                __global_refactored_object__['Сотрудник'].append(parsed_object)

        with open('Refactored_DB.json', 'w', encoding='utf-8') as file_writer:
            json.dump(__global_refactored_object__, file_writer, indent=4, ensure_ascii=False)


def parse_csv():
    import csv
    first: bool = True
    with open("users.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if first:
                print("First row")
                first = not first
                continue
            parsed_object: dict = {
                "user_id": row[0],
                "initials": row[1],
                "phone_number": row[3],
                "group": row[4],
                "state_number": row[5],
            }
            if re.fullmatch(compile_, row[4]):
                __global_refactored_object__['Студент'].append(parsed_object)
            elif row[4] == 'Преподаватель':
                __global_refactored_object__['Преподаватель'].append(parsed_object)
            else:
                __global_refactored_object__['Сотрудник'].append(parsed_object)

        with open('Refactored_DB.json', 'w', encoding='utf-8') as file_writer:
            json.dump(__global_refactored_object__, file_writer, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    # parse_json()
    parse_csv()