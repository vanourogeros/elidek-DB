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


@app.route("/programs/delete/<Name>", methods = ["POST"])
def deleteProgram(Name):
    conn = db.connection
    cur = conn.cursor()
    form2 = ProgramUpdate()
    query = f"""
    DELETE FROM program WHERE Name =  'Name'
    """
    try:
        cur.execute(query)
        conn.commit()
        conn.close()
        flash("Program deleted successfully", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect('/programs')


@app.route("/programs/create", methods = ["GET", "POST"])
def newProgram():
    cur = db.connection.cursor()   
    form = ProgramUpdate()  
    query = """
    SELECT DISTINCT ELIDEK_Sector, ELIDEK_Sector
    FROM program
    """
    cur.execute(query)
    form.sector.choices = [entry for entry in cur.fetchall()]
    cur.close()
    if(request.method == "POST"):
        name = str(request.form.get('name'))
        sector = str(request.form.get('sector'))
        sector2 = str(request.form.get('sector2'))
        if sector2 != '':
            sector = sector2
        query = f"""
        INSERT INTO program (Name, ELIDEK_Sector) VALUES ('{name}', '{sector}')
        """
        try:
            cur = db.connection.cursor() 
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Program created successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    
    return render_template("create_program.html", pageTitle = "Create Program", form = form)



@app.route("/projects", methods = ['GET', 'POST'])
def projects_view():
    form = ProjectFilterForm()
    form2 = ProjUpdate()
    cur = db.connection.cursor()   
    cur.execute("SELECT Executive_ID, CONCAT(Name, ' ', Surname) FROM Executive")
    form2.executive.choices = [entry for entry in cur.fetchall()]
    cur.execute("SELECT Organization_ID, Name FROM Organization")
    form2.organization.choices = [entry for entry in cur.fetchall()]


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
    return render_template("projects.html", projects=projects, pageTitle = "Projects Page", form = form, form2 = form2)

@app.route("/projects/update/<int:projID>", methods = ["POST"])
def updateProject(projID):
    print("awoogra!!!")
    form2 = ProjUpdate()
    cur = db.connection.cursor() 
    cur.execute("SELECT Executive_ID, CONCAT(Name, ' ', Surname) FROM Executive")
    form2.executive.choices = [entry for entry in cur.fetchall()]
    cur.execute("SELECT Organization_ID, Name FROM Organization")
    form2.organization.choices = [entry for entry in cur.fetchall()]

    name = str(request.form.get('name'))
    summary = str(request.form.get('summary'))
    funds = str(request.form.get('funds'))
    executive = str(request.form.get('executive'))
    start_date = str(request.form.get('start_date'))
    end_date = str(request.form.get('end_date'))
    organization = str(request.form.get('organization'))
    print(name,summary,funds,executive,start_date,end_date,organization)
    if(form2.validate_on_submit()):
        
        query = f"""
        UPDATE project SET Name = '{name}', Summary = '{summary}',
        Project_Funds = '{funds}', Start_Date = '{start_date}',
        End_Date = '{end_date}', Organization_ID = {organization},
        Executive_ID = {executive}
        WHERE Project_ID = {str(projID)}
        """
        print(query)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form2.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("projects_view"))  

