from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://anwjsrlrhwkd:<password>@cluster0.da3km.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/homework", methods=["POST"])
def homework_post():
    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    print(name_receive, comment_receive)

    db.fan.insert_one({"name": name_receive, "comment": comment_receive})
    return jsonify({'msg':'저장완료'})

@app.route("/homework", methods=["GET"])
def homework_get():
    data = list(db.fan.find({}, {'_id': False}))
    return jsonify({'orders': data})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)