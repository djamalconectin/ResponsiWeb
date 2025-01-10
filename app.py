import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
from mysql.connector import Error

app = Flask(__name__)

def get_connection():
    try: 
        connection = mysql.connector.connect(
            host = "cjp8b.h.filess.io",
            database = "Datamhs_talksaltto",
            port = "3307",
            user = "Datamhs_talksaltto",
            password = "fa98a148bc17e265226f43d99763700329020e23"
        )
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

try:
    connection = get_connection()
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)

@app.route('/')
def home():
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tbl_mhs")
        result = cursor.fetchall()
        cursor.close()
        connection.close()
    else:
        result = []
        print("Unable to connect to database")
    return render_template('index.html', hasil=result)

@app.route('/tambah/')
def tambah_data():
    return render_template('tambah.html')

@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    nim = request.form['nim']
    nama = request.form['nama']
    asal = request.form['asal']
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO tbl_mhs (nim, nama, asal) VALUES (%s, %s, %s)", (nim, nama, asal))
            connection.commit()
        except Error as e:
            print("Error while inserting data:", e)
        finally:
            cursor.close()
            connection.close()
    return redirect(url_for('halaman_awal'))

@app.route('/ubah/<nim>', methods=['GET'])
def ubah_data(nim):
    connection = get_connection()
    result = []
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM tbl_mhs WHERE nim = %s", (nim,))
            result = cursor.fetchall()
        except Error as e:
            print("Error while fetching data:", e)
        finally:
            cursor.close()
            connection.close()
    return render_template('ubah.html', hasil=result)

@app.route('/proses_ubah/', methods=['POST'])
def proses_ubah():
    no_mhs = request.form['nim_ori']
    nim = request.form['nim']
    nama = request.form['nama']
    asal = request.form['asal']
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            sql = 'UPDATE tbl_mhs SET nim=%s, nama=%s, asal=%s WHERE nim=%s'
            value = (nim, nama, asal, no_mhs)
            cursor.execute(sql, value)
            connection.commit()
        except Error as e:
            print("Error while updating data:", e)
        finally:
            cursor.close()
            connection.close()
    return redirect(url_for('halaman_awal'))

# Hapus Data
@app.route('/hapus/<nim>', methods=['GET'])
def hapus_data(nim):
    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE FROM tbl_mhs WHERE nim=%s', (nim,))
            connection.commit()
        except Error as e:
            print("Error while deleting data:", e)
        finally:
            cursor.close()
            connection.close()
    return redirect(url_for('halaman_awal'))

if __name__ == "__main__":
    app.run(debug=True)

