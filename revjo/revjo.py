import shlex


def prefix(data) -> str:
    if isinstance(data, str):
        if data in ("true", "false", "") or data[0].isdigit() or data.startswith("-"):
            return "-s "
    return ""


def convert(data, pre="", post="") -> str:
    if data is None:
        return "null"
    elif isinstance(data, bool):
        if data:
            return "true"
        else:
            return "false"
    elif isinstance(data, (int, float)):
        return str(data)
    elif isinstance(data, (list, tuple)):
        return pre + "-a -- " + " ".join(
            ["{}{}".format(prefix(x), convert(x, pre="\"$(jo ", post=")\""))
             for x in data]) + post
    elif isinstance(data, str):
        if data.startswith("@"):
            data = "\\"+data
        return shlex.quote(data)
    elif isinstance(data, dict):
        if len(data) == 0:
            return '{}'
        res = pre + " ".join([
            "{}{}={}".format(prefix(v), convert(k), convert(v, pre="\"$(jo ", post=")\""))
            for k, v in data.items()]) + post
        if res.startswith("-"):
            return "-- "+res
        return res
    else:
        raise ValueError("unsupported type: {}".format(type(data)))
