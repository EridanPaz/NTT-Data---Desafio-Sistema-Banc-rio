from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Transacao(ABC):
	@property
	def valor(self):
		pass

	@abstractmethod
	def registrar(self, conta):
		pass
   

class Saque(Transacao):
	def __init__(self, valor):
		self.valor = valor

	@property
	def valor(self):
		return self._valor
	
	def registrar(self, conta):
		transacao_realizada_com_sucesso = conta.sacar(self.valor)

		if transacao_realizada_com_sucesso:
			conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
	def __init__(self, valor):
		self.valor = valor

	@property
	def valor(self):
		return self._valor
	
	def registrar(self, conta):
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
		self.numero 	= numero
		self.agencia 	= "0001"
		self.cliente  	= cliente
		self.historico = Historico()

	@classmethod
	def nova_conta(self, cliente, numero):
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
			saldo -+ valor
			print("\n*** Saque efetuado com sucesso. ***")
			return True

		
	def depositar(self, valor):
		if valor <= 0:
			print("\n*** O valor informado é inválido. Verifique. ***")
			return False
		
		self.saldo += valor
		print("\n*** Depósito efetuado com sucesso. ***")
		return True

	
class Conta_Corrente(Conta):
	def __init__(self, numero, agencia, cliente, historico, limite=700, limite_saque=5):
		super().__init__(numero, cliente)

		self.limite 		= limite
		self.limite_saque = limite_saque

	def sacar(self, valor):
		numero_saque = len([Transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

		excedeu_limite = valor > self.limite
		excedeu_saque  = numero_saque >= self.limite_saque

		if excedeu_limite:
			print("\n*** O valor informado excede o valor limite. ***")
			return False

		if excedeu_saque:
			print(f"\n*** Você já usou o limite de saques diário: {self.limite_saque}. ***")
			return False	

		return super().sacar(valor)			
	
	def __str__(self):
		return f"""\
			Agência:\t{self.agencia}
			C/C:\t\t{self.numero}
			Titulo:\t{self.cliente.nome}
		"""
		

class Cliente:
	def __init__(self, endereco):
		self.endereco = endereco
		self.contas   = []

	def realizar_transacao(self, conta, transacao):
		transacao.registrar(conta)

	def adicionar_conta(self, conta):
		self.contas.append(conta)

	@property
	def endereco(self):
		return self._endereco
	
	@property
	def contas(self):
		return self._contas


class Pessoa_Fisica(Cliente):
	def __init__(self, nome, cpf, data_nascimento, endereco):
		super().__init__(endereco)
		self.nome 				= nome
		self.cpf  				= cpf
		self.data_nascimento = data_nascimento

	def nome(self):
		return self._nome

	def cpf(self):
		return self._cpf

	def data_nascimento(self):
		return self._data_nascimento