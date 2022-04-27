from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from PIL import Image


from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.b7vsn.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta






@app.route("/하연", methods=["POST"])
def movie_post():

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

    return  jsonify({'msg':'저장완료!'})

    # 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.


@app.route("/하연", methods=["GET"])
def book_get():

    book_list = list(db.books.find({},{'_id':False}))


    return jsonify({'books':book_list})




@app.route("/book_rank", methods=["POST"])
def book_rank_post():


    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?gt_network=g&gt_keyword=%EC%84%9C%EC%A0%90&gt_target_id=kwd-4863942907&gt_campaign_id=9979905549&gt_adgroup_id=98010719662&gclid=CjwKCAjwsJ6TBhAIEiwAfl4TWNWY2P94euUWZqNO2LW1XRqhQDlYDrLLUZNC54e4okjoFR0Jb3681RoC0CoQAvD_BwE',headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    charts = soup.select('#main_contents > ul > li')

    for cha in charts:

        num = cha.select_one('div.cover > a > strong').text
        img = cha.select_one('div.cover > a > img')['src']
        title = cha.select_one('div.detail > div.title > a > strong').text


        # print('{}위 -- {} -- {}'.format(num,title,img))

        doc2 = {
            'rank': num,
            'img': img,
            'title': title,
        }

        db.book_rank.insert_one(doc2)
        return  jsonify({'msg':'저장완료!'})


# @app.route("/book_rank", methods=["GET"])
# def book_rank_get():
#
#     book_rank_list = list(db.book_rank.find({},{'_id':False}))
#
#
#     return jsonify({'book2':book_rank_list})






if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)


@app.route('/hy')
def getTicket_hy():
   return render_template('hy.html')


@app.route('/je')
def getTicket_je():
   return render_template('je.html')

@app.route('/hu')
def getTicket_hu():
   return render_template('hu.html')

@app.route('/')
def home():
   return render_template('main.html')


@app.route("/bookj", methods=["POST"])
def book_post_je():

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
def book_get_hy():
   book_list = list(db.books.find({}, {'_id': False}))
   return jsonify({'books': book_list})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)



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
def book_get_hw():

    book_list = list(db.books.find({},{'_id':False}))


    return jsonify({'books':book_list})




if __name__ == '__main__':
   app.run('0.0.0.0', port=5010, debug=True)