from scrapper import Scrap_news_owl
from flask import Flask, render_template, jsonify, request

newScrapper = Scrap_news_owl()


app = Flask(__name__)


@app.route("/")
def go():
    return render_template("index.html")


@app.route("/search")
def search():
    param_value = request.args.get('search')
    hamropatro = newScrapper.hamro_patro(search_title=param_value)
    annapurna = newScrapper.annapurna_post(page=1, search=param_value)
    onlineKhabar = newScrapper.online_khabar(search=param_value)
    data = annapurna+hamropatro+onlineKhabar
    return jsonify(data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
