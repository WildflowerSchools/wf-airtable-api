def get_first_or_default_provided(v):
    if isinstance(v, list) and len(v) > 0:
        return v[0]
    else:
        return v


def get_first_or_default_none(v):
    if isinstance(v, list) and len(v) > 0:
        return v[0]
    else:
        return None


def get_first_or_default_dict(v):
    if isinstance(v, list) and len(v) > 0:
        return v[0]
    else:
        return {}
