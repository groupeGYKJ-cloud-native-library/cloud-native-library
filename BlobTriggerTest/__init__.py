import logging
import mysql.connector
import os
import azure.functions as func

config = {
    'host' : os.environ['HOST_SQL_AZURE'],
    'user' : os.environ['USER_SQL_AZURE'],
    'password' : os.environ['PASSWORD_SQL_AZURE'],
    'database': os.environ['DATABASE_SQL_AZURE'],
    'client_flags' : [mysql.connector.ClientFlag.SSL],
    'ssl_ca': os.environ['SSL_CA_SQL_AZURE']}
    
conn = mysql.connector.connect(**config)
cursor = conn.cursor(dictionary=True)

def insert_row(blob):
    url = "https://stockagelivre.blob.core.windows.net/blob/"+blob
    titre = blob.split(".")[0].replace('-', " ").replace("blob/", " ")
    cursor.execute("INSERT INTO epubs (titre, url) VALUES (%s, %s);", (titre, url))


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    insert_row(myblob.name)
    conn.commit()
    cursor.close()
    conn.close()