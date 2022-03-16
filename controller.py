from model import Model
from view import View
import numpy as np


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View(self)

        self.view.actionOpen_CV_Files.triggered.connect(self.open_files)

        self.view.cvTree.itemDoubleClicked.connect(self.show_cv)
        self.view.lst_currentsSpeedSelector.itemDoubleClicked.connect(self.show_current_contribution)

        self.view.btn_calculate.clicked.connect(self.calculate)

    def main(self):
        self.view.main()

    def show_current_contribution(self, item):
        # try:
        self.view.display_current_contribution(item.file_id)
        # except AttributeError:
        #     pass

    def show_cv(self, item, column):
        try:
            self.view.display_cv(item.file_id, item.cycle_number)
        except AttributeError:
            pass

    def open_files(self):
        paths = self.view.file_dialog('Add BioLogic CV File', "BioLogic (*.mpt)")
        for path in paths:
            file_id = self.model.add_single_file(path)
            self.view.add_cv_to_tree(file_id)
            self.view.display_cv(file_id, 1)
        self.check_files()

    def check_files(self):
        speeds = []
        vertices = []
        cycles = []
        for file_data in self.model.cv_data:
            speeds.append(file_data.speed)
            vertices.append(file_data.first_vertice)
            vertices.append(file_data.second_vertice)
            cycles.append(file_data.cycle_count)
        unique_speeds = np.unique(speeds)
        unique_vertices = np.unique(vertices)
        unique_cycles = np.unique(cycles)
        if len(unique_speeds) >= 3:
            View.feedback_label(self.view.lbl_speedCheck, 'check')
            self.view.lbl_speedText.setText(f"At least 3 speeds (found: {len(unique_speeds)})")
        else:
            View.feedback_label(self.view.lbl_speedCheck, 'error')
            self.view.lbl_speedText.setText(f"Less than 3 speeds (found: {len(unique_speeds)})")

        if len(unique_vertices) == 2:
            View.feedback_label(self.view.lbl_verticeCheck, 'check')
            self.view.lbl_verticeText.setText(f"All vertices Identical (found: { unique_vertices })")
        else:
            View.feedback_label(self.view.lbl_verticeCheck, 'error')
            self.view.lbl_verticeText.setText(f"Differing vertices (found: {unique_vertices})")

        if len(unique_cycles) == 1:
            View.feedback_label(self.view.lbl_cycleNumberCheck, 'check')
            self.view.lbl_cycleNumberText.setText(f"Identical number of cycles (found: { unique_cycles })")
        else:
            View.feedback_label(self.view.lbl_cycleNumberCheck, 'warn')
            self.view.lbl_cycleNumberText.setText(f"Differing number of cycles (found: {unique_cycles})")

        self.view.spn_cycle.setMinimum(1)
        self.view.spn_cycle.setMaximum(unique_cycles[0])

        self.view.spn_cutoff.setMinimum(3)
        self.view.spn_cutoff.setMaximum(len(unique_speeds))

    def calculate(self):
        # TODO: check if prerequisites are met

        self.model.run_fc_calculation(self.view.spn_cycle.value(), self.view.spn_cutoff.value())

        # TODO: display data in UI

        self.view.display_capacitance_plot()
        self.view.display_current_contribution(0)

        slider = self.view.sld_linRegSlider
        slider.setMinimum(self.model.lin_reg_data.index.min())
        slider.setMaximum(self.model.lin_reg_data.index.max())

        slider.sliderMoved.connect(self.view.update_lin_reg_plot)
        self.view.update_lin_reg_plot()


if __name__ == '__main__':
    pyECA = Controller()
    pyECA.main()