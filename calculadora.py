import sqlite3 
import os
import datetime as date 

conn = sqlite3.connect(':memory:')
conn = sqlite3.connect('anuncios')
# calculo de numeros de visualisações necessarias para 01 click
VIEW = 12 / 100 
# calculo de numeros de cliks necessarios para 01 compartilhamento
SHARE = 3 / 20 
# 30 pessoas visualizam o anúncio original (não compartilhado) a cada R$ 1,00 investido.
VIEW_investment = 30  
# o mesmo anúncio é compartilhado no máximo 4 vezes em sequência
MAX_share = 4 

#=======Função para criar tabela clientes e orçamentos no banco de dados anuncio============
def configure_database():
    try:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE clientes (cpf BIGINT(12) NOT NULL, name VARCHAR(50)NULL DEFAULT NULL, PRIMARY KEY("
                       "cpf))")
        cursor.execute("""CREATE TABLE orcamentos (ID INTEGER PRIMARY KEY AUTOINCREMENT,ad_name VARCHAR(50) NULL 
           DEFAULT NULL, start_date VARCHAR(11) NOT NULL, end_date VARCHAR(11) NOT NULL, daily_investment FLOAT(20) 
           NOT NULL, total_investent FLOAT(20) NOT NULL, cpf BIGINT(11) NOT NULL, max_view INT(20) NOT NULL, max_clicks 
           INT(20) NOT NULL, max_share INT(20) NOT NULL, FOREIGN KEY(cpf) REFERENCES clientes(cpf))""")
        conn.commit()
        main()
    except sqlite3.OperationalError:
        main()

#=======Função para inserir dados na tabela de clientes==============
def insertClient(value_cpf, value_name):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (cpf, name) VALUES (" + value_cpf + ",'" + value_name + "')")
    conn.commit()
#=======Função para inserir dados na tabela orçamento==============
def insertDataBudget( ad_name, start_date, end_date, daily_investment,  total_investent, cpf, max_view, max_clicks,  max_share):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orcamentos (ad_name, start_date, end_date, daily_investment,total_investent, cpf, max_view, max_clicks, max_share) VALUES  ('" + ad_name + "','" + start_date + "','" + end_date + "'," + str(daily_investment) + "," + str(total_investent) + ", " + cpf + ", " + str(max_view) + ", " + str(max_clicks) + ", " + str(max_share) + ")")
    conn.commit()
#=======Função para pesquisa por cpf==============
def selectDataCpf(cpf):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, ad_name, start_date, end_date, max_share, max_clicks, max_view, daily_investment, total_investent "
        "FROM orcamentos where orcamentos.cpf = '" + cpf + "' ")
    lines = cursor.fetchall()
    if not lines: 
        print ("Cliente ainda não cadastrado.")
        configure_database()   
    else: 
        print('\n')
        print(f"O(s) orçamento(s) cadastrado(s) nesse CPF é(são):")
        for line in lines:
            print('\n\n')
            print(f"Nome do anuncio: {line[1]}.")
            print(f'ID do anúncio: {line[0]}.')
            print(f'Data de início do anúncio: {line[2]} e a data de fim do anúncio é {line[3]}.')
            print(f'O investimento por dia do anúncio foi de: R${line[7]:.2f}, e o investimento total foi de: '
                f'R${line[8]:.2f}!')
            print(f'O máximo de visualizações no final do período é de {line[6]:.0f}, o máximo de cliques é: '
                f'{line[5]:.0f}'
                f' e o máximo de compartilhamentos é: {line[4]:.0f}.')
    print('\n Fim dos orçamentos! ')
    print('\n')
#=======Função para pesquisa por data==============
def selectDataDate(start_date, end_date):
    cursor = conn.cursor()
    cursor.execute("SELECT clientes.name, orcamentos.ID,orcamentos.cpf, orcamentos.ad_name, orcamentos.start_date, "
                   "orcamentos.end_date, orcamentos.daily_investment, orcamentos.total_investent, "
                   "orcamentos.max_share, orcamentos.max_clicks, orcamentos.max_view FROM orcamentos INNER JOIN "
                   "clientes ON clientes.cpf = orcamentos.cpf WHERE orcamentos.start_date = '" + start_date + "' "
                   "AND orcamentos.end_date = '" + end_date + "'")
    lines = cursor.fetchall()
    print(lines)
    print(f"\n O(s) orçamento(s) cadastrado(s)de {start_date} até {end_date} são:")
    for line in lines:
        print('\n')
        print(f'Nome do Cliente: {line[0]}.')
        print(f"Nome do anuncio: {line[1]}.")
        print(f'ID do anúncio: {line[3]}.')
        print(f'Data de início do anúncio: {line[4]} e a data de fim do anúncio é {line[5]}.')
        print(f'Investimento por dia do anúncio foi de: R${line[6]:.2f}.')
        print(f'Investimento total: R${line[7]:.2f} .')
        print(f'Máximo de visualizações: {line[10]:.0f}.')
        print(f'Máximo de cliques: {line[9]:.0f}.')
        print(f'Máximo de compartilhamentos: {line[8]:.0f}.')
    print('\n Fim dos orçamentos!\n')

def countView(data_input):
    quantity_clicks = data_input * VIEW
    quantity_share = quantity_clicks * SHARE
    quantity_view_share = quantity_share * 40
    return quantity_view_share

