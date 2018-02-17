#This python script simply creates a postgresqsl table
import psycopg2
def create_tables():
    """ create tables in the PostgreSQL database"""
    command ="CREATE TABLE apitests (key VARCHAR ,place_name VARCHAR(155),admin_name1 VARCHAR(155),latitude FLOAT(53),longitude FLOAT(53),accuracy INTEGER)"
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(dbname="apitest", user="Priyanshu", password="pr1yanshu")
        cur = conn.cursor()
        # create table one by one
        #for command in commands:
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("/dberror")
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
