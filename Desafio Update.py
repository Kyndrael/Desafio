import json
import random

# Mensagem de boas-vindas
print("Olá! Bem-vindo ao Banco Central de Ether!")

# Menu principal
menu_principal = """
 [1] Criar Conta
 [2] Login
 [3] Lista de Contas
 [4] Recuperar Usuário
 [5] Sair
 => """

# Submenu de operações bancárias
submenu_bancario = """
 [1] Depositar
 [2] Sacar
 [3] Extrato
 [4] Consulta
 [5] Sair da Conta
 => """

# Função para carregar os dados do arquivo JSON
def carregar_contas():
    try:
        with open("contas_bancarias.json", "r") as f:
            dados = json.load(f)
            return dados["contas"], dados["lista_contas"]
    except FileNotFoundError:
        return {}, []

# Função para salvar os dados no arquivo JSON
def salvar_contas(contas, lista_contas):
    with open("contas_bancarias.json", "w") as f:
        dados = {"contas": contas, "lista_contas": lista_contas}
        json.dump(dados, f, indent=4)

class ContaBancaria:
    def __init__(self, nome, endereco, cpf, senha, agencia="0001"):
        self.nome = nome
        self.endereco = endereco
        self.cpf = cpf
        self.senha = senha
        self.saldo = 0.0
        self.extrato = ""
        self.numero_saques = 0
        self.bloqueado = False
        self.tentativas_erradas = 0
        self.agencia = agencia
        self.numero_conta = str(random.randint(100000, 999999))  # Número da conta gerado aleatoriamente

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Valor inválido para depósito.")

    def sacar(self, valor, limite_saque=500, limite_saques_diarios=3):
        if valor > self.saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif valor > limite_saque:
            print("Operação falhou! O valor do saque excede o limite.")
        elif self.numero_saques >= limite_saques_diarios:
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque: R$ {valor:.2f}\n"
            self.numero_saques += 1
        else:
            print("Operação falhou! O valor informado é inválido.")

    def consultar_saldo(self):
        print("\n================ CONSULTA ================")
        print(f"Saldo consultado: R$ {self.saldo:.2f}")
        print("==========================================")

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não houve movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("==========================================")

    def bloquear(self):
        self.bloqueado = True

class Banco:
    def __init__(self):
        self.contas = {}
        self.lista_contas = []
        self.usuario_logado = None
        self.agencia = "0001"

    def criar_conta(self):
        nome = input("Informe seu nome: ")
        endereco = input("Informe seu endereço: ")
        cpf = input("Informe seu CPF: ")

        if cpf in self.contas:
            print("Erro! CPF já cadastrado.")
            return

        senha = input("Informe sua senha: ")
        conta = ContaBancaria(nome, endereco, cpf, senha, self.agencia)
        self.contas[cpf] = conta
        self.lista_contas.append({'nome': nome, 'endereco': endereco, 'cpf': cpf, 'agencia': self.agencia, 'numero_conta': conta.numero_conta})
        salvar_contas(self.contas, self.lista_contas)  # Salva as contas no arquivo
        print("Conta cadastrada com sucesso!")

    def login(self):
        cpf = input("Informe seu CPF: ")

        if cpf not in self.contas:
            print("Erro! Conta não encontrada.")
            return

        conta = self.contas[cpf]

        if conta.bloqueado:
            print("Erro! Usuário bloqueado devido a múltiplas tentativas erradas.")
            return

        senha = input("Informe sua senha: ")

        if conta.senha != senha:
            conta.tentativas_erradas += 1
            if conta.tentativas_erradas >= 3:
                conta.bloquear()
                print("Número de tentativas excedido. Usuário bloqueado.")
            else:
                print("Senha incorreta.")
        else:
            self.usuario_logado = conta
            conta.tentativas_erradas = 0
            print(f"Bem-vindo, {conta.nome}!")

    def verificar_login(self):
        if self.usuario_logado:
            return True
        print("Erro! Você precisa fazer login primeiro.")
        return False

    def exibir_lista_contas(self):
        if not self.lista_contas:
            print("Ainda não há contas criadas.")
        else:
            print("\n================ LISTA DE CONTAS ================")
            for conta in self.lista_contas:
                print(f"Nome: {conta['nome']}, Endereço: {conta['endereco']}, CPF: {conta['cpf']}, Agência: {conta['agencia']}, Conta: {conta['numero_conta']}")
            print("==========================================")

    def recuperar_usuario(self):
        nome = input("Informe seu nome: ")
        endereco = input("Informe seu endereço: ")
        cpf = input("Informe seu CPF: ")

        for conta in self.contas.values():
            if conta.nome == nome and conta.endereco == endereco and conta.cpf == cpf:
                nova_senha = input("Informe uma nova senha para sua conta: ")
                conta.senha = nova_senha
                conta.tentativas_erradas = 0
                conta.bloquear = False
                salvar_contas(self.contas, self.lista_contas)
                print("Usuário recuperado com sucesso!")
                return
        print("Erro! Não foi encontrada nenhuma conta com os dados informados.")

    def executar_programa(self):
        while True:
            if self.usuario_logado:
                opcao = input(submenu_bancario)
            else:
                opcao = input(menu_principal)

            if opcao == "1":
                if not self.usuario_logado:
                    self.criar_conta()
                else:
                    valor = float(input("Informe o valor do depósito: "))
                    self.usuario_logado.depositar(valor)
                    salvar_contas(self.contas, self.lista_contas)

            elif opcao == "2":
                if not self.usuario_logado:
                    self.login()
                else:
                    valor = float(input("Informe o valor do saque: "))
                    self.usuario_logado.sacar(valor)
                    salvar_contas(self.contas, self.lista_contas)

            elif opcao == "3":
                if self.verificar_login():
                    self.usuario_logado.exibir_extrato()

            elif opcao == "4":
                if self.verificar_login():
                    self.usuario_logado.consultar_saldo()

            elif opcao == "5":
                if self.usuario_logado:
                    print("Saindo... Até logo!")
                    self.usuario_logado = None
                else:
                    print("Erro! Você precisa fazer login primeiro.")

            elif opcao == "6":
                self.exibir_lista_contas()

            elif opcao == "7":
                self.recuperar_usuario()

            elif opcao == "8":
                print("Saindo... Até logo!")
                break

            else:
                print("Operação inválida, por favor selecione novamente a operação desejada.")

# Executar o programa
banco = Banco()
banco.executar_programa()
