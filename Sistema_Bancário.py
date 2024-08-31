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
LIMITE_SAQUES = 3

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

def atualizarExtrato(opcao, valor):
    global extrato
    global numero_saques

    if opcao == "d":
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

def imprimirExtrato():
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")
        
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

        transacoes(opcao, valor)
        atualizarExtrato(opcao, valor)

    elif opcao == "e":
        imprimirExtrato() 

    elif opcao == "q":
        sair()

    else:
        print("Opção inválida. Informe uma das opções do menu para efetuar transações ou sair.")        
      