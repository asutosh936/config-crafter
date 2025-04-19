import sys
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True

def read_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.load(f)

def write_yaml(file_path, data):
    with open(file_path, 'w') as f:
        yaml.dump(data, f)
    print(f"✅ Bogie file updated: {file_path}")

def get_nested_block(data, path):
    keys = path.split('.')
    current = data
    for key in keys:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    return current

def inject_config(bogie_data, otel_config_data, block_path):
    target_block = get_nested_block(bogie_data, block_path)
    for key, value in otel_config_data.items():
        target_block[key] = value

def main():
    if len(sys.argv) != 4:
        print("Usage: python inject_otel_config.py <bogie_file.yaml> <otel_config_file.yaml> <block_path>")
        print("Example: python inject_otel_config.py bogie.yaml otel_config.yaml vars")
        sys.exit(1)

    bogie_file = sys.argv[1]
    otel_config_file = sys.argv[2]
    block_path = sys.argv[3]

    bogie_data = read_yaml(bogie_file)
    otel_config_data = read_yaml(otel_config_file)

    inject_config(bogie_data, otel_config_data, block_path)
    write_yaml(bogie_file, bogie_data)

if __name__ == "__main__":
    main()
