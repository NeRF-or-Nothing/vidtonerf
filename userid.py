assignmentID = str(uuid.uuid1())
jsonFileName = "upload/" + assignmentID + ".json"
jsonSurvey = "upload/" + assignmentID + "_survey.json"

#it ideally should randomly select different info/question no. to different user
Idx = random.sample(range(0,10), 5)   


@app.route("/")
def index():
    return render_template("surveyPage.html", data=Idx)


# write input information from webpage to JSON files, each visitor ideally should have their own JSON file.
@app.route("/record")
def recordData():
    if request.method == 'POST':
        print("READING FORM")
        with open(jsonSurvey, 'w') as f:
            json.dump(request.form, f)
        f.close()


if __name__ == "__main__":
    app.config['JSON_SORT_KEYS'] = False
    app.run(debug = True)
# app.config["TEMPLATES_AUTO_RELOAD"] = True
