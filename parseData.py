import os
import csv
import json

def read_specification(file_path):
    """Read the specification file and return a list of column definitions."""
    with open(file_path, 'r', encoding='utf-8') as spec_file:
        reader = csv.DictReader(spec_file)
        return [(row['column name'], int(row['width']), row['datatype']) for row in reader]

def parse_integer(value):
    """Parse an integer from a string, handling edge cases."""
    if value == '-' or value.strip() == '':
        return 0  # Treat '-' and empty as 0
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Invalid integer value '{value}'.")

def parse_data_file(data_file_path, specifications):
    """Parse the data file according to the specifications."""
    parsed_data = []
    
    with open(data_file_path, 'r', encoding='utf-8') as data_file:
        for line in data_file:
            line = line.rstrip('\n')
            json_object = {}
            start_index = 0
            
            for column_name, width, data_type in specifications:
                value = line[start_index:start_index + width].strip()
                start_index += width
                
                if data_type == 'TEXT':
                    json_object[column_name] = value
                elif data_type == 'BOOLEAN':
                    json_object[column_name] = value == '1'
                elif data_type == 'INTEGER':
                    json_object[column_name] = parse_integer(value)

            parsed_data.append(json_object)
    
    return parsed_data

def write_ndjson(output_file_path, data):
    """Write the parsed data to an NDJSON file."""
    with open(output_file_path, 'w', encoding='utf-8') as ndjson_file:
        for json_object in data:
            ndjson_file.write(json.dumps(json_object) + '\n')

def process_files():
    """Process all data files based on their specifications."""
    data_dir = 'data'
    specs_dir = 'specs'
    output_dir = 'output'

    os.makedirs(output_dir, exist_ok=True)

    for spec_file in os.listdir(specs_dir):
        if spec_file.endswith('.csv'):
            spec_name = spec_file[:-4]  # Remove .csv extension
            specifications = read_specification(os.path.join(specs_dir, spec_file))

            for data_file in os.listdir(data_dir):
                if data_file.startswith(f"{spec_name}_") and data_file.endswith('.txt'):
                    data_path = os.path.join(data_dir, data_file)
                    parsed_data = parse_data_file(data_path, specifications)
                    output_file_name = f"{data_file[:-4]}.ndjson"  # Replace .txt with .ndjson
                    output_path = os.path.join(output_dir, output_file_name)
                    write_ndjson(output_path, parsed_data)

if __name__ == '__main__':
    process_files()
