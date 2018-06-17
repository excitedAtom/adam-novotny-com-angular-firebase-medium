import argparse
import os
import subprocess
import sys

container = "adam-novotny-com"

ap = argparse.ArgumentParser()
ap.add_argument("-a", "--action", required=True, choices=["start", "stop", "rm", "ssh"], help="select action")
ap.add_argument("-m", "--mode", required=True, choices=["stage", "prod"], help="select mode")
args = vars(ap.parse_args())
action = args["action"]
mode = args["mode"]

def main():
    generate_docker_compose()
    if action == "start":
        docker_start()
    elif action == "stop":
        docker_stop()
    elif action == "rm":
        docker_rm()
    elif action == "ssh":
        docker_ssh()
    
def docker_ssh():
    subprocess.call("docker exec -it {} /bin/bash".format(container), shell=True)

def docker_start():
    subprocess.call("""
    docker-compose -f docker-compose.yml up;""", shell=True)

def docker_stop():
    subprocess.call("""
    docker stop {0};
    """.format(container), shell=True)

def docker_rm():
    subprocess.call("""
    docker rm {0};
    """.format(container), shell=True)

def generate_docker_compose():
    filename = 'docker-compose.yml'
    destination_dir = os.path.join(os.path.abspath(os.curdir))
    if not os.path.isdir(destination_dir):
        os.makedirs(destination_dir)
    command = "ng serve --watch --host 0.0.0.0 --port 4200"
    if mode == "prod":
        command = "ng serve --prod --aot --host 0.0.0.0 --port 4200"
    file_text = (
"""version: '3'
services:
  angular:
    container_name: adam-novotny-com
    image: adam-novotny-com-img
    build:
      context: ./adam_novotny_com
      dockerfile: Dockerfile
    volumes:
      - ./adam_novotny_com:/mnt/app
    stdin_open: true
    tty: true
    restart: always
    ports:
      - "4200:4200"
    command: "{}"
    """
    ).format(command)

    # Write file
    with open(os.path.join(destination_dir, filename), "w") as f:
        f.write(file_text)

if __name__ == "__main__":
    main()