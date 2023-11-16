#https://stackoverflow.com/questions/45412051/flask-debugtoolbar-importerror-no-module-named-flask-debugtoolbar

from flask import Flask, request, render_template, redirect, flash

from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 10
app.config["SECRET_KEY"] = "tarvos trigaranus"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

responses = []
survey_length = len(satisfaction_survey.questions)

def wrong_url_redirect():
    flash("You are trying to access an invalid question", 'warning')
    path = f"/questions/{len(responses)}"
    return redirect(path)

@app.route("/")
def go_home():
    responses.clear()
    survey = {
    "title": satisfaction_survey.title, 
    "instructions": satisfaction_survey.instructions
    }
    return render_template("home.html", survey=survey)

@app.route("/questions/<int:id>")
def show_question(id):
    if len(responses) < survey_length and id < survey_length:
        if len(responses) == id:
            current_question = satisfaction_survey.questions[id]
            qa = {
                "id": id,
                "question": current_question.question,
                "choices": current_question.choices,
                "allow_text": current_question.allow_text
            }
            return render_template("question.html",  qa=qa)
        else: #len(resonses) not equal to id
            return wrong_url_redirect()
    if len(responses) < survey_length and id >= survey_length:
        return wrong_url_redirect()
    return redirect("/thankyou")


@app.route("/answer")
def show_answer():
    responses.append(request.args["answer"])
    #print(responses)
    id = int(request.args["id"]) + 1 
    path = f"/questions/{id}"
    return redirect(path)

@app.route("/thankyou")
def say_thankyou():
    return render_template("thankyou.html")