# Biblioteca para segurança no login
from werkzeug.security import generate_password_hash, check_password_hash
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
    
    quantidade_de_emails_cadastrados = cursor.fetchone()
    
    if(quantidade_de_emails_cadastrados[0] > 0):
        print("LOG: Já existe esse e-mail cadastrado no banco!")
        return False 
    
    cursor.execute('''INSERT INTO usuarios (email, nome, senha) 
                   VALUES (?, ?, ?)''', (formulario ['email'],
                    formulario['nome'], generate_password_hash (formulario['senha'],)))
    conexao.commit()
    return True

def verificar_usuario (formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT senha FROM usuarios WHERE email=?''',(formulario['email'],) )
    
    usuario = cursor.fetchone()
    
    if usuario is None:
        return False
        
    else:
        if check_password_hash(usuario[0], (formulario ["senha"])):
            return True
        else:
            return False
        
def criar_tarefa (conteudo):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO tarefas (conteudo, esta_concluida, email_usuario)
                   VALUES (?,?,?)''',(conteudo, False, "dayane@email.com"))
    conexao.commit()
    return True

def selecionar_tarefas ():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT id, conteudo, esta_concluida 
                   FROM tarefas WHERE email_usuario= ?''',('dayane@email.com',))
    
    tarefas = cursor.fetchall() # Busca todos os resultados do select e guarda em "tarefas"
    return tarefas


    
            
        
        
        

if __name__ == '__main__':
    conectar_banco()
    criar_tabelas()
    

