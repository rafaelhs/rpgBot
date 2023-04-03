import sqlite3

### Starting database ###

def start_database():
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS COC_CHARACTER\
            (ID    INTEGER PRIMARY KEY NOT NULL,\
            NOME   TEXT        NOT NULL,\
            FOR    INTEGER     NOT NULL,\
            CON    INTEGER     NOT NULL,\
            TAM    INTEGER     NOT NULL,\
            DES    INTEGER     NOT NULL,\
            APA    INTEGER     NOT NULL,\
            INT    INTEGER     NOT NULL,\
            POD    INTEGER     NOT NULL,\
            EDU    INTEGER     NOT NULL,\
            SOR    INTEGER     NOT NULL,\
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
    try:
        query = '''INSERT INTO COC_CHARACTER
                          (ID, NOME, FOR, CON, TAM, DES, APA, INT, POD, EDU, SOR, SAN, HP, MP) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''

        data = (character['ID'],
            character['NOME'], 
            character['FOR'],   
            character['CON'], 
            character['TAM'], 
            character['DES'], 
            character['APA'], 
            character['INT'], 
            character['POD'], 
            character['EDU'], 
            character['SOR'], 
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
                          (NOME=?, FOR=?, CON=?, TAM=?, DES=?, APA=?, INT=?, POD=?, EDU=?, SOR=?, SAN=?, HP=?, MP=?) 
                          WHERE ID=?;'''

        data = (character['NOME'], 
            character['FOR'],   
            character['CON'], 
            character['TAM'], 
            character['DES'], 
            character['APA'], 
            character['INT'], 
            character['POD'], 
            character['EDU'], 
            character['SOR'], 
            character['SAN'], 
            character['HP'], 
            character['MP'], 
            character['ID'],
        )
        cursor.execute(query, data)
    except Exception:
        print("Failed to update table")
        connection.rollback()
    else:
        connection.commit()
        
def update_coc_character_attr(attr, value, id):
    try:
        query = '''UPDATE COC_CHARACTER SET (?=?) WHERE ID=?;'''
        cursor.execute(query, (attr, value, id))
    except Exception:
        print("Failed to update table")
        connection.rollback()
    else:
        connection.commit()


def delete_coc_character(id):
    try:
        cursor.execute('''DELETE FROM COC_CHARACTER WHERE ID=?;''', (id,))
    except Exception:
        print("Failed to remove from table")