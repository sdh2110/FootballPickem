from dataclasses import dataclass

# Discarded stats
#   Tot_1stD
#   Tot_PF
#   Tot_Yds
#   Tot_Ply
#   Tot_Y-P

@dataclass
class StandardPack:
    __slots__ = "stats_list"
    stats_list: list

    def as_list(self):
        return self.stats_list

    def TO(self):
        return self.stats_list[0]

    def FL(self):
        return self.stats_list[1]

    def pass_Cmp(self):
        return self.stats_list[2]

    def pass_Att(self):
        return self.stats_list[3]

    def pass_Yds(self):
        return self.stats_list[4]

    def pass_TD(self):
        return self.stats_list[5]

    def pass_Int(self):
        return self.stats_list[6]

    def pass_NYA(self):
        return self.stats_list[7]

    def rush_Att(self):
        return self.stats_list[8]

    def rush_Yds(self):
        return self.stats_list[9]

    def rush_TD(self):
        return self.stats_list[10]

    def rush_YA(self):
        return self.stats_list[11]

    def pena_Pen(self):
        return self.stats_list[12]

    def pena_Yds(self):
        return self.stats_list[13]

    def points_for(self):
        return self.stats_list[14]


@dataclass
class BonusPack:
    __slots__ = "stats_list"
    stats_list: list

    def as_list(self):
        return self.stats_list

    def games(self):
        return self.stats_list[0]

    def pass_FD(self):
        return self.stats_list[1]

    def rush_FD(self):
        return self.stats_list[2]

    def pena_FD(self):
        return self.stats_list[3]

    def ScPct(self):
        return self.stats_list[4]

    def TOPct(self):
        return self.stats_list[5]

    def EXP(self):
        return self.stats_list[6]