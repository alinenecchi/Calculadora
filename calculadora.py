import sqlite3 
import os

conn = sqlite3.connect(':memory:')
conn = sqlite3.connect('anuncios')

# calculo de numeros de visualisações necessarias para 01 click
VIEW = 12 / 100 
# calculo de numeros de cliks necessarios para 01 compartilhamento
CLICK = 3 / 20 
# 30 pessoas visualizam o anúncio original (não compartilhado) a cada R$ 1,00 investido.
VIEW_POR_INVESTIMENTO = 30  
# o mesmo anúncio é compartilhado no máximo 4 vezes em sequência
MAX_SHARE = 4 

def configure_database():
    """
    A função configurar_o_banco tem como objetivo verificar se as tabelas já existem no banco, caso não cria-las, caso
    sim, chamar a função main para dar incio no sistema!
    :return:
    """
    try:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE clientes (cpf BIGINT(12) NOT NULL, nome VARCHAR(50)NULL DEFAULT NULL, PRIMARY KEY("
                       "cpf))")
        cursor.execute("""CREATE TABLE orcamentos (ID INTEGER PRIMARY KEY AUTOINCREMENT,nome_anuncio VARCHAR(50) NULL 
           DEFAULT NULL, data_inicio VARCHAR(11) NOT NULL, data_fim VARCHAR(11) NOT NULL, invest_por_dia FLOAT(20) 
           NOT NULL, invest_total FLOAT(20) NOT NULL, cpf BIGINT(11) NOT NULL, max_view INT(20) NOT NULL, max_clic 
           INT(20) NOT NULL, max_share INT(20) NOT NULL, FOREIGN KEY(cpf) REFERENCES clientes(cpf))""")
        conn.commit()
        main()
    except sqlite3.OperationalError:
        main()


def insertClient(value_cpf, value_name):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (cpf, nome) VALUES (" + value_cpf + ",'" + value_name + "')")
    conn.commit()
    
def printOutMenu():
    print ("(1) Pesquisar por um orçamento")
    print ("(2) Fazer um orçamento")
    print ("(0) Encerrar programa")
    
def main():
    print ("Seja bem vindo! Dgite a opção desejada.")
    printOutMenu()
    #decisao1 = int(input('Resposta: '))
    #decisao_inicial(decisao1)


#main()
insertClient("01111111111", "carol")
#configure_database()

