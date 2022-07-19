# Running main.py (a semi-coherent web-server)

## Fire up a terminal and run (inside this folder)
```sh
python main.py
```
### Now if all is well, the last line of output should be something like ``` * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)```
### If the url is clickable, it'll open your browser and navigate you to your local host at port 5000. If not, copy and paste that into your browser. You can now interact with the running flask module!
### To navigate to a subpage, append the url with a forward slash and the location, i.e http://127.0.0.1:5000/hello (this is assuming the page is valid and exists)

## Demo posting a video (or any file)

### Ensure you're in the correct directory (you can post any file but you **want** to post a video)
```sh
curl -X POST -F 'file=@main.py' localhost:5000/video
```

### The Flask API at this point should show some type of logging info if you set this up and ran it correctly.