import os, sqlite3, subprocess, platform, shutil
import webbrowser
from pathlib import Path

def getRootDir()->str:
    return str(Path(__file__).resolve().parent)

bd_dir = getRootDir() + '/bd.db'

def createBD(bd=bd_dir):
    with sqlite3.connect(bd) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS Shortcuts(_id INTEGER PRIMARY KEY AUTOINCREMENT,
            key STRING NOT NULL, value STRING NOT NULL UNIQUE, type STRING NOT NULL, param BOOLEAN NOT NULL DEFAULT 0, CHECK (type IN ('app', 'archive', 'site')))""")


def dropBD(bd=bd_dir):
    if os.path.exists(bd):os.remove(bd)
    else: print(f"O arquivo {bd} não foi encontrado.")

def insertValue(key:str, value:str,  type:str, param:int=0, bd:str=bd_dir ):
    with sqlite3.connect(bd) as conn:
        conn.execute(f"""INSERT INTO Shortcuts (key, value, type, param) VALUES (?,?,?,?)""", (key, value, type, param))

def getKeys(type:str, bd:str=bd_dir) -> list[str]:
    with sqlite3.connect(bd) as conn:
        return [k for (k,) in conn.execute(f"SELECT DISTINCT key FROM Shortcuts WHERE type LIKE ? ORDER BY key", (type,)).fetchall()]

#Gera o parâmetro da função openDir (v. abaixo)
def getValue(key:str, bd:str=bd_dir)-> list[tuple[str, int,str]]:
    with sqlite3.connect(bd) as conn:
        return conn.execute(f"SELECT value, param, type FROM Shortcuts WHERE key LIKE ?", (key,)).fetchall()
def getIDs(key:str,bd:str=bd_dir):
    with sqlite3.connect(bd) as conn:
        rows = conn.execute("SELECT _id FROM Shortcuts WHERE key = ?",(key,)).fetchall()
    return [row[0] for row in rows]

def getColumns(bd:str=bd_dir)->tuple[int,str,str,str,int]:
    with sqlite3.connect(bd) as conn:
        return tuple(c[1] for c in conn.execute(f'PRAGMA table_info(Shortcuts);').fetchall())

def updateValue(id_:int, key:str, value:str, type_:str, param:int, bd:str=bd_dir):
    with sqlite3.connect(bd) as conn:
        conn.execute("UPDATE Shortcuts SET key = ?, value = ?, type = ?, param = ?WHERE _id = ?",
                     (key, value, type_, param, id_))
def deleteKey(key:str, bd:str=bd_dir):
    with sqlite3.connect(bd) as conn:
        conn.execute("DELETE FROM Shortcuts WHERE key = ?",(key,))


#Ver se Funciona
def obterNavegador():
    if shutil.which("xdg-settings"):
        try:
            result = subprocess.check_output(["xdg-settings", "get", "default-web-browser"], text=True).strip()
            if result: return result
        except subprocess.CalledProcessError: pass

#Generalizar o openDir
def openDir(values:list[tuple[str,int, str]]):
    sys = platform.system()
    for value in values:
        v, arg, _ = value
        if v.startswith('http') and arg:subprocess.Popen(['/usr/bin/brave', "--incognito", v])
        elif v.startswith('http'): subprocess.Popen(['/usr/bin/brave', v])
        elif v.startswith('search '): subprocess.Popen(["/usr/bin/brave","--incognito", f'https://duckduckgo.com/?q={v[7:]}'])
        else:
            if sys == 'Windows' : os.startfile(v)                                     #Não sei se funciona
            elif sys == 'Darwin': subprocess.Popen(["open", v])       #Idem
            elif sys == 'Linux' : subprocess.Popen(["xdg-open", v])
   #Ok
            else: print('Erro!')

