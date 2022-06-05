from collections import OrderedDict
import faker
from datetime import datetime
import codecs

locales = OrderedDict([
    ('el-GR', 7),
    ('en-US', 2),
    ('el-CY', 4)
])
fake = faker.Faker(locales)

########################### Executives ###########################

DUMMY_DATA_NUMBER = 200
TABLE_NAME = "Executive"
TABLE_COLUMNS = ["Executive_ID", "Name", "Surname"]
content = ""
# fake_IDs = set(fake.unique.random_int(min=100000, max=999999) for i in range(DUMMY_DATA_NUMBER))

for i in range(DUMMY_DATA_NUMBER):
    ID = 3119000 + i
    firstName = fake.first_name()
    lastName = fake.last_name()
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{ID}","{firstName}", "{lastName}");\n'

########################### Program ###########################

TABLE_NAME = "Program"
TABLE_COLUMNS = ["Program_ID", "Name", "ELIDEK_Sector"]
sectors = ['Food Industry Projects', 'Environmental Projects',
           'Outer Space Public Relations', 'Renewable Energy Sources',
           'Exotic Religions', 'Marine Research Projects',
           'Researcher Underpayment Management']
Programs = []

for i in range(DUMMY_DATA_NUMBER):
    ID = 3119000 + i
    Name = fake.text(max_nb_chars=20)
    Programs.append(Name)
    sector = sectors[i % 7]
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{ID}","{Name}","{sector}");\n'

########################### Organization ###########################

TABLE_NAME = "Organization"
TABLE_COLUMNS = ["Organization_ID", "Acronym", "Name",
                 "Street", "Street_Number", "City", "Postal_Code", "Org_type"]
o_type = ['University', 'Company', 'Research Center']


def acr(text):
    # add first letter
    res = text[0]

    # iterate over string
    for j in range(1, len(text)):
        if text[j - 1] == ' ':
            # add letter next to space
            res += text[j]

    # uppercase output
    res = res.upper()
    return res


def capitalize(text):
    # add first letter
    res = text[0].upper()
    # iterate over string
    for j in range(1, len(text)):
        if text[j - 1] == ' ':
            # add letter next to space
            res += text[j].upper()
        else:
            res += text[j]
    return res

ORG_NUMBER = DUMMY_DATA_NUMBER//4
for i in range(ORG_NUMBER):
    Organization_ID = 3119000 + i
    Name = capitalize(fake.text(max_nb_chars=20).replace('.', ''))
    Org_type = o_type[i % 3]
    if Org_type == 'University':
        Name += ' University'
    if Org_type == 'Company':
        Name += ' Company'
    if Org_type == 'Research Center':
        Name += ' Research Center'
    Acronym = acr(Name)
    Street = fake.street_name()
    Street_Number = fake.unique.random_int(min=1, max=10000)
    City = fake.city()
    Postal_Code = fake.unique.random_int(min=10000, max=99999)
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Organization_ID}", "{Acronym}", "{Name}", "{Street}", "{Street_Number}", "{City}", "{Postal_Code}", "{Org_type}");\n'


########################### Researcher ###########################

TABLE_NAME = "Researcher"
TABLE_COLUMNS = ["Researcher_ID", "Name", "Surname", "Gender",
                 "Birth_Date", "Recruitment_Date", "Organization_ID"]
researcher_org = {}
for i in range(8 * DUMMY_DATA_NUMBER):
    genders = ['Male', 'Female', 'Other']
    Researcher_ID = 3119000 + i
    Name = fake.first_name()
    Surname = fake.last_name()
    Gender = genders[i % 3]
    Birth_Date = fake.date_of_birth(minimum_age=20, maximum_age=60)
    Recruitment_Date = fake.date_this_decade()
    Organization_ID = 3119000 + fake.random_int(min=0, max=ORG_NUMBER - 1)
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Researcher_ID}", "{Name}", "{Surname}", "{Gender}", "{Birth_Date}", "{Recruitment_Date}", "{Organization_ID}");\n'
    researcher_org[Researcher_ID] = Organization_ID
