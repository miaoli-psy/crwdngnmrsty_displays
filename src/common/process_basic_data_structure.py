import random


def get_diff_between_2_lists(list1, list2):
    li_dif = [i for i in list1 + list2 if i not in list1 or i not in list2]
    return li_dif


def cal_average(lst):
    return round(sum(lst) / len(lst), 2)


def get_random_item_from_list(posilist: list) -> tuple:
    random_index = random.randint(0, len(posilist)-1)
    return posilist[random_index]


def random_split_list(inputlist, weight = 0.5):
    random.shuffle(inputlist)
    len_lst1 = int(weight * len(inputlist))
    return inputlist[0: len_lst1], inputlist[len_lst1:]
