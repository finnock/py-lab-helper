import math

from PyQt5.QtWidgets import (QMainWindow, QApplication, QFileDialog, QTreeWidgetItem, QListWidgetItem)
from PyQt5.QtGui import (QBrush, QColor, QFont)
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from pylabhelper.echem import fitting_function
import numpy as np

class View(QMainWindow):

    def __init__(self, controller):
        """
        Load .ui file, initialize window
        """
        self.app = QApplication([])
        QMainWindow.__init__(self)

        self.controller = controller
        self.model = controller.model

        loadUi("matplotlib-test.ui", self)

        self.cvTree.clear()

    def main(self):
        """
        Run Application loop
        """

        self.show()
        self.app.exec_()

    def file_dialog(self, title, type_filter):
        return QFileDialog.getOpenFileNames(self, title, '', type_filter)[0]

    def display_cv(self, file_id, cycle_number):
        self.display_tp_plot(file_id, cycle_number)
        self.display_ui_plot(file_id, cycle_number)
        # todo update text labels with cycle info/data

    def add_cv_to_tree(self, file_id):
        cv_data = self.model.cv_data[file_id]

        speed = f"{cv_data.speed} mV/s"
        cycles = f"{cv_data.cycle_count}"
        filename = cv_data.filename

        cv_item = QTreeWidgetItem([speed, cycles, filename])
        cv_item.setToolTip(2, filename)

        for cycle_number in cv_data.data.cycle.unique()[1:-1]:
            cycle_widget = QTreeWidgetItem([f"Cycle {cycle_number}"])
            cycle_widget.speed = cv_data.speed
            cycle_widget.cycle_number = cycle_number
            cycle_widget.file_id = file_id
            cv_item.addChild(cycle_widget)

        self.cvTree.addTopLevelItem(cv_item)

        item = QListWidgetItem(f"{cv_data.speed} mV/s")
        item.setCheckState(Qt.Checked)
        self.lst_speedSelector.addItem(item)

        item = QListWidgetItem(f"{cv_data.speed} mV/s")
        item.file_id = file_id
        self.lst_currentsSpeedSelector.addItem(item)

    def display_tp_plot(self, file_id, cycle_number):
        # get file data from model
        file = self.model.cv_data[file_id]

        # get cycle data from model
        cycle = file.data[file.data['cycle'] == cycle_number]

        # check if plots created
        canvas = self.timePotentialPlot.canvas
        if not hasattr(canvas, 'top_plot'):
            canvas.top_plot = canvas.figure.add_subplot(2, 1, 1)
            canvas.bottom_plot = canvas.figure.add_subplot(2, 1, 2)

        # display data
        ax = canvas.top_plot
        ax.clear()
        ax.plot(file.data.time, file.data.potential, label='complete file', color='darkgrey')
        ax.plot(cycle['time'], cycle['potential'], label=f"Cycle {cycle_number}")
        ax.set_title(file.filename, fontsize=10)
        ax.plot()
        ax.legend()

        # display all extracted cycles
        ax = canvas.bottom_plot
        ax.clear()
        for cycle_identifier in file.data.cycle.unique():
            sub_cycle = file.data[file.data['cycle'] == cycle_identifier]

            if cycle_identifier in ('start', 'end'):
                ax.plot(sub_cycle.time, sub_cycle.potential, linestyle='--', color='grey')
            else:
                ax.plot(sub_cycle.time, sub_cycle.potential, linestyle='-')

        # draw canvas
        canvas.figure.tight_layout()
        canvas.draw()

    def display_ui_plot(self, file_id, cycle_number):

        # get cycle data from model
        file = self.model.cv_data[file_id]
        cycle = file.data[file.data['cycle'] == cycle_number]
        interp_cycle = file.interp_data[file.interp_data['cycle'] == cycle_number]

        # check if plots created
        canvas = self.cyclePlot.canvas
        if not hasattr(canvas, 'plot'):
            canvas.plot = canvas.figure.add_subplot(1, 1, 1)

        # display data
        ax = canvas.plot
        ax.clear()
        ax.plot(cycle.potential, cycle.current, label=f"Cycle {cycle_number}", color='blue', linewidth=2.0)
        ax.plot(interp_cycle.potential, interp_cycle.current, label=f"Interpolated", color='red', linewidth=1.0)
        ax.set_title(f"{self.model.cv_data[file_id].speed} mv/s, Cycle {cycle_number}", fontsize=10)
        ax.legend()

        # draw canvas
        canvas.figure.tight_layout()
        canvas.draw()

    def display_capacitance_plot(self):

        # Fetch Analysis Data from model
        fc_data_up = self.model.fc_data[self.model.fc_data.direction == 'up']
        fc_data_down = self.model.fc_data[self.model.fc_data.direction == 'down']

        # check if plots created
        canvas = self.capacitancePlot.canvas
        if not hasattr(canvas, 'top_plot'):
            canvas.top_plot, canvas.bottom_plot = canvas.figure.subplots(2, 1,
                                                                         gridspec_kw={'height_ratios': [1, 3]},
                                                                         sharex=True)
            # canvas.bottom_plot = canvas.figure.add_subplot(2, 1, 2, sharex=canvas.top_plot)

        # display data
        rsqAx = canvas.top_plot
        # ax2 = ax.twinx()
        rsqAx.clear()
        rsqAx.plot(
            fc_data_up.potential,
            fc_data_up.rSq,
            color='green', label='rSq - up')
        rsqAx.plot(
            fc_data_down.potential,
            fc_data_down.rSq,
            color='blue', label='rSq - down')
        rsqAx.legend()

        capAx = canvas.bottom_plot
        capAx.clear()
        capAx.plot(fc_data_up.potential,
                   fc_data_up.capacitive,
                   label=f"Capacity in F - up",
                   color='green')
        capAx.plot(fc_data_down.potential,
                   fc_data_down.capacitive,
                   label=f"Capacity in F - down",
                   color='blue')
        capAx.legend()


        # line_c = ax2.plot(fc_data.potential, fc_data.capacitive, label=f"Capacitive Contribution", color='blue')
        # ax.spines['left'].set_color(line_f[0].get_color())
        # ax2.spines['left'].set_color(line_f[0].get_color())
        # ax2.spines['right'].set_color(line_c[0].get_color())
        #ax.set_title(f"{self.model.cv_data[file_id].speed} mv/s, Cycle {cycle_number}", fontsize=10)
        # ax.legend(line_f+line_c, [line_f[0].get_label(), line_c[0].get_label()], loc=0)

        # draw canvas
        canvas.figure.tight_layout()
        canvas.draw()

    def display_current_contribution(self, file_id):

        fc_data = self.model.fc_data

        canvas = self.currentContributionsPlot.canvas
        if not hasattr(canvas, 'plot'):
            canvas.plot = canvas.figure.add_subplot(1, 1, 1)

        ax = canvas.plot
        ax.clear()

        file_speed = self.model.cv_data[file_id].speed
        cycle = self.model.cv_data[file_id].get_interpolated_cycle(self.spn_cycle.value())

        faradayic_current = fc_data.faradayic * math.sqrt(file_speed)
        capacitive_current = fc_data.capacitive * file_speed

        ax.plot(
            fc_data.potential,
            faradayic_current,
            label=f"Faradayic Current @ {file_speed} mV/s",
            color='red')

        ax.plot(
            fc_data.potential,
            capacitive_current,
            label=f"Capacitive Current",
            color='blue')

        ax.plot(
            cycle.potential,
            cycle.current,
            color='green',
            label='Measured Cycle')

        ax.plot(
            cycle.potential,
            capacitive_current + faradayic_current,
            label='Sum Cap+Far'
        )

        ax.legend()

        canvas.figure.tight_layout()
        canvas.draw()

    def update_lin_reg_plot(self):

        canvas = self.linRegPlot.canvas
        if not hasattr(canvas, 'top_plot'):
            canvas.top_plot, canvas.bottom_plot =\
                canvas.figure.subplots(2, 1, gridspec_kw={'height_ratios': [1, 3]})

        # Fetch and compute Data
        fc_data_up = self.model.fc_data[self.model.fc_data.direction == 'up']
        fc_data_down = self.model.fc_data[self.model.fc_data.direction == 'down']
        lin_reg_data = self.model.lin_reg_data
        f_reg_data = self.model.f_reg_data
        index = self.sld_linRegSlider.value()
        row = lin_reg_data.loc[index]

        x = list(lin_reg_data.columns.values)[1:-4]
        y = list(lin_reg_data.loc[index])[1:-4]

        speeds = list(f_reg_data.columns.values)[1:-4]
        currents = list(f_reg_data.loc[index])[1:-4]

        rsqAx = canvas.top_plot
        rsqAx.clear()
        if(row.direction == 'up'):
            rsqAx.plot(fc_data_up.potential, fc_data_up.rSq, color='green', label='rSq - up')
            rsqAx.plot(fc_data_down.potential, fc_data_down.rSq, color='grey', label='rSq - down')
        else:
            rsqAx.plot(fc_data_up.potential, fc_data_up.rSq, color='grey', label='rSq - up')
            rsqAx.plot(fc_data_down.potential, fc_data_down.rSq, color='blue', label='rSq - down')

        rsqAx.plot([row.potential], [row.rSq], ".", color='red')

        # rsqAx.axvline(x=row.potential, color='red', linestyle='--')
        rsqAx.legend()

        # print(f"{row.potential}, {row.faradayic}, {row.capacitive}, {row.rSq}")

        linAx = canvas.bottom_plot
        linAx.clear()

        # linAx.plot(speeds, currents, label=f"Potential: {row.potential}", marker='o', linestyle='-')
        # linAx.plot(speeds, fitting_function(np.array(speeds), row.capacitive, row.faradayic), label=f"Fitted Function")
        linAx.plot(x, y, label=f"Potential: {row.potential}", marker='o', linestyle='-')
        linAx.axline((0, row.faradayic), color='green', slope=row.capacitive,
              label=f"Linear Fit R²: {row.rSq:.2f}")
        linAx.legend()

        canvas.figure.tight_layout()
        canvas.draw()

    @staticmethod
    def feedback_label(lbl, status):
        if status == 'check':
            lbl.setText('✓')
            lbl.setStyleSheet("color: '#00aa00'")

        if status == 'warn':
            lbl.setText('✓')
            lbl.setStyleSheet("color: '#ffaa00'")

        if status == 'error':
            lbl.setText('X')
            lbl.setStyleSheet("color: '#ff0000'")
