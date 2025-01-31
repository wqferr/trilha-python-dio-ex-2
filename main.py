from typing import Optional

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[u] Criar usuário
[c] Criar conta
[q] Sair

=> """

saldo = 0
LIMITE_PADRAO = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
AGENCIA = "0001"


def valida_cpf(cpf: str):
    if len(cpf) != 11:
        return False
    else:
        return cpf.isnumeric()


def encontra_usuario(lista_usuarios: list[dict], *, cpf: str):
    for usuario in lista_usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None


def novo_usuario(
    lista_usuarios: list[dict],
    *,
    nome: str,
    cpf: str,
    endereco: str,
) -> Optional[dict]:
    if not valida_cpf(cpf):
        print("CPF inválido.")
        return None

    usuario_com_cpf = encontra_usuario(lista_usuarios, cpf=cpf)
    if usuario_com_cpf is None:
        usuario = dict(nome=nome, cpf=cpf, endereco=endereco)
        lista_usuarios.append(usuario)
        return usuario
    else:
        print(f"Usuário com CPF duplicado: {cpf}.")
        return None


def nova_conta(lista_contas: list[dict], *, usuario: dict) -> Optional[dict]:
    if usuario is None:
        print("Uma conta precisa de um usuário vinculado.")
        return None
    else:
        conta = dict(agencia=AGENCIA, numero=len(lista_contas) + 1, usuario=usuario)
        lista_contas.append(conta)
        return conta


def saque(
    *,
    saldo,
    valor,
    extrato,
    limite,
    numero_saques,
    limite_saques,
) -> dict:
    if numero_saques >= limite_saques:
        print("Operação excederia limite de saques diários.")
    elif valor <= 0:
        print("Valor inválido: saque só suporta quantias positivas.")
    elif valor > limite:
        print("Operação excederia limite por saque.")
    elif valor > saldo:
        print("Saldo insuficiente.")
    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    return dict(saldo=saldo, extrato=extrato, numero_saques=numero_saques)


def deposito(saldo, valor, extrato, /) -> dict:
    if valor <= 0:
        print("Valor inválido: depósito só suporta quantias positivas.")
    else:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"

    return dict(saldo=saldo, extrato=extrato)


def exibe_extrato(saldo, /, *, extrato) -> None:
    if extrato:
        print(extrato)
    else:
        print("Extrato vazio.")
    print(f"\nSaldo: R$ {saldo:.2f}")


contas = []
usuarios = []

while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Valor do depósito: "))
        resultado = deposito(saldo, valor, extrato)
        saldo = resultado["saldo"]
        extrato = resultado["extrato"]

    elif opcao == "s":
        valor = float(input("Valor do saque: "))
        resultado = saque(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            limite=LIMITE_PADRAO,
            numero_saques=numero_saques,
        )
        saldo = resultado["saldo"]
        extrato = resultado["extrato"]
        numero_saques = resultado["numero_saques"]

    elif opcao == "e":
        exibe_extrato(saldo, extrato=extrato)

    elif opcao == "u":
        nome = input("Nome: ")
        cpf = input("CPF: ")
        endereco = input("Endereço: ")
        novo_usuario(usuarios, nome=nome, cpf=cpf, endereco=endereco)

    elif opcao == "c":
        cpf = input("CPF do usuário: ")
        usuario = encontra_usuario(usuarios, cpf=cpf)
        if usuario is None:
            print("Usuário não encontrado.")
        else:
            conta = nova_conta(contas, usuario=usuario)
            print(f"Conta número {conta['numero']} criada.")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
