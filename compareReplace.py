import sys
from ruamel.yaml import YAML
from deepdiff import DeepDiff

yaml = YAML()
yaml.preserve_quotes = True

def load_yaml_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return yaml.load(f)
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        sys.exit(1)

def save_yaml_file(filepath, data):
    try:
        with open(filepath, 'w') as f:
            yaml.dump(data, f)
        print(f"✅ Updated {filepath} successfully.")
    except Exception as e:
        print(f"❌ Error saving {filepath}: {e}")
        sys.exit(1)

def format_diff(diff):
    output = []

    if 'dictionary_item_added' in diff:
        output.append("🔹 Keys added:")
        for item in diff['dictionary_item_added']:
            output.append(f"  + {item.path()}")

    if 'dictionary_item_removed' in diff:
        output.append("🔸 Keys removed:")
        for item in diff['dictionary_item_removed']:
            output.append(f"  - {item.path()}")

    if 'values_changed' in diff:
        output.append("🔁 Values changed:")
        for item in diff['values_changed']:
            output.append(f"  ~ {item.path()}: {item.t1} ➜ {item.t2}")

    if 'iterable_item_added' in diff:
        output.append("🔹 List items added:")
        for item in diff['iterable_item_added']:
            output.append(f"  + {item.path()} ➜ {item.t2}")

    if 'iterable_item_removed' in diff:
        output.append("🔸 List items removed:")
        for item in diff['iterable_item_removed']:
            output.append(f"  - {item.path()} ➜ {item.t1}")

    return "\n".join(output)

def merge_data(source, updates):
    if isinstance(source, dict) and isinstance(updates, dict):
        for k, v in updates.items():
            if k in source:
                source[k] = merge_data(source[k], v)
            else:
                source[k] = v
    elif isinstance(source, list) and isinstance(updates, list):
        return updates  # Replace list directly
    else:
        return updates
    return source

def compare_and_merge(file1, file2):
    data1 = load_yaml_file(file1)
    data2 = load_yaml_file(file2)

    diff = DeepDiff(data1, data2, view='tree')

    if not diff:
        print("✅ No differences found.")
        return

    print("❌ Differences found:\n")
    print(format_diff(diff))
    choice = input("\n❓ Do you want to apply these changes to the source file? (y/n): ").lower()
    if choice == 'y':
        updated_data = merge_data(data1, data2)
        save_yaml_file(file1, updated_data)
    else:
        print("ℹ️ Merge aborted by user.")

def main():
    if len(sys.argv) != 3:
        print("Usage: python compare_merge_yaml.py <source.yaml> <target.yaml>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    compare_and_merge(file1, file2)

if __name__ == "__main__":
    main()
