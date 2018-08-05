# Converts json article from medium to firestore database
# Example url: https://medium.com/@adamnovo/50-percent-of-2017-icos-have-failed-already-66eddefaacc7?format=json
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

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--mode", required=True, choices=["stage", "prod"], help="mode")
ap.add_argument("-d", "--download", required=True, choices=["y", "n"], help="download articles")
args = vars(ap.parse_args())
download = args["download"]
mode = args["mode"]

def main():
    load_articles()

def load_articles():
    db = get_db()
    db_collection = "medium"
    docs = db.collection("medium").get()
    for doc in docs:
        id = doc.id
        doc_dict = doc.to_dict()
        title = doc_dict["title"]
        url = doc_dict["url"]
        article = get_article(url)
        check_article_json_structure(article)
        article_clean = get_clean_article(title, article)
        print("{} loading to firebase".format(title))
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

def get_db():
    creds_filename = "adamnovotnycom-stage-firebase-adminsdk.json"
    if mode == "prod":
        creds_filename = "adamnovotnycom-prod-firebase-adminsdk.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(os.path.join(
        os.path.dirname( __file__ ), "instance", creds_filename))
    db = firestore.Client()
    return db

def get_clean_article(name, article):
    article_clean = {}
    article_clean["url"] = name
    article_clean["title"] = article["payload"]["value"]["title"]
    article_clean["url_medium"] = "https://medium.com/@adam5ny/" + article["payload"]["value"]["uniqueSlug"]
    article_clean["date_unix"] = article["payload"]["value"]["firstPublishedAt"]
    article_clean["date_str"] = convert_unix_date(article["payload"]["value"]["firstPublishedAt"])
    paragraphs_clean = []
    paragraphs_medium = article["payload"]["value"]["content"]["bodyModel"]["paragraphs"]
    for i in range(1, len(paragraphs_medium)): #skip #0, which is the title
        par_clean = {}
        par = paragraphs_medium[i]
        if (par["type"] == 1 or par["type"] == 6 or par["type"] == 7 or par["type"] == 8
                or par["type"] == 9 or par["type"] == 10):
            par_clean["type"] = par["type"]
            if par["type"] == 8:
                par_clean["text"] = par["text"]
            else:
                par_clean["text"] = par["text"]
            links = []
            if "markups" in par:
                for j in par["markups"]:
                    if j["type"] == 3:
                        links.append(j["href"])
            par_clean["links"] = links
            paragraphs_clean.append(par_clean)
    article_clean["paragraphs"] = paragraphs_clean
    return article_clean

def convert_unix_date(unix_date):
    unix_date = int(unix_date) / 1000
    date = datetime.datetime.fromtimestamp(unix_date).strftime(
        '%m/%d/%Y')
    return date

def insert_article_db(name, data_dict):
    db = get_db()
    db_collection = "blog"
    collection_ref = db.collection(db_collection).document(name)
    collection_ref.set(data_dict)

if __name__ == "__main__":
    main()