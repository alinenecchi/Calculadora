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

def insertDataBudget( cpf, ad_name, start_date, end_date, max_share, max_clicks, max_view, daily_investment, total_investent):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orcamentos (cpf, ad_name, start_date, end_date, max_share, max_clicks, max_view, daily_investment, "
        "total_investent) VALUES ('" + cpf + "','" + ad_name + "','" + start_date + "','" + end_date + "','" + str(
        max_share) + "," + str(max_clicks) + ", " + str(max_view) + ", " + str(daily_investment) + ", " + str(total_investent) + ")")
    conn.commit()

def selectDataCpf(cpf):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, ad_name, start_date, end_date, max_share, max_clicks, max_view, daily_investment, total_investent "
        "FROM orcamentos where orcamentos.cpf = '" + cpf + "' ")
    linhas = cursor.fetchall()
    print('\n')
    print(f"O(s) orçamento(s) cadastrado(s) nesse CPF é(são):")
    for linha in linhas:
        print('\n\n')
        print(f"Nome do anuncio: {linha[1]}.")
        print(f'ID do anúncio: {linha[0]}.')
        print(f'Data de início do anúncio: {linha[2]} e a data de fim do anúncio é {linha[3]}.')
        print(f'O investimento por dia do anúncio foi de: R${linha[4]:.2f}, e o investimento total foi de: '
              f'R${linha[5]:.2f}!')
        print(f'O máximo de visualizações no final do período é de {linha[7]:.0f}, o máximo de cliques é: '
              f'{linha[8]:.0f}'
              f'e o máximo de compartilhamentos é: {linha[9]:.0f}.')
    print('\n Fim dos orçamentos! ')
    print('\n')

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
#insertClient("01111111111", "carol")
#configure_database()