@app.route("/projects/delete/<int:projID>", methods = ["POST"])
def deleteProject(projID):
    cur = db.connection.cursor() 
    
    query = f"""
    DELETE FROM project WHERE Project_ID = {projID}
    """
    try:
        cur.execute(query)
        db.connection.commit()
        db.connection.close()
        flash("Project deleted successfully", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect('/projects')


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
    cur.close()

    return render_template("fetch_project.html", proj_researchers=proj_researchers, pageTitle = f"Researchers working on Project with ID {projectID}")

@app.route("/executive", methods = ["GET", "POST"])
def executive_view():
    cur = db.connection.cursor()   
    form = ExecUpdate()

    query = """
    SELECT *
    FROM Executive
    """
        
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    executive = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()

    return render_template("executive.html", executive=executive, pageTitle = "Executives Page", form = form)

@app.route("/executive/update/<int:execID>", methods = ["POST"])
def updateExec(execID):
    print("awoogra!!!!")
    form = ExecUpdate()
    name = str(request.form.get('name'))
    surname = str(request.form.get('surname'))
    if(form.validate_on_submit()):
        query = f"""
        UPDATE executive SET Name = '{name}', Surname = '{surname}' WHERE Executive_ID = {str(execID)}
        """
        print(query)
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
    return redirect('/executive')

@app.route("/executive/create", methods = ["GET","POST"])
def insertExec():
    form = ExecUpdate()
    id = request.form.get('execID')
    name = str(request.form.get('name'))
    surname = str(request.form.get('surname'))
    exec_id = 0
    if(request.method == "POST" and form.validate_on_submit()):
        query1 =  """SELECT MAX(Executive_ID) FROM executive"""
        
        try:
            cur = db.connection.cursor()
            if (id == '0' or id == ''):

                cur.execute(query1)
                temp = cur.fetchall()
                exec_id = int(temp[0][0]+1)
            else:
                exec_id = id
            query2 = f"""
            INSERT INTO executive (Executive_ID, Name, Surname) VALUES ('{exec_id}', '{name}', '{surname}')
            """
            cur.execute(query2)
            db.connection.commit()
            cur.close()
            flash("Executive created successfully", "success")

        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_executive.html", pageTitle = "Create Executive", form = form)


@app.route('/executive/delete/<int:execID>', methods = ["POST"])
def deleteexec(execID):
    conn = db.connection
    cur = conn.cursor()
    query = f"""
        DELETE FROM executive WHERE Executive_ID =  {execID}
        """
    try:
        cur.execute(query)
        conn.commit()
        conn.close()
        flash("Executive deleted successfully", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect('/executive')

@app.route("/projects-per-researcher", methods = ["GET", "POST"])
def projects_per_researcher_view():
    create_form = WorksOnAdd()
    delete_form = WorksOnDelete()

    create_eval_form = EvalAdd()
    delete_eval_form = EvalDelete()

    cur = db.connection.cursor() 
    query = """
    SELECT P.Researcher_ID, P.Full_Name, P.Project_ID, P.Project_Name, E.Researcher_ID AS Evaluator_ID
    FROM projects_per_researcher P INNER JOIN Evaluation E
    on P.Project_ID = E.Project_ID;
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]

   
    # Set researcher fields 
    query = """
    SELECT DISTINCT Researcher_ID, CONCAT(Researcher_ID, ', ', Full_Name)
    FROM projects_per_researcher
    """
    cur.execute(query)
    create_form.researcher.choices = [entry for entry in cur.fetchall()]
    cur.execute(query)
    delete_form.researcher_d.choices = [entry for entry in cur.fetchall()]

    # Set project fields 
    query = """
    SELECT DISTINCT Project_ID, CONCAT(Project_ID, ', ', Project_Name)
    FROM projects_per_researcher
    ORDER BY Project_ID
    """
    cur.execute(query)
    create_form.project.choices = [entry for entry in cur.fetchall()]
    cur.execute(query)
    delete_form.project_d.choices = [entry for entry in cur.fetchall()]
    
    # Select researcher - evaluator
    query = """
    SELECT DISTINCT Researcher_ID, CONCAT(Researcher_ID, ', ', Full_Name)
    FROM projects_per_researcher
    """
    cur.execute(query)
    create_eval_form.researcher.choices = [entry for entry in cur.fetchall()]
    cur.execute(query)
    delete_eval_form.researcher_d.choices = [entry for entry in cur.fetchall()]

    # Select project to be evaluated
    query = """
    SELECT DISTINCT Project_ID, CONCAT(Project_ID, ', ', Project_Name)
    FROM projects_per_researcher
    ORDER BY Project_ID
    """
    cur.execute(query)
    create_eval_form.project.choices = [entry for entry in cur.fetchall()]
    cur.execute(query)
    delete_eval_form.project_d.choices = [entry for entry in cur.fetchall()]

    

    #works on insert
    if(request.method == "POST" and create_form.validate_on_submit() and request.form.get('researcher') != 'None'):
        try:
            researcher = request.form.get('researcher')
            project = request.form.get('project')
            start_date = request.form.get('start_date')
            query = f"""
                    INSERT INTO Works_On (Researcher_ID, Project_ID, Start_Date) 
                    VALUES ({researcher},{project},'{start_date}')
                """
            print(query)
            cur.execute(query)
            db.connection.commit()
            flash("Researcher added project successfully", "success")
            return render_template("projects_per_researcher.html", results=results, pageTitle = "Projects per Researcher Page",
     create_form = create_form, delete_form = delete_form)
        except Exception as e:
            print("not a creation")
            if '1054' not in str(e):
                flash(str(e), "danger")
    #works on delete
    if(request.method == "POST" and delete_form.validate_on_submit() and request.form.get('researcher_d') != 'None'):
        try:
            researcher = request.form.get('researcher_d')
            project = request.form.get('project_d')
            query = f"""
                    DELETE FROM Works_On
                    WHERE Researcher_ID = {researcher} AND Project_ID = {project}
                """
            print(query)
            cur.execute(query)
            db.connection.commit()
            flash("Researcher removed from project successfully", "success")
            return render_template("projects_per_researcher.html", results=results, pageTitle = "Projects per Researcher Page",
     create_form = create_form, delete_form = delete_form)
        except Exception as e:
            print("not a deletion")
            if '1054' not in str(e):
                flash(str(e), "danger")

    #evals insert           
    if(request.method == "POST" and create_eval_form.validate_on_submit() and request.form.get('researcher') != 'None'):
        try:
            researcher = request.form.get('researcher')
            project = request.form.get('project')
            eval_date = request.form.get('eval_date')
            eval_grade = request.form.get('eval_grade')
            query = f"""
                    INSERT INTO Evaluation (Researcher_ID, Project_ID, Evaluation_Date, Evaluation_Grade) 
                    VALUES ({researcher},{project},'{eval_date}',{eval_grade})
                """
            print(query)
            cur.execute(query)
            db.connection.commit()
            flash("Researcher-Evaluator added to project successfully", "success")
            return render_template("projects_per_researcher.html", results=results, pageTitle = "Projects per Researcher Page",
     create_eval_form = create_eval_form, delete_eval_form = delete_eval_form)
        except Exception as e:
            print("not a creation")
            if '1054' not in str(e):
                flash(str(e), "danger")

    #evals delete
    if(request.method == "POST" and delete_eval_form.validate_on_submit() and request.form.get('researcher_d') != 'None'):
        try:
            researcher = request.form.get('researcher_d')
            project = request.form.get('project_d')
            query = f"""
                    DELETE FROM Evaluation
                    WHERE Researcher_ID = {researcher} AND Project_ID = {project}
                """
            print(query)
            cur.execute(query)
            db.connection.commit()
            flash("Evaluator removed from project successfully", "success")
            return render_template("projects_per_researcher.html", results=results,  pageTitle = "Projects per Researcher Page",
     create_eval_form = create_eval_form, delete_eval_form = delete_eval_form)
        except Exception as e:
            print("not a deletion")
            if '1054' not in str(e):
                flash(str(e), "danger")



    cur.close()
    return render_template("projects_per_researcher.html", results=results,   pageTitle = "Projects per Researcher Page",
     create_form = create_form, delete_form = delete_form, create_eval_form = create_eval_form, delete_eval_form = delete_eval_form)




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

