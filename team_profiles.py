from dataclasses import dataclass
from stats_packs import *
from helper_functions import percent_difference


@dataclass
class TeamProfile:
    __slots__ = "name", "standard_stats", "extra_stats"
    name: str
    standard_stats: StandardPack
    extra_stats: ExtraOffensePack

    def __init__(self, line = None):
        if line is None:
            self.name = None
            self.standard_stats = None
            self.extra_stats = None
            return

        stat_html_codes = line.split("</td>")

        name_html_code = stat_html_codes[0]
        name_html_code = name_html_code.split('.htm">')[1]
        self.name = name_html_code[:-4]

        stat_html_codes = stat_html_codes[1:-1]
        stats = []

        for html_code in stat_html_codes:
            stat = float(html_code.split(">")[1])
            stats.append(stat)

        standard = []
        extra = []

        extra.append(stats[0])
        standard += stats[5:7]
        #extra.append(stats[7])
        standard += stats[8:14]
        extra.append(stats[14])
        standard += stats[15:19]
        extra.append(stats[19])
        standard += stats[20:22]
        extra += stats[22:26]
        standard.append(stats[1])

        self.standard_stats = StandardPack(standard)
        self.extra_stats = ExtraOffensePack(extra)

    def mk_average_team(self):
        games_played = self.extra_stats.games()
        standard = self.standard_stats.as_list()
        extra = self.extra_stats.as_list()

        if games_played <= 1:
            return self

        for i in range(len(standard)):
            standard[i] /= games_played

        for i in range(1, len(extra)):
            extra[i] /= games_played

        averaged_team = TeamProfile()
        averaged_team.name = self.name
        averaged_team.standard_stats = StandardPack(standard)
        averaged_team.extra_stats = ExtraOffensePack(extra)

        return averaged_team