# -*- coding: utf-8 -*-
import os
import Pyro4

def main():
    storage = Pyro4.Proxy("PYRONAME:storage.proxy")
    running = True

    while running:
        commands = """
        Bem vindo!

        Digite a opção desejada:

        1 - Criar arquivo
        2 - Deletar arquivo
        3 - Ler arquivo
        4 - Listar arquivos
        5 - Sair
        6 - Enviar PDF
        """
        print(commands)

        opt = int(input("\tInput: "))

        if opt == 1:
            filename = input("\n\tDigite o nome do arquivo: ")
            file = input("\tDigite o conteudo do arquivo: ")
            storage.save(bytes(file, 'utf8'), filename)
            print("\tArquivo salvo. ")

        elif opt == 2:
            filename = input("\n\tDigite o nome do arquivo: ")
            print("\tResposta: {}".format(storage.delete(filename)))

        elif opt == 3:
            filename = input("\tDigite o nome do arquivo: ")
            print("\tResposta: {}".format(storage.retrieve(filename)))

        elif opt == 4:
            arquivos = storage.list()['content']

            print('\n\tArquivos: ')

            for arquivo in arquivos:
                print('\t\t{}'.format(arquivo))

        elif opt == 5:
            running = False

        elif opt == 6:
            with open('hello.pdf', 'rb') as f:
                data = f.read()
                storage.save(data, 'hello1.pdf')


        else:
            print("\tDigite uma opção válida")


if __name__ == '__main__':
    main()