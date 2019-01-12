from dataclasses import dataclass

# Discarded stats
#   Tot_1stD
#   Tot_PF
#   Tot_Yds
#   Tot_Ply
#   Tot_Y-P

@dataclass
class StandardPack:
    __slots__ = "TO", "FL", "pass_Cmp", "pass_Att", "pass_Yds", \
                "pass_TD", "pass_Int", "pass_NYA", "rush_Att", "rush_Yds", \
                "rush_TD", "rush_YA", "pena_Pen", "pena_Yds", "points_for"
    TO: float
    FL: float
    pass_Cmp: float
    pass_Att: float
    pass_Yds: float
    pass_TD: float
    pass_Int: float
    pass_NYA: float
    rush_Att: float
    rush_Yds: float
    rush_TD: float
    rush_YA: float
    pena_Pen: float
    pena_Yds: float
    points_for: float

    def __init__(self, stats_list):
        self.TO = stats_list[0]
        self.FL = stats_list[1]
        self.pass_Cmp = stats_list[2]
        self.pass_Att = stats_list[3]
        self.pass_Yds = stats_list[4]
        self.pass_TD = stats_list[5]
        self.pass_Int = stats_list[6]
        self.pass_NYA = stats_list[7]
        self.rush_Att = stats_list[8]
        self.rush_Yds = stats_list[9]
        self.rush_TD = stats_list[10]
        self.rush_YA = stats_list[11]
        self.pena_Pen = stats_list[12]
        self.pena_Yds = stats_list[13]
        self.points_for = stats_list[14]

    def as_list(self):
        stats_list = []
        stats_list.append(self.TO)
        stats_list.append(self.FL)
        stats_list.append(self.pass_Cmp)
        stats_list.append(self.pass_Att)
        stats_list.append(self.pass_Yds)
        stats_list.append(self.pass_TD)
        stats_list.append(self.pass_Int)
        stats_list.append(self.pass_NYA)
        stats_list.append(self.rush_Att)
        stats_list.append(self.rush_Yds)
        stats_list.append(self.rush_TD)
        stats_list.append(self.rush_YA)
        stats_list.append(self.pena_Pen)
        stats_list.append(self.pena_Yds)
        stats_list.append(self.points_for)
        return stats_list


@dataclass
class BonusPack:
    __slots__ = "games", "pass_FD", "rush_FD", "pena_FD", "ScPct", "TOPct", "EXP"
    games: int
    pass_FD: float
    rush_FD: float
    pena_FD: float
    ScPct: float
    TOPct: float
    EXP: float

    def __init__(self, stats_list):
        self.games = stats_list[0]
        self.pass_FD = stats_list[1]
        self.rush_FD = stats_list[2]
        self.pena_FD = stats_list[3]
        self.ScPct = stats_list[4]
        self.TOPct = stats_list[5]
        self.EXP = stats_list[6]

    def as_list(self):
        stats_list = []
        stats_list.append(self.games)
        stats_list.append(self.pass_FD)
        stats_list.append(self.rush_FD)
        stats_list.append(self.pena_FD)
        stats_list.append(self.ScPct)
        stats_list.append(self.TOPct)
        stats_list.append(self.EXP)
        return stats_list