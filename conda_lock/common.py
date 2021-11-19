import json
import os
import pathlib

from itertools import chain
from typing import Dict, Iterable, List, TypeVar


T = TypeVar("T")


def get_in(keys, nested_dict, default=None):
    """
    >>> foo = {'a': {'b': {'c': 1}}}
    >>> get_in(['a', 'b'], foo)
    {'c': 1}

    """
    import operator

    from functools import reduce

    try:
        return reduce(operator.getitem, keys, nested_dict)
    except (KeyError, IndexError, TypeError):
        return default


def read_file(filepath: str) -> str:
    with open(filepath, mode="r") as fp:
        return fp.read()


def write_file(obj: str, filepath: str) -> None:
    with open(filepath, mode="w") as fp:
        fp.write(obj)


def read_json(filepath: str) -> Dict:
    with open(filepath, mode="r") as fp:
        return json.load(fp)


def ordered_union(collections: Iterable[Iterable[T]]) -> List[T]:
    return list({k: k for k in chain.from_iterable(collections)}.values())


def relative_path(source: pathlib.Path, target: pathlib.Path) -> str:
    """
    Get posix representation of the relative path from the parent of `source` to `target`
    """
    source_abs = pathlib.PurePosixPath(source.parent.resolve())
    target_abs = pathlib.PurePosixPath(target.resolve())
    common = pathlib.PurePosixPath(os.path.commonpath((source_abs, target_abs)))
    up = [".."] * len(source_abs.relative_to(common).parents)
    down = target_abs.relative_to(common)
    return str(pathlib.PurePosixPath(*up) / down)
