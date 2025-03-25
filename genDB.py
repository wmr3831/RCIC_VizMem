import sqlite3

# Connect to a database file; if it doesn't exist, it will be created.
conn = sqlite3.connect('participant_data.db')
cursor = conn.cursor()

# Optionally, create a table if it doesn't already exist.
cursor.execute('''
    CREATE TABLE IF NOT EXISTS p_log (
        pid INTEGER PRIMARY KEY,
        consent INTEGER NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS stim_info (
        pid INTEGER NOT NULL,
        obj INTEGER NOT NULL,
        angle INTEGER NOT NULL,
        PRIMARY KEY (pid, obj),
        FOREIGN KEY (pid) REFERENCES p_log(pid)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS rc_data (
        pid INTEGER NOT NULL,
        trial INTEGER NOT NULL,
        obj INTEGER NOT NULL,
        stim INTEGER NOT NULL,
        oristimpath TEXT NOT NULL,
        invstimpath TEXT NOT NULL,
        response INTEGER NOT NULL,
        PRIMARY KEY (pid, trial, obj),
        FOREIGN KEY (pid) REFERENCES p_log(pid)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS fc_data (
        pid INTEGER NOT NULL,
        trial INTEGER NOT NULL,
        obj INTEGER NOT NULL,
        dtype INTEGER NOT NULL,
        response INTEGER NOT NULL,
        PRIMARY KEY (pid, trial),
        FOREIGN KEY (pid) REFERENCES p_log(pid)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS color_data (
        pid INTEGER NOT NULL,
        trial INTEGER NOT NULL,
        obj INTEGER NOT NULL,
        response INTEGER NOT NULL,
        PRIMARY KEY (pid, trial), 
        FOREIGN KEY (pid) REFERENCES p_log(pid)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS debrief (
        pid INTEGER PRIMARY KEY,
        agree INTEGER NOT NULL,
        FOREIGN KEY (pid) REFERENCES p_log(pid)
    )
''')

conn.commit()
conn.close()