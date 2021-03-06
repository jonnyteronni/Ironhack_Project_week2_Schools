import mysql.connector
from getpass import getpass
from os import sys
import datetime

# SQL Python link code
# Table to export table to database
#def table_to_sql(df, cnx, table):
#    df.to_sql(table, cnx, if_exists = 'replace', index = False)


# Create tables if they do not exist on database
#Tables Sql creation code


def connect_to_sql():
    # Connection to SQL database
    password = getpass('Please write your localhost root password:\n')
    cnx = mysql.connector.connect(user = 'root',password = password, host ='localhost', database = 'competitive_landscape')

    # Check if connection is working
    if cnx.is_connected():
        print("Connection open")
    else:
        print("Connection is not successfully open")

    return cnx.cursor(), cnx

def create_sql_tables(cursor):
    q_schools = ("CREATE TABLE IF NOT EXISTS "
    "schools ("
    "school VARCHAR(100) PRIMARY KEY ,"
    "website VARCHAR(1000),"
    "description TEXT,"
    "LogoUrl VARCHAR(100),"
    "LastUpdated Date)")

    q_locations = ("CREATE TABLE IF NOT EXISTS "
    "locations ("
    "location_id INT PRIMARY KEY,"
    "description VARCHAR(500),"
    "country_id INT,"
    "country_name VARCHAR(100),"
    "country_abbrev VARCHAR(100),"
    "city_id INT,"
    "city_name VARCHAR(100),"
    "city_keyword VARCHAR(100),"
    "state_id VARCHAR(100),"
    "state_name VARCHAR(100),"
    "state_abbrev VARCHAR(100),"
    "state_keyword VARCHAR(100),"
    "school VARCHAR(100),"
    "LastUpdated Date, "
    "CONSTRAINT locations_FK_1 FOREIGN KEY (school) "
    "REFERENCES schools (school)) "
    "ENGINE = InnoDB;")

    q_courses = ("CREATE TABLE IF NOT EXISTS "
    "courses ("
    "courses VARCHAR(100),"
    "school VARCHAR(100),"
    "PRIMARY KEY (courses, school),"
    "LastUpdated Date, "
    "CONSTRAINT courses_FK_1 FOREIGN KEY (school)"
    "REFERENCES schools (school))"
    "ENGINE = InnoDB;")

    q_badges = ("CREATE TABLE IF NOT EXISTS "
    "badges ("
    "school VARCHAR(100),"
    "keyword VARCHAR(100),"
    "PRIMARY KEY (school, keyword),"
    "name VARCHAR(100),"
    "description VARCHAR(500),"
    "LastUpdated Date, "
    "CONSTRAINT badges_FK_1 FOREIGN KEY (school) "
    "REFERENCES schools (school)) "
    "ENGINE = InnoDB;")

    q_reviews = ("CREATE TABLE IF NOT EXISTS "
    "reviews ("
    "id INT PRIMARY KEY,"
    "name VARCHAR(100),"
    "anonymous VARCHAR(100),"
    "hostProgramName VARCHAR(100),"
    "graduatingYear INT,"
    "isAlumni VARCHAR(100),"
    "jobTitle VARCHAR(100),"
    "tagline VARCHAR(1000),"
    "createdAt Date,"
    "queryDate Date,"
    "program VARCHAR(100),"
    "overallScore VARCHAR(100),"
    "comments TEXT,"
    "overall VARCHAR(100),"
    "curriculum INT,"
    "jobSupport INT,"
    "review_body TEXT,"
    "school VARCHAR(100),"
    "LastUpdated Date, "
    "CONSTRAINT reviews_FK_1 FOREIGN KEY (school) "
    "REFERENCES schools (school))"
    "ENGINE = InnoDB;")

    # Execute all tables to SQL database
    cursor.execute(q_schools)
    cursor.execute(q_badges)
    cursor.execute(q_locations)
    cursor.execute(q_reviews)
    cursor.execute(q_courses)

def print_to_sql_tables(cursor, reviews_df, locations_df, courses_df, badges_df, schools_df,cnx):

    # Insert rows on tables from dataframes
    # Table Reviews

    # {'sql_table_name' : 'dataframe_column_name'}

    review_cols = {"id":"id",
        "name":"name",
        "anonymous":"anonymous",
        "hostProgramName":"hostProgramName",
        "graduatingYear":"graduatingYear",
        "isAlumni":"isAlumni",
        "jobTitle":"jobTitle",
        "tagline":"tagline",
        "createdAt":"createdAt",
        "queryDate":"queryDate",
        "program":"program",
        "overallScore":"overallScore",
        "comments":"comments",
        "overall":"overall",
        "curriculum":"curriculum",
        "jobSupport":"jobSupport",
        "review_body":"review_body",
        "school":"school"}

    locations_cols = {'location_id':'location_id', 'description':'description', 'country_id':'country_id', 'country_name':'country_name', 'country_abbrev':'country_abbrev',
       'city_id':'city_id', 'city_name':'city_name', 'city_keyword':'city_keyword', 'state_id':'state_id', 'state_name':'state_name',
       'state_abbrev':'state_abbrev', 'state_keyword':'state_keyword', 'school':'school'}

    courses_cols = {'courses':'courses', 'school':'school'}

    badges_cols = {'name':'name', 'keyword':'keyword', 'description':'description', 'school':'school'}

    schools_cols = {'website':'website', 'description':'description', 'LogoUrl':'LogoUrl', 'school':'school'}


    def print_table_to_sql (df, cols, sql_db_name,cnx):
        query = ''
        list_keys = list(cols.keys())
        for row in range(len(df.index)):
            values = list(str(df.iloc[row, n]) for n in range(len(list_keys)))
            values = tuple(values + [datetime.datetime.now()])
            query = "INSERT INTO competitive_landscape." + sql_db_name + " ("
            for n in range(len(list_keys)):
                query += list_keys[n] + ", "
            query += 'LastUpdated' + ')  VALUES ('
            query += '%s,' * (len(list_keys)) + '%s);'
            try:
                cursor.execute(query, values)
                cnx.commit()
            except mysql.connector.IntegrityError as err:
                print("Error: {}".format(err))

    print_table_to_sql(schools_df, schools_cols, "schools",cnx)
    print_table_to_sql(locations_df, locations_cols, "locations",cnx)
    print_table_to_sql(reviews_df, review_cols, "reviews",cnx)
    print_table_to_sql(courses_df, courses_cols, "courses",cnx)
    print_table_to_sql(badges_df, badges_cols, "badges",cnx)



def commit_sql(cursor, cnx):
    # Commits everything to SQL database and closes connections
    cnx.commit()


def close_sql(cursor,cnx):
    cursor.close()
    cnx.close()
