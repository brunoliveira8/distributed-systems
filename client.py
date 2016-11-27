# -*- coding: utf-8 -*-
import os
import Pyro4
import serpent


def main():
    storage = Pyro4.Proxy("PYRONAME:storage.proxy")
    running = True

    while running:
        commands = """
        Bem vindo!

        Digite a opção desejada:

        1 - Criar e enviar arquivo txt
        2 - Enviar arquivo pdf
        3 - Deletar arquivo
        4 - Ler arquivo
        5 - Listar arquivos
        6 - Sair
        """
        print(commands)

        opt = int(input("\tInput: "))

        if opt == 1:
            filename = input("\n\tDigite o nome do arquivo: ")
            file = input("\tDigite o conteudo do arquivo: ")
            storage.save(bytes(file, 'utf8'), filename)

            print("\n\tArquivo enviado. ")

        elif opt == 2:
            filename = input("\n\tDigite o nome do arquivo: ")
            with open(filename, 'rb') as f:
                data = f.read()
                storage.save(data, filename)

            print("\n\tArquivo enviando. ")

        elif opt == 3:
            filename = input("\n\tDigite o nome do arquivo: ")
            print("\n\tResposta: {}".format(storage.delete(filename)))

        elif opt == 4:
            filename = input("\tDigite o nome do arquivo: ")
            response = storage.retrieve(filename)

            if response['code'] == '200':
                with open(filename, 'wb') as f:
                    f.write(serpent.tobytes(response['content']))

                    print("\n\tO arquivo foi salvo.")

            else:
                print("\n\tO arquivo não existe.")

        elif opt == 5:
            arquivos = storage.list()['content']

            print('\n\tArquivos: ')

            for arquivo in arquivos:
                print('\t\t{}'.format(arquivo))

        elif opt == 6:
            running = False

        else:
            print("\tDigite uma opção válida")


if __name__ == '__main__':
    main()
