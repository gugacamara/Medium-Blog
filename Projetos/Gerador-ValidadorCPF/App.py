import re
import random
import sys
from designQt import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication

#herda do QMainWindow e do meu arquivo de design Ui_MainWindow
class GeradorValidadorCpf(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        
        #Botôes
        #Seleciona o botão para gerar o CPF.
        self.btnGeraCPF.clicked.connect(self.geradora)
        #Seleciona o botão para validar o CPF.
        self.btnValidaCPF.clicked.connect(self.valida)
    
    #Removendo caracteres especiais com expressão regular.
    def remover_caracteres(self, cpf):
        return re.sub(r'[^0-9]', '', cpf)

    #Todas as sequencias de mesmo digito são validáveis, por isso verificar se é e eliminar
    def verificar_sequencia(self, cpf):
        sequencia = cpf[0] * len(cpf)
        if sequencia == cpf:
            return True
        else:
            return False

    #Criando os dois digitos finais do CPF.
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

    #Inserindo os caracteres especiais do CPF.
    def inserindo_caracteres(self, cpf):
        return f'{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}'

    #Gerando CPF.
    def geradora(self):
        #Números aleatórios de 1 a 9.
        randomico = [random.randint(1, 9) for x in range(9)]

        #Encontrando o primeiro digito
        primeiro_digito = self.encontrando_digito(randomico)
        randomico.append(primeiro_digito)

        #Encontrando o segundo digito
        segundo_digito = self.encontrando_digito(randomico)
        randomico.append(segundo_digito)

        cpf = "".join(map(str, randomico))
        cpf_string = self.inserindo_caracteres(cpf)
        
        self.inputGeraCPF.setText(cpf_string)
        
        return cpf_string

    #Validando CPF.
    def valida(self):
        #CPF do input do APP.
        cpf = self.inputValidaCPF.text()
        #cpfUser é o cpf digitado pelo usuario sem os caracteres especiais
        cpfUser = self.remover_caracteres(cpf)

        #Verificando se o cpf tem os 11 digitos minimos.
        if len(cpfUser) != 11:
            self.labelValidaCPF.setText(f'O CPF está incorreto!')
            return False

        #Verificando se o cpf tem sequencias de mesmo digito
        if self.verificar_sequencia(cpfUser):
            self.labelValidaCPF.setText(f'O CPF não pode ser uma sequência!')
            return False
        
        #cpf_teste é o cpf fatiado para ser calculado e gerado os dois valores finais
        cpf_teste = list(cpfUser[0:9])
        cpf_teste = [int(i) for i in cpf_teste]
        
        #Encontrando o primeiro digito
        primeiro_digito = self.encontrando_digito(cpf_teste)
        cpf_teste.append(primeiro_digito)

        #Encontrando o segundo digito
        segundo_digito = self.encontrando_digito(cpf_teste)
        cpf_teste.append(segundo_digito)

        #Transformando o cpf_teste em string para comparar com o cpfUser(string)
        cpf_teste_string = "".join(map(str, cpf_teste))

        #Quando for válido mostrar o cpf formatado corrigido, inválido mostra o que o usuário digitou
        if cpfUser == cpf_teste_string:
            cpf_formatado = self.inserindo_caracteres(cpf_teste_string)
            self.labelValidaCPF.setText(f'O CPF {cpf_formatado} é válido!')
        else:
            cpf_formatado = self.inserindo_caracteres(cpfUser)
            self.labelValidaCPF.setText(f'O CPF {cpf_formatado} é inválido!')

if __name__ == '__main__':
    Qt = QApplication(sys.argv)
    app = GeradorValidadorCpf()
    app.show()
    Qt.exec_()

