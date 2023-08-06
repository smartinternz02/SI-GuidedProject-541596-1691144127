from urllib import request
from flask import Flask, render_template, request
import ibm_db

app = Flask(__name__)
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;USERNAME=shn79817;PASSWORD=qEUkr1gnjxlwPTH3;SECURITY=SSL;SSLSERVERCERTIFICATE=DigiCertGlobalRootCA.crt", '', '')
print(ibm_db.active(conn))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form['username']
        pword = request.form['password']
        print(uname, pword)
        sql = 'SELECT * FROM REGISTER_FDP WHERE USERNAME=? AND PASSWORD=?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.bind_param(stmt, 2, pword)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        if out:
            role = out['ROLE']
            if role == 0:
                return render_template("profile_admin.html")
            elif role == 1:
                return render_template("profile_faculty.html")
            else:
                return render_template("profile_student.html")
        else:
            msg = "Invalid Credentials"
            return render_template("login.html", msg=msg)
    return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
