# elidek-DB
Project for the Databases 2022 class in NTUA ECE that simulates a Database for the Hellenic Foundation for Research and Innovation (ELIDEK). 

## Authors
- Ioannis Protogeros  03119008 [vanourogeros](https://github.com/vanourogeros)
- Myrsini Kellari     03119082 [mpyrsini](https://github.com/mpyrsini)
- Chrysa Pratikaki    03119131 [cpratikaki](https://github.com/cpratikaki)

## ER Diagram (in Greek)
![image](https://user-images.githubusercontent.com/61976410/172052702-79ff2b1a-d2b6-43cc-85ad-787644115772.png)

## Relational Model
![image](https://user-images.githubusercontent.com/61976410/172052725-99211133-2059-4af2-8b0c-930bece7b258.png)

## Installation Guide
- Clone this repository using the command `git clone https://github.com/vanourogeros/elidek-D`
in a local working directory
- Use the command `pip install requirements.txt` in said directory to download the needed libraries
- Create the database using a DBSM that supports MySQL/MariaDB and run the scripts `elidek_create_schema.sql` and `elidek_insert_data.sql`
- Use the command `python3 run.py` or `python run.py` and visit `http://localhost:3000/` from a browser

## Tools Used
The tool used for this project as shown in the file requirements.txt are
>click==8.1.2 <br>
>dnspython==2.2.1<br>
>email-validator==1.1.3<br>
>Faker==13.3.4<br>
>Flask==2.1.1<br>
>Flask-MySQLdb==1.0.1<br>
>Flask-WTF==1.0.1<br>
>idna==3.3<br>
>importlib-metadata==4.11.3<br>
>itsdangerous==2.1.2<br>
>Jinja2==3.1.1<br>
>MarkupSafe==2.1.1<br>
>mysqlclient==2.1.0<br>
>python-dateutil==2.8.2<br>
>six==1.16.0<br>
>Werkzeug==2.1.1<br>
>WTForms==3.0.1<br>
>zipp==3.8.0

## Usage
Through the developed UI the user (that in this simulation is supposedly a manager working in ELIDEK) may have access to the results of various queries. They may also manipulate (create, update, delete) the entirety of the database (<b>All</b> tables regarding the entities, relationships between them etc.) using various forms (Flask WTForms) provided by the website.

## Screenshots
![image](https://user-images.githubusercontent.com/61976410/172053255-3ae5b0bc-fcf1-47c3-a19e-8e99536d3d08.png)
![image](https://user-images.githubusercontent.com/61976410/172053312-3486b596-458b-406d-aa4b-0eb087c155fa.png)
![image](https://user-images.githubusercontent.com/61976410/172053694-205dcafc-39dc-4d2a-bda9-5c56d839c79d.png)
![image](https://user-images.githubusercontent.com/61976410/172053343-ff14cd0c-c94b-4a88-8650-04afe31e78dd.png)
![image](https://user-images.githubusercontent.com/61976410/172053411-9840532b-ac6c-4e3b-b8d2-e274eab07c4c.png)

### Disclaimers
- Because of the aims of this project and the limited time for its completion in regards to its requirements, less focus was given to the visual aesthetics of the UI and more to the functionality of the Database and its connection to the website.
- All data was randomly generated by the Faker python library and any correlation to real world names, phone numbers, etc. is purely coincidental.

