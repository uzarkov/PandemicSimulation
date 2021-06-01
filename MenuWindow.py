from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QSizePolicy, QSlider, QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStackedLayout, QLabel
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtCore, QtGui
from SimulationWindow import SimulationWindow
from ParamPack import ParamPack


class MyWindow(QMainWindow):
    front_wid = None

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.setFixedSize(1109, 736)
        self.simulation_window = QWidget()
        self.setWindowTitle("Pandemic Simulation")

        # Central Widget
        self.central_widget = QWidget()
        self.layout_for_widgets = QStackedLayout()

        # Main widget
        self.main_widget = QWidget()
        self.main_widget.setStyleSheet(
            "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.73, fx:0.499, fy:0.5, stop:0 rgba(121, 167, 200, 255), stop:1 rgba(255, 255, 255, 255));")
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(23)
        font.setBold(True)
        font.setWeight(75)

        # title_label
        self.title_label = QLabel(self.main_widget)
        self.title_label.setGeometry(QtCore.QRect(340, 0, 441, 81))
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("background: transparent;")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)

        # logo_label
        self.logo_label = QLabel(self.main_widget)
        self.logo_label.setGeometry(QtCore.QRect(500, 80, 111, 91))
        self.logo_label.setStyleSheet("background: transparent;")
        self.logo_label.setText("")
        self.logo_label.setPixmap(QtGui.QPixmap("virus_logo.png"))

        # population widget
        self.population_widget = QWidget(self.main_widget)
        self.population_widget.setGeometry(QtCore.QRect(240, 190, 591, 61))
        self.population_widget.setStyleSheet("background: transparent;")

        self.horizontalLayout_6 = QHBoxLayout(self.population_widget)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)

        self.population_label = QLabel(self.population_widget)
        self.population_label.setMinimumSize(QtCore.QSize(250, 0))
        font.setPointSize(14)
        self.population_label.setFont(font)
        self.population_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.population_label.setStyleSheet("background: transparent;")
        self.population_label.setTextFormat(QtCore.Qt.AutoText)
        self.population_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.population_label)
        self.population_value = QLabel(self.population_widget)
        self.population_value.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.population_value.sizePolicy().hasHeightForWidth())
        self.population_value.setSizePolicy(sizePolicy)
        self.population_value.setMinimumSize(QtCore.QSize(102, 22))
        self.population_value.setMaximumSize(QtCore.QSize(102, 22))
        self.population_value.setFont(font)
        self.population_value.setBaseSize(QtCore.QSize(0, 0))
        self.population_value.setFocusPolicy(QtCore.Qt.NoFocus)
        self.population_value.setAlignment(QtCore.Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.population_value)
        self.population_slider = QSlider(self.population_widget)
        self.population_slider.setMinimumSize(QtCore.QSize(200, 0))
        self.population_slider.setStyleSheet("background: transparent;")
        self.population_slider.setOrientation(QtCore.Qt.Horizontal)

        self.horizontalLayout_6.addWidget(self.population_slider)
        self.population_slider.setMaximum(300)
        self.population_slider.setMinimum(1)
        self.population_slider.setValue(1)
        self.population_slider.setTickInterval(1)
        self.population_slider.valueChanged.connect(
            lambda: self.slider_value_change(self.population_slider, self.population_value))

        # Infection widget
        self.infection_widget = QWidget(self.main_widget)
        self.infection_widget.setGeometry(QtCore.QRect(240, 270, 591, 61))
        self.infection_widget.setStyleSheet("background: transparent;")

        self.horizontalLayout_2 = QHBoxLayout(self.infection_widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.infection_label = QLabel(self.infection_widget)
        self.infection_label.setMinimumSize(QtCore.QSize(250, 0))
        self.infection_label.setFont(font)
        self.infection_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.infection_label.setStyleSheet("background: transparent;")
        self.infection_label.setTextFormat(QtCore.Qt.AutoText)
        self.infection_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.infection_label.setObjectName("infection_label")
        self.horizontalLayout_2.addWidget(self.infection_label)
        self.infection_value = QLabel(self.infection_widget)
        self.infection_value.setEnabled(True)
        self.infection_value.setFont(font)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infection_value.sizePolicy().hasHeightForWidth())
        self.infection_value.setSizePolicy(sizePolicy)
        self.infection_value.setMinimumSize(QtCore.QSize(102, 22))
        self.infection_value.setMaximumSize(QtCore.QSize(102, 22))
        self.infection_value.setBaseSize(QtCore.QSize(0, 0))
        self.infection_value.setFocusPolicy(QtCore.Qt.NoFocus)
        self.infection_value.setAlignment(QtCore.Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.infection_value)
        self.infection_slider = QSlider(self.infection_widget)
        self.infection_slider.setMinimumSize(QtCore.QSize(200, 0))
        self.infection_slider.setStyleSheet("background: transparent;")
        self.infection_slider.setOrientation(QtCore.Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.infection_slider)
        self.infection_slider.setMaximum(100)
        self.infection_slider.setMinimum(0)
        self.infection_slider.setValue(0)
        self.infection_slider.setTickInterval(1)
        self.infection_slider.valueChanged.connect(
            lambda: self.slider_percentage_value_change(self.infection_slider, self.infection_value))

        # Death widget
        self.death_widget = QWidget(self.main_widget)
        self.death_widget.setGeometry(QtCore.QRect(240, 350, 591, 61))
        self.death_widget.setStyleSheet("background: transparent;")

        self.horizontalLayout_3 = QHBoxLayout(self.death_widget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.death_label = QLabel(self.death_widget)
        self.death_label.setMinimumSize(QtCore.QSize(250, 0))
        font.setPointSize(14)
        self.death_label.setFont(font)
        self.death_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.death_label.setStyleSheet("background: transparent;")
        self.death_label.setTextFormat(QtCore.Qt.AutoText)
        self.death_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.death_label)
        self.death_value = QLabel(self.death_widget)
        self.death_value.setEnabled(True)
        self.death_value.setFont(font)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.death_value.sizePolicy().hasHeightForWidth())
        self.death_value.setSizePolicy(sizePolicy)
        self.death_value.setMinimumSize(QtCore.QSize(102, 22))
        self.death_value.setMaximumSize(QtCore.QSize(102, 22))
        self.death_value.setBaseSize(QtCore.QSize(0, 0))
        self.death_value.setFocusPolicy(QtCore.Qt.NoFocus)
        self.death_value.setAlignment(QtCore.Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.death_value)
        self.death_slider = QSlider(self.death_widget)
        self.death_slider.setMinimumSize(QtCore.QSize(200, 0))
        self.death_slider.setStyleSheet("background: transparent;")
        self.death_slider.setOrientation(QtCore.Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.death_slider)
        self.death_slider.setMaximum(100)
        self.death_slider.setMinimum(0)
        self.death_slider.setValue(0)
        self.death_slider.setTickInterval(1)
        self.death_slider.valueChanged.connect(
            lambda: self.slider_percentage_value_change(self.death_slider, self.death_value))

        # Sickness time widget
        self.sickness_widget = QWidget(self.main_widget)
        self.sickness_widget.setGeometry(QtCore.QRect(240, 430, 591, 61))
        self.sickness_widget.setStyleSheet("background: transparent;")

        self.horizontalLayout_4 = QHBoxLayout(self.sickness_widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)

        self.sickness_label = QLabel(self.sickness_widget)
        self.sickness_label.setMinimumSize(QtCore.QSize(250, 0))
        font.setPointSize(14)
        self.sickness_label.setFont(font)
        self.sickness_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sickness_label.setStyleSheet("background: transparent;")
        self.sickness_label.setTextFormat(QtCore.Qt.AutoText)
        self.sickness_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.sickness_label)
        self.sckness_value = QLabel(self.sickness_widget)
        self.sckness_value.setEnabled(True)
        self.sckness_value.setFont(font)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sckness_value.sizePolicy().hasHeightForWidth())
        self.sckness_value.setSizePolicy(sizePolicy)
        self.sckness_value.setMinimumSize(QtCore.QSize(102, 22))
        self.sckness_value.setMaximumSize(QtCore.QSize(102, 22))
        self.sckness_value.setBaseSize(QtCore.QSize(0, 0))
        self.sckness_value.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sckness_value.setAlignment(QtCore.Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.sckness_value)
        self.sickness_slider = QSlider(self.sickness_widget)
        self.sickness_slider.setMinimumSize(QtCore.QSize(200, 0))
        self.sickness_slider.setStyleSheet("background: transparent;")
        self.sickness_slider.setOrientation(QtCore.Qt.Horizontal)

        self.horizontalLayout_4.addWidget(self.sickness_slider)
        self.sickness_slider.setMaximum(50)
        self.sickness_slider.setMinimum(10)
        self.sickness_slider.setValue(10)
        self.sickness_slider.setTickInterval(1)
        self.sickness_slider.valueChanged.connect(
            lambda: self.slider_value_change(self.sickness_slider, self.sckness_value))

        # Reinfection widget
        self.reinfection_widget = QWidget(self.main_widget)
        self.reinfection_widget.setGeometry(QtCore.QRect(240, 510, 591, 61))
        self.reinfection_widget.setStyleSheet("background: transparent;")

        self.horizontalLayout_5 = QHBoxLayout(self.reinfection_widget)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)

        self.reinfection_label = QLabel(self.reinfection_widget)
        self.reinfection_label.setMinimumSize(QtCore.QSize(250, 0))
        font.setPointSize(14)
        self.reinfection_label.setFont(font)
        self.reinfection_label.setFocusPolicy(QtCore.Qt.NoFocus)
        self.reinfection_label.setStyleSheet("background: transparent;")
        self.reinfection_label.setTextFormat(QtCore.Qt.AutoText)
        self.reinfection_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.reinfection_label)
        self.reinfection_value = QLabel(self.reinfection_widget)
        self.reinfection_value.setEnabled(True)
        self.reinfection_value.setFont(font)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reinfection_value.sizePolicy().hasHeightForWidth())
        self.reinfection_value.setSizePolicy(sizePolicy)
        self.reinfection_value.setMinimumSize(QtCore.QSize(102, 22))
        self.reinfection_value.setMaximumSize(QtCore.QSize(102, 22))
        self.reinfection_value.setBaseSize(QtCore.QSize(0, 0))
        self.reinfection_value.setFocusPolicy(QtCore.Qt.NoFocus)
        self.reinfection_value.setAlignment(QtCore.Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.reinfection_value)
        self.reinfection_slider = QSlider(self.reinfection_widget)
        self.reinfection_slider.setMinimumSize(QtCore.QSize(200, 0))
        self.reinfection_slider.setStyleSheet("background: transparent;")
        self.reinfection_slider.setOrientation(QtCore.Qt.Horizontal)

        self.horizontalLayout_5.addWidget(self.reinfection_slider)
        self.reinfection_slider.setMaximum(100)
        self.reinfection_slider.setMinimum(0)
        self.reinfection_slider.setValue(0)
        self.reinfection_slider.setTickInterval(1)
        self.reinfection_slider.valueChanged.connect(
            lambda: self.slider_percentage_value_change(self.reinfection_slider, self.reinfection_value))

        # Start button
        self.start_button = QPushButton(self.main_widget)
        self.start_button.setGeometry(QtCore.QRect(450, 620, 221, 51))
        font.setPointSize(12)
        self.start_button.setFont(font)
        self.start_button.setStyleSheet("background-color: rgb(131, 197, 197);")
        self.start_button.clicked.connect(self.start_simulation)

        # translating
        _translate = QtCore.QCoreApplication.translate
        self.title_label.setText(_translate("MainWindow", "Pandemic Simulation"))
        self.infection_label.setText(_translate("MainWindow", "Infection chance"))
        self.infection_value.setText(_translate("MainWindow", "0 %"))
        self.start_button.setText(_translate("MainWindow", "Start a simulation"))
        self.death_label.setText(_translate("MainWindow", "Death chance"))
        self.death_value.setText(_translate("MainWindow", "0%"))
        self.sickness_label.setText(_translate("MainWindow", "Sickness duration"))
        self.sckness_value.setText(_translate("MainWindow", "0"))
        self.reinfection_label.setText(_translate("MainWindow", "Reinfection chance"))
        self.reinfection_value.setText(_translate("MainWindow", "0%"))
        self.population_label.setText(_translate("MainWindow", "Population size"))
        self.population_value.setText(_translate("MainWindow", "0"))

        self.setCentralWidget(self.main_widget)

    def start_simulation(self):
        population = self.population_slider.value()

        death_str = (self.death_slider.value())
        death_chance = int(death_str) / 100

        infection_str = self.infection_slider.value()
        infection_chance = int(infection_str) / 100

        sickness_time = self.sickness_slider.value()

        reinfection_str = self.reinfection_slider.value()
        reinfection_chance = int(reinfection_str) / 100

        param_pack = ParamPack(population, infection_chance, death_chance, sickness_time,
                               reinfection_chance)
        self.simulation_window = SimulationWindow(param_pack)
        self.hide()
        self.simulation_window.show()

    def slider_value_change(self, slider, value):
        new_value = slider.value()
        value.setNum(new_value)

    def slider_percentage_value_change(self, slider, value):
        new_value = slider.value()
        value.setText(str(new_value) + "%")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow()
    main.show()

    sys.exit(app.exec_())
