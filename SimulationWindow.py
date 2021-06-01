from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel

from PyQt5.QtGui import QPainter, QBrush, QFont
from PyQt5.QtCore import Qt
from model import Model
import constants
from PyQt5.QtChart import *
import time


class SimulationWindow(QMainWindow):

    def __init__(self, param_pack, parent=None):
        super(SimulationWindow, self).__init__(parent)
        self.length = 1109
        self.height = 736
        self.setFixedSize(self.length, self.height)
        self.setWindowTitle("Pandemic Simulation")
        self.central_widget = CentralWidget(self, self.length, self.height, param_pack)
        self.setCentralWidget(self.central_widget)


class CentralWidget(QWidget):

    def __init__(self, parent, length, height, param_pack):
        super().__init__(parent)

        self.model = Model(param_pack)
        self.parent = parent
        self.param_pack = param_pack
        self.title_label = QLabel(self)
        self.finish_button = QPushButton(self)
        self.finish_button.clicked.connect(self.save_and_finish)
        self.init_ui(length, height)
        self.plot_widget = PlotWidget(self, self.model)
        self.stat_widget = StatisticsWidget(self, self.model, self.plot_widget)
        self.simulation_widget = SimulationWidget(self, self.model, self.stat_widget)

    def init_ui(self, length, height):
        self.setFixedSize(length, height)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: rgb(214, 214, 214);')
        self.title_label.setGeometry(QtCore.QRect(500, 10, 131, 31))
        font1 = QFont()
        font1.setPointSize(17)
        font1.setBold(True)
        self.title_label.setFont(font1)
        self.title_label.setText("Simulation")
        self.finish_button.setGeometry(QtCore.QRect(480, 680, 201, 41))
        font1.setPointSize(10)
        font1.setWeight(75)
        self.finish_button.setFont(font1)
        self.finish_button.setAttribute(Qt.WA_StyledBackground, True)
        self.finish_button.setStyleSheet("background-color: green;")
        self.finish_button.setText("Save and finish")
        self.finish_button.hide()
        self.show()

    def show_button(self):
        self.finish_button.show()

    def save_and_finish(self):
        file = open("SimulationData.txt", 'a', encoding="utf-8")
        file.write("\n-------------\nParams:\n")
        p, i, d, s, r = self.param_pack.pack_data()
        params = f"\nPopulation: {p}\nInfection chance: {i}\nDeath chance: {d}\nSickness duration: {s}\nReinfection " \
                 f"chance: {r}\n "
        file.write(params)
        p, d, h, s, c, ds = self.model.data_package()
        result = f"\nResults:\nPopulation: {p}\nDays: {d}\nHealthy: {h}\nSick: {s}\nRecovered: {c}\nDead: {ds}\n"
        file.write(result)
        file.close()

        self.parent.close()


class SimulationWidget(QWidget):
    def __init__(self, parent, model, data_widget):
        super().__init__(parent)

        self.parent = parent
        self.model = model
        self.initUI()
        self.data_widget = data_widget

    def initUI(self):
        self.setGeometry(QtCore.QRect(10, 60, 600, 600))
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))

        self.model.tick()
        for color, cell_list in self.model.population.items():
            for cell in cell_list:
                if cell.state == "green":
                    qp.setBrush(QBrush(Qt.green, Qt.SolidPattern))
                if cell.state == "red":
                    qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
                if cell.state == "blue":
                    qp.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
                qp.drawEllipse(int(cell.location.x), int(cell.location.y),
                               constants.CELL_RADIUS, constants.CELL_RADIUS)

        if self.model.is_complete():
            self.data_widget.update_data(self.model)
            qp.end()
            self.parent.show_button()
            return
        else:
            self.data_widget.update_data(self.model)
            time.sleep(0.015)
            self.update()


class PlotWidget(QWidget):
    def __init__(self, parent, model):
        super().__init__(parent)

        self.initUI()
        self.sim_plot = StatChart(model)
        self.chart_view = QChartView(self.sim_plot)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.chart_view)
        self.setLayout(self.layout)

    def initUI(self):
        self.setGeometry(QtCore.QRect(620, 210, 481, 451))
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.show()

    def update_data(self, model):
        self.sim_plot.update_data(model)


