# 🏦 Modelando o Sistema Bancário em POO com Python

Projeto desenvolvido como desafio prático do **Bootcamp Suzano Python Developer** na plataforma [DIO](https://web.dio.me), dentro do módulo de Programação Orientada a Objetos com Python.

Esta é a **terceira versão** do Sistema Bancário. As versões anteriores foram desenvolvidas com código procedural e depois com funções. Aqui, toda a lógica é reorganizada em **classes e objetos**, aplicando os pilares da POO: **abstração**, **encapsulamento**, **herança** e **polimorfismo**.

---

## Curso

- **Curso:** "Modelando o Sistema Bancário em POO com Python"
- **Instrutor:** Guilherme Arthur de Carvalho (Analista de Sistemas)
  - [LinkedIn](https://www.linkedin.com/in/decarvalhogui/)
- **Repositório de estudos geral:** [Bootcamp Suzano Python Developer](https://github.com/ahaerdy/DIO-learning/tree/main/Suzano%20-%20Python%20Developer)

---

## Objetivo

Refatorar o sistema bancário [anterior](https://github.com/ahaerdy/DIO-projeto-sistema-bancario-com-funcoes-python), substituindo variáveis soltas e dicionários por uma **modelagem completa com classes e objetos**. O desafio é dividido em duas partes:

- **Parte 1** (`desafio-parte_1.py`): Modelagem das classes do domínio do sistema — clientes, contas, transações e histórico.
- **Parte 2** (`desafio_parte_2.py`): Integração das classes ao menu interativo, conectando a interface com o usuário à lógica encapsulada nos objetos.

---

## Funcionalidades

| Opção | Operação | Descrição |
|-------|----------|-----------|
| `d` | Depositar | Registra um depósito na conta do cliente |
| `s` | Sacar | Realiza saque com validações de limite e saldo |
| `e` | Extrato | Exibe histórico de transações e saldo atual |
| `nu` | Novo usuário | Cadastra um cliente pelo CPF |
| `nc` | Nova conta | Vincula uma conta corrente a um cliente |
| `lc` | Listar contas | Exibe todas as contas criadas |
| `q` | Sair | Encerra o programa |

---

## Como o Projeto Foi Desenvolvido

### Da estrutura procedural à orientação a objetos

Nas versões anteriores, o estado do sistema (saldo, extrato, número de saques) era mantido em variáveis simples dentro de um loop. Com POO, esse estado passa a viver **dentro dos objetos**, que também carregam os comportamentos associados. Cada entidade do mundo real — cliente, conta, transação — vira uma classe com responsabilidades bem definidas.

---

## Parte 1 — Modelagem das Classes

### 1. Classes `Cliente` e `PessoaFisica` — hierarquia de clientes

```python
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
```

**Como funciona:**

`Cliente` é a classe base que representa qualquer tipo de cliente do banco. Ela armazena o endereço e uma lista de contas vinculadas ao cliente, além de definir dois comportamentos: realizar uma transação e adicionar uma conta.

`PessoaFisica` **herda** de `Cliente` via `super().__init__(endereco)`, reaproveitando toda a inicialização da classe pai e acrescentando os atributos específicos de uma pessoa física: nome, CPF e data de nascimento.

Essa separação prepara o sistema para evoluções futuras — como adicionar `PessoaJuridica` — sem alterar o código existente.

O método `realizar_transacao` delega a execução ao próprio objeto de transação:

```python
def realizar_transacao(self, conta, transacao):
    transacao.registrar(conta)
```

Isso é **polimorfismo**: o cliente não precisa saber se a transação é um saque ou um depósito — ele apenas chama `registrar()`, e cada tipo de transação sabe o que fazer.

---

### 2. Classes `Conta` e `ContaCorrente` — hierarquia de contas

```python
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    # ... demais propriedades

    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
```

**Como funciona:**

Os atributos prefixados com `_` (como `_saldo`, `_numero`) seguem a convenção Python de **encapsulamento**: indicam que são de uso interno da classe e não devem ser acessados diretamente de fora. O acesso externo é feito exclusivamente via **properties** (`@property`), que funcionam como getters somente-leitura:

```python
@property
def saldo(self):
    return self._saldo
```

O método de classe `nova_conta` é um **factory method**: uma forma alternativa de construir objetos sem chamar `__init__` diretamente. Ele usa `cls` (referência à própria classe) para criar instâncias, o que permite que subclasses o reutilizem corretamente.

Os métodos `sacar` e `depositar` retornam `True` ou `False` para indicar se a operação foi bem-sucedida — isso permite que quem chamou o método tome decisões com base no resultado.

---

```python
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [t for t in self.historico.transacoes if t["tipo"] == Saque.__name__]
        )
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
```

**Como funciona:**

`ContaCorrente` **especializa** `Conta` adicionando dois novos atributos: limite por saque (padrão R$ 500,00) e limite de saques diários (padrão 3). Ela **sobrescreve** o método `sacar` para incluir essas validações extras antes de chamar o comportamento original via `super().sacar(valor)`.

O número de saques já realizados é calculado em tempo real consultando o histórico — sem precisar de um contador separado:

```python
numero_saques = len(
    [t for t in self.historico.transacoes if t["tipo"] == Saque.__name__]
)
```

O método `__str__` define como o objeto deve ser representado como texto, permitindo que `print(conta)` exiba os dados formatados corretamente — sem necessidade de código extra em quem chama.

---

### 3. Classe `Historico` — registro de transações

```python
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )
```

**Como funciona:**

Cada `Conta` possui seu próprio objeto `Historico`, criado automaticamente no `__init__` da classe `Conta`. Toda transação bem-sucedida é registrada aqui como um dicionário com três campos: tipo, valor e data/hora.

O tipo é obtido via `transacao.__class__.__name__` — que retorna o nome da classe da instância como string (`"Saque"` ou `"Deposito"`). Isso evita hardcode de strings e garante que o registro reflita sempre o tipo real do objeto.

---

### 4. Classe abstrata `Transacao` e suas implementações

```python
from abc import ABC, abstractclassmethod, abstractproperty

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
```

**Como funciona:**

`Transacao` é uma **classe abstrata** (herda de `ABC`). Ela define um contrato: qualquer classe que a herde **obrigatoriamente** deve implementar `valor` e `registrar`. Tentar instanciar `Transacao` diretamente gera erro — ela existe apenas para ser especializada.

`Saque` e `Deposito` cumprem esse contrato. O método `registrar` em cada uma delas chama o método correspondente na conta (`sacar` ou `depositar`) e, somente se a operação foi bem-sucedida (retornou `True`), adiciona a transação ao histórico:

```python
def registrar(self, conta):
    sucesso_transacao = conta.sacar(self.valor)
    if sucesso_transacao:
        conta.historico.adicionar_transacao(self)
```

Esse design garante que **nunca haja um registro no histórico de uma operação que falhou**.

---

## Parte 2 — Integrando as Classes ao Menu

### 5. Funções auxiliares de busca

```python
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return
    return cliente.contas[0]
```

**Como funciona:**

`filtrar_cliente` usa **list comprehension** para varrer a lista de clientes e encontrar aquele cujo CPF coincide, retornando o objeto `PessoaFisica` ou `None`. Esse padrão é reutilizado por praticamente todas as operações do menu como primeira etapa de validação.

`recuperar_conta_cliente` retorna a primeira conta do cliente. O comentário `# FIXME` presente no código original é uma anotação honesta do instrutor indicando uma limitação conhecida da versão atual — em versões futuras, o cliente poderia escolher entre suas contas.

---

### 6. Funções de operação — depósito e saque

```python
def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)
```

**Como funciona:**

Cada operação segue o mesmo fluxo em três etapas: localizar o cliente pelo CPF, recuperar sua conta, e então criar um objeto de transação e delegá-lo ao cliente. Nenhuma validação de valor ou de saldo acontece aqui — isso é responsabilidade das classes `Deposito`, `Conta` e `ContaCorrente`. A função apenas **orquestra** os objetos.

```python
transacao = Deposito(valor)          # cria o objeto de transação
cliente.realizar_transacao(conta, transacao)  # delega a execução
```

Internamente, `realizar_transacao` chama `transacao.registrar(conta)`, que por sua vez chama `conta.depositar(valor)`. Toda a lógica de negócio está encapsulada nas classes — a função do menu apenas conecta as peças.

A função `sacar` segue exatamente o mesmo padrão, criando um objeto `Saque` no lugar de `Deposito`.

---

### 7. Função `exibir_extrato`

```python
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
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
```

**Como funciona:**

O extrato é gerado percorrendo a lista `conta.historico.transacoes` — uma lista de dicionários, onde cada item contém `tipo`, `valor` e `data`. O acesso ao saldo é feito via `conta.saldo`, que aciona a `@property` definida em `Conta` e retorna `self._saldo` de forma controlada.

---

### 8. Funções `criar_cliente` e `criar_conta`

```python
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\n=== Conta criada com sucesso! ===")
```

**Como funciona:**

Em `criar_cliente`, a verificação de CPF duplicado é feita antes de coletar qualquer dado do usuário — economizando interações desnecessárias. O objeto `PessoaFisica` é criado com argumentos nomeados para maior clareza e adicionado à lista `clientes`.

Em `criar_conta`, o método de classe `ContaCorrente.nova_conta(cliente, numero)` é utilizado para criar a instância — padrão factory method definido em `Conta`. A conta criada é adicionada tanto à lista global `contas` quanto à lista interna do próprio objeto `cliente.contas`, mantendo os dois registros sincronizados.

---

### 9. Função `main()` — ponto de entrada

```python
def main():
    clientes = []
    contas = []

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
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

main()
```

**Como funciona:**

`main()` mantém apenas duas listas — `clientes` e `contas` — e o loop de interação com o usuário. Todo o estado do sistema vive **dentro dos objetos**, não em variáveis soltas. A função apenas direciona cada opção do menu à função correspondente, que por sua vez acessa e manipula os objetos adequados.

---

## Como Executar

**Pré-requisito:** Python 3.10+ instalado.

```bash
# Clone o repositório
git clone https://github.com/ahaerdy/DIO-projeto-sistema-bancario-em-poo-com-python.git
cd DIO-projeto-sistema-bancario-em-poo-com-python

# Parte 1 — apenas a modelagem das classes (sem menu):
python desafio-parte_1.py

# Parte 2 — sistema completo e funcional:
python desafio_parte_2.py
```

---

## ✅ Regras de Negócio

- ✅ Cada cliente possui CPF único no sistema.
- ✅ Um cliente pode ter mais de uma conta corrente.
- ✅ Limite de **R$ 500,00** por operação de saque.
- ✅ Máximo de **3 saques** por sessão.
- ✅ Não é possível sacar mais do que o saldo disponível.
- ✅ Todas as operações bem-sucedidas são registradas no histórico da conta com tipo, valor e data/hora.
- ✅ Operações que falham **não são registradas** no histórico.

---

## Conceitos POO Aplicados

| Conceito | Onde é aplicado |
|----------|-----------------|
| **Abstração** | Classe `Transacao` (ABC) define o contrato sem implementação |
| **Encapsulamento** | Atributos `_saldo`, `_numero` etc. acessados via `@property` |
| **Herança** | `PessoaFisica` ← `Cliente` / `ContaCorrente` ← `Conta` / `Saque`, `Deposito` ← `Transacao` |
| **Polimorfismo** | `realizar_transacao` chama `registrar()` sem saber o tipo da transação |
| **Factory method** | `Conta.nova_conta(cls, cliente, numero)` |
| **`__str__`** | `ContaCorrente` define sua representação textual |
| **`super()`** | Reaproveitamento do `__init__` e do método `sacar` da classe pai |
| **List comprehension** | `filtrar_cliente`, contagem de saques em `ContaCorrente.sacar` |
| **`@property`** | Getters somente-leitura para atributos encapsulados |

---

## 📁 Arquivos do Projeto

| Arquivo | Descrição |
|---------|-----------|
| `desafio-parte_1.py` | Modelagem das classes (Parte 1 do desafio — sem menu) |
| `desafio_parte_2.py` | Sistema completo com menu integrado às classes (Parte 2) |
| `README.md` | Este arquivo |

---

## Certificado

Certificado de conclusão disponível em: [https://hermes.dio.me/certificates/EXCY5DYB.pdf](https://hermes.dio.me/certificates/EXCY5DYB.pdf)

---

Referências: 

- [Repositório de Estudos - Bootcamp Suzano Python Developer](https://github.com/ahaerdy/DIO-learning/tree/main/Suzano%20-%20Python%20Developer)
- [Repositório de Estudos – Bootcamp NTT DATA - Engenharia de Dados com Python](https://github.com/ahaerdy/DIO-learning/tree/main/NTT%20DATA-Engenharia%20de%20Dados%20com%20Python#-reposit%C3%B3rio-de-estudos--bootcamp-ntt-data-engenharia-de-dados-com-python)