from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from elidekdb import app, db  # initially created by __init__.py, need to be used here
from elidekdb.forms import *


@app.route("/")
def index():
    return render_template("landing.html", pageTitle="Landing Page")


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
    update_form = ProgramUpdate()
    cur.close()
    # print(programs[1])

    return render_template("programs.html", programs=programs,
                           pageTitle="Programs Page", update_form=update_form)


@app.route("/programs/update/<int:program_ID>", methods=["POST"])
def updateProgram(program_ID):
    update_form = ProgramUpdate()
    cur = db.connection.cursor()

    if (update_form.validate_on_submit()):
        try:
            name = str(request.form.get('name'))
            sector = str(request.form.get('sector'))
            query = f"""
            UPDATE program SET Name = '{name}', ELIDEK_Sector = '{sector}'
            WHERE Program_ID = {program_ID}
            """
            cur.execute(query)
            db.connection.commit()
            flash("Program succesfully updated", "success")
        except Exception as e:
            flash(str(e), "danger")

    return redirect('/programs')


@app.route("/programs/delete/<int:program_ID>", methods=["POST"])
def deleteProgram(program_ID):
    conn = db.connection
    cur = conn.cursor()
    form2 = ProgramUpdate()
    query = f"""
    DELETE FROM program WHERE Program_ID =  {program_ID}
    """
    try:
        cur.execute(query)
        conn.commit()
        conn.close()
        flash("Program deleted successfully", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect('/programs')


@app.route("/programs/create", methods=["GET", "POST"])
def newProgram():
    cur = db.connection.cursor()
    form = ProgramCreate()
    query = """
    SELECT DISTINCT ELIDEK_Sector, ELIDEK_Sector
    FROM program
    """
    cur.execute(query)
    form.sector.choices = [entry for entry in cur.fetchall()]
    if(request.method == "POST"):
        name = str(request.form.get('name'))
        sector = str(request.form.get('sector'))
        sector2 = str(request.form.get('sector2'))
        cur.execute("SELECT MAX(Program_ID) FROM PROGRAM")
        id = str(cur.fetchall()[0][0]+1)
        if sector2 != '':
            sector = sector2
        query = f"""
        INSERT INTO program (Program_ID, Name, ELIDEK_Sector) VALUES ({id}, '{name}', '{sector}')
        """
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Program created successfully", "success")
        except Exception as e:
            flash(str(e), "danger")

    return render_template("create_program.html", pageTitle="Create Program", form=form)


@app.route("/projects", methods=['GET', 'POST'])
def projects_view():
    form = ProjectFilterForm()
    form2 = ProjUpdate()
    cur = db.connection.cursor()
    cur.execute("SELECT Executive_ID, CONCAT(Name, ' ', Surname) FROM Executive")
    form2.executive.choices = [entry for entry in cur.fetchall()]
    cur.execute("SELECT Organization_ID, Name FROM Organization")
    form2.organization.choices = [entry for entry in cur.fetchall()]

    query = f"""
    SELECT  DISTINCT Program_ID, CONCAT(Program_ID, ', ',Name)
    FROM program
    """
    cur.execute(query)
    form2.associated_program.choices = [entry for entry in cur.fetchall()]

    query = f"""
    SELECT Researcher_ID, CONCAT(Researcher_ID, ', ', Name, ' ', Surname, ', org: ', Organization_ID)  
    FROM Researcher
    ORDER BY Organization_ID, Researcher_ID
    """
    cur.execute(query)
    form2.research_manager.choices = [entry for entry in cur.fetchall()]

    query = """
    SELECT Project_ID, P.Name AS P_Name, Summary, Project_Funds, Start_Date, End_Date, CONCAT(E.Name, ' ',  E.Surname) AS E_Name, Organization_ID, P.Program_ID AS P_Program, P.Research_Manager_ID AS P_remanager 
    FROM Project P INNER JOIN Executive E 
    ON P.Executive_ID = E.Executive_ID
    """

    if(request.method == "POST" and form.submit_filter.data and form.validate_on_submit()):
        min_Start_Date = str(request.form.get('min_Start_Date'))
        max_Start_Date = str(request.form.get('max_Start_Date'))
        min_End_Date = str(request.form.get('min_End_Date'))
        max_End_Date = str(request.form.get('max_End_Date'))
        min_Duration = str(request.form.get('min_Duration'))
        max_Duration = str(request.form.get('max_Duration'))
        executive = str(request.form.get('executive_f'))
        flag = False

        print("form!")
        print(max_Start_Date)
        where_or_and = 'WHERE'
        if min_Start_Date != '' and min_Start_Date != 'None':
            flag = True
            query += f'WHERE DATEDIFF(Start_Date, \'{min_Start_Date}\') > 0'
            where_or_and = '\n    AND'
        if max_Start_Date != '' and max_Start_Date != 'None':
            flag = True
            query += f'{where_or_and} DATEDIFF(Start_Date, \'{max_Start_Date}\') < 0'
            where_or_and = '\n    AND'
        if min_End_Date != '' and min_End_Date != 'None':
            flag = True
            query += f'{where_or_and} DATEDIFF(End_Date, \'{min_End_Date}\') > 0'
            where_or_and = '\n    AND'
        if max_End_Date != '' and max_End_Date != 'None':
            flag = True
            query += f'{where_or_and} DATEDIFF(End_Date, \'{max_End_Date}\') < 0'
            where_or_and = '\n    AND'
        if min_Duration != '' and min_Duration != 'None':
            flag = True
            query += f'{where_or_and} DATEDIFF(End_Date, Start_Date) > {min_Duration}'
            where_or_and = '\n    AND'
        if max_Duration != '' and max_Duration != 'None':
            flag = True
            query += f'{where_or_and} DATEDIFF(End_Date, Start_Date) < {max_Duration}'
            where_or_and = '\n    AND'
        if executive != '' and executive != 'None':
            flag = True
            query += f'{where_or_and} CONCAT(E.Name, \' \',  E.Surname) = \'{executive}\''
            where_or_and = '\n    AND'

    query += '\n    ORDER BY Project_ID'
    print(query)

    print(query)
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    projects = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    # print(projects)
    #programs = cur.fetchall()
    cur.close()
    return render_template("projects.html", projects=projects, pageTitle="Projects Page", form=form, form2=form2)


@app.route("/projects/update/<int:projID>", methods=["POST"])
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
    associated_program = str(request.form.get('associated_program'))
    research_manager = str(request.form.get('research_manager'))
    # print(name,summary,funds,executive,start_date,end_date,organization,associated_program,research_manager)
    query = f"""
    SELECT  DISTINCT Program_ID, CONCAT(Program_ID, ', ',Name)
    FROM program
    """
    cur.execute(query)
    form2.associated_program.choices = [entry for entry in cur.fetchall()]

    query = f"""
    SELECT Researcher_ID, CONCAT(Researcher_ID, ', ', Name, ' ', Surname, ', org: ', Organization_ID)  
    FROM Researcher
    ORDER BY Organization_ID, Researcher_ID
    """
    cur.execute(query)
    form2.research_manager.choices = [entry for entry in cur.fetchall()]
    if(form2.validate_on_submit()):

        query = f"""
        UPDATE project SET Name = '{name}', Summary = '{summary}',
        Project_Funds = '{funds}', Start_Date = '{start_date}',
        End_Date = '{end_date}', Organization_ID = {organization},
        Executive_ID = {executive}, Program_ID = {associated_program}, Research_Manager_ID = {research_manager}
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


@app.route("/projects/delete/<int:projID>", methods=["POST"])
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


@app.route("/projects/create", methods=["GET", "POST"])
def createProject():
    form = ProjectCreate()
    cur = db.connection.cursor()
    cur.execute("SELECT Executive_ID, CONCAT(Name, ' ', Surname) FROM Executive")
    form.executive.choices = [entry for entry in cur.fetchall()]

    query = f"""
    SELECT  DISTINCT Program_ID,Name
    FROM program
    """
    cur.execute(query)

    form.associated_program.choices = [entry for entry in cur.fetchall()]
    cur.execute(
        "SELECT Organization_ID, CONCAT(Organization_ID, ', ', Name) FROM Organization")
    form.organization.choices = [entry for entry in cur.fetchall()]

    query = f"""
    SELECT Researcher_ID, CONCAT(Researcher_ID, ', ', Name, ' ', Surname, ', org: ', Organization_ID)  
    FROM Researcher
    ORDER BY Organization_ID, Researcher_ID
    """
    cur.execute(query)
    form.research_manager.choices = [entry for entry in cur.fetchall()]

    projID = str(request.form.get('projID'))
    name = str(request.form.get('name'))
    summary = str(request.form.get('summary'))
    funds = str(request.form.get('funds'))
    executive = str(request.form.get('executive'))
    start_date = str(request.form.get('start_date'))
    end_date = str(request.form.get('end_date'))
    organization = str(request.form.get('organization'))
    associated_program = str(request.form.get('associated_program'))
    research_manager = str(request.form.get('research_manager'))

    print(projID, name, summary, funds, executive, start_date,
          end_date, organization, associated_program, research_manager)

    if(request.method == "POST" and form.validate_on_submit()):
        query1 = """SELECT MAX(Project_ID) FROM project"""

        try:
            cur = db.connection.cursor()
            if (id == '0' or id == ''):

                cur.execute(query1)
                temp = cur.fetchall()
                exec_id = int(temp[0][0]+1)
            else:
                exec_id = id
            query2 = f"""
            INSERT INTO project (Project_ID, Name, Summary, Project_Funds, Start_Date, End_Date, Executive_ID, Program_ID, Organization_ID,  Research_Manager_ID) 
            VALUES ('{projID}', '{name}', '{summary}','{funds}', '{start_date}', '{end_date}','{executive}', '{associated_program}', '{organization}','{research_manager}')
            """
            cur.execute(query2)
            db.connection.commit()
            cur.close()
            flash("Project created successfully", "success")

        except Exception as e:  # OperationalError
            flash(str(e), "danger")

    # else, response for GET request
    return render_template("create_project.html", pageTitle="Create Project", form=form)


@app.route("/projects/<int:projectID>", methods=["GET", "POST"])
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
    proj_researchers = [dict(zip(column_names, entry))
                        for entry in cur.fetchall()]

    query = f"""
    SELECT *
    FROM Work_To_Be_Submitted
    WHERE Project_ID = {projectID}
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    works = [dict(zip(column_names, entry)) for entry in cur.fetchall()]

    work_form = AddDeleteWork()
    if (request.method == "POST" and work_form.validate_on_submit()):
        try:
            title = str(request.form.get("title"))
            summary = str(request.form.get("summary"))
            submission_date = str(request.form.get("submission_date"))
            add_or_delete = str(request.form.get("add_or_delete"))
            query = f"""
            INSERT INTO Work_To_Be_Submitted (Title, Project_ID, Summary, Submission_Date)
            VALUES ("{title}", {projectID}, "{summary}", "{submission_date}")
            """ if add_or_delete == 'Add Selected Work' else f"""
            DELETE FROM Work_To_Be_Submitted Where Project_ID = {projectID} AND Title = "{title}"
            """
            print(query)
            cur.execute(query)
            flash("Request completed successfully", "success")
            db.connection.commit()
        except Exception as e:
            flash(str(e), "danger")
    cur.close()

    return render_template("fetch_project.html", proj_researchers=proj_researchers, works=works,
                           pageTitle=f"Researchers working on Project with ID {projectID}", ID=f"{projectID}", work_form=work_form)


@app.route("/executive", methods=["GET", "POST"])
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

    return render_template("executive.html", executive=executive, pageTitle="Executives Page", form=form)


@app.route("/executive/update/<int:execID>", methods=["POST"])
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


@app.route("/executive/create", methods=["GET", "POST"])
def insertExec():
    form = ExecUpdate()
    id = request.form.get('execID')
    name = str(request.form.get('name'))
    surname = str(request.form.get('surname'))
    exec_id = 0
    if(request.method == "POST" and form.validate_on_submit()):
        query1 = """SELECT MAX(Executive_ID) FROM executive"""

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

        except Exception as e:  # OperationalError
            flash(str(e), "danger")

    # else, response for GET request
    return render_template("create_executive.html", pageTitle="Create Executive", form=form)


@app.route('/executive/delete/<int:execID>', methods=["POST"])
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


@app.route("/projects-per-researcher", methods=["GET", "POST"])
def projects_per_researcher_view():
    create_form = WorksOnAdd()
    delete_form = WorksOnDelete()

    create_eval_form = EvalAdd()
    delete_eval_form = EvalDelete()

    cur = db.connection.cursor()
    query = """
    SELECT DISTINCT P.Researcher_ID, P.Full_Name, P.Org_ID, P.Project_ID, P.Project_Name, E.Researcher_ID AS Evaluator_ID
    FROM projects_per_researcher P INNER JOIN Evaluation E
    on P.Project_ID = E.Project_ID
    UNION
    SELECT Researcher_ID, Full_Name, Org_ID, Project_ID, Project_Name, NULL
    FROM projects_per_researcher
    WHERE Project_ID NOT IN (SELECT Project_ID FROM Evaluation)
    ORDER BY Researcher_ID
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]

    # Set researcher fields
    query = """
    SELECT DISTINCT Researcher_ID, CONCAT(Researcher_ID, ', ', Full_Name, ' Org. ID: ', Org_ID)
    FROM projects_per_researcher
    """
    cur.execute(query)
    create_form.researcher.choices = [entry for entry in cur.fetchall()]
    cur.execute(query)
    delete_form.researcher_d.choices = [entry for entry in cur.fetchall()]

    # Set project fields
    query = """
    SELECT DISTINCT Project_ID, CONCAT(Project_ID, ', ', Project_Name, '- Org. ID: ', Org_ID)
    FROM projects_per_researcher
    ORDER BY Project_ID
    """
    cur.execute(query)
    create_form.project.choices = [entry for entry in cur.fetchall()]
    cur.execute(query)
    delete_form.project_d.choices = [entry for entry in cur.fetchall()]

    # Select researcher - evaluator
    query = """
    SELECT DISTINCT Researcher_ID, CONCAT(Researcher_ID, ', ', Full_Name, '- Org. ID: ', Org_ID)
    FROM projects_per_researcher
    """
    cur.execute(query)
    create_eval_form.researcher.choices = [entry for entry in cur.fetchall()]
    cur.execute(query)
    delete_eval_form.researcher_d.choices = [entry for entry in cur.fetchall()]

    # Select project to be evaluated
    query = """
    SELECT DISTINCT Project_ID, CONCAT(Project_ID, ', ', Project_Name, '- Org. ID: ', Org_ID)
    FROM projects_per_researcher
    ORDER BY Project_ID
    """
    query2 = """
    SELECT DISTINCT Project_ID, CONCAT(Project_ID, ', ', Project_Name, '- Org. ID: ', Org_ID)
    FROM projects_per_researcher
    WHERE Project_ID NOT IN (SELECT Project_ID FROM Evaluation)
    ORDER BY Project_ID
    """
    cur.execute(query2)
    create_eval_form.project.choices = [entry for entry in cur.fetchall()]
    cur.execute(query)
    delete_eval_form.project_d.choices = [entry for entry in cur.fetchall()]

    # works on insert
    if(request.method == "POST" and create_form.validate_on_submit() and request.form.get('checkbox') == 'Yes'):
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
            return render_template("projects_per_researcher.html", results=results, pageTitle="Projects per Researcher Page",
                                   create_form=create_form, delete_form=delete_form)
        except Exception as e:
            print("not a creation")
            if '1054' not in str(e) and "'create_form' is undefined" not in str(e):
                flash(str(e), "danger")
    # works on delete
    if(request.method == "POST" and delete_form.validate_on_submit() and request.form.get('checkbox_d') == 'Yes'):
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
            return render_template("projects_per_researcher.html", results=results, pageTitle="Projects per Researcher Page",
                                   create_form=create_form, delete_form=delete_form)
        except Exception as e:
            print("not a deletion")
            if '1054' not in str(e) and "'create_form' is undefined" not in str(e):
                flash(str(e), "danger")

    # evals insert
    if(request.method == "POST" and create_eval_form.validate_on_submit() and request.form.get('checkbox_ea') == 'Yes'):
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
            return render_template("projects_per_researcher.html", results=results, pageTitle="Projects per Researcher Page",
                                   create_eval_form=create_eval_form, delete_eval_form=delete_eval_form)
        except Exception as e:
            print("not a creation")
            if '1054' not in str(e) and "'create_form' is undefined" not in str(e):
                flash(str(e), "danger")

    # evals delete
    if(request.method == "POST" and delete_eval_form.validate_on_submit() and request.form.get('checkbox_ed') == 'Yes'):
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
            return render_template("projects_per_researcher.html", results=results,  pageTitle="Projects per Researcher Page",
                                   create_eval_form=create_eval_form, delete_eval_form=delete_eval_form)
        except Exception as e:
            print("not a deletion")
            if '1054' not in str(e) and "'create_form' is undefined" not in str(e):
                flash(str(e), "danger")

    cur.close()
    return render_template("projects_per_researcher.html", results=results,   pageTitle="Projects per Researcher Page",
                           create_form=create_form, delete_form=delete_form, create_eval_form=create_eval_form, delete_eval_form=delete_eval_form)


@app.route("/projects-per-field", methods=["GET", "POST"])
def projects_per_field_view():
    cur = db.connection.cursor()
    add_form = AddProjectField()
    remove_form = RemoveProjectField()
    create_form = newField()
    delete_form = deleteField()
    edit_form = editField()
    #  create query results
    query = """
    SELECT *
    FROM projects_per_field
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]

    # Set project fields
    query = """
    SELECT DISTINCT Project_ID, CONCAT(Project_ID, ', ', Project_Name)
    FROM projects_per_field
    ORDER BY Project_ID
    """
    cur.execute(query)
    add_form.project.choices = [entry for entry in cur.fetchall()]
    cur.execute(query)
    remove_form.project_d.choices = [entry for entry in cur.fetchall()]

    # Set field fields (haha)
    query = """
    SELECT DISTINCT Field_ID, CONCAT(Field_ID, ', ', Name)
    FROM Research_Field
    ORDER BY Field_ID
    """
    cur.execute(query)
    add_form.field.choices = [entry for entry in cur.fetchall()]
    cur.execute(query)
    remove_form.field_d.choices = [entry for entry in cur.fetchall()]
    cur.execute(query)
    delete_form.field.choices = [entry for entry in cur.fetchall()]
    cur.execute(query)
    edit_form.field.choices = [entry for entry in cur.fetchall()]

    if(request.method == "POST" and add_form.validate_on_submit() and request.form.get('checkbox') == 'Yes'):
        try:
            field = request.form.get('field')
            project = request.form.get('project')
            query = f"""
                    INSERT INTO Refers_To (Field_ID, Project_ID) 
                    VALUES ({field},{project})
                """
            print(query)
            cur.execute(query)
            db.connection.commit()
            flash("Field added to project successfully", "success")
        except Exception as e:
            flash(str(e), "danger")

    if(request.method == "POST" and remove_form.validate_on_submit() and request.form.get('checkbox_d') == 'Yes'):
        try:
            field = request.form.get('field_d')
            project = request.form.get('project_d')
            query = f"""
                    DELETE FROM Refers_To 
                    WHERE Field_ID = {field} AND Project_ID = {project}
                """
            print(query)
            cur.execute(query)
            db.connection.commit()
            flash("Field removed from project successfully", "success")
        except Exception as e:
            flash(str(e), "danger")

    if(request.method == "POST" and create_form.validate_on_submit() and request.form.get('checkbox_cf') == 'Yes'):
        try:
            cur.execute("SELECT 1+MAX(Field_ID) FROM Research_Field")
            field_id = cur.fetchone()[0]
            field_name = request.form.get('field_name')
            query = f"""
                    INSERT INTO Research_Field (Field_ID, Name) 
                    Values({field_id},'{field_name}')
                """
            print(query)
            cur.execute(query)
            db.connection.commit()
            flash("Field created successfully", "success")
        except Exception as e:
            flash(str(e), "danger")

    if(request.method == "POST" and delete_form.validate_on_submit() and request.form.get('checkbox_df') == 'Yes'):
        try:
            field_id = request.form.get('field')
            query = f"""
                    DELETE FROM Research_Field
                    WHERE Field_ID = {field_id}
                """
            print(query)
            cur.execute(query)
            db.connection.commit()
            flash("Field deleted successfully", "success")
        except Exception as e:
            flash(str(e), "danger")

    if(request.method == "POST" and edit_form.validate_on_submit() and request.form.get('checkbox_ef') == 'Yes'):
        try:
            field_id = request.form.get('field')
            field_name = request.form.get('field_name')
            query = f"""
                    UPDATE Research_Field
                    SET Name = '{field_name}'
                    WHERE Field_ID = {field_id}
                """
            print(query)
            cur.execute(query)
            db.connection.commit()
            flash("Field edited successfully", "success")
        except Exception as e:
            flash(str(e), "danger")

    cur.close()

    return render_template("projects_per_field.html", results=results, pageTitle="Projects per Research Field",
                           add_form=add_form, remove_form=remove_form, create_form=create_form, delete_form=delete_form, edit_form=edit_form)


