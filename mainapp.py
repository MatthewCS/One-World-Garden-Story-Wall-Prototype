import data
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
import re
import sqlite3


app = Flask(__name__, static_url_path='/static')


@app.route("/")
def index_page():
    return redirect("/submit", code=302)


@app.route("/submit")
def submission_page():

    user_id = str(datetime.now())

    with sqlite3.connect('test.db') as conn:
        cursor = conn.cursor()
        user_id += data.get_new_id(cursor)

    user_id = re.sub("[^0-9]", "", user_id)

    return render_template("submit.html")


@app.route("/send_data", methods=['POST'])
def post_story():

    if request.method == "POST":

        if "story" not in request.args:
            return "Error: required story field not found in the URL!"

        story = request.args["story"]
        author = request.args["author"] if "author" in request.args else ""
        contact = request.args["contact"] if "contact" in request.args else ""
        # video = request.args["video"] if "video" in request.args else ""

        with sqlite3.connect('test.db') as conn:
            cursor = conn.cursor()
            id = data.add_data_to_table(cursor, conn, author, story, contact)

        if video != "":
            # video uploading stuff would go here, in a more perfect world
            pass

        return "Success!"



@app.route("/approve_poem", methods=['POST'])
def approve_poem():

    if request.method == "POST":

        id = request.args["id"] if "id" in request.args else ""
        status = request.args["status"] if "status" in request.args else ""

        if id == "":
            return "Error: required id field not found"
        elif status == "":
            return "Error: required status field not found"

        with sqlite3.connect('test.db') as conn:
            cursor = conn.cursor()
            if status == "approve":
                data.authenticate_story(conn, cursor, id)
            elif status == "deny":
                data.remove_story(conn, cursor, id)
            else:
                return "Error: status field not set to \"approve\" or \"deny\""
        return "Success!"


@app.route("/submitted")
def thank_you_page():
    return render_template("thank_you.html")


@app.route("/pending")
def pending_page():

    with sqlite3.connect('test.db') as conn:
        cursor = conn.cursor()
        stories = list(data.get_unauthorized_stories(cursor))

        return render_template("evaluate.html", stories=stories)

@app.route("/approved")
def approved_page():

    with sqlite3.connect('test.db') as conn:
        cursor = conn.cursor()
        stories = list(data.get_authorized_stories(cursor))

        return render_template("approved.html", stories=stories)


if __name__ == "__main__":
    app.run()
