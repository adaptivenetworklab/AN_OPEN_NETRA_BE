import yaml

def read_values_file(filepath):
    with open(filepath, 'r') as stream:
        try:
            values = yaml.safe_load(stream)
            return values
        except yaml.YAMLError as exc:
            print(exc)
            return None

def write_values_file(filepath, values):
    with open(filepath, 'w') as outfile:
        try:
            yaml.dump(values, outfile, default_flow_style=False)
        except yaml.YAMLError as exc:
            print(exc)

# Specify the path to your values.yaml
values_file_path = 'values.yaml'
values = read_values_file(values_file_path)

# Modify the values as needed
values['f1cuPort'] = '2156' # Example modification

# Write the modified values back to the file
write_values_file(values_file_path, values)
print(values)