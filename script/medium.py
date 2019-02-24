# Converts json article from Medium to Firestore database
# Example url: https://medium.com/@adamnovo/50-percent-of-2017-icos-have-failed-already-66eddefaacc7
# Requirements
#   - save service-account-creds.json Gcloud file in folder instance/
#   - pip install --upgrade google-cloud-firestore

import argparse
import datetime
import json
import requests
import os
import pickle
import sys
from google.cloud import firestore
from google.cloud import storage

import GSheet

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--mode", required=True, choices=["stage", "prod"], help="mode")
ap.add_argument("-b", "--backup", required=True, choices=["y", "n"], help="Backup data to firebase storage")
args = vars(ap.parse_args())
mode = args["mode"]
backup = args["backup"]

os.environ["mode"] = mode
from secrets import creds_filename, bucket_name, medium_posts_gsheet

def main():
    init_firebase()
    headers, rows = GSheet.main(medium_posts_gsheet)
    for row in rows:
        for i in range(len(headers)):
            if headers[i] == "title":
                title = row[i]
            elif headers[i] == "url":
                url = row[i] + "?format=json"
        print("{} moving from medium to firebase".format(title))
        article = get_article(url)
        check_article_json_structure(article)
        article_clean = get_clean_article(title, article)
        insert_article_db(title, article_clean)

def get_article(url_medium):
    r = requests.get(url_medium)
    article_str = r.text
    article = json.loads(article_str[16:])
    return article

def check_article_json_structure(article):
    if not isinstance(article["payload"]["value"]["title"], str):
        raise Exception("json Medium API changed")
    if not isinstance(article["payload"]["value"]["uniqueSlug"], str):
        raise Exception("json Medium API changed")
    if not isinstance(article["payload"]["value"]["firstPublishedAt"], int):
        raise Exception("json Medium API changed")
    if not isinstance(article["payload"]["value"]["content"]["bodyModel"]["paragraphs"], list):
        raise Exception("json Medium API changed")

def init_firebase():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(os.path.join(
        os.path.dirname( __file__ ), "instance", creds_filename))

def get_clean_article(name, article):
    article_clean = {}
    article_clean["url"] = name
    article_clean["title"] = article["payload"]["value"]["title"]
    article_clean["url_medium"] = "https://medium.com/@excitedAtom/" + article["payload"]["value"]["uniqueSlug"]
    article_clean["date_unix"] = article["payload"]["value"]["firstPublishedAt"]
    article_clean["date_str"] = convert_unix_date(article["payload"]["value"]["firstPublishedAt"])
    paragraphs_clean = []
    paragraphs_medium = article["payload"]["value"]["content"]["bodyModel"]["paragraphs"]
    for i in range(1, len(paragraphs_medium)): #skip #0, which is the title
        par_clean = {}
        par = paragraphs_medium[i]
        if (par["type"] == 1 or par["type"] == 4 or par["type"] == 6 or par["type"] == 7 
                or par["type"] == 8 or par["type"] == 9 or par["type"] == 10,
                par["type"] == 13):
            par_clean["type"] = par["type"]
            if par["type"] == 8:
                par_clean["text"] = par["text"]
            elif par["type"] == 4:
                # image
                par_clean["text"] = par["text"]
                par_clean["id"] = par["metadata"]["id"]
                if backup == "y":
                    backup_image_to_firebase_storage(par_clean["id"])
            else:
                par_clean["text"] = par["text"]
            if "markups" in par and par["type"] != 4:
                # insert a tags in appropriate places based on start and end index
                hrefs = par["markups"]
                len_inserted = 0
                for i in hrefs:
                    if i["type"] == 3:
                        url = i["href"]
                        start_href = len_inserted + int(i["start"])
                        start_tag = """<a href="{}" target="_blank">""".format(url)
                        par_clean["text"] = insert_into_string(start_href, par_clean["text"], start_tag)
                        len_inserted += len(start_tag)
                        end_href = len_inserted + int(i["end"])
                        end_tag = "</a>"
                        par_clean["text"] = insert_into_string(end_href, par_clean["text"], end_tag)
                        len_inserted += len(end_tag)
            paragraphs_clean.append(par_clean)
    article_clean["paragraphs"] = paragraphs_clean
    return article_clean

def convert_unix_date(unix_date):
    unix_date = int(unix_date) / 1000
    date = datetime.datetime.fromtimestamp(unix_date).strftime("%b %d, %Y")
    return date

def insert_into_string(index, text, insertion_str):
    return text[:index] + insertion_str + text[index:]

def insert_article_db(name, data_dict):
    db = firestore.Client()
    db_collection = "blog"
    collection_ref = db.collection(db_collection).document(name)
    collection_ref.set(data_dict)

def backup_image_to_firebase_storage(image_id):
    url = "https://cdn-images-1.medium.com/max/2600/{}".format(image_id)
    local_filename = download_file(url, image_id)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(image_id)
    blob.upload_from_filename(local_filename)
    print("Image {} backed up to firebase".format(image_id))

def download_file(url, image_id):
    local_filename = os.path.abspath(os.path.join("backup", "images", image_id))
    with requests.get(url, stream=True) as r:
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    return local_filename

if __name__ == "__main__":
    main()