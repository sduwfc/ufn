import requests
from tqdm import tqdm
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
import os

PUBLIC_PREFIX = "http://219.142.246.77:65000"

def get_sid(account, password):
    url = f"{PUBLIC_PREFIX}/webapi/auth.cgi"
    payload = {
        "api": "SYNO.API.Auth",
        "version": 3,
        "method": "login",
        "account": account,
        "passwd": password,
        "session": "FileStation",
        "format": "cookie"
    }

    try:
        response = requests.get(url, params=payload)

        if response.status_code == 200:
            data = response.json()
            if data['success']:
                sid = data['data']['sid']
                return sid
            else:
                print("Login failed, please check your account and password.")
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed due to an error: {e}")

    return None

def create_folder(sid, path="/home", name="ufn"):
    url = f"{PUBLIC_PREFIX}/webapi/entry.cgi"
    payload = {
        "api": "SYNO.FileStation.CreateFolder",
        "version": 2,
        "method": "create",
        "force_parent": "true",
        "folder_path": path,
        "name": name,
        "_sid": sid
    }

    try:
        response = requests.get(url, params=payload)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"Default folder {name} at path {path}")
            else:
                print("Failed to create folder, please check your inputs and permissions.")
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed due to an error: {e}")


def create_callback(encoder):
    progress_bar = tqdm(total=encoder.len, ncols=100, unit='B', unit_scale=True)

    def callback(monitor):
        progress_bar.update(monitor.bytes_read - progress_bar.n)

    return callback

def upload_file_to_synology(sid, filepath, upload_path="/home/ufn"):
    url = f"{PUBLIC_PREFIX}/webapi/entry.cgi?api=SYNO.FileStation.Upload&version=2&method=upload&_sid={sid}"
    filename = os.path.basename(filepath)
    try:
        with open(filepath, 'rb') as payload:
            args = {
                'path': upload_path,
                'create_parents': 'true',
                'overwrite': 'true'
            }
            data = {**args, 'file': (filename, payload, 'application/octet-stream')}
            encoder = MultipartEncoder(fields=data)
            monitor = MultipartEncoderMonitor(encoder, create_callback(encoder))
            headers = {'Content-Type': monitor.content_type}
            response = requests.post(url, data=monitor, headers=headers, verify=True)
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f"File {filename} uploaded successfully to {upload_path}")
                else:
                    print("Failed to upload file, please check your inputs and permissions.")
            else:
                print(f"Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed due to an error: {e}")
        print(f"Exception details: {e.__dict__}")


def upload_file(filepath, account, password):
    print(f'Uploading file: {filepath}')
    sid = get_sid(account, password)
    create_folder(sid)
    upload_file_to_synology(sid, filepath)

def upload_directory(dirpath, account, password):
    print(f'Uploading directory: {dirpath}')
    sid = get_sid(account, password)
    dir_name = os.path.basename(dirpath)
    create_folder(sid, path="/home/ufn", name=dir_name)
    upload_path = f"/home/ufn/{dir_name}"

    for filename in os.listdir(dirpath):
        if os.path.isfile(os.path.join(dirpath, filename)):
            upload_file_to_synology(sid, os.path.join(dirpath, filename), upload_path=upload_path)
