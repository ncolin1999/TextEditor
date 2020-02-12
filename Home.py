import os
import shutil
import sys
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciLexerJava, QsciLexerHTML, QsciPrinter, QsciLexerCSharp, \
    QsciLexerBatch
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QTreeView, \
    QFileSystemModel, QWidget, QStyleFactory, QTabWidget, QAction, QInputDialog, QFileDialog, QDialog, QMenu, \
    QMessageBox, QLabel, QLineEdit, QPushButton, QCheckBox, QRadioButton, QFrame


class treeview(QTreeView):

    def mousePressEvent(self, QMouseEvent):
        self.clearSelection()
        super().mousePressEvent(QMouseEvent)


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.form_widget = FormWidget()
        self.setCentralWidget(self.form_widget)

        self.menubar = self.menuBar()
        self.toolbar = self.addToolBar("toolbar")

        self.file = self.menubar.addMenu("&File")
        self.edit = self.menubar.addMenu("&Edit")
        self.view = self.menubar.addMenu("&View")
        self.help = self.menubar.addMenu("&Help")

        self.helpOpen = QAction('Open')
        self.helpOpen.setShortcut('Ctrl+H')
        self.help.addAction(self.helpOpen)
        self.helpOpen.triggered.connect(lambda: os.startfile('help.pdf'))

        self.new = QAction(QIcon('newFile.png'), "New")
        self.new.setShortcut('Ctrl+N')
        self.open = QAction(QIcon('openFile.png'), "Open")
        self.open.setShortcut('Ctrl+O')
        self.save = QAction(QIcon('saveFile.png'), "Save")
        self.save.setShortcut('Ctrl+s')
        self.saveas = QAction(QIcon('saveasFile.png'), "Save As")

        self.print = QAction(QIcon('printFile.ico'), 'Print')
        self.print.setShortcut('Ctrl+P')
        self.exit = QAction('Exit')
        self.exit.setShortcut('Ctrl+Q')
        self.terminal = QAction(QIcon('terminal.png'), 'CMD')
        self.terminal.setShortcut('alt+r')

        self.file.addAction(self.new)
        self.file.addAction(self.open)
        self.file.addAction(self.save)
        self.file.addAction(self.saveas)
        self.file.addAction(self.print)
        self.file.addAction(self.exit)
        self.toolbar.addAction(self.new)
        self.toolbar.addAction(self.open)
        self.toolbar.addAction(self.save)
        self.toolbar.addAction(self.saveas)
        self.toolbar.addAction(self.print)
        self.toolbar.addAction(self.terminal)

        self.new.triggered.connect(self.newFile)
        self.open.triggered.connect(self.openFile)
        self.save.triggered.connect(self.saveFile)
        self.saveas.triggered.connect(self.saveasFile)
        self.print.triggered.connect(self.printFile)
        self.exit.triggered.connect(self.close)
        self.terminal.triggered.connect(self.Opencmd)

        self.undo = QAction('Undo')
        self.undo.setShortcut('Ctrl+Z')
        self.cut = QAction('Cut')
        self.cut.setShortcut('Ctrl+X')
        self.copy = QAction('Copy')
        self.copy.setShortcut('Ctrl+C')
        self.paste = QAction('Paste')
        self.paste.setShortcut('Ctrl+V')
        self.delete = QAction('Delete')
        self.delete.setShortcut('Delete')
        self.goto = QAction('Find')
        self.goto.setShortcut('Ctrl+F')
        self.find_and_replace = QAction('Replace')
        self.find_and_replace.setShortcut('Ctrl+R')

        self.edit.addAction(self.undo)
        self.edit.addAction(self.cut)
        self.edit.addAction(self.copy)
        self.edit.addAction(self.paste)
        self.edit.addAction(self.delete)
        self.edit.addAction(self.goto)
        self.edit.addAction(self.find_and_replace)

        self.undo.triggered.connect(self.undoText)
        self.cut.triggered.connect(self.cutText)
        self.copy.triggered.connect(self.copyText)
        self.paste.triggered.connect(self.pasteText)
        self.delete.triggered.connect(self.deleteText)
        self.goto.triggered.connect(self.findText)
        self.find_and_replace.triggered.connect(self.replaceText)

        self.Mtoolbar = QMenu('ToolBar')
        self.Mexplorer = QMenu("Explorer")
        self.Mnumbering = QMenu("Numbering")
        self.reset = QAction('Reset')

        self.reset.triggered.connect(self.resetWindow)

        self.view.addMenu(self.Mtoolbar)
        self.view.addMenu(self.Mexplorer)
        self.view.addMenu(self.Mnumbering)
        self.view.addAction(self.reset)

        self.thide = QAction("Hide")
        self.tshow = QAction("Show")

        self.ehide = QAction("Hide")
        self.eshow = QAction("Show")

        self.nhide = QAction("Hide")
        self.nshow = QAction("Show")

        self.Mtoolbar.addAction(self.thide)
        self.Mtoolbar.addAction(self.tshow)
        self.Mexplorer.addAction(self.ehide)
        self.Mexplorer.addAction(self.eshow)
        self.Mnumbering.addAction(self.nhide)
        self.Mnumbering.addAction(self.nshow)

        self.thide.triggered.connect(self.hide)
        self.tshow.triggered.connect(self.show)

        self.ehide.triggered.connect(self.hide)
        self.eshow.triggered.connect(self.show)

        self.nhide.triggered.connect(self.hide)
        self.nshow.triggered.connect(self.show)

        self.setWindowTitle("TextPad")
        self.setWindowIcon(QIcon('icon.png'))
        newEdit = QsciScintilla(self)
        newEdit.setFont(QFont('Times', 10))
        newEdit.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        newEdit.setAutoCompletionCaseSensitivity(False)
        newEdit.setAutoCompletionReplaceWord(False)
        newEdit.setAutoCompletionSource(QsciScintilla.AcsDocument)
        newEdit.setAutoCompletionThreshold(1)
        self.form_widget.tab.addTab(newEdit, QIcon('icon.png'), "Untitled")
        self.form_widget.tab.currentWidget().setFocus()
        self.showMaximized()
        self.show()

    def newFile(self):
        text, ok = QInputDialog.getText(self, 'New', 'Enter File name:')
        if ok:
            newEdit = QsciScintilla()
            newEdit.setMarginType(0, QsciScintilla.NumberMargin)
            newEdit.setMarginWidth(0, '00000000')
            newEdit.setBraceMatching(QsciScintilla.SloppyBraceMatch)
            newEdit.setAutoCompletionCaseSensitivity(False)
            newEdit.setAutoCompletionReplaceWord(False)
            newEdit.setAutoCompletionSource(QsciScintilla.AcsDocument)
            newEdit.setAutoCompletionThreshold(1)
            self.form_widget.checkExtensionToHighlight(text, newEdit)
            newEdit.setFont(QFont('Times', 10))
            self.form_widget.tab.insertTab(0, newEdit, QIcon('icon.png'), text)
            self.form_widget.tab.setCurrentIndex(0)

    def openFile(self):
        files = QFileDialog.getOpenFileNames(self, "Open", FormWidget.path)
        if files[0]:
            FormWidget.filepath = files[0]
            FormWidget.path = os.path.dirname(files[0][0])
            self.form_widget.tree.setRootIndex(self.form_widget.model.index(FormWidget.path))
            for i in files[0]:
                n = os.path.basename(i)
                for j in range(self.form_widget.tab.count()):
                    if n == self.form_widget.tab.tabText(j):
                        self.form_widget.tab.removeTab(j)
                        break
                newEdit = QsciScintilla()
                newEdit.setFont(QFont('Times', 10))
                newEdit.setMarginType(0, QsciScintilla.NumberMargin)
                newEdit.setMarginWidth(0, '00000000')
                self.form_widget.checkExtensionToHighlight(i, newEdit)
                try:
                    newEdit.setText(open(i).read())
                    newEdit.setBraceMatching(QsciScintilla.SloppyBraceMatch)
                    newEdit.setAutoCompletionCaseSensitivity(False)
                    newEdit.setAutoCompletionReplaceWord(False)
                    newEdit.setAutoCompletionSource(QsciScintilla.AcsDocument)
                    newEdit.setAutoCompletionThreshold(1)
                    self.form_widget.tab.insertTab(0, newEdit, QIcon('icon.png'), n)
                    self.form_widget.tab.setCurrentIndex(0)
                except:
                    QMessageBox.warning(self, 'Warning', 'Unsupported file type', QMessageBox.Ok)

    def saveFile(self):
        fname = self.form_widget.tab.tabText(self.form_widget.tab.currentIndex())
        lfname = [os.path.basename(n) for n in FormWidget.filepath]
        if fname not in lfname:
            file = QFileDialog.getSaveFileName(self, 'Save', FormWidget.path)
            if file[0]:
                p = open(file[0], 'w')
                p.write(self.form_widget.tab.currentWidget().text())
                p.close()
                FormWidget.filepath.append(file[0])
                # print(FormWidget.filepath)
                self.form_widget.tab.setTabText(self.form_widget.tab.currentIndex(), os.path.basename(file[0]))
                self.form_widget.checkExtensionToHighlight(file[0], self.form_widget.tab.currentWidget())
        else:
            for index in range(len(lfname)):
                if lfname[index] == fname:
                    p = open(FormWidget.filepath[index], 'w')
                    p.write(self.form_widget.tab.currentWidget().text())
                    p.close()
                    break

    def saveasFile(self):
        file = QFileDialog.getSaveFileName(self, 'Save As', FormWidget.path)
        if file[0]:
            p = open(file[0], 'w')
            p.write(self.form_widget.tab.currentWidget().text())
            p.close()
            self.form_widget.checkExtensionToHighlight(file[0], self.form_widget.tab.currentWidget())

    def printFile(self):
        printer = QsciPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QDialog.Accepted:
            printer.printRange(self.form_widget.tab.currentWidget())


    def Opencmd(self):
        os.chdir(FormWidget.path)
        os.startfile('cmd')

    def undoText(self):
        self.form_widget.tab.currentWidget().undo()

    def cutText(self):
        self.form_widget.tab.currentWidget().cut()

    def copyText(self):
        self.form_widget.tab.currentWidget().copy()

    def pasteText(self):
        self.form_widget.tab.currentWidget().paste()

    def deleteText(self):
        # self.form_widget.tab.currentWidget().textCursor().removeSelectedText()
        self.form_widget.tab.currentWidget().removeSelectedText()

    def findText(self):
        def Find():
            flag = None
            if r1.isChecked():
                self.form_widget.tab.currentWidget().findFirst(l.text(), True, cs.isChecked(), True, False, False)
                flag = self.form_widget.tab.currentWidget().findNext()
            elif r2.isChecked():
                flag = self.form_widget.tab.currentWidget().findFirst(l.text(), True, cs.isChecked(), True, False)
            if not flag:
                QMessageBox.information(self, 'TextPad', 'Match not found', QMessageBox.Ok, QMessageBox.Ok)

        d = QDialog(self)
        d.setWindowTitle('Find')
        d.setWindowIcon(QIcon('icon.png'))
        d.setFixedSize(300, 130)

        label = QLabel("What to find", d)
        label.move(10, 5)
        l = QLineEdit(d)
        l.move(100, 5)
        b1 = QPushButton("Find Next", d)
        b1.move(210, 5)
        b1.clicked.connect(Find)
        b2 = QPushButton("Cancel", d)
        b2.move(210, 35)
        b2.clicked.connect(d.close)
        cs = QCheckBox("Case sensitive", d)
        cs.move(10, 62)
        f = QFrame(d)
        f.setFixedSize(120, 40)
        f.move(120, 59)
        f.setToolTip('Direction')
        r1 = QRadioButton("Up", f)
        r1.move(5, 5)
        r2 = QRadioButton("Down", f)
        r2.setChecked(True)
        r2.move(55, 5)
        d.show()

    def replaceText(self):
        def Find():
            flag = self.form_widget.tab.currentWidget().findFirst(l1.text(), True, cs.isChecked(), True, False)
            if not flag:
                QMessageBox.information(self, 'TextPad', 'Match not found', QMessageBox.Ok, QMessageBox.Ok)

        def replace():
            self.form_widget.tab.currentWidget().replaceSelectedText(l2.text())

        def replaceall():
            flag = False
            try:
                text = self.form_widget.tab.currentWidget()
                while not flag:
                    flag = text.findFirst(l1.text(), True, cs.isChecked(), True, False)
                    if flag:
                        text.replaceSelectedText(l2.text())
                        flag = False
                    else:
                        flag = True
            except Exception as s:
                print(s)

        d = QDialog(self)
        d.setWindowTitle('Replace')
        d.setWindowIcon(QIcon('icon.png'))
        d.setFixedSize(300, 130)

        label1 = QLabel("What to find", d)
        label1.move(10, 5)
        label2 = QLabel('Replace with', d)
        label2.move(10, 35)
        l1 = QLineEdit(d)
        l1.move(100, 5)
        l2 = QLineEdit(d)
        l2.move(100, 35)
        b1 = QPushButton("Find Next", d)
        b1.move(210, 5)
        b1.clicked.connect(Find)
        b2 = QPushButton("Replace", d)
        b2.move(210, 35)
        b2.clicked.connect(replace)
        b3 = QPushButton("Replace All", d)
        b3.move(210, 65)
        b3.clicked.connect(replaceall)
        b4 = QPushButton("cancel", d)
        b4.move(210, 95)
        b4.clicked.connect(d.close)

        cs = QCheckBox("Case sensitive", d)
        cs.move(10, 62)
        d.show()

    def hide(self):
        if self.sender() == self.thide:
            self.toolbar.hide()
        elif self.sender() == self.ehide:
            self.form_widget.tree.hide()
        else:
            index = self.form_widget.tab.currentIndex()
            tab = self.form_widget.tab
            for i in range(tab.count()):
                tab.setCurrentIndex(i)
                tab.currentWidget().setMarginLineNumbers(0, False)
                tab.currentWidget().setMarginWidth(0, '0')
            self.form_widget.tab.setCurrentIndex(index)

    def show(self):
        if self.sender() == self.tshow:
            self.toolbar.show()
        elif self.sender() == self.eshow:
            self.form_widget.tree.show()
        else:
            index = self.form_widget.tab.currentIndex()
            tab = self.form_widget.tab
            for i in range(tab.count()):
                tab.setCurrentIndex(i)
                tab.currentWidget().setMarginLineNumbers(0, True)
                tab.currentWidget().setMarginWidth(0, '00000000')
            self.form_widget.tab.setCurrentIndex(index)

    def resetWindow(self):
        self.toolbar.show()
        self.form_widget.tree.show()
        self.show()


