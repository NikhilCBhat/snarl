import os
import json
import argparse

JSON_DIR = "tests/Manager"
EXECUTABLE = "testManager"

def create_json_file_paths(t_id):
    formats = ["{}-in", "{}-out", "{}-actual"]
    return [os.path.join(JSON_DIR, f.format(t_id)+".json") for f in formats]

def create_json_dict(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def run_tests(test_ids_to_run):

    if not test_ids_to_run:
        test_ids_to_run = {int(f.split('-')[0]) for f in os.listdir(JSON_DIR) if f.endswith('json')}

    for t_id in test_ids_to_run:
        input_file, expected_output_file, actual_output_file = create_json_file_paths(t_id)
        os.system("./{} < {} > {}".format(EXECUTABLE, input_file, actual_output_file))

        try:
            actual_data = create_json_dict(actual_output_file)
            expected_output = create_json_dict(expected_output_file)

            if actual_data != expected_output:
                print("\nERROR for t_id = {}".format(t_id))
                print("Actual\n{}\nExpected\n{}".format(json.dumps(actual_data), json.dumps(expected_output)))
            else:
                print("\nSuccess: for t_id = {}".format(t_id))
        except Exception as e:
            print("\nError for t_id = {}".format(t_id))
            print(str(e))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--ids', '-i', nargs='+', type=int)
    args = parser.parse_args()
    run_tests(args.ids)



