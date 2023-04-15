
import random

class GeradorCpf:
    def __init__(self):
        pass

    #Função para encontrar os dois ultimos digitos do CPF.
    def encontrando_digito(self, cut_cpf):
        MULT_CPF = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        if len(cut_cpf) == 9:
            MULT_CPF = MULT_CPF[1:10]

        mult = [x * y for x, y in zip(cut_cpf, MULT_CPF)]
        soma = sum(mult)
        digito = 11 - (soma % 11)
        if digito > 9:
            digito = 0
        return digito
    
    #Função para adicionar os caracteres especiais do CPF.
    def inserindo_caracteres(self, cpf):
        return f'{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}'

    #Função para gerar 9 números aleatórios de 1 a 9 e gerar o CPF.
    def geradora(self):
        randomico = [random.randint(1, 9) for x in range(9)]

        #encontrando o primeiro digito.
        primeiro_digito = self.encontrando_digito(randomico)
        randomico.append(primeiro_digito)

        #encontrando o segundo digito.
        segundo_digito = self.encontrando_digito(randomico)
        randomico.append(segundo_digito)

        #transformando a lista em string.
        cpf = "".join(map(str, randomico))
        
        #inserindo os caracteres especiais.
        cpf = self.inserindo_caracteres(cpf)

        return print(cpf)

app = GeradorCpf()
app.geradora()

