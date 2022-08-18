from time import sleep

def cleanup(client):
    while(True):
        # Check MongoDB, delete files and clear MongoDB for completed jobs
        sleep(900)