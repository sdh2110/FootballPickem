import random
from helper_functions import percent_diff
from helper_functions import percent_hard_diff
from helper_functions import mk_list_to_percents


def mk_comparison_chart(cmp_function, data):
    cmp_chart = []
    for entry in data:
        cmps_for_entry = []
        for cmp_entry in data:
            cmps_for_entry.append(int(cmp_function(entry, cmp_entry) * 100))
        cmp_chart.append(cmps_for_entry)
    return cmp_chart


def highlight_differences(cmp_chart):
    diff_chart = []
    for i in range(len(cmp_chart)):
        diff_chart.append(mk_list_to_percents(cmp_chart[i]))
        for j in range(len(diff_chart[i])):
            diff_chart[i][j] = diff_chart[i][j] ** 3
        diff_chart[i] = mk_list_to_percents(diff_chart[i])
    return diff_chart


def cleanup_chart(cmp_chart):
    for i in range(len(cmp_chart)):
        for j in range(len(cmp_chart)):
            if cmp_chart[i][j] <= 50:
                cmp_chart[i][j] = 0
    return cmp_chart


def print_chart(chart, spacing):
    for line in chart:
        for val in line:
            val = str(val)
            for _ in range(len(val), spacing):
                print(end = " ")
            print(val, end = " ")
        print()


def get_chart_codes(cmp_chart):
    codes = []
    for line in cmp_chart:
        code = ""
        for val in line:
            if val == 0:
                code += '0'
            else:
                code += '1'
        codes.append(code)
    return codes


def create_entry_code(idx):
    if idx < 0 or idx > 675:
        raise IndexError("Index out of range in create_entry_code")
    else:
        chars = [chr(ord("A") + idx // 26), chr(ord("A") + idx % 26)]
        code = ""
        return code.join(chars)


def get_entry_classes(chart_codes):
    entry_classes_dct = {}
    for i in range(len(chart_codes)):
        if chart_codes[i] in entry_classes_dct:
            entry_classes_dct[chart_codes[i]].append(i)
        else:
            entry_classes_dct[chart_codes[i]] = [i]
    entry_classes = []
    for key in entry_classes_dct:
        class_code = create_entry_code(len(entry_classes))
        entry_classes.append([class_code] + entry_classes_dct[key])
    return entry_classes


def mk_entry_class():
    entry = []
    for _ in range(5):
        entry.append(random.randint(50, 500))
    return entry


def get_variant(entry_class):
    variant = []
    for val in entry_class:
        variant.append(val + random.randint(-25, 25))
    return variant


def test_mass_cmp():
    entry_classes = []
    for _ in range(4):
        entry_classes.append(mk_entry_class())

    entry_data = []
    for i in range(20):
        entry_data.append(get_variant(entry_classes[i // 5]))

    cmp_chart = mk_comparison_chart(percent_diff, entry_data)
    print_chart(cmp_chart, 3)
    print()

    #hlight_chart = highlight_differences(cmp_chart)
    cmp_chart2 = mk_comparison_chart(percent_hard_diff, cmp_chart)
    cmp_chart2 = mk_comparison_chart(percent_hard_diff, cmp_chart2)
    cmp_chart2 = cleanup_chart(cmp_chart2)
    print_chart(cmp_chart2, 3)
    print()

    print_chart(entry_data, 5)
    print()

    print_chart(entry_classes, 5)
    print()

    print_chart(get_entry_classes(get_chart_codes(cmp_chart2)), 3)


#test_mass_cmp()