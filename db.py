import psycopg2
from psycopg2 import Error
import datetime
from variables import username, password, database_name, port, host

def connect_to_database():
    try:
        connection = psycopg2.connect(user=username,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database_name)
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return

def new_deadline(connection, name, date, link):
    try:
        query = "INSERT INTO deadlines (name,date,link, reminded, finished) VALUES(%s, %s, %s, FALSE)"
        val = (name, date, link)
        
        cursor = connection.cursor()

        cursor.execute(query, val)
        connection.commit()
        print("New deadline added to the table")
    except (Exception, Error) as error:
        print("Error while executing the query", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def list_deadlines(connection):
    try:
        query = "SELECT * FROM deadlines ORDER BY date"
        
        cursor = connection.cursor()

        cursor.execute(query)

        deadlines = cursor.fetchmany(5)
        deadlines_formatted = []
        for i in range(len(deadlines)):
            deadlines_formatted.append("INSTUTION: " + str(deadlines[i][0]) + "   DEADLINE: " + str(deadlines[i][1]) + "   LINK: " + str(deadlines[i][2]))
        connection.commit()
        return deadlines_formatted
    except (Exception, Error) as error:
        print("Error while executing the query", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def remind_deadline(connection):
    try:
        query = "SELECT * FROM deadlines ORDER BY date"
        
        cursor = connection.cursor()

        cursor.execute(query)

        deadlines = cursor.fetchmany(7)
        deadlines_formatted = []
        for i in range(len(deadlines)):
            days_difference = (deadlines[i][1] - datetime.datetime.now().date()).days
            if days_difference <= 7 and days_difference > 0:
                deadlines_formatted.append("INSTUTION: " + deadlines[i][0] + "   DEADLINE: " + str(deadlines[i][1]) + "   LINK: " + deadlines[i][2])
                update_query = "UPDATE deadlines SET reminded = TRUE WHERE name = %s"
                cursor.execute(update_query, (deadlines[i][0],))
        connection.commit()
        return deadlines_formatted
    except (Exception, Error) as error:
        print("Error while executing the query", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def warn_deadline(connection):
    try:
        query = "SELECT * FROM deadlines ORDER BY date"
        
        cursor = connection.cursor()

        cursor.execute(query)

        deadlines = cursor.fetchmany(7)
        deadlines_formatted = []
        for i in range(len(deadlines)):
            days_difference = (deadlines[i][1] - datetime.datetime.now().date()).days
            if days_difference == 0:
                deadlines_formatted.append("INSTUTION: " + deadlines[i][0] + "   DEADLINE: " + str(deadlines[i][1]) + "   LINK: " + deadlines[i][2])
                delete_query = "DELETE FROM deadlines WHERE name = %s"
                cursor.execute(delete_query, (deadlines[i][0],))
        connection.commit()
        return deadlines_formatted
    except (Exception, Error) as error:
        print("Error while executing the query", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

# conn = connect_to_database()
# dnm = warn_deadline(conn)
# print(dnm)

