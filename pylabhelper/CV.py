import os.path
import pylabhelper.biologic as biologic


class CV:

    def __init__(self, path):
        """ Creating a CV object from a measurement file """

        self.path = path
        self.filename, self.extension = os.path.splitext(os.path.basename(path))

        if self.extension == '.mpt':
            data = biologic.read_mpt(path)

            self.first_vertice = data['first_vertice']
            self.second_vertice = data['second_vertice']
            self.speed = data['speed']
            self.ocp = data['open_circuit_potential']
            self.original_data = data['data']

            self._create_recycled_data()

    def _extract_cycle_keys(self):
        # Extract Maxima and Minima from each cycle
        max_keys = []
        min_keys = []

        for cycle_number in self.original_data.cycle.unique():
            if self.first_vertice > self.second_vertice:
                # Cycle is upper - lower - upper
                cycle_df = self.original_data[self.original_data.cycle == cycle_number]
                max_keys.append(cycle_df.potential.idxmax())

                # Possibility 1      Possibility 2          Possibility 3
                # EOC in between     EOC smaller than L     EOC bigger than U
                #                                            S          E
                #                                            \          /
                #  U1  U2  U3         U1  U2  U3              \U1  U2  /U3
                #  /\  /\  /\         /\  /\  /\               \  /\  /
                #  S \/  \/ E        /  \/  \/  \               \/  \/
                #    L1  L2         /   L1  L2   \              L1  L2
                #  ____----         S            E

                # ignore data before first maximum
                min_keys.append(cycle_df.loc[cycle_df.potential.idxmax():].potential.idxmin())
            else:
                # Cycle is lower - upper - lower
                raise Exception('direction not yet defined')

        return [max_keys, min_keys]

    def _create_recycled_data(self):
        max_keys, min_keys = self._extract_cycle_keys()
        self.data = self.original_data.copy()

        if max_keys[0] < min_keys[0]:
            # First extreme is upper vertex
            # --> Cycle is upper - lower - upper
            self.data.loc[0: max_keys[0], 'cycle'] = 'start'
            self.data.loc[0: max_keys[0], 'direction'] = 'up'
            for max_key_index in range(len(max_keys) - 1):
                self.data.loc[max_keys[max_key_index]: max_keys[max_key_index + 1], 'cycle'] = max_key_index + 1
                self.data.loc[max_keys[max_key_index]: min_keys[max_key_index], 'direction'] = 'down'
                self.data.loc[min_keys[max_key_index]: max_keys[max_key_index + 1], 'direction'] = 'up'

            self.data.loc[max_keys[-1]:, 'cycle'] = 'end'
            self.data.loc[max_keys[-1]:min_keys[-1], 'direction'] = 'down'
            self.data.loc[min_keys[-1]:, 'direction'] = 'up'
        else:
            # First extreme is lower vertex
            # --> Cycle is lower - upper - lower
            raise Exception('direction yet unimplemented')
