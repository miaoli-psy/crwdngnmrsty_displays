def get_diff_between_2_lists(list1, list2):
    li_dif = [i for i in list1 + list2 if i not in list1 or i not in list2]
    return li_dif