@app.route("/specific-research-field", methods=['GET', 'POST'])
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

    return render_template("specific_field.html", results=results, results2=results2, form=form, pageTitle="Projects for chosen Research Field")


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
                having Projects_This_Year = Projects_Last_Year AND Projects_This_Year >= 10
                order by O
            ) X INNER JOIN Organization ON Organization.Organization_ID = X.O
            """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()

    return render_template("consecutive_years.html", results=results, pageTitle="Organizations with same number of projects -more than 10- in two concecutive years")


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

    return render_template("top_three_field_pairs.html", results=results, pageTitle="Top three field pairs")


@app.route("/most-prolific-researchers")
def prolific_researchers():

    cur = db.connection.cursor()
    cur.execute("DROP VIEW IF EXISTS project_count")
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
            ORDER BY project_cnt DESC LIMIT 10;
            """
    cur.execute(query)

    query = """
            select DISTINCT * FROM
            project_count
            """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()

    return render_template("prolific_researchers.html", results=results, pageTitle="Prolific Researchers")


@app.route("/executive-money-bags")
def top_executives_view():

    cur = db.connection.cursor()
    cur.execute("DROP VIEW IF EXISTS company_funders")
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

    return render_template("top_executives.html", results=results, pageTitle="Executives giving most money to a company")


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

    return render_template("no_work_projects.html", results=results, pageTitle="Researchers on many projects with no work")


