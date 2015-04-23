import itertools
from collections import Counter
import stat
import pathlib as pl


def is_dir(p):
    return stat.S_ISDIR(p.lstat().st_mode)


def add_path(paths, roots, new_root_i, new_path):
    new_root = roots[new_root_i]
    path_rel = new_path.relative_to(new_root)
    if path_rel in paths:
        old_root_i = paths[path_rel]
        if old_root_i is None:
            add_dir(paths, roots, new_root_i, new_path)
        else:
            old_root = roots[old_root_i]
            old_path = old_root / path_rel
            if is_dir(old_path) and is_dir(new_path):
                paths[path_rel] = None
                add_dir(paths, roots, old_root_i, old_path)
                add_dir(paths, roots, new_root_i, new_path)
            else:
                print('warning: "{}" shadows "{}"'.format(new_path, old_path))
                paths[path_rel] = new_root_i
    else:
        paths[path_rel] = new_root_i


def add_dir(paths, roots, root_i, path):
    assert is_dir(path)
    for child_path in path.iterdir():
        add_path(paths, roots, root_i, child_path)


def add_roots(paths, roots):
    for i, root in enumerate(roots):
        add_dir(paths, roots, i, root)


abspath = pl.Path('/home/hans/utest')
roots = [abspath / pl.Path(r) for r in ('a', 'b', 'c')]
for r in roots: assert is_dir(r)

paths = {}

add_roots(paths, roots)


