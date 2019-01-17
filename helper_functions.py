def percent_diff(lst1, lst2):
    percent_list = []

    for i in range(len(lst1)):
        percent_diff = 0
        if lst1[i] > lst2[i]:
            percent_diff = (lst1[i] - lst2[i]) / lst1[i]
        elif lst1[i] < lst2[i]:
            percent_diff = (lst2[i] - lst1[i]) / lst2[i]
        percent_list.append(percent_diff)

    total_diff = 0
    for percent in percent_list:
        total_diff += percent

    return 1 - (total_diff / len(percent_list))


def percent_hard_diff(lst1, lst2):
    percent_list = []

    for i in range(len(lst1)):
        difference = 0
        larger = 100
        if lst1[i] > lst2[i]:
            difference = lst1[i] - lst2[i]
            larger = lst1[i]
        elif lst1[i] < lst2[i]:
            difference = lst2[i] - lst1[i]
            larger = lst2[i]

        if difference <= 7:
            percent_list.append(0)
        elif difference >= 20:
            percent_list.append(1)
        else:
            percent_list.append(difference / larger)

    total_diff = 0
    for percent in percent_list:
        total_diff += percent

    return 1 - (total_diff / len(percent_list))


def mk_list_to_percents(lst):
    total = 0
    for val in lst:
        total += val
    percents = []
    for val in lst:
        percents.append(int(val / total * 100))
    return percents


def get_file_location(folder_name, file_name, extention = ".data"):
    return folder_name + "//" + file_name + extention


def make_floats(list_of_strs):
    int_list = []
    for string in list_of_strs:
        int_list.append(float(string))
    return int_list


def combine_by_percent(first, second, percent_of_first):
    return (first * percent_of_first) + (second * (1 - percent_of_first))