########################### Project ###########################

TABLE_NAME = "Project"
TABLE_COLUMNS = ["Project_ID", "Name", "Summary", "Project_Funds",
                 "Start_Date", "End_Date", "Executive_ID", "Program_ID", "Organization_ID", "Research_Manager_ID"]
startdates = []
enddates = []
paris = []
project_org = [[] for i in range(DUMMY_DATA_NUMBER)]

for i in range(6*DUMMY_DATA_NUMBER):
    Project_ID = 3119000 + i
    Name = capitalize(fake.text(max_nb_chars=20).replace('.', ''))
    Summary = fake.text(max_nb_chars=75)
    Project_Funds = fake.unique.random_int(min=100001, max=999999)
    Start_Date = fake.past_date(datetime.strptime('2019-11-05', "%Y-%m-%d"))
    if Start_Date.month == 2 and Start_Date.day == 29:
        Start_Date = Start_Date.replace(day=28)
        print(Start_Date)
    startdates.append(Start_Date)
    start_year = Start_Date.year
    d1 = Start_Date.replace(year=start_year + 1)
    d2 = Start_Date.replace(year=start_year + 4)
    End_Date = fake.date_between_dates(d1, d2)
    enddates.append(End_Date)
    Executive_ID = 3119000 + fake.random_int(min=0, max=DUMMY_DATA_NUMBER - 1)
    Program_ID = 3119000 + fake.random_int(min=0, max=DUMMY_DATA_NUMBER - 1)
    Research_Manager_ID = 3119000 + fake.unique.random_int(min=0, max=6*DUMMY_DATA_NUMBER - 1)
    Organization_ID = researcher_org[Research_Manager_ID]
    project_org[Organization_ID - 3119000].append(Project_ID)
    project_org.append(Organization_ID)
    paris.append((Research_Manager_ID, Project_ID))
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Project_ID}", "{Name}", "{Summary}", "{Project_Funds}", "{Start_Date}", "{End_Date}", "{Executive_ID}", "{Program_ID}", "{Organization_ID}", "{Research_Manager_ID}");\n'
    content += f'INSERT INTO {"Works_On"} ({",".join(["Researcher_ID", "Project_ID", "Start_Date"])}) VALUES ("{Research_Manager_ID}", "{Project_ID}", "{Start_Date}");\n'


########################### University ###########################

TABLE_NAME = "University"
TABLE_COLUMNS = ["University_ID", "Ministry_Budget", "Org_type"]

for i in range(ORG_NUMBER // 3 + 1):
    University_ID = 3119000 + 3 * i
    Ministry_Budget = fake.random_int(min=6900, max=690000)
    Org_type = 'University'
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{University_ID}", "{Ministry_Budget}", "{Org_type}");\n'

########################### Research_Center ###########################

TABLE_NAME = "Research_Center"
TABLE_COLUMNS = ["Research_Center_ID", "Ministry_Budget", "Actions_Budget", "Org_type"]

for i in range(ORG_NUMBER // 3):
    Research_Center_ID = 3119002 + 3 * i
    Ministry_Budget = fake.random_int(min=6900, max=690000)
    Actions_Budget = fake.random_int(min=6900, max=690000)
    Org_type = 'Research Center'
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Research_Center_ID}", "{Ministry_Budget}", "{Actions_Budget}", "{Org_type}");\n'

########################### Company ###########################

TABLE_NAME = "Company"
TABLE_COLUMNS = ["Company_ID", "Equity", "Org_type"]

for i in range(ORG_NUMBER // 3 + 1):
    Company_ID = 3119001 + 3 * i
    Equity = fake.random_int(min=6900, max=690000)
    Org_type = 'Company'
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Company_ID}", "{Equity}", "{Org_type}");\n'

########################### Research Field ###########################

TABLE_NAME = "Research_Field"
TABLE_COLUMNS = ["Field_ID", "Name"]
fields = ['Physics', 'Chemistry', 'Humanities', 'Creative Arts', 'Engineering', 'Economics', 'Mathematics',
          'Computer Science', 'Biology', 'Medical Sciences', 'Education', 'Religion']
for i in range(len(fields)):
    Field_ID = i + 1
    Name = fields[i]
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Field_ID}", "{Name}");\n'

