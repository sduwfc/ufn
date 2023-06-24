import argparse
import os
import json
from getpass import getpass

from .utils import upload_file,upload_directory

UFN_CONFIG_DIR = 'ufn_config'  # The name of the config directory
UFN_CONFIG_FILE = 'config.json'  # The name of the config file

def main():
    parser = argparse.ArgumentParser(prog='ufn', description='Upload files or directories.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', type=str, help='the file to upload')
    group.add_argument('--dir', type=str, help='the directory to upload')

    args = parser.parse_args()

    # Check for config directory
    ufn_config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), UFN_CONFIG_DIR)
    config_file_path = os.path.join(ufn_config_path, UFN_CONFIG_FILE)
    if os.path.exists(config_file_path):
        # Load the account and password
        with open(config_file_path, 'r') as config_file:
            config_data = json.load(config_file)
            account = config_data.get('account')
            password = config_data.get('password')
    else:
        print(f"No existing ufn config found at {ufn_config_path}.")
        should_create_config = input("Would you like to create one to save your account and password? (y/n) ").lower() == 'y'
        account = input("Please enter your account: ")
        password = getpass("Please enter your password: ")

        if should_create_config:
            # Ensure the directory exists
            os.makedirs(ufn_config_path, exist_ok=True)
            # Save the account and password
            with open(config_file_path, 'w') as config_file:
                json.dump({'account': account, 'password': password}, config_file)

    if args.file:
        if not os.path.isfile(args.file):
            print(f"The file {args.file} does not exist")
            return
        abs_file_path = os.path.abspath(args.file)
        upload_file(abs_file_path, account, password)
    elif args.dir:
        if not os.path.isdir(args.dir):
            print(f"The directory {args.dir} does not exist")
            return
        abs_dir_path = os.path.abspath(args.dir)
        upload_directory(abs_dir_path, account, password)

if __name__ == '__main__':
    main()
