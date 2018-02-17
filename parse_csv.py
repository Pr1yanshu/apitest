# This file parses the csv file and copies all its content to a postgresql table name 'apitests' 
import psycopg2

def process_csv(conn, file_obj, table_name):
	cur = conn.cursor()
	cur.copy_expert(sql=SQL_STATEMENT % table_name, file=file_obj)
	conn.commit()
	cur.close()

if __name__ == '__main__':
	my_file = open("Database/IN.csv")
	SQL_STATEMENT = "COPY %s FROM STDIN WITH CSV HEADER DELIMITER AS ','"
	conn = psycopg2.connect(dbname="apitest", user="Priyanshu", password="pr1yanshu")
	try:
		process_csv(conn, my_file, "apitests")
	except Exception as e:
		print(e)
	finally:
		conn.close()