@app.route("/organizations")
def orgs_view():
    cur = db.connection.cursor()
    form = Org()
    query = """
    SELECT Organization_ID, Acronym, Name, Street, Street_Number,
    City, Postal_Code, Organization.Org_Type, Ministry_Budget AS budget1, NULL AS budget2
    FROM organization INNER JOIN University ON Organization_ID=University_ID
    UNION
    SELECT Organization_ID, Acronym, Name, Street, Street_Number,
    City, Postal_Code, Organization.Org_Type, Ministry_Budget AS budget1, Actions_Budget AS budget2
    FROM organization INNER JOIN Research_Center ON Organization_ID=Research_Center_ID
    UNION
    SELECT Organization_ID, Acronym, Name, Street, Street_Number,
    City, Postal_Code, Organization.Org_Type, Equity AS budget1, NULL AS budget2
    FROM organization INNER JOIN Company ON Organization_ID=Company_ID
    ORDER BY Organization_ID
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    organizations = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()

    return render_template("organizations.html", organizations=organizations, pageTitle="organizations Page", form=form)


@app.route("/organizations/delete/<int:orgID>", methods=["POST"])
def delete_orgs(orgID):
    cur = db.connection.cursor()
    query = f"""
        DELETE FROM organization WHERE Organization_ID =  {orgID}
        """
    try:
        cur.execute(query)
        db.connection.commit()
        db.connection.close()
        flash("Organization deleted successfully", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect('/organizations')


@app.route("/organizations/update/<int:orgID>", methods=["POST"])
def update_orgs(orgID):
    cur = db.connection.cursor()
    form = Org()
    name = str(request.form.get('name'))
    acr = str(request.form.get('acr'))
    street = str(request.form.get('street'))
    number = request.form.get('number')
    city = str(request.form.get('city'))
    pos = request.form.get('pos')
    budget1 = request.form.get('budget1')
    budget2 = request.form.get('budget2')
    
    #cur.execute("SELECT DISTINCT Org_type, Org_type FROM organization")
    #form.type.choices = [entry for entry in cur.fetchall()] 
    form.type.choices = [u'Research Center',u'University',u'Company']
    type = request.form.get('type')

    if(form.validate_on_submit()):
        query = f"""
        UPDATE organization SET Acronym = '{acr}', Name = '{name}',
        Street = '{street}', Street_Number = {number}, City = '{city}',
        Postal_Code = {pos}  WHERE Organization_ID =  {orgID}
        """
        print(query)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()         
            if type == "University":
                query = f"""
                UPDATE University SET Ministry_Budget={budget1}
                WHERE University_ID='{orgID}'
                """
                cur.execute(query)
                db.connection.commit()
            elif type == "Company":
                query = f"""
                UPDATE Company SET Equity={budget1}
                WHERE Company_ID='{orgID}'
                """
                cur.execute(query)
                db.connection.commit()
            elif type == "Research Center":
                query = f"""
                UPDATE Research_Center SET Ministry_Budget={budget1}, Actions_Budget={budget2}
                WHERE Research_Center_ID='{orgID}'
                """
                cur.execute(query)
                db.connection.commit() 
                cur.close()   
            flash("Organization updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect('/organizations')

@app.route("/organizations/create", methods = ["GET","POST"])
def createOrg():
    cur = db.connection.cursor() 
    form = Org()

    #cur.execute("SELECT DISTINCT Org_type, Org_type FROM organization")
    #form.type.choices = [entry for entry in cur.fetchall()] 
    form.type.choices = [u'Research Center',u'University',u'Company']

    orgID = request.form.get('orgID')
    name = str(request.form.get('name'))
    acr = str(request.form.get('acr'))
    street = str(request.form.get('street'))
    number = request.form.get('number')
    city = str(request.form.get('city'))
    pos = request.form.get('pos')
    type = str(request.form.get('type'))
    budget1 = request.form.get('budget1')
    budget2 = request.form.get('budget2')
    res_id = 0

    if(request.method == "POST"):
        
        
        try:
            query1 =  """SELECT MAX(Organization_ID) FROM organization"""
            cur = db.connection.cursor()
            if (orgID == '0' or orgID == ''):

                cur.execute(query1)
                temp = cur.fetchall()
                res_id = int(temp[0][0] + 1)
            else:
                res_id = orgID
            query2 = f"""
            INSERT INTO organization (Organization_ID, Acronym, Name, Street, Street_Number, City, Postal_Code, Org_type)
            VALUES ('{res_id}', '{acr}','{name}', '{street}', '{number}', '{city}', '{pos}', '{type}')
            """
            cur.execute(query2)
            if (type == 'Research Center') :
                query = f""" INSERT INTO research_center (Research_Center_ID, Org_Type, Ministry_Budget,Actions_Budget)
                VALUES ('{res_id}','{type}','{budget1}','{budget2}')
                """
            elif (type == 'University') :
                query = f""" INSERT INTO university (University_ID, Org_Type, Ministry_Budget)
                VALUES ('{res_id}','{type}','{budget1}')
                """
            else :
                query = f""" INSERT INTO company (Company_ID, Org_Type, Equity)
                VALUES ('{res_id}','{type}','{budget1}')
                """
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Organization created successfully", "success")
            redirect("/organizations")

        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_organization.html", pageTitle = "Create Organization", form = form)  

@app.route("/organizations/phones/<int:orgID>", methods = ["GET", "POST"])
def org_phones(orgID):
    cur = db.connection.cursor()
    form = orgPhone()
    query = f"""
    SELECT Phone_Number FROM Org_Phone WHERE Organization_ID={orgID}
    ORDER BY Phone_Number
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    
    if(form.validate_on_submit() and request.method == "POST"):
        try:
            phone_number = request.form.get("phone_number")
            query = f"""
            INSERT INTO org_phone (Organization_ID, Phone_Number)
            VALUES ('{orgID}', '{phone_number}')
            """
            print(query)
            cur.execute(query)
            db.connection.commit()
            flash("Phone successfully added!", "success")
            redirect('/organizations/phones/orgID')
        except Exception as e:
            flash(str(e), "danger")

    return render_template("organization_phones.html", pageTitle = f"Phones for Organization with ID {orgID}",
     results=results, form = form, orgID=orgID)  

