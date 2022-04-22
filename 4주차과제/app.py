from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://stacy:wldms0231@cluster0.x0ed3.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
   return render_template('index.html')

@app.route("/homework", methods=["POST"])
def homework_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']

    doc = {
        'name':name_receive,
        'comment':comment_receive
    }
    db.hw.insert_one(doc)

    return jsonify({'msg':'응원완료!'})

@app.route("/homework", methods=["GET"])
def homework_get():
    comment_list = list(db.hw.find({},{'_id':False}))
    return jsonify({'comments':comment_list})

if __name__ == '__main__':
   app.run('127.0.0.6', port=5000, debug=True)