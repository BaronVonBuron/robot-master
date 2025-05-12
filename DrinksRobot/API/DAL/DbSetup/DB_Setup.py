import sqlite3
import os
import uuid
# Find nuværende sti (hvor scriptet køres fra)
cwd = os.getcwd()

# Find projektroden uanset hvor scriptet køres fra
project_root_name = "robotProgram_protoype-master"
if project_root_name in cwd:
    project_root = cwd.split(project_root_name)[0] + project_root_name
else:
    raise ValueError(f"Projektmappen '{project_root_name}' blev ikke fundet i den aktuelle sti.")

# Konstruér den relative sti til databasen
db_path = os.path.join(project_root, "DrinksRobot", "API", "DAL", "Database", "drinks.db")

# ✅ Opret mappen, hvis den ikke findes
os.makedirs(os.path.dirname(db_path), exist_ok=True)

print("Database path:", db_path)

# Opret forbindelse til databasen
conn = sqlite3.connect(db_path)
print(f"Databasen er oprettet på {db_path}")

cursor = conn.cursor()
# Aktiver foreign keys
cursor.execute("PRAGMA foreign_keys = ON;")



# Opret BottleTable
cursor.execute("""
CREATE TABLE IF NOT EXISTS BottleTable (
    BottleId INTEGER PRIMARY KEY AUTOINCREMENT,
    BottlePosition INTEGER,
    URScriptGet TEXT,
    URScriptPour TEXT,
    URScriptBack TEXT,
    Img TEXT,
    Title TEXT,
    BottleType TEXT,
    UseCount INTEGER
);
""")
# Opret ContentId
cursor.execute("""
CREATE TABLE IF NOT EXISTS ContentTable (
    ContentId INTEGER PRIMARY KEY AUTOINCREMENT,
    BottleName TEXT,
    BottleId INTEGER,   -- This column references a BottleId
    DrinkId INTEGER,
    FOREIGN KEY (BottleId) REFERENCES BottleTable(BottleId),  
    FOREIGN KEY (DrinkId) REFERENCES DrinkTable(DrinkId) 
);
""")

# Opret FærdigDrinkTabel
cursor.execute("""
CREATE TABLE IF NOT EXISTS DrinkTable (
    DrinkId INTEGER PRIMARY KEY AUTOINCREMENT,
    DrinkName TEXT,
    Img TEXT,
    UseCount INTEGER
);
""")

# Opret LogTable
cursor.execute("""
CREATE TABLE IF NOT EXISTS LogTable (
    LogId INTEGER PRIMARY KEY AUTOINCREMENT,
    LogTime TEXT,
    LogMsg TEXT,
    LogType TEXT
);
""")

# Gem og luk
conn.commit()
conn.close()