@app.route("/organizations/phones/<int:orgID>/delete/<int:phone_number>", methods = ["GET", "POST"])
def delete_org_phone(orgID, phone_number):
    cur = db.connection.cursor()
    query = f"""
    DELETE FROM org_phone
    WHERE organization_ID = {orgID} 
    AND phone_number = {phone_number}
    """
    cur.execute(query)
    db.connection.commit()
    flash("Phone successfully deleted!", "success")
    return redirect(f'/organizations/phones/{orgID}')

@app.route("/researchers", methods = ["GET", "POST"])
def researchers_view():
    cur = db.connection.cursor()
    form = updateRes()
    query = """
    SELECT *
    FROM researcher
    """
    cur.execute(query)
    column_names = [i[0] for i in cur.description]
    researchers = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()

    cur = db.connection.cursor()
    #cur.execute("SELECT DISTINCT Gender,Gender FROM Researcher")
    #form.gender.choices = [entry for entry in cur.fetchall()]
    form.gender.choices = [u'Male',u'Female',u'Other']
    cur.execute("SELECT Organization_ID, Name FROM Organization")
    form.orgID.choices = [entry for entry in cur.fetchall()]
    cur.close()
    return render_template("researchers.html", researchers=researchers, pageTitle="Researchers Page", form=form)


