from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from elidekdb import app, db ## initially created by __init__.py, need to be used here

@app.route("/")
def index():
    return render_template("landing.html", pageTitle = "Landing Page")


@app.route("/programs")
def programs_view():
    cur = db.connection.cursor()   

    query = """
    SELECT *
    FROM Program
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    programs = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    #programs = cur.fetchall()
    cur.close()
    #print(programs[1])

    return render_template("programs.html", programs=programs, pageTitle = "Programs Page")
