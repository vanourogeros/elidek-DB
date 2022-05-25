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
        GROUP BY Researcher.Researcher_ID
        """

        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        results2 = [dict(zip(column_names, entry)) for entry in cur.fetchall()]

        cur.close()

    return render_template("specific_field.html", results=results, results2 = results2, form = form, pageTitle = "Projects for chosen Research Field")


@app.route("/organizations-consecutive-year-projects")
def consecutive_year_orgs_view():
    cur = db.connection.cursor()   

    query = """
            select Organization.Organization_ID, Organization.Name, Organization.Acronym, X.Y AS Year, Projects_This_Year
            from
            (
                select DISTINCT Organization_ID AS O, YEAR(Start_Date) as Y,
                (
                    select count(*)
                    from project
                    where YEAR(Start_Date) = Y
                    AND Organization_ID = O
                ) AS Projects_This_Year,
                (
                    select count(*)
                    from project
                    where YEAR(Start_Date) + 1 = Y
                    AND Organization_ID = O
                ) AS Projects_Last_Year
                from project
                having Projects_This_Year = Projects_Last_Year
                order by O
            ) X INNER JOIN Organization ON Organization.Organization_ID = X.O
            """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()

    return render_template("consecutive_years.html", results=results, pageTitle = "Organizations with same number of projects in two concecutive years (more than 10 soon)")

@app.route("/top-three-field-pairs")
def top_field_pairs_view():
    cur = db.connection.cursor()   

    query = """
            SELECT Field_1, R1.Name AS Name_1, Field_2, R2.Name AS Name_2, pair_count
            FROM
            (
                SELECT DISTINCT X.Field_ID AS Field_1, Y.Field_ID AS Field_2,
                    (
                        SELECT COUNT(*)
                        FROM Refers_to XX INNER JOIN Refers_To YY
                        ON XX.Project_ID = YY.Project_ID 
                        WHERE XX.Field_ID = X.Field_ID AND YY.Field_ID = Y.Field_ID AND XX.Field_ID <> YY.Field_ID
                    ) AS pair_count
                FROM Refers_to X INNER JOIN Refers_To Y
                ON X.Project_ID = Y.Project_ID
                WHERE X.Field_ID < Y.Field_ID
                ORDER BY pair_count DESC LIMIT 3
                ) AS top_pairs
                INNER JOIN Research_Field R1 ON R1.Field_ID = top_pairs.Field_1 
                INNER JOIN Research_Field R2 ON top_pairs.Field_2 = R2.Field_ID
            """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()

    return render_template("top_three_field_pairs.html", results=results, pageTitle = "Top three field pairs")

@app.route("/most-prolific-researchers")
def prolific_researchers():

    cur = db.connection.cursor()

    query = """
            CREATE VIEW IF NOT EXISTS project_count AS
            SELECT DISTINCT Researcher.Researcher_ID AS R_ID, CONCAT(Researcher.Name, ' ', Researcher.Surname) AS Full_Name, FLOOR(DATEDIFF(NOW(), Birth_Date)/365) AS Age,
            (
                SELECT COUNT(*) FROM Works_On INNER JOIN Researcher
                ON Works_On.Researcher_ID = Researcher.Researcher_ID
                INNER JOIN Project ON Project.Project_ID = Works_On.Project_ID
                WHERE Researcher.Researcher_ID = R_ID AND DATEDIFF(Project.End_Date, NOW()) > 0
            ) AS project_cnt
            FROM Works_On INNER JOIN Researcher
            ON Works_On.Researcher_ID = Researcher.Researcher_ID
            WHERE DATEDIFF(NOW(), Birth_Date) < 365*40
            ORDER BY project_cnt DESC;
            """
    cur.execute(query)   

    query = """
            select DISTINCT T2.R_ID, T2.Full_Name, T2.Age, T2.project_cnt FROM
            (select * from project_count
            HAVING project_cnt = MAX(project_cnt)) T1
            INNER JOIN project_count T2 ON T1.project_cnt = T2.project_cnt
            """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()

    return render_template("prolific_researchers.html", results=results, pageTitle = "Prolific Researchers")

@app.route("/executive-money-bags")
def top_executives_view():

    cur = db.connection.cursor()
    query = """
        CREATE VIEW IF NOT EXISTS company_funders AS
        SELECT DISTINCT Executive.Executive_ID, CONCAT(Executive.Name, ' ', Executive.Surname) AS Full_Name, Organization.Name AS comp_name, SUM(Project.Project_Funds) AS Total_Funds FROM 
        Executive INNER JOIN Project 
        ON Executive.Executive_ID = Project.Executive_ID
        INNER JOIN Organization ON Project.Organization_ID = Organization.Organization_ID
        WHERE Organization.Org_Type = "Company"
        GROUP BY Executive.Executive_ID, Organization.Organization_ID
        ORDER BY Total_Funds DESC
        """
    cur.execute(query)
    query = """
            SELECT Executive_ID, Full_Name, comp_name, MAX(Total_Funds) as new_Total_Funds
            FROM company_funders
            GROUP BY Executive_ID
            ORDER BY new_Total_Funds DESC LIMIT 5
            """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()

    return render_template("top_executives.html", results=results, pageTitle = "Executives giving most money to a company")

@app.route("/researchers-on-projects-without-work")
def many_no_work_projects_view():
    cur = db.connection.cursor()
    query = """
    SELECT R.Researcher_ID, CONCAT(R.Name,' ',R.Surname) AS Full_Name, COUNT(X.Project_ID) AS project_cnt FROM
    (
    SELECT Project_ID from Project 
    WHERE Project_ID NOT IN (SELECT Project_ID from work_to_be_submitted)
    ) X
    INNER JOIN Works_On Y ON X.Project_ID = Y.Project_ID
    INNER JOIN Researcher R ON Y.Researcher_ID = R.Researcher_ID
    GROUP BY R.Researcher_ID
    HAVING project_cnt >= 5
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()

    return render_template("no_work_projects.html", results=results, pageTitle = "Researchers on many projects with no work")