@app.route("/researchers/update/<int:Researcher_ID>", methods=["POST"])
def updateResearcher(Researcher_ID):

    cur = db.connection.cursor()
    form = updateRes()
    #cur.execute("SELECT DISTINCT Gender,Gender FROM Researcher")
    #form.gender.choices = [entry for entry in cur.fetchall()]
    form.gender.choices = [u'Male',u'Female',u'Other']
    cur.execute("SELECT Organization_ID, Name FROM Organization")
    form.orgID.choices = [entry for entry in cur.fetchall()]

    name = str(request.form.get('name'))
    surname = str(request.form.get('surname'))
    gender = str(request.form.get('gender'))
    birth_date = str(request.form.get('birth_date'))
    r_date = str(request.form.get('r_date'))
    orgID = str(request.form.get('orgID'))

    if (request.method == "POST" and form.validate_on_submit()):
        try:
            query = f"""
            UPDATE Researcher SET Name = '{name}', Surname = '{surname}', Gender = '{gender}', Birth_Date = '{birth_date}', Recruitment_Date = '{r_date}', Organization_ID = {orgID}
            WHERE Researcher_ID = {Researcher_ID}
            """

            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Researcher succesfully updated", "success")
        except Exception as e:
            flash(str(e), "danger")

    return redirect('/researchers')


