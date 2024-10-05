import flask, json
import re, io

app = flask.Flask(__name__)


def process(raw_wordbank):
    lines = raw_wordbank.split()
    words = {"Normal": set()}
    bank_name = ""
    for line in lines:
        if line:
            if not line[0].isalpha():
                bank_name = line[1:-2].capitalize()
                if bank_name not in words:
                    words[bank_name] = set()
            elif bank_name:
                line = "".join([i for i in line if i.isalpha()])
                words[bank_name].add(line.lower())
                words["Normal"].add(line.lower())
    for key in words:
        words[key] = sorted(list(words[key]))
    return words


@app.route("/")
def home():
    return flask.render_template("index.html")


@app.route("/download_json", methods=["GET"])
def download_json():
    paragraph = flask.request.args.get("paragraph", "")
    words = paragraph.replace("+", "").replace("'", '"')
    return flask.Response(
        words,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment;filename=wordBank.json"},
    )


@app.route("/segment_text", methods=["GET"])
def classify_url():
    paragraph = flask.request.args.get("paragraph", "")
    words = process(paragraph)
    return flask.render_template("wordbank.html", words=words)
