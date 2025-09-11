from flask import Flask, render_template, jsonify
import requests, os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/comicgenerator")
def comicgenerator():
    return render_template("comicgenerator.html")

@app.route("/comicreader")
def comicreader():
    return render_template("comicreader.html")

if __name__ == '__main__':
    app.run(debug=True)
