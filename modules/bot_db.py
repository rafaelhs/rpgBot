import sqlite3

### Starting database ###

def start_database():
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS COC_CHARACTER\
            (ID    INTEGER PRIMARY KEY NOT NULL,\
            NAME   TEXT        NOT NULL,\
            STR    INTEGER     NOT NULL,\
            CON    INTEGER     NOT NULL,\
            SIZ    INTEGER     NOT NULL,\
            DEX    INTEGER     NOT NULL,\
            APP    INTEGER     NOT NULL,\
            INT    INTEGER     NOT NULL,\
            POW    INTEGER     NOT NULL,\
            EDU    INTEGER     NOT NULL,\
            LUK    INTEGER     NOT NULL,\
            SAN    INTEGER     NOT NULL,\
            HP     INTEGER     NOT NULL,\
            MP     INTEGER     NOT NULL);''')
    except Exception as e:
        print(f'Failed to create database: {e}')
    else:
        print("Database initialized")
    
connection = sqlite3.connect('rpg-bot.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
start_database()
    
###

def create_coc_character(character):
    print(character)
    try:
        query = '''INSERT INTO COC_CHARACTER
                          (ID, NAME, STR, CON, SIZ, DEX, APP, INT, POW, EDU, LUK, SAN, HP, MP) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''

        data = (character['ID'],
            character['NAME'], 
            character['STR'],   
            character['CON'], 
            character['SIZ'], 
            character['DEX'], 
            character['APP'], 
            character['INT'], 
            character['POW'], 
            character['EDU'], 
            character['LUK'], 
            character['SAN'], 
            character['HP'], 
            character['MP'], 
        )
        cursor.execute(query, data)
    except Exception as e:
        print("Failed to insert into table")
        connection.rollback()
    else:
        connection.commit()

def get_coc_character(id):
    cursor.execute('''SELECT * FROM COC_CHARACTER WHERE ID=?;''', (id,))
    character = cursor.fetchone()
    if character == None:
        return None
    else:
        return dict(character)
    
def update_coc_character(character):
    try:
        query = '''UPDATE COC_CHARACTER SET 
                NAME=?, STR=?, CON=?, SIZ=?, DEX=?, APP=?, INT=?, POW=?, EDU=?, LUK=?, SAN=?, HP=?, MP=? 
                WHERE ID=?;'''
        data = (character['NAME'], 
            character['STR'],   
            character['CON'], 
            character['SIZ'], 
            character['DEX'], 
            character['APP'], 
            character['INT'], 
            character['POW'], 
            character['EDU'], 
            character['LUK'], 
            character['SAN'], 
            character['HP'], 
            character['MP'], 
            character['ID'],
        )
        cursor.execute(query, data)
    except Exception as e:
        print(e)
        print("Failed to update table")
        connection.rollback()
    else:
        connection.commit()
        
def update_coc_character_attr(attr, value, id):
    try:
        query = f'''UPDATE COC_CHARACTER SET {attr}=? WHERE ID=?;'''
        cursor.execute(query, (value, id))
    except Exception as e:
        print(e)
        print("Failed to update table")
        connection.rollback()
    else:
        connection.commit()

def delete_coc_character(id):
    try:
        cursor.execute('''DELETE FROM COC_CHARACTER WHERE ID=?;''', (id,))
    except Exception:
        print("Failed to remove from table")