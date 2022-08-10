def replace_xs_key(xs: str, key: str, value: str) -> str:
    return xs.replace(f"""/* REPLACE:{key} */""", value)
