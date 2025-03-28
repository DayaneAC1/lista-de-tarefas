import sqlite3

def conectar_banco():
    conexao = sqlite3.connect("tarefa.db")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''create table if not exists usuarios
                   (email text primary key,nome text,senha text)''')
    
    cursor.execute('''create table if not exists tarefas 
                   (id integer primary key, conteudo text, esta_concluida integer, email_usuario text, foreign key (email_usuario) references usuarios(email))''')
    
    conexao.commit()
    
def criar_usuario (formulario):
    # Verificar se o email já existe no Banco de Dados
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT COUNT (email) FROM usuarios WHERE email=?''',(formulario['email'],))
    conexao.commit()
    
    quantidade_de_emails_cadastrados = cursor.fetchone()
    +
    if(quantidade_de_emails_cadastrados[0] > 0):
        print("LOG: Já existe esse e-mail cadastrado no banco!")
        return False 
    
    cursor.execute('''INSERT INTO usuarios (email, nome, senha) VALUES (?, ?, ?)''', (formulario ['email'], formulario['nome'], formulario ['senha']))
    conexao.commit()
    return True

if __name__ == '__main__':
    conectar_banco()
    criar_tabelas()
    

