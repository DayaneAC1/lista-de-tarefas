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
                   (id integer primary key, conteudo text, esta_concluida integer, 
                   email_usuario text, foreign key (email_usuario) references usuarios(email))''')
    
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

def login(formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    #Verificando se o e-mail existe no banco de dados
    cursor.execute('''SELECT COUNT(email) FROM usuarios WHERE email=?''',(formulario['email'],))
    conexao.commit()
    
    quantidade_de_emails = cursor.fetchone()
    print(quantidade_de_emails)
    
    #Se o e-mail não estiver cadastrado, retorna False
    
    if quantidade_de_emails[0] == 0:
        print("E-mail não cadastrado! Tente novamente")
        return False
    
    #Obtenha a senha criptografada do usuário no banco
    
    cursor.execute('''SELECT senha FROM usuarios WHERE email=?''', (formulario['email'],))
    conexao.commit()
    senha_criptografada = cursor.fetchone()
    
    #Verificando se a senha fornecida corresponde à senha armazenada
    return check_password_hash(senha_criptografada[0], formulario['senha'])

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


def marcar_tarefa_como_feita(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT esta_concluida FROM tarefas WHERE id=?''', (id,))
    esta_concluida = cursor.fetchone()
    esta_concluida = esta_concluida[0]
    
    if (esta_concluida):
        esta_concluida = False
    else:
        esta_concluida = True
    
    cursor.execute('''UPDATE tarefas SET esta_concluida = ? WHERE id=? ''', (esta_concluida,id))
    conexao.commit()
    return True
    
def excluir_tarefa(id, email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    #Verificar se o email que quer excluir a tarefa é realmente dono da tarefa
    cursor.execute('''SELECT email_usuario FROM tarefas WHERE id=?''', (id,))
    conexao.commit()
    email = cursor.fetchone()
    if(email[0] != email[0]):
        return False
    else:
        cursor.execute('''DELETE FROM tarefas WHERE id=?''', (id,))
        conexao.commit()
        return True
    
def excluir_usuario(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute('''DELETE FROM tarefas WHERE email_usuario=?''',(email,))
    cursor.execute('''DELETE FROM usuarios WHERE email=?''',(email,))
    conexao.commit()
    return True
    
    


    
            
        
        
        

if __name__ == '__main__':
    conectar_banco()
    criar_tabelas()
    

