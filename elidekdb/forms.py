from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, IntegerRangeField, SelectField
from wtforms.validators import DataRequired, Email, Optional, NumberRange

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field

class ProgramUpdate(FlaskForm):
    name = StringField(label = "Executive Name", validators = [DataRequired(message = "Name is a required field.")])
    sector = SelectField(u'Field name', validate_choice=False)
    submit = SubmitField("Update")

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
    execID = IntegerField(label = "Executive ID", validators = [Optional()])
    name = StringField(label = "Executive Name", validators = [DataRequired(message = "Name is a required field.")])
    surname = StringField(label = "Executive Surname", validators = [DataRequired(message = "Name is a required field.")])
    submit = SubmitField("Create") #it is used for executive insertion

class SelectResearchField(FlaskForm):
    ResearchField = SelectField(u'Field name', validate_choice=False)
    submit = SubmitField("get it bozo")

class ProjUpdate(FlaskForm):
    projID = IntegerField(label = "Project ID")
    name = StringField(label = "Project Name", validators = [DataRequired(message = "Name is a required field.")])
    summary = StringField(label = "Project Summary", validators = [DataRequired(message = "Name is a required field.")])
    submit = SubmitField("Update")