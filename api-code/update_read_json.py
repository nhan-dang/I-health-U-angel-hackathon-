import json
import os
import sys

def load_data(path):
    with open(path, 'r') as file:
        content = file.read()
    food_data_array = json.loads(content)
    new_dict = dict()

    # base recommendation 
    base = access_new_json(os.path.join(os.getcwd(), "categories.json"))[0]

    # for normalizing the ratings
    import numpy as np
    def softmax(x):
	    """Compute softmax values for each sets of scores in x."""
	    e_x = np.exp(x - np.max(x))
	    return list(e_x / e_x.sum())

    for i in food_data_array:
        if i['name'] not in new_dict:
            new_dict.setdefault(i['name'], dict())
            # new_dict[i['name']]['usda_id'] = i['usda_id']
            new_dict[i['name']]['fat'] = i['fat']
            new_dict[i['name']]['calories'] = i['calories']
            new_dict[i['name']]['proteins'] = i['proteins']
            new_dict[i['name']]['carbohydrates'] = i['carbohydrates']
            new_dict[i['name']]['serving'] = 1
            new_dict[i['name']]['nutrients'] = i['nutrients']
            if 'fibers' not in i:
                new_dict[i['name']]['fibers'] = 0
            else:
                new_dict[i['name']]['fibers'] = i['fibers']

            new_dict[i['name']]['ratings'] = softmax([i['fat']*i['serving']           / base['fat'],
            										  i['proteins']*i['serving']      / base['proteins'],
            										  i['carbohydrates']*i['serving'] / base['carbohydrates']])
        else:
            pass
    return new_dict


def write_new_json(path, new_dict):
    with open(path, 'w') as outfile:
        json.dump(new_dict, outfile)


def access_new_json(path):
    with open(path, 'r') as file:
        content = file.read()
    data = json.loads(content)
    return data


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: update_read_json.py --update or update_read_json.py --access")
    elif sys.argv[1] == '--update':
        '''
        The old food json file is readable but not in correct format we want to use
        Write to new json file. However not really readable
        Manually add or update records in old json is preferable
        '''
        print("Update new_foods.json for processing\n")
        new_dict = load_data(os.path.join(os.getcwd(), "foods.json"))
        write_new_json(os.path.join(os.getcwd(), "new_foods.json"), new_dict)
    elif sys.argv[1] == '--access':
        '''This will be modify later to get data for processing if required'''
        print("Accessing new json files\n")
        access_new_json(os.path.join(os.getcwd(), "new_foods.json"))
    else:
        print("The arguments only accept: --access or --update")
