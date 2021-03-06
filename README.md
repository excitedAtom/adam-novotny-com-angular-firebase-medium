# adam-novotny-com-angular-firebase-medium

- The application serves a custom Firebase-hosted website that includes a list blog posts available on Medium
- Use case: publishers can to take advantage of excellent distribution platforms such as Medium, while keeping direct ownership of the content in case the distribution platform no longer supports or removes the content
- Workflow: 
  - blogs are published to Medium.com first
  - a simple Python script is then used to download json-formatted articles from Medium and upload content to [Firebase Cloud Firestore](https://firebase.google.com/docs/firestore/) to be hosted on custom website
  - the script can be run periodically as a serverless function
- Tech stack: [Angular](https://angular.io) front end, [Firebase](https://firebase.google.com) backend, [Medium.com](https://www.medium.com) blog publishing platform, [Python 3](https://www.python.org/downloads/release/python-360/)
- **Example deployment: [adamnovotny.com](https://www.adamnovotny.com)**

## Download articles from Medium and upload content to Firebase

        >> save new article titles and urls in a Google Sheet that should be made public (published) and url stored in script/instance/secrets.ini
        python script/medium.py -m [stage/prod] -b y

## Run docker stage or prod server + build + deploy

        python script/docker.py -m [stage/prod] -a start;
        # separate terminal:
        python script/docker.py -m [stage/prod] -a ssh;
        npm audit fix;
        ng build [--prod] --aot;
        # separate terminal:
        firebase logout;
        firebase login;
        python script/firebase.py -m [stage/prod];