def max_view(data_input, max_share=MAX_share):
    if max_share == 0:
        return 0
    amount_view = data_input
    round_view = data_input

    for i in range(max_share):
        round_view = countView(round_view)
        amount_view += round_view
        if i > max_share:
            print('Error!')
            break
    return amount_view

def countClick(data_input):
    quantity_click = data_input * VIEW
    return quantity_click

def countShare(data_input):
    quantity_share = countClick(data_input) * SHARE
    return quantity_share

def countDays(start_date, end_date):
    date_start = date.datetime.strptime(start_date, '%d/%m/%Y')
    date_end = date.datetime.strptime(end_date, '%d/%m/%Y')
    
    if date_start == date_end:
        quantity_days = 1
    else:
        quantity_days = 1 + abs((date_end - date_start).days)
    return quantity_days

def inputCpf():
    cpf = str(input('Digite o cpf do cliente (apenas números): '))
    if len(cpf) != 11:
        print("Cpf tem que ter 11 digitos!") 
    return cpf

#=======Função para pesquisar anuncio -> opção de filtro por cpf ou data============
def searchBudget(option):
    if option == 1:
        os.system("cls")
        cpf = inputCpf() 
        selectDataCpf(cpf)
        main()

    if option == 2:
        os.system("cls")
        date_start = str(input('Digite a data de início da publicação [dd/mn/YYYY]: '))
        date_end = str(input('Digite a data de término da publicação [dd/mn/YYYY]: '))
        selectDataDate(date_start, date_end)
        main()

    if option == 0:
        conn.close()
        quit()

#===============Função para cadastrar novo anuncio==========
def toDoBudget(option):
    if option == 0:
        conn.close()
        quit()

    if option == 1:
        os.system("cls")
        cpf = inputCpf()
        name = str(input('Por favor, digite o nome do cliente: '))
        insertClient(cpf, name)
        print('Cadastro realizado com sucesso!')
        printAdMenu()
        answer = int(input('Resposta: '))
        if answer == 1:
            registerAd()
        if answer == 2:
            os.system("cls")
            main()
        if answer == 0:
            conn.close()
            quit()

    if option == 2:
        registerAd()

#========Função para registrar o anuncio========
def registerAd():
    os.system("cls")
    cpf = inputCpf()
    ad_name = str(input('Digite o nome do anuncio: '))
    daily_investment = float(input('Digite o valor do investimento diário: R$ '))
    start_date = str(input('Digite a data de íncio da publicação [dd/mn/YYYY]: '))
    end_date = str(input('Digite a data de término da publicação [dd/mn/YYYY]: '))
    view_investment = daily_investment * VIEW_investment
    total_investent = countDays(start_date, end_date) * daily_investment
    qnt_max_views = max_view(view_investment, MAX_share) * countDays(start_date, end_date)                                                                        
    qnt_max_clicks = countClick(view_investment) * countDays(start_date,end_date)
                                                                                         
    qnt_max_share = countShare(view_investment) * countDays(start_date, end_date)
    insertDataBudget(ad_name, start_date, end_date, daily_investment,total_investent, cpf, qnt_max_views, qnt_max_clicks,qnt_max_share)

    print('Orçamento realizado com sucesso!')
    print('\n')
    print(f'Nome do anúncio: {ad_name}. ')
    print(f'Valor investido por dia: R${daily_investment:.2f}. ')
    print(f'Esse valor, investido por {countDays(start_date, end_date)} dias, somou o total de '
    f'R${total_investent:.2f}. ')
    print(f'A data de início foi: {start_date} e o fim foi da publicação foi {end_date}. ')
    print(f'A somatória de visualizações foi de {qnt_max_views:.0f}, de clicks foi de: '
    f'{qnt_max_clicks:.0f} '
    f'e de compartilhamentos foi de {qnt_max_share:.0f}. ')
    print('\n\nFim do cadastro!\n')
    printResMenu()
    question = int(input('Resposta: '))
    if question == 1:
        os.system("cls")
        main()
    if question == 0:
        conn.close()
        quit()


#==============Menus================
def printOutMenu():
    print ("(1) Pesquisar por um orçamento")
    print ("(2) Fazer um orçamento")
    print ("(0) Encerrar programa")

def printAdMenu():
    print('Você deseja iniciar o cadastro do anúncio?')
    print ("(1) Sim")
    print ("(2) Voltar")
    print ("(0) Encerrar programa")

def printNoYesMenu():
    print ("(1) Sim")
    print ("(2) Não")

def printResMenu():
    print ("(1) Voltar para menu")
    print ("(2) Encerrar")

def mainMenu(option):
    if option == 1:
        os.system("cls")
        print('O que voce deseja?\n')
        print('Digite 1 para: Pesquisar por CPF do cliente')
        print('Digite 2 para: Pesquisar por data do anúncio')
        res = int(input('Resposta: '))
        searchBudget(res)

    if option == 2:
        os.system("cls")
        print('O que voce deseja?\n')
        print('(1) Cadastrar um novo cliente!')
        print('(2)Realizar um orçamento! (Apenas se o Cliente já foi cadastrado!)')
        res = int(input('Resposta: '))
        toDoBudget(res)

    if option == 0:
        conn.close()
        quit()

def main():
    print ("Seja bem vindo! Digite a opção desejada.")
    printOutMenu()
    res = int(input('Resposta: '))
    mainMenu(res)


#=======Chamada da função==============
configure_database()
#main()
#insertClient("00000000001", "ane")
#selectDataDate("20/10/2020", "20/11/2021")

