#non-included libraries
import sqlite3

def db_start(db): #start the database
    con = sqlite3.connect(db.filename+'.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS main_table (IP,HOST,SUBNET,PORT)')
    con.commit()
    con.close()


def db_insert(parsed_data,db): #insert scanned data into database
    con = sqlite3.connect(db.filename+'.db')
    cur = con.cursor()
    cleaned_data = clean_set(parsed_data,cur,con)
    for each in cleaned_data:
        #if (list(cur.execute("SELECT * FROM main_table WHERE IP=?",(each['ipv4'],))) == []):
        temp = each['ipv4'].split('.')
        subnet = temp[0]+"."+temp[1]+"."+temp[2]+".0"
        cur.execute("INSERT INTO main_table VALUES (?,?,?,?)",(each['ipv4'],each['hostname'],subnet,each['ports']))
        con.commit()
    con.close()

def clean_set(data_set,cursor,conn): #check if a given dataset is already in the database
    clean = []
    for entry in data_set:
        cursor.execute("SELECT 1 FROM main_table WHERE IP = '"+entry['ipv4']+"';")
        if (cursor.fetchone()) == None:
            clean.append(entry)
        else:
            update_entry(entry,cursor,conn)
    return clean
    
def update_entry(entry,cursor,conn): #this will update if there is already an entry in the database
    cursor.execute("SELECT * FROM main_table WHERE IP = '"+entry['ipv4']+"';")
    already_in = cursor.fetchone()

    #PORT SETUP BLOCK
    final_insert = already_in[3]
    already_ports = already_in[3].split(":")
    new_ports=entry['ports'].split(":")
    for part in new_ports:
        if part not in already_ports:
            final_insert = final_insert + part + ":"
    
    #HOST SETUP BLOCK
    final_host = already_in[1]
    already_host = already_in[1].split(',')
    new_host = entry['hostname'].split(',')
    for part in new_host:
        if part not in already_host:
            if already_in[1]=="":
                final_host = part
            else:
                final_host = final_host + "," + part
    
    #THIS DOES THE FINAL INSERT        
    if final_insert != already_in[3] or final_host != already_in[1]:
        cursor.execute("UPDATE main_table SET HOST = '"+final_host+"',PORT = '"+final_insert+"' WHERE IP ='"+entry['ipv4']+"';")
        conn.commit()
    

def db_clear(db): #Clears a database
    con = sqlite3.connect(db.filename+'.db')
    cur = con.cursor()
    cur.execute('DELETE FROM main_table')
    con.commit()
    con.close()

def db_export(db): #Gets raw export
    con = sqlite3.connect(db.filename+'.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM main_table')
    data = cur.fetchall()
    return(data)

def db_spreadsheet_format(db): #Formats data for spreadsheet readiness
    con = sqlite3.connect(db.filename+'.db')
    cur = con.cursor()
    cur.execute('SELECT DISTINCT Subnet FROM main_table')
    data = cur.fetchall()
    returndict = {}
    for subnet in data[0]:
        cur.execute("SELECT * FROM main_table WHERE Subnet =='" + subnet + "';")
        returndict[subnet] = cur.fetchall()
    
    return returndict
