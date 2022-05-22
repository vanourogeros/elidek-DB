from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from elidekdb import app, db ## initially created by __init__.py, need to be used here

@app.route("/")
def index():
    return render_template("landing.html", pageTitle = "Landing Page")


@app.route("/programs")
def programs_view:
    cur = db.connection.cursor()   

    query = """
    SELECT DISTINCT 
    Name, ELISEK_Sector
    FROM Programs
    """
    cur.execute(query)
    programs = cur.fetchall()

    return render_template("programs.html", programs=programs)