class FormWidget(QWidget):
    path = os.path.expanduser('~\\Documents')  # to the root directory for explorer
    filepath = []  # contain a list of full path of files
    fpath = ''  # contain full path of file which we have to move,copy in explorer
    operation = ''  # contain operation which we have to perform

    def __init__(self):
        super().__init__()
        self.tree = treeview() #created new classs inheriting QTreeView class at top  of page
        self.model = QFileSystemModel()
        # self.model.setNameFilters(['TextFile(*.txt *.java *.py)'])
        # self.model.setNameFilterDisables(False)
        self.model.setRootPath('')
        self.tree.setModel(self.model)
        # self.tree.setCurrentIndex(self.model.index(r'C:\Users\user\Dropbox\PycharmProjects'))
        self.tree.setRootIndex(self.model.index(FormWidget.path))
        self.tree.doubleClicked.connect(self.findPath)
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)
        # self.tree.header().hide()
        self.tree.setFixedWidth(200)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.contextmenu)

        self.tab = QTabWidget()
        self.tab.setTabShape(1)
        self.tab.setTabsClosable(True)
        self.tab.tabCloseRequested.connect(self.closeTab)
        self.tab.setMovable(True)

        hBox = QHBoxLayout()
        hBox.addWidget(self.tree)
        hBox.addWidget(self.tab)
        self.setLayout(hBox)

    def contextmenu(self, position):
        path = ''
        index = ''

        menu = QMenu()
        new = QMenu("New")
        newf = QAction("New File")
        newd = QAction("New Directory")
        new.addAction(newf)
        new.addAction(newd)
        cut = QAction("Cut")
        copy = QAction("Copy")
        paste = QAction("Paste")
        delete = QAction("Delete")
        rename = QAction("Rename")
        explorer = QAction("Explorer")
        menu.addMenu(new)
        menu.addAction(cut)
        menu.addAction(copy)
        menu.addAction(paste)
        menu.addAction(delete)
        menu.addAction(rename)
        menu.addAction(explorer)

        try:
            index = self.tree.selectedIndexes()[0]
            path = self.sender().model().filePath(index)
            if os.path.isfile(path):
                path = os.path.dirname(path)
        except:
            path = FormWidget.path
            if FormWidget.operation != 'cc' and FormWidget.operation != 'c':
                paste.setDisabled(True)
                cut.setDisabled(True)
                copy.setDisabled(True)
                delete.setDisabled(True)
                rename.setDisabled(True)
            else:
                cut.setDisabled(True)
                copy.setDisabled(True)
                delete.setDisabled(True)
                rename.setDisabled(True)


        action = menu.exec_(self.tree.mapToGlobal(position))

        if action == newf:
            text, ok = QInputDialog.getText(self, 'New File', 'Enter File name:')
            if ok:
                p = open(path + "/" + text, 'w')
                p.close()
        elif action == newd:
            text, ok = QInputDialog.getText(self, 'New Directory', 'Enter Directory name:')
            if ok:
                os.mkdir(path + "/" + text)
        elif action == delete:
            try:
                if self.model.isDir(index):
                   shutil.rmtree(path)
                else:
                    self.model.remove(index)
            except Exception as s:
                print(s)
        elif action == rename:
            text, ok = QInputDialog.getText(self, "Rename", "Enter new name:", text=os.path.basename(self.sender().model().filePath(index)))

            if ok:
                if self.model.isDir(index):
                    os.rename(path, os.path.dirname(path) + "/" + text)
                else:
                    os.rename(self.sender().model().filePath(index), path + '/' + text)
        elif action == cut:
            FormWidget.fpath = self.sender().model().filePath(index)
            FormWidget.operation = 'c'
        elif action == copy:
            FormWidget.fpath = self.sender().model().filePath(index)
            FormWidget.operation = 'cc'

        elif action == paste:
            if FormWidget.operation == 'c':
                shutil.move(FormWidget.fpath, path)

            elif FormWidget.operation == 'cc':
                if os.path.isfile(FormWidget.fpath):
                    shutil.copy(FormWidget.fpath, path)
                else:
                    shutil.copytree(FormWidget.fpath, path+"/"+os.path.basename(FormWidget.fpath))
            FormWidget.operation = ''
        elif action == explorer:
            os.startfile(FormWidget.path)

    def findPath(self, index):
        path = self.sender().model().filePath(index)

        if os.path.isfile(path):
            global name
            FormWidget.filepath.append(path)
            name = os.path.basename(path)
            for i in range(self.tab.count()):
                if name == self.tab.tabText(i):
                    self.tab.removeTab(i)
                    break

            newEdit = QsciScintilla()
            self.checkExtensionToHighlight(path, newEdit)
            newEdit.setFont(QFont('Times', 10))
            newEdit.setMarginType(0, QsciScintilla.NumberMargin)
            newEdit.setMarginWidth(0, '00000000')
            try:
               newEdit.setText(open(path).read())
               newEdit.setBraceMatching(QsciScintilla.SloppyBraceMatch)
               newEdit.setAutoCompletionCaseSensitivity(False)
               newEdit.setAutoCompletionReplaceWord(False)
               newEdit.setAutoCompletionSource(QsciScintilla.AcsDocument)
               newEdit.setAutoCompletionThreshold(1)
               self.tab.insertTab(0, newEdit, QIcon('icon.png'), os.path.basename(path))
               self.tab.setCurrentIndex(0)
            except:
                QMessageBox.warning(self, "Warning", "Unsupported file type", QMessageBox.Ok)

    def checkExtensionToHighlight(self, path, editor):
        _, extension = os.path.splitext(path)

        if extension == '.py':
            editor.setLexer(QsciLexerPython(self))
        elif extension == '.html':
            editor.setLexer(QsciLexerHTML(self))
        elif extension == '.java':
            editor.setLexer(QsciLexerJava(self))
        elif extension == '.cs':
            editor.setLexer(QsciLexerCSharp(self))
        elif extension == '.bat':
            editor.setLexer(QsciLexerBatch(self))

    def closeTab(self, index):
        if self.tab.count() != 1:
            self.tab.removeTab(index)
        else:
            QMessageBox.warning(self, 'warning', "You can not close the last tab", QMessageBox.Ok, QMessageBox.Ok)


app = QApplication(sys.argv)
r = App()
app.setStyle(QStyleFactory.create('fusion'))
sys.exit(app.exec_())
