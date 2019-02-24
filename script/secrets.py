import configparser
import os

cp = configparser.ConfigParser()
cp.read(os.path.abspath(os.path.join(os.path.dirname( __file__ ), "instance", "secrets.ini")))
creds_filename = cp[os.environ["mode"]]["creds_filename"]
bucket_name = cp[os.environ["mode"]]["bucket_name"]
medium_posts_gsheet = cp[os.environ["mode"]]["medium_posts_gsheet"]
firebase_project = cp[os.environ["mode"]]["firebase_project"]