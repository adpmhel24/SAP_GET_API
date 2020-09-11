import json
from sap_app import db, app, auth, bcrypt
from sap_app._helpers import data_rows, CustomJSONEncoder
from sap_app.models import User
from flask import jsonify, request, abort, url_for

app.json_encoder = CustomJSONEncoder

@app.route('/api/getso', methods=["GET"])
@auth.login_required
def get_so():
    docnum = request.args.get('docnum')
    if docnum:
        rq = db.engine.execute(f"SELECT * FROM [db_for_ai].[dbo].[vSO] a1 WHERE a1.DocDate>='20200910' and a1.docnum = {docnum}")
        data = data_rows(rq)
    else:
        rq = db.engine.execute("SELECT * FROM [db_for_ai].[dbo].[vSO] a1 WHERE a1.DocDate>='20200910'")
        data = data_rows(rq)
    response = jsonify(data), 201
    return response

@app.route('/api/getitr', methods=["GET"])
@auth.login_required
def get_itr():
    docnum = request.args.get('docnum')
    if docnum:
        rq = db.engine.execute(f"SELECT * FROM [db_for_ai].[dbo].[vITR] a1 WHERE a1.DocDate>='20200910' and a1.docnum = {docnum}")
        data = data_rows(rq)
    else:
        rq = db.engine.execute("SELECT * FROM [db_for_ai].[dbo].[vITR] a1 WHERE a1.DocDate>='20200910'")
        data = data_rows(rq)
    response = jsonify(data), 201
    return response

@app.route('/api/getpo', methods=["GET"])
@auth.login_required
def get_po():
    row_list = []
    docnum = request.args.get('docnum')
    if docnum:
        rq = db.engine.execute(f"SELECT * FROM [db_for_ai].[dbo].[vPO] a1 WHERE a1.DocDate>='20200910' and a1.docnum = {docnum}")
        data = data_rows(rq)
    else:
        rq = db.engine.execute("SELECT * FROM [db_for_ai].[dbo].[vPO] a1 WHERE a1.DocDate>='20200910'")
        data = data_rows(rq)
    response = jsonify(data), 201
    return response

@app.route('/api/users/create', methods = ['POST'])
@auth.login_required
def new_user():
    fullname = request.args.get('fullname')
    email = request.args.get('email')
    password = request.args.get('password')
    if email is None or password is None or fullname is None:
        abort(400) # missing arguments
    if User.query.filter_by(email = email).first() is not None:
        abort(400) # existing user
    user = User(fullname = fullname, email=email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'email': user.email }), 201

@app.route('/api/get_token')
def get_auth_token():
    email = request.args.get('email')
    password = request.args.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        if user.verify_password(password):
            token = user.generate_auth_token()
            return jsonify({'success': True, 'token': token}), 201

@auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user:
        return True
    return False