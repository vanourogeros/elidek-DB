from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, IntegerRangeField
from wtforms.validators import DataRequired, Email, Optional, NumberRange

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
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
    
    execID = IntegerField(label = "Executive ID", validators = [NumberRange(min=3119000, max=999999999999)])

    name = StringField(label = "Executive Name", validators = [Optional()])

    surname = StringField(label = "Executive Surname", validators = [Optional()])

    submit = SubmitField("Update")