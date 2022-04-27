from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup


client = MongoClient('mongodb+srv://anwjsrlrhwkd:spa0000@cluster0.da3km.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.dbsparta


app = Flask(__name__)


@app.route('/jy')
def jy_page():
    return  render_template('jy.html')

@app.route('/list', methods=['GET'])
def jy_list():
    data = list(db.book.find({}, {'_id':False}))
    return jsonify({'orders': data})

@app.route('/post', methods=['POST'])
def jy_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    # 크롤링
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    re = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(re.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content'].split("-")[0]
    img = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']


    # DB
    data = {'title' : title,
            'img' : img,
            'star' : star_receive,
            'comment' : comment_receive,
            'desc' : desc}

    db.book.insert_one(data)

    return jsonify({'msg':'success'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)



