from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Optional, NumberRange

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field

class ProgramUpdate(FlaskForm):
    sector = SelectField(u'Sector name', validate_choice=False)
    sector2 = StringField(label="Add new sector name", validators = [Optional()])
    name = StringField(label = "Program Name", validators = [DataRequired(message = "Name is a required field.")])
    #name = SelectField(u'Sector name', validate_choice=False)
    sector = StringField(u'Sector name')
    submit = SubmitField("Submit", validators = [DataRequired(message = "Name is a required field.")])



class ProjectFilterForm(FlaskForm):
    min_Start_Date = DateField(label = "Start Date From:", validators = [Optional()])
    max_Start_Date = DateField(label = "Start Date To:", validators = [Optional()])
    min_End_Date = DateField(label = "End Date From:", validators = [Optional()])
    max_End_Date = DateField(label = "End Date To:", validators = [Optional()])
    min_Duration = IntegerField(label = "Duration From (in days)", validators = [Optional(), NumberRange(min=365, max=1460)])
    max_Duration = IntegerField(label = "Duration To (in days)", validators = [Optional(), NumberRange(min=365, max=1460)])
    executive = StringField(label = "Executive Name", validators = [Optional()])
    submit = SubmitField("Filter")


class ExecUpdate(FlaskForm):
    execID = IntegerField(label = "Executive ID", validators = [Optional()] )
    name = StringField(label = "Executive Name", validators = [DataRequired(message = "Name is a required field.")])
    surname = StringField(label = "Executive Surname", validators = [DataRequired(message = "Name is a required field.")])
    submit = SubmitField("Create") #it is used for executive insertion

class SelectResearchField(FlaskForm):
    ResearchField = SelectField(u'Field name', validate_choice=False)
    submit = SubmitField("get it bozo")

class ProjUpdate(FlaskForm):
    projID = IntegerField(label = "Project ID")
    name = StringField(label = "Project Name", validators = [DataRequired(message = "Name is a required field.")])
    summary = TextAreaField(label = "Project Summary", validators = [DataRequired(message = "Name is a required field.")])
    funds = IntegerField(label = "Project Funds", validators = [NumberRange(min=100000, max=1000000)])
    executive = SelectField(u'Executive', validate_choice=False)
    start_date = DateField(label = "Start Date")
    end_date = DateField(label = "End Date")
    organization = SelectField(u'Org ID', validate_choice=False)
    submit = SubmitField("Update")

class WorksOnAdd(FlaskForm):
    researcher = SelectField(u'Org ID', validate_choice=False)
    project = SelectField(u'Org ID', validate_choice=False)
    start_date = DateField(label = "Start Date", validators = [DataRequired(message = "Name is a required field.")])
    submit = SubmitField("Add Researcher to Project")

class WorksOnDelete(FlaskForm):
    researcher_d = SelectField(u'Org ID', validate_choice=False)
    project_d = SelectField(u'Org ID', validate_choice=False)
    submit_d = SubmitField("Remove Researcher from Project")