class StatChart(QChart):
    def __init__(self, model):
        super().__init__(flags=Qt.WindowStaysOnTopHint)

        self.setBackgroundVisible(False)
        self.setPlotAreaBackgroundVisible(True)

        self.set0 = QBarSet("Dead")
        self.set0.setColor(Qt.black)
        self.set1 = QBarSet("Infected")
        self.set1.setColor(Qt.red)

        self.set2 = QBarSet("Recovered")
        self.set2.setColor(Qt.blue)

        self.set3 = QBarSet("Healthy")
        self.set3.setColor(Qt.green)

        self.set4 = QBarSet("Population")
        self.set4.setColor(Qt.yellow)

        population_size, day, healthy_size, sick_size, cured_size, dead_size = model.data_package()

        self.set0.append([dead_size])
        self.set1.append([sick_size])
        self.set2.append([cured_size])
        self.set3.append([healthy_size])
        self.set4.append([population_size])

        self.series = QHorizontalBarSeries()
        self.series.append(self.set0)
        self.series.append(self.set1)
        self.series.append(self.set2)
        self.series.append(self.set3)
        self.series.append(self.set4)
        self.addSeries(self.series)

        self.axis_x = QValueAxis()
        self.addAxis(self.axis_x, Qt.AlignBottom)
        self.series.attachAxis(self.axis_x)
        self.axis_x.applyNiceNumbers()

        font = QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(10)
        font.setBold(True)
        self.legend().setFont(font)
        self.show()

    def update_data(self, model):
        population_size, day, healthy_size, sick_size, cured_size, dead_size = model.data_package()
        self.set0.remove(0)
        self.set1.remove(0)
        self.set2.remove(0)
        self.set3.remove(0)
        self.set4.remove(0)

        self.set0.append([dead_size])
        self.set1.append([sick_size])
        self.set2.append([cured_size])
        self.set3.append([healthy_size])
        self.set4.append([population_size])


class StatisticsWidget(QWidget):
    def __init__(self, parent, model, plot_widget):
        super().__init__(parent)

        self.plot_widget = plot_widget

        font = QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(10)
        font.setBold(True)

        self.day_label = QLabel(self)
        self.day_label.setGeometry(QtCore.QRect(280, 30, 191, 16))
        self.day_label.setFont(font)

        self.healthy_label = QLabel(self)
        self.healthy_label.setGeometry(QtCore.QRect(60, 70, 191, 16))
        self.healthy_label.setFont(font)

        self.cured_label = QLabel(self)
        self.cured_label.setGeometry(QtCore.QRect(280, 70, 191, 16))
        self.cured_label.setFont(font)

        self.infected_label = QLabel(self)
        self.infected_label.setGeometry(QtCore.QRect(60, 110, 191, 16))
        self.infected_label.setFont(font)

        self.dead_label = QLabel(self)
        self.dead_label.setGeometry(QtCore.QRect(280, 110, 191, 16))
        self.dead_label.setFont(font)

        self.population_count_label = QLabel(self)
        self.population_count_label.setGeometry(QtCore.QRect(60, 30, 201, 16))
        self.population_count_label.setFont(font)

        self.initUI()

    def initUI(self):
        self.setGeometry(QtCore.QRect(620, 60, 481, 141))
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.show()

    def update_data(self, model):
        population_size, day, healthy_size, sick_size, cured_size, dead_size = model.data_package()
        self.day_label.setText("Day: " + str(day))
        self.healthy_label.setText("Healthy: " + str(healthy_size))
        self.infected_label.setText("Infected: " + str(sick_size))
        self.cured_label.setText("Recovered: " + str(cured_size))
        self.dead_label.setText("Dead: " + str(dead_size))
        self.population_count_label.setText("Population: " + str(population_size))
        self.plot_widget.update_data(model)


