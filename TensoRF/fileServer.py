from flask import Flask, appcontext_popped
from flask import send_from_directory
import time
from multiprocessing import Process
import os


app = Flask(__name__)

@app.route('/output/videos/<path:path>')
def send_video(path):
    return send_from_directory('output/videos',path)

@app.route('/output/models/<path:path>')
def send_model(path):
    return send_from_directory('output/models',path)

def dummy_nerf():
    count = 0
    while(True):
        print(f"Job {count} Started ")
        time.sleep(1)
        print(f"Job {count} complete")
        print()
        count+=1

def start_flask():
    global app
    app.run(debug=True)

# Demonstrating how files will be pulled from the cache
"""if __name__ == "__main__":
    flaskProcess = Process(target=start_flask, args= ())
    nerfProcess = Process(target=dummy_nerf, args= ())

    flaskProcess.start()
    nerfProcess.start()

    flaskProcess.join()
    nerfProcess.join()"""

