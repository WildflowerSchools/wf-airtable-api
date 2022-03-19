def get_first_or_default_none(v):
    if len(v) > 0:
        return v[0]
    else:
        return None


def get_first_or_default_dict(v):
    if len(v) > 0:
        return v[0]
    else:
        return {}
