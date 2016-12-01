# Manual do Programa

O trabalho foi realizado utilizando a linguagem de programação [Python 3.5](https://www.python.org/) e a biblioteca [Pyro 4](https://pythonhosted.org/Pyro4/index.html).


## Biblioteca Pyro4

Esta biblioteca implementa o mecanismo **RMI** (Remote Method Invocation). Com isso, o sistema foi construído utilizando orientação a objeto e possui quatros classes: AbstractStorage, StorageProxy, StoragePrimary e StorageSecundary.

## Instalação

Para rodar o sistema você precisa ter instalado:
* [Python 3.5](https://www.python.org/downloads/) (já vem instalado em sistemas Ubuntu e OSX)
* [Pyro 4](https://pythonhosted.org/Pyro4/install.html#obtaining-and-installing-pyro) (pode ser instalador usando o pip, gerenciador de pacotes do Python)

## Como criar os servidores?

Toda a parte de gerência do sistema é feito através do script **manage.py**. Esse script fornece uma CLI onde você pode:

1. Inicializar o serviço. (Cria o proxy, a máquina primária e o servidor de DNS)
2. Adicionar uma cópia secundária.
3. Simular a falha e a recuperação de uma cópia.

## Como utilizar o cliente?

Através da CLI fornecida pelo script **client.py** você pode:

1. Criar e enviar arquivo no formato txt.
2. Enviar arquivo no formato PDF.
3. Deletar arquivos.
4. Ler arquivos.
5. Listar os arquivos.

