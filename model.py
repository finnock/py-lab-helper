import pylabhelper.echem as echem

class Model:
    """
    Object holding all data for the pyECA
    """

    def __init__(self):
        """
        Default Constructor.
        """
        # TODO: add better doc
        self.cv_data = []

    def load_single_file(self, path):
        self.cv_data = echem.read_cv_file(path)

    def add_single_file(self, path):
        self.cv_data.append(echem.read_cv_file(path))
        return len(self.cv_data)-1

    def run_fc_calculation(self, cycle_number, cutoff):
        self.fc_data, self.lin_reg_data, self.f_reg_data = echem.fc_analysis(self.cv_data, cycle_number, cutoff)
