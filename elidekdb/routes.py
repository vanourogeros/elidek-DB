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
        query = """
        SELECT Project_ID, P.Name AS P_Name, Summary, Project_Funds, Start_Date, End_Date, CONCAT(E.Name, ' ',  E.Surname) AS E_Name, Organization_ID
        FROM Project P INNER JOIN Executive E 
        ON P.Executive_ID = E.Executive_ID
        """
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
        if min_Start_Date != '' and min_Start_Date != 'None':
            query += f'WHERE DATEDIFF(P.Start_Date, \'{min_Start_Date}\') > 0'
            where_or_and = '\n    AND'
        if max_Start_Date != '' and max_Start_Date != 'None':
            query += f'{where_or_and} DATEDIFF(P.Start_Date, \'{max_Start_Date}\') < 0'
            where_or_and = '\n    AND'
        if min_End_Date != '' and min_End_Date != 'None':
            query += f'{where_or_and} DATEDIFF(P.End_Date, \'{min_End_Date}\') > 0'
            where_or_and = '\n    AND'
        if max_End_Date != '' and max_End_Date != 'None':
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

@app.route("/executive", methods = ['GET', 'POST'])
def executive_view():
    cur = db.connection.cursor()   
    form = ExecUpdate()

    query = """
    SELECT *
    FROM Executive
    """

    if(request.method == "POST" and form.validate_on_submit()):
        name = str(request.form.get('name'))
        surname = str(request.form.get('surname'))
        
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    executive = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()

    return render_template("executive.html", executive=executive, pageTitle = "Executives Page", form = form)

@app.route("/executive/update/<int:execID>", methods = ["POST"])
def updateExec(execID):
    
    form = ExecUpdate()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = """
        UPDATE executive SET Name = 'name', Surname = 'surname' WHERE Executive_ID = {execID}
        """
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Executive updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("executive_view"))

@app.route("/executive/delete/<int:execID>", methods = ["POST"])
def deleteExec(execID):
    query = f"""
    DELETE FROM executive WHERE Executive_ID = {execID}
    """
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Executive deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("executive_view"))

@app.route("/projects-per-researcher")
def projects_per_researcher_view():
    cur = db.connection.cursor()   

    query = """
    SELECT *
    FROM projects_per_researcher
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()

    return render_template("projects_per_researcher.html", results=results, pageTitle = "Projects per Researcher Page")

@app.route("/projects-per-field")
def projects_per_field_view():
    cur = db.connection.cursor()   

    query = """
    SELECT *
    FROM projects_per_field
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()

    return render_template("projects_per_field.html", results=results, pageTitle = "Projects per Research Field")

@app.route("/specific-research-field", methods = ['GET', 'POST'])
def specific_research_field():
    form = SelectResearchField()
    cur = db.connection.cursor()   
    query = """
    SELECT DISTINCT Field_ID, Field_Name
    FROM projects_per_field
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    results = []
    results2 = []
    #print([entry for entry in cur.fetchall()])
    form.ResearchField.choices = [entry for entry in cur.fetchall()]
    cur.close()

    if(request.method == "POST"):
        ResearchField = str(request.form.get('ResearchField'))
        cur = db.connection.cursor()   

        query = f"""
        SELECT Project.Project_ID, Name
        FROM Project INNER JOIN Refers_To
        ON Project.Project_ID = Refers_To.Project_ID
        WHERE Field_ID = {ResearchField}
        AND DATEDIFF(Project.End_Date, NOW()) > 0
        """

        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]

        query = f"""
        SELECT Researcher.Researcher_ID, CONCAT(Researcher.Name,' ',Researcher.Surname) AS Full_Name, Works_On.Start_Date
        FROM Refers_To INNER JOIN Project
        ON Project.Project_ID = Refers_To.Project_ID AND Field_ID = {ResearchField}
        INNER JOIN Works_On
        ON Project.Project_ID = Works_On.Project_ID
        INNER JOIN Researcher
        ON Works_On.Researcher_ID = Researcher.Researcher_ID
        WHERE DATEDIFF(NOW(), Works_On.Start_Date) > 365
        ORDER BY Researcher.Researcher_ID
        """

        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        results2 = [dict(zip(column_names, entry)) for entry in cur.fetchall()]

        cur.close()

    return render_template("specific_field.html", results=results, results2 = results2, form = form, pageTitle = "Projects for chosen Research Field")
