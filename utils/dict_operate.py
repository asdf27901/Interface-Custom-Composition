from contextlib import suppress


def update_dict(d1: dict, d2: dict) -> None:
    if not isinstance(d1, dict) or not isinstance(d2, dict):
        raise TypeError('Params of update_dict should be dict')
    for i in d1:
        if d2.get(i, None):
            if isinstance(d1[i], list):
                d1[i] = [d2[i]]
            else:
                d1[i] = d2[i]
        if isinstance(d1[i], dict):
            update_dict(d1[i], d2)


def delete_keys_from_dict_by_keys(need_dele_dict: dict, keys: list) -> None:
    for key in keys:
        with suppress(KeyError):
            del need_dele_dict[key]

    for value in need_dele_dict.values():
        if isinstance(value, dict):
            delete_keys_from_dict_by_keys(value, keys)


def get_model_dict(d: dict) -> dict:
    pop = []
    for key in d.keys():
        if not d[key] and key in ['query', 'body', 'data']:
            pop.append(key)

    for i in pop:
        d.pop(i)
    return d


def set_none_to_null(d: dict) -> None:
    for key, value in d.items():
        if isinstance(value, dict):
            set_none_to_null(d[key])
        else:
            if value in ['None', 'null', 'none', 'Null', 'NULL']:
                d[key] = None


def whether_dict_in_dict(dict_a: dict, dict_b: dict) -> bool:
    flag = False
    for key in dict_a:
        if dict_b.get(key, None) and dict_a[key] == dict_b[key]:
            return True

        if isinstance(dict_a[key], dict):
            return whether_dict_in_dict(dict_a[key], dict_b)

    return flag
