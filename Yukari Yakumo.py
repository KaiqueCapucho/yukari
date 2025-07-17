import subprocess
import sys, sqlite3
import webbrowser

#Improvements: print opcional p/outros livros, mecanismo p/alterar página salva, delete, melhorar código/lógica

def create(bd='./Ran_Yakumo.db'):
    conn = sqlite3.connect(bd)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Apps(_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   apps STRING NOT NULL, dir STRING NOT NULL UNIQUE)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Websites(_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   sites STRING NOT NULL, url STRING, private INTEGER NOT NULL CHECK (private IN (0, 1)))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Livros(_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   livros STRING NOT NULL, dir STRING NOT NULL UNIQUE, page INTEGER NOT NULL)""")
    conn.commit()
    cursor.close(), conn.close()

def insert(inp:str, cursor):
    if inp.startswith('add site'):
        cursor.execute(f"""INSERT INTO Websites (sites,url,private) values(?,?,?)""",
                       (inp[9:], input('url?:'), input('private?(0||1): ')))
    elif inp.startswith('add game'):
        cursor.execute(fr"""INSERT INTO Apps (apps,dir) values(?,?)""",
                       (inp[9:], commutatio(input('dir?: '))))
    elif inp.startswith('add book'):
        cursor.execute(fr"""INSERT INTO Livros (livros,dir,page) values(?,?,?)""",
                       (inp[9:], commutatio(input('dir?: ')), input('page?: ')))
    else: return inp

#Um tanto confuso. Melhorar o código
def Index(ager: tuple, tabella: str, locus: str):
    with sqlite3.connect(locus) as connect:
        cursor = connect.cursor()
        itens = cursor.execute(f"SELECT {', '.join(ager)} FROM {tabella}").fetchall()
        itens = sorted(set(itens))
    num_cols = len(ager)
    if num_cols == 1:
        print(f"{ager[0]}:"), print(', '.join(str(row[0]) for row in itens))
    else:
        # Transpõe os dados para calcular larguras
        colunas = list(zip(*itens)) if itens else [[] for _ in ager]
        # Calcula largura ideal por coluna
        larguras = []
        for i, nome_coluna in enumerate(ager):
            conteudos = [str(x) for x in colunas[i]] if colunas[i] else []
            max_conteudo = max([len(str(nome_coluna))] + [len(c) for c in conteudos], default=0)
            larguras.append(max_conteudo + 2)  # margem extra
        # Formato dinâmico
        formato = ''.join([f'{{:<{w}}}' for w in larguras])
        # Cabeçalho
        print(formato.format(*ager))
        # Conteúdo
        for linha in itens:
            print(formato.format(*[str(c) for c in linha]))
    print('')
    # Retorna a primeira coluna como lista
    return [linha[0].lower() for linha in itens]

def Ostium(opus, arg=0):
    if opus.endswith('.docx'): subprocess.Popen(['C:\\Program Files (x86)\\Microsoft Office\\Office14\\WINWORD.exe', opus])
    elif opus.endswith('.xlsx'): subprocess.Popen(['C:\\Program Files (x86)\\Microsoft Office\\Office14\\EXCEL.EXE', opus])
    elif opus.endswith('.txt'): subprocess.Popen(['C:\\Windows\\System32\\notepad.exe', opus])
    elif opus.endswith('.pdf'): webbrowser.open(opus)
    elif opus.endswith('.exe'): subprocess.Popen(opus)
    elif opus.endswith('.db'): subprocess.Popen(["C:/Program Files/SQLiteStudio/SQLiteStudio.exe", opus])
    elif opus.startswith('http'):
        if arg: subprocess.Popen(["C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe", "--incognito", opus])
        else: subprocess.Popen(["C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",opus])
    else: print('Erro! Extensão de arquivo inválida')

create()
commutatio = lambda x: (x[1:-1] if x.strip().startswith('"') and x.strip().endswith('"') else x).replace('\\', '/')

#Essa parte dos livros ainda está meio ruim

sites = Index(('sites',), 'Websites', './Ran_Yakumo.db')
apps = Index(('apps',), 'Apps', './Ran_Yakumo.db')
books = Index(('livros', 'page'), 'Livros', './Ran_Yakumo.db')

# Input
connector = sqlite3.connect('./Ran_Yakumo.db')
cursor = connector.cursor()
output = []
while (inp:= input().lower()) != '':
    try: output.append(insert(inp, cursor))
    except Exception as e:
        print(f'Erro! {e}')
        continue
    else: connector.commit()

# Output
for out in output:
    try:
        if out in sites:
                for outS in cursor.execute(f'SELECT url, private FROM Websites WHERE sites LIKE ?', [out]).fetchall():
                    Ostium(*outS)
        elif out in apps:
            for outA in cursor.execute(f'SELECT dir FROM Apps WHERE apps LIKE ?', [out]).fetchall():
                Ostium(*outA)
        elif out in books:
            for outB in cursor.execute(f'SELECT dir FROM Livros WHERE livros LIKE ?', [out]).fetchall():
                Ostium(*outB)
    except Exception as e:
        print(f'Erro de output! - {e}')
        continue
# Search system (working)
    #elif out.startswith('search '): Ostium('https://google.com/' + out[7:], 1)

#Ending
connector.commit()
cursor.close(), connector.close()
sys.exit()


