from collections import OrderedDict
import faker
from datetime import datetime
import codecs

locales = OrderedDict([
    ('en-US', 7),
    ('en-PH', 2),
    ('en-IN', 4)
])
fake = faker.Faker(locales)

########################### Executives ###########################

DUMMY_DATA_NUMBER = 50
TABLE_NAME = "Executive"
TABLE_COLUMNS = ["Executive_ID","Name", "Surname"]
content = ""
#fake_IDs = set(fake.unique.random_int(min=100000, max=999999) for i in range(DUMMY_DATA_NUMBER))

for i in range(DUMMY_DATA_NUMBER):
    ID = 3119000+i
    firstName = fake.first_name()
    lastName = fake.last_name()
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{ID}","{firstName}", "{lastName}");\n'

########################### Program ###########################

TABLE_NAME = "Program"
TABLE_COLUMNS = ["Name", "ELIDEK_Sector"]
sectors = ['Food Industry Projects', 'Environmental Projects',
           'Outer Space Public Relations', 'Renewable Energy Sources',
           'Exotic Religions', 'Marine Research Projects',
           'Researcher Underpayment Management']
Programs = []

for i in range(DUMMY_DATA_NUMBER):
    Name = fake.text(max_nb_chars=20)
    Programs.append(Name)
    sector = sectors[i % 7]
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Name}","{sector}");\n'

########################### Organization ###########################

TABLE_NAME = "Organization"
TABLE_COLUMNS = ["Organization_ID", "Acronym", "Name", "Phone_Number",
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


for i in range(DUMMY_DATA_NUMBER):
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
    Phone_Number = str(2100000000 + fake.unique.random_int(min=9999999, max=699999999))
    Street = fake.street_name()
    Street_Number = fake.unique.random_int(min=1, max=10000)
    City = fake.city()
    Postal_Code = fake.unique.random_int(min=10000, max=99999)
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Organization_ID}", "{Acronym}", "{Name}", "{Phone_Number}", "{Street}", "{Street_Number}", "{City}", "{Postal_Code}", "{Org_type}");\n'

########################### Project ###########################

TABLE_NAME = "Project"
TABLE_COLUMNS = ["Project_ID", "Name", "Summary", "Project_Funds",
                 "Start_Date", "End_Date", "Executive_ID", "Program_Name", "Organization_ID"]

for i in range(DUMMY_DATA_NUMBER):
    Project_ID = 3119000 + i
    Name = capitalize(fake.text(max_nb_chars=20).replace('.', ''))
    Summary = fake.text(max_nb_chars=75)
    Project_Funds = fake.unique.random_int(min=100001, max=999999)
    Start_Date =  fake.past_date(datetime.strptime('2019-11-05', "%Y-%m-%d"))
    start_year = Start_Date.year
    d1 = Start_Date.replace(year = start_year + 1)
    d2 = Start_Date.replace(year = start_year + 4)
    End_Date = fake.date_between_dates(d1, d2)
    Executive_ID = 3119000 + fake.random_int(min=0, max=DUMMY_DATA_NUMBER-1)
    Program_Name = Programs[fake.unique.random_int(min=0, max=DUMMY_DATA_NUMBER-1)]
    Organization_ID = 3119000 + fake.random_int(min=0, max=DUMMY_DATA_NUMBER-1)
    content += f'INSERT INTO {TABLE_NAME} ({",".join(TABLE_COLUMNS)}) VALUES ("{Project_ID}", "{Name}", "{Summary}", "{Project_Funds}", "{Start_Date}", "{End_Date}", "{Executive_ID}", "{Program_Name}", "{Organization_ID}");\n'




with open(f"dummy_data.txt", 'w') as f:
    f.write(content)
