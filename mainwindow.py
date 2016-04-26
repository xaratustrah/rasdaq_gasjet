"""
A client/server code for Raspberry Pi ADC input

Xaratustrah
2016

Modificated by HoSnoopy for the internal Gastarget in the ESR in GSI
2016



"""

from PyQt5.QtWidgets import QMainWindow, QDialog, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt, QCoreApplication, QThread, QTimer
from mainwindow_ui import Ui_MainWindow
from aboutdialog_ui import Ui_AbooutDialog
from zmq_listener import ZMQListener
from version import __version__


class mainWindow(QMainWindow, Ui_MainWindow):
    """
    The main class for the GUI window
    """

    def __init__(self):
        """
        The constructor and initiator.
        :return:
        """
        # initial setup
        super(mainWindow, self).__init__()
        self.setupUi(self)

        radius = 2.5e-5
        m = 4.002602/6.02214129e26
        X = 1.63
        Korr = 5.7
        Saug = 1320
        Label = 'Helium'

        self.gasart_label.setText(Label)

        text, ok = QInputDialog.getText(self, 'Settings', 'Enter the host address:', QLineEdit.Normal, '140.181.97.133')
        if ok:
            host = str(text)
        text, ok = QInputDialog.getText(self, 'Settings', 'Enter the port number:', QLineEdit.Normal, '10000')
        if ok:
            port = int(text)
        text, ok = QInputDialog.getText(self, 'Settings', 'Enter the topic number for Dump-Pressure:', QLineEdit.Normal, '10001')
        if ok:
            topic = str(text)
        text, ok = QInputDialog.getText(self, 'Settings', 'Enter the topic number for Temperature:', QLineEdit.Normal, '10004')
        if ok:
            topic2 = str(text)


        self.thread = QThread()
        self.zeromq_listener = ZMQListener(host, port, topic)
        self.zeromq_listener.moveToThread(self.thread)

        self.thread.started.connect(self.zeromq_listener.loop)


        # Connect signals
        self.connect_signals()

        QTimer.singleShot(0, self.thread.start)
        self.show_message('Connected to server: {}:{}'.format(host, port))

    def connect_signals(self):
        """
        Connects signals.
        :return:
        """

        # Action about and Action quit will be shown differently in OSX

        self.actionAbout.triggered.connect(self.show_about_dialog)
        self.actionQuit.triggered.connect(QCoreApplication.instance().quit)
        self.zeromq_listener.message.connect(self.signal_received)
        self.actionWasserstoff.triggered.connect(self.Wasserstoff)
        self.actionHelium.triggered.connect(self.Helium)
        self.actionNeon.triggered.connect(self.Neon)
        self.actionArgon.triggered.connect(self.Argon)
        self.actionKrypton.triggered.connect(self.Krypton)
        self.actionXenon.triggered.connect(self.Xenon)
        self.actionStickstoff.triggered.connect(self.Stickstoff)

    def signal_received(self, message):
        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.display(float(message))

    def closeEvent(self, event):
        self.zeromq_listener.running = False
        self.thread.quit()
        self.thread.wait()

    def show_message(self, message):
        """
        Implementation of an abstract method:
        Show text in status bar
        :param message:
        :return:
        """
        self.statusbar.showMessage(message)

    def Wasserstoff(self):
        m = 2.016/6.02214129e26
        X = 1.4054
        Korr = 2.4
        Saug = 1100
        Label = 'Wasserstoff'
        self.gasart_label.setText(Label)

    def Helium(self):
        m = 4.002602/6.02214129e26
        X = 1.63
        Korr = 5.7
        Saug = 1320
        Label = 'Helium'
        self.gasart_label.setText(Label)

    def Neon(self):
        m= 20.179/6.02214129e26
        X= 1.6669
        Korr = 3.8
        Saug = 1000
        Label = 'Neon'
        self.gasart_label.setText(Label)

    def Argon(self):
        m = 39.948/6.02214129e26
        X = 1.6696
        Korr = 0.8
        Saug = 1000
        Label = 'Argon'
        self.gasart_label.setText(Label)

    def Krypton(self):
        m = 83.798/6.02214129e26
        X =  1.6722
        Korr = 0.5
        Saug = 850
        Label = 'Krypton'
        self.gasart_label.setText(Label)

    def Xenon(self):
        m = 131.293/6.02214129e26
        X = 1.6773
        Korr = 0.4
        Saug = 850
        Label = 'Xenon'
        self.gasart_label.setText(Label)

    def Stickstoff(self):
        m = 28.0134/6.02214129e26
        X = 1.4013
        Korr = 1
        Saug = 1320
        Label = 'Stickstoff'
        self.gasart_label.setText(Label)


    def show_about_dialog(self):
        """
        Show about dialog
        :return:
        """
        about_dialog = QDialog()
        about_dialog.ui = Ui_AbooutDialog()
        about_dialog.ui.setupUi(about_dialog)
        about_dialog.ui.labelVersion.setText('Version: {}'.format(__version__))
        about_dialog.exec_()
        about_dialog.show()
