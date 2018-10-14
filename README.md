# adam-novotny-com-angular-firebase-medium

- The application serves a custom Firebase-hosted website and a blog.
- Use case: publishers can to take advantage of excellent distribution platforms such as Medium, while keeping direct ownership of the content in case the distribution platform no longer supports or removes the content.
- Workflow: 
  - blogs are published to Medium first
  - a simple Python script is then used to download json-formatted articles from Medium and upload content to [Firebase Cloud Firestore](https://firebase.google.com/docs/firestore/) to be hosted on custom website
  - the script can be run periodically as a serverless function
- Tech stack: [Angular](https://angular.io) front end, [Firebase](https://firebase.google.com) backend, [Medium.com](https://www.medium.com) blog publishing platform, [Python 3](https://www.python.org/downloads/release/python-360/), [Google Sheets](https://www.google.com/sheets)
- **Example deployment: [adamnovotny.com](https://www.adamnovotny.com)**

## 0) Download articles from Medium and upload content to Firebase

        >> save new article titles and urls in firestore/medium/{id}
        >> download images from medium and save to assets/images/[medium_id].jpg
        python script/medium.py -m stage
        python script/medium.py -m prod

## 1) Run docker development server, build and deploy

        python script/docker.py -a start -m stage
        python script/docker.py -a ssh -m stage
        ng build --aot
        python script/firebase.py -m stage

## 2) Run docker production server

        python script/docker.py -a start -m prod
        python script/docker.py -a ssh -m prod
        ng build --prod --aot
        python script/firebase.py -m prod