from dataclasses import dataclass
from stats_packs import StandardPack
from helper_functions import make_floats
from helper_functions import combine_by_percent
import global_data
from os import listdir
from os import remove


@dataclass
class Opponent:
    __slots__ = "name", "decay", "stat_percents"
    name: str
    decay: float
    stat_percents: StandardPack

    def __init__(self, op_line):
        opponent_info = op_line.split("|")
        self.name = opponent_info[0]
        self.decay = float(opponent_info[1])
        self.stat_percents = StandardPack(make_floats(opponent_info[2].split()))

    def get_save_str(self):
        save_str = self.name + "|" + str(self.decay) + "|"
        for stat in self.stat_percents.as_list():
            save_str += " " + str(stat)
        return save_str


@dataclass
class OpponentStrengths:
    __slots__ = "filename", "opponents"
    filename: str
    opponents: dict

    def __init__(self, filename, editing = True):
        self.filename = filename
        self.opponents = {}
        for line in open(filename):
            this_op = Opponent(line)
            self.opponents[this_op.name] = this_op
        if editing:
            self.filename += ".bk"
            self.save_to_file()
            self.filename = filename

    def save_to_file(self):
        file = open(self.filename, "w")
        for op in self.opponents.values():
            file.write(op.get_save_str() + "\n")
        file.close()

    def update_op(self, op_name, op_pcts):
        old_op_pcts = self.opponents[op_name].stat_percents.as_list()
        for i in range(len(op_pcts)):
            op_pcts[i] = combine_by_percent(old_op_pcts[i], op_pcts[i], \
                                         global_data.OP_STRS_SAVE_RATE * self.opponents[op_name].decay)
        self.opponents[op_name].stat_percents = StandardPack(op_pcts)

    def phaseout_data(self):
        for key in self.opponents:
            self.opponents[key].decay *= global_data.OP_STRS_PHASEOUT_RATE


def clear_backups(year):
    folder_path = str(year)
    file_names = listdir(folder_path)

    for file_name in file_names:
        if file_name[-3:] == ".bk":
            remove(folder_path + "/" + file_name)