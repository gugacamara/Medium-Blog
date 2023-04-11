from os import path, listdir, walk
import string
from sys import argv
from fpdf import FPDF
import getpass
from design import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
import platform


class Kindle(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        #inicializando a aplicação.
        self.init_App()

        #btn refresh.
        self.btnRefresh.clicked.connect(self.init_App)
        #item clicked listBooks.
        self.listBooks.clicked.connect(self.display_User)
        #btn create pdf.
        self.btnPdf.clicked.connect(self.pdf_User)
        #btn search.
        self.btnSearch.clicked.connect(self.search_String_User)

    #Inicializando a aplicação, buscando o arquivo My Clippings.txt do kindle.
    def init_App(self):
        so = platform.system()
        self.arquivo = None

        if so == 'Linux':
            self.arquivo = self.search_Cuts_Linux()
            if self.arquivo == None:
                self.inputText.setPlaceholderText('O seu arquivo de notas não foi encontrado! '
                'verifique se ele está na pasta documents do seu Kindle.')
            else:
                self.list_All_Cuts = self.all_N_And_H(self.arquivo)
                #clear and add items(atualize) to books in listBooks
                self.listBooks.clear()
                self.listBooks.addItems(self.all_Books(self.list_All_Cuts))
                #create .txt backup
                self.backup_Txt(self.listToString(self.list_All_Cuts)) 

        elif so == 'Windows':
            self.arquivo = self.search_Cuts_Windows()
            if self.arquivo == None:
                self.inputText.setPlaceholderText('O seu arquivo de notas não foi encontrado! '
                'verifique se ele está na pasta documents do seu Kindle.')
            else:
                self.list_All_Cuts = self.all_N_And_H(self.arquivo)
                #clear and add items(atualize) to books in listBooks
                self.listBooks.clear()
                self.listBooks.addItems(self.all_Books(self.list_All_Cuts))
                #create .txt backup
                self.backup_Txt(self.listToString(self.list_All_Cuts))

        else:
            self.inputText.setPlaceholderText('Sistema operacional não suportado! necessário Linux ou Windows.')

    #Buscando o arquivo My Clippings.txt do kindle no Linux.
    def search_Cuts_Linux(self):
        user = getpass.getuser()

        for discos in listdir(f'/media/{user}/'):
            disco = discos

            for pastas in listdir(f'/media/{user}/{disco}/'):
                pasta = pastas
                try:
                    if pasta == 'documents':
                        for arquivo in listdir(f'/media/{user}/{disco}/{pasta}/'):
                            if arquivo == 'My Clippings.txt':
                                cuts = (f'/media/{user}/{disco}/{pasta}/{arquivo}')
                                return cuts
                            
                except Exception as e:
                    print(f'Error: {e}, My Clippings não encontrado!')
                    return False

    #Buscando o arquivo My Clippings.txt do kindle no Windows.
    def search_Cuts_Windows(self):
        letras = string.ascii_uppercase
        #percorrendo todos os discos.
        for letra in letras:
            #verificando se o disco existe.
            if path.exists(f"{letra}:\\"):
                disco = listdir(f"{letra}:\\")
            else:
                continue
            #percorrendo todos os arquivos do disco.
            for dirs in disco:
                try:
                    #seto as pastas documents. 
                    if 'documents' in dirs:
                        #procuro por my clippings na pasta documents.
                        for raiz, _, arquivos in walk(f"{letra}:\\{dirs}", topdown=False):
                            if 'My Clippings.txt' in arquivos:
                                cuts = (f"{raiz}\\My Clippings.txt")  
                                return cuts

                except Exception as e:
                    print(f'Error: {e}, My Clippings não encontrado!')
                    return False

    #Todas as notas e highlights.       
    def all_N_And_H(self, arquivo):
        with open(arquivo, 'r', encoding='utf-8') as file:
            arquivo = file.readlines()
            #adicionando a lista temporaria na lista principal a cada '====='
            temporaria = []
            notes_and_highlights = []
            for i in arquivo:
                temporaria.append(i)
                if i == '==========\n' or i == '==========':
                    notes_and_highlights.append(temporaria)
                    temporaria = []
        return notes_and_highlights

    #Todos os titulos dos livros.
    def all_Books(self, lista):
        #separando os livros
        books = []
        #o 1 index é o nome do livro
        for i in lista:
            if i[0] not in books:
                books.append(i[0])
        return books

    #O livro e suas respectivas notas e highlights.
    def book_Your_N_H(self, name_click):
        lista = self.list_All_Cuts
        #separando os livros com suas notas
        books = []
        #o 1 index é o nome do livro
        for i in lista:
            #livros com suas notas
            if i[0] == name_click or i[0] == f'{name_click}\n':
                books.append(i)
        return books

    #Todas as notas(sem uso no APP).
    def all_Notes(self, lista):
        #separando as notas
        notes = []
        for i in lista:
            for note in i:
                #a nota está em i, nota é um elem de i
                if 'Sua nota' in note:
                    notes.append(i)                  
        return notes

    #Todos os highlights(sem uso no APP).
    def all_Highlights(self, lista):
        #separando os highlights
        highlights = []
        for i in lista:
            for highlight in i:
                #o highlight está em i, highlight é um elem de i
                if 'Seu destaque' in highlight:
                    highlights.append(i)
        return highlights

    #Converter a lista de notas para string.
    def listToString(self, lista):
        #De lista para string
        list_to_string = ' '.join([ str(elem) for i in lista for elem in i ])
        list_to_string = list_to_string.replace(r'==========', '\n')
        return list_to_string

    #Pesquisa por notas e highlights do usuario.
    def search_String(self, string):
        lista = self.list_All_Cuts
        # print(lista)
        # if lista == None:
        #     return self.inputText.setPlaceholderText('Nenhum arquivo selecionado!')
        string = string.lower()
        found = []
        for i in lista:
            for elem in i:
                #para seja minuscula como a string
                elem = elem.lower()
                if string in elem:
                    #i é a lista com a string procurada.
                    found.append(i)
        
        if found == []:
            return 'Not Found'

        texto = self.listToString(found)

        return texto

    #Gerando o pdf com as notas e highlights selecionadas.
    def pdf_Generator(self, texto):
        pdf = FPDF('P', 'mm', 'A4')
        pdf.set_font('Arial', size=12)
        pdf.add_page()
        #pdf.set_margins(20, 20, 20)
        texto = texto.encode('latin-1', 'ignore').decode('latin-1')
        pdf.multi_cell(w=0, h=7, txt=texto, border=0 ,align='L', fill=False)

        #nome do usuario logado
        user = getpass.getuser()
        #pelo pyqt5 eu deixo o usuario escolher o local e nome do arquivo
        try:
            caminho, _ = QFileDialog.getSaveFileName(
                self.centralwidget, 'Salvar PDF', f'C:/Users/{user}/Downloads/', 'PDF(*.pdf)',
                #options = QFileDialog.DontUseNativeDialog
                )
            #salvando o pdf
            if caminho != '':
                pdf.output(caminho)
        except:
            return None
    
    #Seta as notas e highlights do livro selecionado(clicado) pelo usuario.
    def display_User(self):
        item = self.listBooks.currentItem()
        name_book = str(item.text())
        cuts_book = self.book_Your_N_H(name_book)
        self.inputText.setText(self.listToString(cuts_book))

    #Botão para criar o pdf.
    def pdf_User(self):
        #create pdf clicked
        if self.inputText.toPlainText() != '':
            texto = self.inputText.toPlainText()
            self.pdf_Generator(texto)
        else:
            self.inputText.setPlaceholderText('Não há nada para criar um PDF.')
    
    #Botão para pesquisar as notas e highlights do usuario.
    def search_String_User(self):
        string = self.inputSearch.text()
        if string == '':
            self.inputText.clear()
            return self.inputText.setPlaceholderText('Digite algo para pesquisar.')

        #verificando se há algum livro para que possa ser pesquisado
        if self.listBooks.currentItem() == None:
            #verificar se o usuario atualizou a lista de livros e refazer a pesquisa
            if self.listBooks.count() > 0:
                self.listBooks.setCurrentRow(0)
                return self.search_String_User()
            else:
                return self.inputText.setPlaceholderText('Nenhum arquivo para pesquisa!')
        
        #desmarcando o Livro selecionado
        if self.listBooks.currentItem() != None:
            self.listBooks.currentItem().setSelected(False)

        item = self.search_String(string)
        if item == 'Not Found':
            self.inputText.clear()
            return self.inputText.setPlaceholderText('Não foi encontrado nada sobre sua pesquisa, verifique se digitou corretamente.')
        
        self.inputText.setText(item)
        self.inputSearch.clear()

    #Cria uma cópia do arquivo de notas e highlights do seu kindle.
    def backup_Txt(self, texto):
        with open('mycuts.txt', 'w', encoding='utf8') as file:
            file.write(texto)
            file.close()

if __name__ == '__main__':
    qt = QApplication(argv)
    kindle = Kindle()
    kindle.show()
    qt.exec_()

