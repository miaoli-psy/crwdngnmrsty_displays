import ast


def str_to_list(string: str) -> list:
    """
    convert list-like str to list
    :param string: "[(0, 100), (105, 10) ...]"
    :return: list of tuples
    """
    return ast.literal_eval(string)