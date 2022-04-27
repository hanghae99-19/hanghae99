from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.ryfyy.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/성인", methods=["POST"])
def book_post_si():

    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content'][:40] + '.....'

    doc = {
        'title': title,
        'image': image,
        'desc': desc,
        'star': star_receive,
        'comment': comment_receive,
        'url': url_receive

    }

    db.books.insert_one(doc)

    return jsonify({'msg': '저장완료.'})

@app.route("/성인", methods=["GET"])
def book_get_si():
    book_list = list(db.books.find({}, {'_id': False}))

    return jsonify({'books': book_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