########################### Research Field ###########################

TABLE_NAME = "Work_to_be_Submitted"
TABLE_COLUMNS = ["Title", "Project_ID", "Summary", "Submission_Date"]
for i in range(DUMMY_DATA_NUMBER):
    Title = capitalize(fake.text(max_nb_chars=20)).replace('.', '')
    Summary = fake.text(max_nb_chars=75)
    Project_ID = 3119000 + fake.random_int(min=0, max=49)
    idx = Project_ID - 3119000
    d1 = startdates[idx]
    d2 = enddates[idx]
    Submission_Date = fake.date_between_dates(d1, d2)
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Title}", "{Project_ID}", "{Summary}", "{Submission_Date}");\n'

TABLE_NAME = "Works_On"
TABLE_COLUMNS = ["Researcher_ID", "Project_ID", "Start_Date"]

for i in range(10 * DUMMY_DATA_NUMBER):
    Researcher_ID = 3119000 + fake.random_int(min=0, max=3*DUMMY_DATA_NUMBER - 1)
    org = researcher_org[Researcher_ID]
    if len(project_org[org - 3119000]) <= 1:
        continue
    Project_ID = project_org[org - 3119000][fake.random_int(min=0, max=len(project_org[org - 3119000]) - 1)]
    print(Project_ID - 3119000)
    d1 = startdates[Project_ID - 3119000]
    d2 = enddates[Project_ID - 3119000]
    Start_Date = fake.date_between_dates(d1, d2)
    if (Researcher_ID, Project_ID) not in paris:
        paris.append((Researcher_ID, Project_ID))
        content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Researcher_ID}", "{Project_ID}", "{Start_Date}");\n'

TABLE_NAME = "Evaluation"
TABLE_COLUMNS = ["Researcher_ID", "Project_ID", "Evaluation_Date", "Evaluation_Grade"]

for i in range(6*DUMMY_DATA_NUMBER):
    Researcher_ID = 3119000 + fake.random_int(min=0, max=8*DUMMY_DATA_NUMBER-1)
    Project_ID = 3119000 + i
    d1 = startdates[Project_ID - 3119000]
    d2 = enddates[Project_ID - 3119000]
    Evaluation_Date = fake.date_between_dates(d1.replace(year=d1.year - 3), d1)
    Evaluation_Grade = fake.random_int(min=1, max=10)
    if Project_ID not in project_org[researcher_org[Researcher_ID] - 3119000]:
        content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Researcher_ID}", "{Project_ID}", "{Evaluation_Date}", "{Evaluation_Grade}");\n'
    else:
        i -= 1

TABLE_NAME = "Org_Phone"
TABLE_COLUMNS = ["Organization_ID", "Phone_Number"]
for i in range(2 * DUMMY_DATA_NUMBER):
    Organization_ID = 3119000 + i if i < 50 else 3119000 + fake.random_int(min=0, max=49)
    Phone_Number = str(2100000000 + fake.unique.random_int(min=9999999, max=699999999))
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Organization_ID}", "{Phone_Number}");\n'

TABLE_NAME = "Refers_To"
TABLE_COLUMNS = ["Field_ID", "Project_ID"]
paris = []
for i in range(4 * DUMMY_DATA_NUMBER):
    Project_ID = 3119000 + i % DUMMY_DATA_NUMBER
    Field_ID = fake.random_int(min=1, max=12)
    if (Project_ID, Field_ID) not in paris:
        paris.append((Project_ID, Field_ID))
        content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Field_ID}", "{Project_ID}");\n'

#with open(f"dummy_data.txt", 'w') as f:
f = open("dummy_data.txt", "w", encoding="utf-8")
f.write(content)
