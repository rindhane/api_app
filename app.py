from flask import Flask ,request , jsonify, g
import os
import sqlite3
#Init app
app= Flask(__name__)


#Database config
basedir = os.path.abspath(os.path.dirname(__file__))
db_path=basedir+'/equityBSE.db'

#database handlers:
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


#Row Factory for resutls from database
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

#Get single product 
@app.route('/stocks/<id>',methods=['GET'])
def get_product(id):
    try:
        db= get_db()
        db.row_factory = make_dicts
        result=db.execute(f'select * from {id}').fetchall()
    except sqlite3.OperationalError:
        result=[]
    return jsonify(result)

#trial Testing link
@app.route("/",methods=["GET"])
def get():
    return jsonify({"msg":'Hello_world'})

#Run Server
if __name__=="__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
