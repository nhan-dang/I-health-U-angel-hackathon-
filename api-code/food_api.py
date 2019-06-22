import json
import os


def load_data(path):
    with open(path, 'r') as file:
        content = file.read()
    food_data_array = json.loads(content)
    new_dict = dict()
    for i in food_data_array:
        if i['name'] not in new_dict:
            new_dict.setdefault(i['name'], dict())
            # new_dict[i['name']]['usda_id'] = i['usda_id']
            new_dict[i['name']]['fat'] = i['fat']
            new_dict[i['name']]['calories'] = i['calories']
            new_dict[i['name']]['proteins'] = i['proteins']
            new_dict[i['name']]['carbohydrates'] = i['carbohydrates']
            new_dict[i['name']]['serving'] = i['serving']
            new_dict[i['name']]['nutrients'] = i['nutrients']
        else:
            pass
    return new_dict


def write_new_json(path, new_dict):
    with open(path, 'w') as outfile:
        json.dump(new_dict, outfile)


def access_new_json(path):
    with open(path, 'r') as file:
        content = file.read()
    food_data_array = json.loads(content)
    print(food_data_array)


if __name__ == "__main__":
    if not os.path.exists(os.path.join(os.getcwd(), "new_foods.json")):
        new_dict = load_data(os.path.join(os.getcwd(), "foods.json"))
        write_new_json(os.path.join(os.getcwd(), "new_foods.json"), new_dict)
    else:
        access_new_json(os.path.join(os.getcwd(), "new_foods.json"))
