import ran_yakumo as ran
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QLineEdit, QComboBox, QFormLayout, QGroupBox, QMessageBox

class TelaAddEdit(QWidget):
    def __init__(self, parent=None, key=None):
        super().__init__(parent)
        uic.loadUi(Path(__file__).parent/"telas/chen.ui", self)
        self.key, self.entries = key, []
        self.ids = ran.getIDs(key)
        if key:
            self.titulo.setText("Editar/Remover Dados")
            self.edtChave.setText(key)
            for value, param, type_ in ran.getValue(key): self.createEntries(value, param, type_)
        else: self.createEntries()

        self.btnCancela.clicked.connect(self.close)
        self.btnConfirma.clicked.connect(self.btnConfirmar)

    def createEntries(self, value="", param=None, type_=None):
        grupo = QGroupBox()
        layout = QFormLayout(grupo)

        valor = QLineEdit(value)
        valor.setPlaceholderText("Value")

        nota = QLineEdit(str(param or ""))
        nota.setPlaceholderText("Parameter")

        tipo = QComboBox()
        tipo.addItems(["site",  "archive","app"])
        tipo.setCurrentText(type_)

        for campo in (valor, nota, tipo): layout.addRow(campo)

        self.layoutCampos.addWidget(grupo)
        self.entries.append((valor, nota, tipo))

    def btnConfirmar(self):
        if not (key:= self.edtChave.text().strip()):
            QMessageBox.warning(self, "Aviso", "A Key não pode estar vazia.")
            return
        print('ok')
        for i, (valor, nota, tipo) in enumerate(self.entries):
            print('ok 2')
            try: param = int(nota.text())
            except ValueError:
                QMessageBox.warning(self, "Aviso", "Parameter deve ser um número.")
                return
            if self.key is None: ran.insertValue(key, valor.text(), tipo.currentText(), param)
            else: ran.updateValue(self.ids[i], key, valor.text(),tipo.currentText(),param)
        self.close()