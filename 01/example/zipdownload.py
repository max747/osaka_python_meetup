from datetime import datetime
import os
from urllib.request import urlopen
from zipfile import ZipFile


def download_zip(url):
    with urlopen(url) as resp:
        data = resp.read()
        return data


def get_todays_dirname():
    return datetime.today().strftime("%Y%m%d")


def save_as_binary(dest_path, data):
    with open(dest_path, "wb") as f:
        f.write(data)


def extract_zipfile(zipfilename, dest_dir):
    with ZipFile(zipfilename) as zf:
        names = zf.namelist()
        for name in names:
            if "/" in name or ".." in name:
                raise ValueError("cannot extract zipfile {}: to avoid security risk".format(zipfilename))
        zf.extractall(dest_dir)


def main():
    #url = "http://www.post.japanpost.jp/zipcode/dl/kogaki/zip/37kagawa.zip"
    url = "http://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip"
    data = download_zip(url)

    filename = url.split("/")[-1]
    rootdir = "download"

    todays_dir = os.path.join(rootdir, get_todays_dirname())
    os.makedirs(todays_dir)
    todays_path = os.path.join(todays_dir, filename)

    latest_dir = os.path.join(rootdir, "latest")
    os.makedirs(latest_dir)
    latest_path = os.path.join(latest_dir, filename)

    save_as_binary(todays_path, data)
    save_as_binary(latest_path, data)

    extract_zipfile(latest_path, latest_dir)


if __name__ == "__main__":
    main()
