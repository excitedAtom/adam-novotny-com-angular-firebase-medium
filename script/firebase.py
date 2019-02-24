import argparse
import os
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--mode", required=True, choices=["stage", "prod"], help="select mode")
args = vars(ap.parse_args())
mode = args["mode"]

os.environ["mode"] = mode
from secrets import firebase_project

def main():
    subprocess.call("""
    cd adam_novotny_com;
    firebase login;
    firebase use {};
    firebase deploy;
    """.format(firebase_project), shell=True)


if __name__ == "__main__":
    main()