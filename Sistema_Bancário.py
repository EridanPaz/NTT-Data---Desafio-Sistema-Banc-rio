from abc import ABC, abstractmethod, abstractclassmethod, abstractproperty
from datetime import datetime
import textwrap

class Transacao(ABC):
	@property
	@abstractproperty
	def valor(self):
		pass

	@abstractclassmethod
	#@classmethod
	def efetuar_transacao(self, conta):
		pass
   

class Saque(Transacao):
	def __init__(self, valor):
		self._valor = valor

	@property
	def valor(self):
		return self._valor
	
	def efetuar_transacao(self, conta):
		transacao_realizada_com_sucesso = conta.sacar(self.valor)

		if transacao_realizada_com_sucesso:
			conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
	def __init__(self, valor):
		self._valor = valor

	@property
	def valor(self):
		return self._valor
	
	def efetuar_transacao(self, conta):
		transacao_realizada_com_sucesso = conta.depositar(self.valor)

		if transacao_realizada_com_sucesso:
			conta.historico.adicionar_transacao(self)
		

class Historico:
	def __init__(self):
		self._transacoes = []
	
	@property
	def transacoes(self, transacao):
		return self._transacoes
	
	def adicionar_transacao(self, transacao):
		self._transacoes.append(
			{
				"tipo": transacao.__class__.__name__,
				"valor": transacao.valor,
				"data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")
			}
		)
	

class Conta:
	def __init__(self, numero, cliente):
		self._saldo     = 0
		self._numero 	 = numero
		self._agencia 	 = "0001"
		self._cliente   = cliente
		self._historico = Historico()

	@classmethod
	def nova_conta(cls, cliente, numero):
		return cls(numero, cliente)
	
	@property
	def saldo(self):
		return self._saldo
	
	@property
	def numero(self):
		return self._numero
	
	@property
	def agencia(self):
		return self._agencia
	
	@property
	def cliente(self):
		return self._cliente
	
	@property
	def historico(self):
		return self._historico
	
	def sacar(self, valor):
		if valor <= 0:			
			print("\n*** O valor informado é inválido. Verifique. ***")
			return False
		
		saldo 		  = self.saldo
		excedeu_saldo = valor > saldo
		
		if excedeu_saldo:
			print("\n*** Você não tem saldo suficiente para a operação. ***")
			return False
		else:
			self._saldo -+ valor
			print("\n=== Saque efetuado com sucesso. ===")
			return True
		
	def depositar(self, valor):
		if valor <= 0:
			print("\n*** O valor informado é inválido. Verifique. ***")
			return False
		
		self._saldo += valor
		print("\n=== Depósito efetuado com sucesso. ===")
		return True

	
class Conta_Corrente(Conta):
	def __init__(self, numero, cliente, limite=500, limite_saque=3):
		super().__init__(numero, cliente)

		self._limite 		 = limite
		self._limite_saque = limite_saque

	def sacar(self, valor):
		numero_saque  = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
		#numero_saque = len([transacao["tipo"] == Saque.__name__ for transacao in self.historico.transacoes])

		excedeu_limite = valor > self._limite
		excedeu_saque  = numero_saque >= self._limite_saque

		if excedeu_limite:
			print("\n*** O valor informado excede o valor limite. ***")

		elif excedeu_saque:
			print(f"\n*** Você já usou o limite de saques diário: {self.limite_saque}. ***")

		else:
			return super().sacar(valor) 	

		return False			
		
	def __str__(self):
		return f"""\
			Agência:\t{self.agencia}
			C/C:\t\t{self.numero}
			Titular:\t{self.cliente.nome}
		"""	
		

class Cliente:
	def __init__(self, endereco):
		self.endereco = endereco
		self.contas   = []

	def realizar_transacao(self, conta, transacao):
		transacao.efetuar_transacao(conta)

	def adicionar_conta(self, conta):
		self.contas.append(conta)

	# @property
	# def endereco(self):
	# 	return self._endereco
	
	# @property
	# def contas(self):
	# 	return self._contas


class Pessoa_Fisica(Cliente):
	def __init__(self, nome, cpf, endereco): #, data_nascimento, endereco):
		super().__init__(endereco)
		self.nome = nome
		self.cpf  = cpf
		#self.data_nascimento = data_nascimento	

	# def nome(self):
	# 	return self._nome

	# def cpf(self):
	# 	return self._cpf

	# def data_nascimento(self):
	# 	return self._data_nascimento


def filtrar_cliente(cpf, clientes):
	cliente_filtrado = [cliente for cliente in clientes if cliente.cpf == cpf]
	return cliente_filtrado[0] if cliente_filtrado else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n*** Cliente não possui conta! ***")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n*** Cliente não encontrado! ***")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n*** Cliente não encontrado! ***")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n*** Cliente não encontrado! ***")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf     = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n*** Já existe cliente com esse CPF! ***")
        return

    nome = input("Informe o nome completo: ")
    #data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = Pessoa_Fisica(nome=nome, cpf=cpf, endereco=endereco) #data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
	cpf 		= input("Informe o CPF do cliente: ")
	cliente = filtrar_cliente(cpf, clientes)

	if not cliente:
		print("\n*** Cliente não encontrado, fluxo de criação de conta encerrado! ***")
		return

	conta = Conta_Corrente.nova_conta(cliente=cliente, numero=numero_conta)
	contas.append(conta)

	cliente.contas.append(conta)
	print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

		
def menu():
	menu = """\n
	================ MENU ===============
	[d]\tDepositar
	[s]\tSacar
	[e]\tExtrato
	[nc]\tNova conta
	[ld]\tListar contas
	[nu]\tNovo usuário
	[q]\tSair
	=> """
	return input(textwrap.dedent(menu))		


def main():
    clientes = []
    contas   = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("\n*** Operação inválida, por favor selecione novamente a operação desejada. ***")


main()