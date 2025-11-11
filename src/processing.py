def filter_by_state(all_dics: list, state_filter: str = "EXECUTED") -> list:
    """ Функция фильтрации по состоянию(state)"""

    filtred_all_dics: list = []

    for dic in all_dics:
        if dic["state"] == state_filter:
            filtred_all_dics.append(dic)

    return filtred_all_dics


def sort_by_date(all_dics: list, sorting_rule: str) -> list:
    """Функция сортировки по дате. По умолчанию - убывание"""

    sorted_list: list = []

    if sorting_rule == "reverse":
        sorted_list = sorted(all_dics, key=lambda dic: dic["date"], reverse=False)
    else:
        sorted_list = sorted(all_dics, key=lambda dic: dic["date"], reverse=True)

    return sorted_list
