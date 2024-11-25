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

# Inicialização de dados do banco
saldo_inicial = 0.0
limite_saque = 500
limite_saques_diarios = 3
contas = {}  # Armazena dados das contas no formato CPF -> {dados da conta}
lista_contas = []  # Lista para exibir informações das contas
usuario_logado = None  # Controla o login do usuário

# Função para exibir mensagem de erro caso o CPF não esteja cadastrado
def mensagem_erro_cpf():
    print("Erro! Conta não encontrada.")

# Função para bloquear usuário após tentativas falhas
def bloquear_usuario(cpf):
    contas[cpf]['bloqueado'] = True
    print("Número de tentativas excedido. Usuário bloqueado.")

# Função para exibir o extrato do usuário
def exibir_extrato(cpf):
    conta = contas[cpf]
    print("\n================ EXTRATO ================")
    print("Não houve movimentações." if not conta['extrato'] else conta['extrato'])
    print(f"\nSaldo: R$ {conta['saldo']:.2f}")
    print("==========================================")

# Função para consultar saldo do usuário
def consultar_saldo(cpf):
    conta = contas[cpf]
    print("\n================ CONSULTA ================")
    print(f"Saldo consultado: R$ {conta['saldo']:.2f}")
    print("==========================================")

# Função para exibir a lista de contas cadastradas
def exibir_lista_contas():
    if not lista_contas:
        print("Ainda não há contas criadas.")
    else:
        print("\n================ LISTA DE CONTAS ================")
        for conta in lista_contas:
            print(f"Nome: {conta['nome']}, Endereço: {conta['endereco']}, CPF: {conta['cpf']}")
        print("==========================================")

# Função para recuperação de conta
def recuperar_usuario():
    nome = input("Informe seu nome: ")
    endereco = input("Informe seu endereço: ")
    cpf = input("Informe seu CPF: ")

    # Verifica se os dados fornecidos correspondem a uma conta
    for conta in contas.values():
        if conta['nome'] == nome and conta['endereco'] == endereco and conta['cpf'] == cpf:
            nova_senha = input("Informe uma nova senha para sua conta: ")
            conta['senha'] = nova_senha
            conta['tentativas_erradas'] = 0  # Reseta o contador de tentativas erradas
            conta['bloqueado'] = False  # Desbloqueia a conta
            print("Usuário recuperado com sucesso! Agora você pode acessar sua conta com a nova senha.")
            return
    print("Erro! Não foi encontrada nenhuma conta com os dados informados.")

# Função de login
def login():
    global usuario_logado
    cpf = input("Informe seu CPF: ")
    
    if cpf not in contas:
        mensagem_erro_cpf()
        return
    
    conta = contas[cpf]
    
    if conta['bloqueado']:
        print("Erro! Usuário bloqueado devido a múltiplas tentativas erradas.")
        return
    
    senha = input("Informe sua senha: ")

    if conta['senha'] != senha:
        conta['tentativas_erradas'] += 1
        if conta['tentativas_erradas'] >= 3:
            bloquear_usuario(cpf)
        else:
            print("Senha incorreta.")
    else:
        usuario_logado = cpf  # Marca o usuário como logado
        conta['tentativas_erradas'] = 0  # Reseta as tentativas erradas
        print(f"Bem-vindo, {conta['nome']}!")

# Função para verificar se o usuário está logado
def verificar_login():
    if usuario_logado:
        return True
    print("Erro! Você precisa fazer login primeiro.")
    return False

# Função para criar uma conta bancária
def criar_conta():
    nome = input("Informe seu nome: ")
    endereco = input("Informe seu endereço: ")
    cpf = input("Informe seu CPF: ")

    # Verifica se o CPF já está cadastrado
    if cpf in contas:
        print("Erro! CPF já cadastrado.")
        return

    senha = input("Informe sua senha: ")
    contas[cpf] = {'nome': nome, 'endereco': endereco, 'cpf': cpf, 'senha': senha, 'saldo': saldo_inicial, 'extrato': "", 'numero_saques': 0, 'bloqueado': False, 'tentativas_erradas': 0}
    lista_contas.append({'nome': nome, 'endereco': endereco, 'cpf': cpf})
    print("Conta cadastrada com sucesso!")

# Função principal que mantém o menu e o fluxo
def executar_programa():
    global usuario_logado

    while True:
        if usuario_logado:
            opcao = input(submenu_bancario)
        else:
            opcao = input(menu_principal)

        if opcao == "1":
            if not usuario_logado:
                criar_conta()
            else:
                valor = float(input("Informe o valor do depósito: "))
                if valor > 0:
                    conta = contas[usuario_logado]
                    conta['saldo'] += valor
                    conta['extrato'] += f"Depósito: R$ {valor:.2f}\n"
                else:
                    print("Operação falhou! O valor informado é inválido.")

        elif opcao == "2":
            if not usuario_logado:
                login()
            else:
                valor = float(input("Informe o valor do saque: "))
                conta = contas[usuario_logado]
                if valor > conta['saldo']:
                    print("Operação falhou! Você não tem saldo suficiente.")
                elif valor > limite_saque:
                    print("Operação falhou! O valor do saque excede o limite.")
                elif conta['numero_saques'] >= limite_saques_diarios:
                    print("Operação falhou! Número máximo de saques excedido.")
                elif valor > 0:
                    conta['saldo'] -= valor
                    conta['extrato'] += f"Saque: R$ {valor:.2f}\n"
                    conta['numero_saques'] += 1
                else:
                    print("Operação falhou! O valor informado é inválido.")

        elif opcao == "3":
            if verificar_login():
                exibir_extrato(usuario_logado)

        elif opcao == "4":
            if verificar_login():
                consultar_saldo(usuario_logado)

        elif opcao == "5":
            if usuario_logado:
                print("Saindo... Até logo!")
                usuario_logado = None  # Limpa o estado de login
            else:
                print("Erro! Você precisa fazer login primeiro.")

        elif opcao == "6":
            exibir_lista_contas()

        elif opcao == "7":
            recuperar_usuario()

        elif opcao == "8":
            print("Saindo... Até logo!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Chamada para executar o programa
executar_programa()
