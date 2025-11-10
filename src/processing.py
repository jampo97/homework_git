def filter_by_state(all_dics, state_filter="EXECUTED") -> list:
    """" Функция фильтрации по состоянию(state)"""

    filtred_all_dics: list = []

    for dic in all_dics:
        if dic['state'] == state_filter:
            filtred_all_dics.append(dic)

    return filtred_all_dics

