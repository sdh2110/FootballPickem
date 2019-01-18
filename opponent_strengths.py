from dataclasses import dataclass
from stats_packs import StandardPack
from helper_functions import make_floats
from helper_functions import combine_by_percent
import global_data
from os import listdir
from os import remove


@dataclass
class OpponentStrengths:
    __slots__ = "filename", "opponents"
    filename: str
    opponents: dict

    def __init__(self, filename, editing = True):
        self.filename = filename
        self.opponents = {}
        for line in open(filename):
            opponent_info = line.split("|")
            self.opponents[opponent_info[0]] = [float(opponent_info[1]), \
                                                StandardPack(make_floats(opponent_info[2].split()))]
        if editing:
            self.filename += ".bk"
            self.save_to_file()
            self.filename = filename

    def save_to_file(self):
        file = open(self.filename, "w")
        for op in self.opponents:
            op_string = op + "|" + str(self.opponents[op][0]) + "|"
            for stat in self.opponents[op][1].as_list():
                op_string += " " + str(stat)
            file.write(op_string + "\n")
        file.close()

    def update_op(self, op_name, op_pcts):
        old_op_pcts = self.opponents[op_name][1].as_list()
        for i in range(len(op_pcts)):
            op_pcts[i] = combine_by_percent(old_op_pcts[i], op_pcts[i], \
                                         global_data.OP_STRS_SAVE_RATE * self.opponents[op_name][0])
        self.opponents[op_name][1] = StandardPack(op_pcts)

    def phaseout_data(self):
        for key in self.opponents:
            self.opponents[key][0] *= global_data.OP_STRS_PHASEOUT_RATE


def clear_backups(year):
    folder_path = str(year)
    file_names = listdir(folder_path)

    for file_name in file_names:
        if file_name[-3:] == ".bk":
            remove(folder_path + "/" + file_name)