def filter_by_state(all_dicts: list[dict], state_filter: str | None = "EXECUTED") -> list[dict]:
    """Функция фильтрации по состоянию(state)"""

    filtered_all_dicts: list[dict] = []

    for person in all_dicts:
        if person["state"] == state_filter:
            filtered_all_dicts.append(person)

    return filtered_all_dicts


def sort_by_date(all_dicts: list[dict], sorting_rule: bool | None = True) -> list[dict]:
    """Функция сортировки по дате. По умолчанию - возрастание"""

    sorted_list: list[dict] = []

    if sorting_rule is True:
        sorted_list = sorted(all_dicts, key=lambda x: x["date"], reverse=False)
    else:
        sorted_list = sorted(all_dicts, key=lambda x: x["date"], reverse=True)

    return sorted_list


print(
    sort_by_date(
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        ],
    )
)
