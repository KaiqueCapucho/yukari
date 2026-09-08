import sys, ran_yakumo as ran, chen_yakumo as chen
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidgetItem, QListWidget, QMenu

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(Path(__file__).parent/"telas/yukari.ui", self)
        # Configuração das listas
        self.createList(self.listSites,"site",ran.getKeys("site"))
        self.createList(self.listApps,"app",ran.getKeys("app"))
        self.createList(self.listArchs,"archive",ran.getKeys("archive"))
        # Configuração dos ícones em vermelho (edtFilter, btnSearch)
        self.btnSearch.clicked.connect(lambda:self.btnOnClick(self.txtSearch.toPlainText()))  # Botão procurar
        self.edtFilter.textChanged.connect(self.filter) #

    def createList(self, listWidget, tipo, keys):
        addButton = QPushButton("+ Add")
        addButton.clicked.connect(lambda: self.openTelaAddEdit())
        addButton.setDefault(True) #Enter pressiona o botão

        item = QListWidgetItem()
        listWidget.addItem(item)
        listWidget.setItemWidget(item,  addButton)

        for key in keys:
            btn = QPushButton(key)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus) #Impossibilita que o botão seja focado
            btn.setDefault(True) #Enter pressiona o botão
            btn.clicked.connect(lambda checked=False, k=key: self.btnOnClick(k))
            # Adiciona os botões nas listas
            item = QListWidgetItem()
            listWidget.addItem(item)
            listWidget.setItemWidget(item, btn)
            # Configura um click c/botão direito do mouse p/abrir um menu de edição/remoção do PushButton
            btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            btn.customContextMenuRequested.connect(lambda pos, b=btn, i=item: self.showMenu(b, pos, i)) #pos dá a posição onde o menu é aberto

    def openTelaAddEdit(self, key=None):
        self.newWindow = chen.TelaAddEdit(key=key)
        self.newWindow.show()

    def btnOnClick(self, keys):
        for key in keys.strip().splitlines():
            if key.startswith('search'): ran.openDir([(key, 1, '')]) #formata o search p/padrão da função openDir
            else: ran.openDir(ran.getValue(key))
        self.close()

    def filter(self, txt:str):
        def filterList(list:QListWidget):
            for i in range(list.count()):
                item = list.item(i)
                button = list.itemWidget(item)
                if button: item.setHidden(txt.lower() not in button.text().lower())
        filterList(self.listSites), filterList(self.listApps), filterList(self.listArchs)

    def showMenu(self, botao, pos, item):
        menu = QMenu(self)
        editar = menu.addAction("Editar")
        remover = menu.addAction("Remover")
        acao = menu.exec(botao.mapToGlobal(pos))
        if acao == editar: self.openTelaAddEdit(botao.text())
        elif acao == remover:
            ran.deleteKey(botao.text())
            item.listWidget().takeItem(item.listWidget().row(item))

class MyListWidget(QListWidget):
    def keyPressEvent(self, event):     # Permite que o botão dentro da lista seja ativado c/Enter
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            item = self.currentItem()
            if item is not None:
                if (btn:=self.itemWidget(item)) is not None: btn.click()
            return
        super().keyPressEvent(event)
    def focusOutEvent(self, event):     #Remove a seleção do botão quando muda-se o foco (não está funcionando como deveria)

        self.clearSelection()
        super().focusOutEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    App().show()
    sys.exit(app.exec())