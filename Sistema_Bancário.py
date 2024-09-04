import datetime

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo         = 0
limiteDeSaque = 500
extrato       = ""
numero_saques = 0
LIMITE_SAQUES = 10
dataEHora     =  datetime.datetime.fromisoformat('0001-01-01')

def excedeuQtdeLimiteDeSaques(qtdeSaque):
    excedeu = qtdeSaque == LIMITE_SAQUES
    return excedeu

def excedeOValorLimiteDeSaque(valor):
    excedeuLimite = valor > limiteDeSaque

    return excedeuLimite

def excedeOValorDoSaldo(valor):
    excedeuLimite = valor > saldo

    return excedeuLimite

def transacoes(opcao, valor):
    global saldo
    if opcao == "d":
        saldo += valor
    else:
        saldo -= valor   

def atualizarExtrato(opcao, valor, data_E_Hora):    
    global extrato
    global numero_saques    
    global dataEHora 
    dataEHora = data_E_Hora
    
    texto = ""

    if opcao == "d":
        texto = "Depósito: R$ "
    else:
        texto = "Saque: R$ "

    dt = data_E_Hora.strftime("%d/%m/%Y %H:%M")        

    extrato += f"{texto} {valor:.2f}  {dt}\n"        
    
    if(data_E_Hora.date() != dataEHora.date()):
        numero_saques = 1
    else:
        numero_saques += 1

def imprimirExtrato():
    print("\n================= EXTRATO =================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Limite de transações por dia dia: {LIMITE_SAQUES}.")
    print(f"Quantidade de transações efetuados no dia: {numero_saques}.")
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("=============================================")
        
def sair():
    exit()

while True:

    opcao = input(menu)

    if (opcao == "d") or (opcao == "s"):
        valor = float(input("Informe o valor para a operação: "))

        if valor < 1:
            print("O valor deve ser maior que zero.")
            continue

        if (opcao == "s"):            
            if excedeuQtdeLimiteDeSaques(numero_saques):
                print("Você excedeu o limite de saques de hoje. O sistema foi fechado.")
                sair()
            if excedeOValorLimiteDeSaque(valor):
                print(f"O valor excede o valor limite para saque em  R$ {valor - limiteDeSaque}.")
                continue
            if excedeOValorDoSaldo(valor):
                print(f"O valor excede o limite do saldo em  R$ {valor - saldo}.")
                continue    

        print(dataEHora.date())
        transacoes(opcao, valor)
                
        dataEHoraAtual = datetime.datetime.today()
        print(dataEHoraAtual.date())

        atualizarExtrato(opcao, valor, dataEHoraAtual)

    elif opcao == "e":
        imprimirExtrato() 

    elif opcao == "q":
        sair()

    else:
        print("Opção inválida. Informe uma das opções do menu para efetuar transações ou sair.")        