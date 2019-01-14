from dataclasses import dataclass
from stats_packs import StandardPack
from helper_functions import make_floats
from helper_functions import combine_by_percent
import global_data


@dataclass
class OpponentStrengths:
    __slots__ = "filename", "opponents"
    filename: str
    opponents: dict

    def __init__(self, filename):
        self.filename = filename
        self.opponents = {}
        for line in open(filename):
            opponent_info = line.split("|")
            self.opponents[opponent_info[0]] = [float(opponent_info[1]), \
                                                StandardPack(make_floats(opponent_info[2].split()))]

    def save_to_file(self):
        file = open(self.filename, "w")
        for op in self.opponents:
            op_string = op + "|" + str(self.opponents[op][0]) + "|"
            for stat in self.opponents[op][1].as_list():
                op_string += " " + str(stat)
            file.write(op_string + "\n")
        file.close()

    def update_op(self, op_name, op_pcts):
        for i in range(len(op_pcts)):
            self.opponents[op_name][1][i] = combine_by_percent(self.opponents[op_name][1][i], op_pcts[i], \
                                                            global_data.OP_STRS_SAVE_RATE * self.opponents[op_name][0])

    def phaseout_data(self):
        for key in self.opponents:
            self.opponents[key][0] *= global_data.OP_STRS_PHASEOUT_RATE