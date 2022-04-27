from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup


from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.arjwt.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
   return render_template('hu.html')

@app.route("/현욱", methods=["POST"])
def book_post():

    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content'][:40]+'.....'
    image = soup.select_one('meta[property="og:image"]')['content']



    doc = {

        'title' : title,
        'image' : image,
        'desc' : desc,
        'star' : star_receive,
        'comment' : comment_receive,
        'url' : url_receive

    }


    db.books.insert_one(doc)

    return  jsonify({'msg':'기록완료!'})


@app.route("/현욱", methods=["GET"])
def book_get():

    book_list = list(db.books.find({},{'_id':False}))


    return jsonify({'books':book_list})




if __name__ == '__main__':
   app.run('0.0.0.0', port=5010, debug=True)