@app.route("/researchers/create", methods=["GET", "POST"])
def createResearcher():
    cur = db.connection.cursor()
    form = createRes()

    cur.execute("SELECT DISTINCT Gender,Gender FROM Researcher")
    form.gender.choices = [entry for entry in cur.fetchall()]
    cur.execute("SELECT Organization_ID, Name FROM Organization")
    form.orgID.choices = [entry for entry in cur.fetchall()]

    id = request.form.get('resID')
    name = str(request.form.get('name'))
    surname = str(request.form.get('surname'))
    gender = str(request.form.get('gender'))
    birth_date = str(request.form.get('birth_date'))
    r_date = str(request.form.get('r_date'))
    orgID = str(request.form.get('orgID'))
    res_id = 0

    if(request.method == "POST" and form.validate_on_submit()):
        query1 = """SELECT MAX(Researcher_ID) FROM Researcher"""

        try:
            cur = db.connection.cursor()
            if (id == '0' or id == ''):

                cur.execute(query1)
                temp = cur.fetchall()
                res_id = int(temp[0][0]+1)
            else:
                res_id = id
            query2 = f"""
            INSERT INTO Researcher (Researcher_ID, Name, Surname, Gender, Birth_Date, Recruitment_Date, Organization_ID) VALUES ('{res_id}', '{name}', '{surname}', '{gender}', '{birth_date}', '{r_date}', '{orgID}')
            """
            cur.execute(query2)
            db.connection.commit()
            cur.close()
            flash("Researcher created successfully", "success")

        except Exception as e:  # OperationalError
            flash(str(e), "danger")

    # else, response for GET request
    return render_template("create_researcher.html", pageTitle="Create Researcher", form=form)


@app.route("/researchers/delete/<int:Researcher_ID>", methods=["POST"])
def deleteResearcher(Researcher_ID):
    cur = db.connection.cursor()

    query = f"""
    DELETE FROM Researcher WHERE Researcher_ID = {Researcher_ID}
    """
    try:
        cur.execute(query)
        db.connection.commit()
        db.connection.close()
        flash("Researcher deleted successfully", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect('/researchers')
