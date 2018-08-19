import argparse
import os
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--mode", required=True, choices=["stage", "prod"], help="select mode")
args = vars(ap.parse_args())
mode = args["mode"]

def main():
    request_str = """From docker running env: {}
        > ng build --prod --aot
        Confirm: y/n
    """.format(mode)
    build_ok = input(request_str)
    if build_ok != "y":
        sys.exit("Invalid input")
    project = "adam-novotny-com-stage"
    if mode == "prod":
        project = "adamnovotnycom-prod"
    subprocess.call("""
    cd adam_novotny_com;
    firebase login;
    firebase use {};
    firebase deploy;
    """.format(project), shell=True)


if __name__ == "__main__":
    main()