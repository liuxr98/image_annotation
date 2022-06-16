from uuid import uuid4


def make_unique(string):
    ident = uuid4().__str__()
    return f"{ident}-{string}"


