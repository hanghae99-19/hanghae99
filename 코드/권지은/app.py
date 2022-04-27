from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://stacy:wldms0231@cluster0.x0ed3.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
   return render_template('je.html')

@app.route("/bookj", methods=["POST"])
def book_post():

    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content'][:40] + '.....'
    image = soup.select_one('meta[property="og:image"]')['content']

    doc = {
        'title': title,
        'image': image,
        'desc': desc,
        'star': star_receive,
        'comment': comment_receive
    }
    db.books.insert_one(doc)

    return jsonify({'msg': '저장완료!'})

@app.route("/bookj", methods=["GET"])
def book_get():
    book_list = list(db.books.find({},{'_id':False}))
    return jsonify({'books': book_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)