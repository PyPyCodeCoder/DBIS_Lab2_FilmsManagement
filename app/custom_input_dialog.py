from PyQt5.QtWidgets import QInputDialog, QLineEdit


class CustomInputDialog(QInputDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(400, 200)

    @staticmethod
    def getText(parent, title, label, mode=QLineEdit.Normal, text="", options=None, **kwargs):
        dialog = CustomInputDialog(parent)
        dialog.setWindowTitle(title)
        dialog.setLabelText(label)
        dialog.setTextValue(text)
        dialog.setTextEchoMode(mode)
        if options:
            dialog.setOptions(options)
        dialog.setInputMode(QInputDialog.TextInput)
        result = dialog.exec_()
        value = dialog.textValue()
        return value, result == QInputDialog.Accepted
    