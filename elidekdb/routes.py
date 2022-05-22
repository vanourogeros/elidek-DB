from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from elidekdb import app, db ## initially created by __init__.py, need to be used here

@app.route("/")
def index():
    try:
        return render_template("landing.html", pageTitle = "Landing Page")
