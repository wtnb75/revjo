import shlex


def prefix(data) -> str:
    if isinstance(data, str):
        if data in ("true", "false", "") or data[0].isdigit() or data.startswith("-"):
            return "-s "
    return ""


def convert(data) -> str:
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
        return "\"$(jo -a -- " + " ".join(["{}{}".format(prefix(x), convert(x)) for x in data]) + ")\""
    elif isinstance(data, str):
        if data.startswith("@"):
            data = "\\"+data
        return shlex.quote(data)
    elif isinstance(data, dict):
        if len(data) == 0:
            return '{}'
        return "\"$(jo -- " + " ".join([
            "{}{}={}".format(prefix(v), convert(k), convert(v))
            for k, v in data.items()]) + ")\""
    else:
        raise ValueError("unsupported type: {}".format(type(data)))
