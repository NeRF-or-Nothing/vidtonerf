from flask import Flask
 
# Flask constructor takes the name of 
# current module (__name__) as argument.
# Weird right?
app = Flask(__name__)
  
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return "Hello World"

# Using angled brackets allows you to reference the variable 
# inside as a function argument tied to the route
@app.route('/<name>')
def hello_name(name: str):
    return f"Hello {name}"

# weburl/balls (so for most test purposes it'll be localhost:5000/balls) 
@app.route('/balls')
def balls():
    return "balls"

# main driver function
if __name__ == '__main__': 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
