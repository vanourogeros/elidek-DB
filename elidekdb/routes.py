from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from elidekdb import app, db ## initially created by __init__.py, need to be used here
from elidekdb.forms import *

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

@app.route("/projects", methods = ['GET', 'POST'])
def projects_view():
    form = ProjectFilterForm()
    cur = db.connection.cursor()   

    query = """
    SELECT Project_ID, P.Name AS P_Name, Summary, Project_Funds, Start_Date, End_Date, CONCAT(E.Name, ' ',  E.Surname) AS E_Name, Organization_ID
    FROM Project P INNER JOIN Executive E 
    ON P.Executive_ID = E.Executive_ID
    """

    if(request.method == "POST" and form.validate_on_submit()):
        min_Start_Date = str(request.form.get('min_Start_Date'))
        max_Start_Date = str(request.form.get('max_Start_Date'))
        min_End_Date = str(request.form.get('min_End_Date'))
        max_End_Date = str(request.form.get('max_End_Date'))
        min_Duration = str(request.form.get('min_Duration'))
        max_Duration = str(request.form.get('max_Duration'))
        executive = str(request.form.get('executive'))
        print("form!")
        print(max_Start_Date)
        where_or_and = 'WHERE'
        if min_Start_Date != '':
            query += f'WHERE DATEDIFF(P.Start_Date, \'{min_Start_Date}\') > 0'
            where_or_and = '\n    AND'
        if max_Start_Date != '':
            query += f'{where_or_and} DATEDIFF(P.Start_Date, \'{max_Start_Date}\') < 0'
            where_or_and = '\n    AND'
        if min_End_Date != '':
            query += f'{where_or_and} DATEDIFF(P.End_Date, \'{min_End_Date}\') > 0'
            where_or_and = '\n    AND'
        if max_End_Date != '':
            query += f'{where_or_and} DATEDIFF(P.End_Date, \'{max_End_Date}\') < 0'
            where_or_and = '\n    AND'
        if min_Duration != '':
            query += f'{where_or_and} DATEDIFF(P.End_Date, P.Start_Date) > {min_Duration}'
            where_or_and = '\n    AND'
        if max_Duration != '':
            query += f'{where_or_and} DATEDIFF(P.End_Date, P.Start_Date) < {max_Duration}'
            where_or_and = '\n    AND'
        if executive != '':
            query += f'{where_or_and} CONCAT(E.Name, \' \',  E.Surname) = \'{executive}\''
            where_or_and = '\n    AND'

    print(query)
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    projects = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    #print(projects)
    #programs = cur.fetchall()
    cur.close()
    #print(programs[1])

    return render_template("projects.html", projects=projects, pageTitle = "Projects Page", form = form)

@app.route("/projects/<int:projectID>")
def fetch_project_researchers(projectID):
    cur = db.connection.cursor()   

    query = f"""
    SELECT XX.Researcher_ID, CONCAT(Name,' ', Surname) AS Full_Name, Gender, Recruitment_Date FROM (
    SELECT X.Researcher_ID
    FROM Project P INNER JOIN Works_On X
    ON P.Project_ID = X.Project_ID
    WHERE P.Project_ID = {projectID}
    ) XX INNER JOIN Researcher YY 
    ON XX.Researcher_ID = YY.Researcher_ID
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    proj_researchers = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    #programs = cur.fetchall()
    cur.close()
    #print(programs[1])

    return render_template("fetch_project.html", proj_researchers=proj_researchers, pageTitle = f"Researchers working on Project with ID {projectID}")
