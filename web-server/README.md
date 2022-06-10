# Installing Flask

### Honestly this will probably work for any OS, although you **should** know what command runs python.
### If you're unsure, run 
```sh
where python
``` 
### or 
```sh 
which python
```
### in a terminal.
### If there aren't any results or there's an error, try those two commands with "python3" as the argument instead. (These commands are Unix-like but I believe "which" works in Windows.)
</br>

### Then, install flask 
###
```sh
python -m pip install flask
```
</br>

# Running app.py (a dummy test)

## Fire up a terminal and run
```sh
flask run
```
### Now if all is well, the last line of output should be something like ``` * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)```
### If the url is clickable, it'll open your browser and navigate you to your local host at port 5000. If not, copy and paste that into your browser. You can now interact with the running flask module!
### To navigate to a subpage, append the url with a forward slash and the location, i.e http://127.0.0.1:5000/hello (this is assuming the page is valid and exists)
