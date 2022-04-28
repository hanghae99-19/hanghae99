from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

client = MongoClient('mongodb+srv://stacy:wldms0231@cluster0.x0ed3.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


# pages
@app.route('/')
def get_home_page():
    return render_template('main.html')

@app.route('/hy')
def get_hy_page():
    return render_template('hy.html')

@app.route('/je')
def get_je_page():
    return render_template('je.html')

@app.route('/hu')
def get_hu_page():
    return render_template('hu.html')

@app.route('/si')
def get_si_page():
    return render_template('si.html')

@app.route('/jy')
def get_jy_page():
    return render_template('jy.html')


# list
@app.route("/하연", methods=["GET"])
def get_hy_list():
    book_list = list(db.db_hy.find({},{'_id':False}))
    return jsonify({'db_hy':book_list})

@app.route("/bookj", methods=["GET"])
def get_je_list():
    book_list = list(db.db_je.find({}, {'_id': False}))
    return jsonify({'db_je': book_list})

@app.route("/현욱", methods=["GET"])
def get_hw_list():
    book_list = list(db.db_hw.find({},{'_id':False}))
    return jsonify({'db_hw':book_list})

@app.route('/list', methods=['GET'])
def get_jy_list():
    data = list(db.db_jy.find({}, {'_id':False}))
    return jsonify({'db_jy': data})

@app.route("/성인", methods=["GET"])
def get_si_list():
    book_list = list(db.db_si.find({}, {'_id': False}))
    return jsonify({'db_si': book_list})


# post
@app.route("/하연", methods=["POST"])
def post_hy():
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

    db.db_hy.insert_one(doc)

    return  jsonify({'msg':'저장완료!'})

    # 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.

@app.route("/book_rank", methods=["POST"])
def post_hy_book_rank():


    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?gt_network=g&gt_keyword=%EC%84%9C%EC%A0%90&gt_target_id=kwd-4863942907&gt_campaign_id=9979905549&gt_adgroup_id=98010719662&gclid=CjwKCAjwsJ6TBhAIEiwAfl4TWNWY2P94euUWZqNO2LW1XRqhQDlYDrLLUZNC54e4okjoFR0Jb3681RoC0CoQAvD_BwE',headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    charts = soup.select('#main_contents > ul > li')

    for cha in charts:

        num = cha.select_one('div.cover > a > strong').text
        img = cha.select_one('div.cover > a > img')['src']
        title = cha.select_one('div.detail > div.title > a > strong').text



        doc2 = {
            'rank': num,
            'img': img,
            'title': title,
        }

        db.book_rank.insert_one(doc2)
        return  jsonify({'msg':'저장완료!'})

app.route("/bookj", methods=["POST"])
def post_je():
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
   db.db_je.insert_one(doc)

   return jsonify({'msg': '저장완료!'})

@app.route("/현욱", methods=["POST"])
def post_hw():

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

    db.db_hw.insert_one(doc)

    return  jsonify({'msg':'기록완료!'})

@app.route('/post', methods=['POST'])
def post_jy():
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
            'image' : img,
            'star' : star_receive,
            'comment' : comment_receive,
            'desc' : desc}

    db.db_jy.insert_one(data)

    return jsonify({'msg':'success'})

@app.route("/성인", methods=["POST"])
def post_si():
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

    db.db_si.insert_one(doc)

    return jsonify({'msg': '저장완료.'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


