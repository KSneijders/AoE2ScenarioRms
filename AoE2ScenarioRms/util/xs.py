from typing import Any


def replace_xs_key(xs: str, key: str, value: str) -> str:
    return xs.replace(f"""/* REPLACE:{key} */""", value)


def to_xs_bool(v: Any) -> str:
    return 'true' if v else 'false'
