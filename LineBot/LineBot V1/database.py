from decouple import config
import pymysql
import pymysql.cursors


def connectToDatabase():
    """ Connects to the database """
    conn = pymysql.connect(host=config('MARIA_HOST'),
                             user=config('MARIA_USER'),
                             password=config('MARIA_PASSWD'),
                             db=config('MARIA_DB_NAME'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return conn


def addRow(conn, title, url, text):
    """ Creates a new record """
    with conn.cursor() as cursor:
        sql = "INSERT INTO comments(course_name, course_url, course_comment) VALUES (%s, %s, %s)"
        cursor.execute(sql,(title, url, text))
        conn.commit()


def fetch(conn):
    with conn.cursor() as cursor:
        sql = "SELECT * FROM comments WHERE comment_id = 1"
        cursor.execute(sql)


def resetTable(conn): 
    with conn.cursor() as cursor:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS comments;")
        cursor.execute("CREATE TABLE IF NOT EXISTS comments(comment_id int auto_increment, course_name varchar(255) not null, course_url varchar(255) not null, course_comment longtext, primary key(comment_id));")
        conn.commit() 


