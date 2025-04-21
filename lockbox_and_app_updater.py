import requests
import argparse
import json

def make_post_call(url, data):
    print(f"\nMaking POST request to: {url}")
    print(f"With JSON body:\n{json.dumps(data, indent=2)}\n")

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print("Response Status Code:", response.status_code)
        print("Response Body:\n", response.json())
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

def parse_arguments():
    parser = argparse.ArgumentParser(description="REST API POST Client with Sample Args")
    parser.add_argument('--url', type=str, default="https://jsonplaceholder.typicode.com/posts",
                        help='API endpoint to call (default is JSONPlaceholder)')
    parser.add_argument('--data', nargs=2, action='append', metavar=('KEY', 'VALUE'),
                        help='Optional POST body parameters (use multiple times)')
    parser.add_argument('--sample', nargs=2, action='append', metavar=('KEY', 'VALUE'),
                        help='Sample optional parameters (not necessarily used in POST body)')

    args = parser.parse_args()

    data_dict = dict(args.data) if args.data else {}
    sample_dict = dict(args.sample) if args.sample else {}

    return args.url, data_dict, sample_dict

if __name__ == "__main__":
    url, post_data, sample_args = parse_arguments()

    print("\n--- User Provided Arguments ---")
    print("URL:         ", url)
    print("POST Data:   ", post_data)
    print("Sample Args: ", sample_args)

    # Only POST with the actual post_data
    make_post_call(url, post_data)
