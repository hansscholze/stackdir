import itertools
from collections import Counter
import stat
import pathlib as pl

abspath = pl.Path('/home/hans/utest')
roots = [abspath / pl.Path(r) for r in ('a', 'b', 'c')]

paths = dict(((p.relative_to(roots[0]), 0) for p in roots[0].iterdir()))

merges = set()

def is_dir(p):
    return stat.S_ISDIR(p.lstat().st_mode)

def add_path(roots, paths, merges, new_root_i, new_path):
    new_root = roots[new_root_i]
    path_rel = new_path.relative_to(new_root)
    try:
        old_root_i = paths.pop(path_rel)
    except KeyError:
        paths[path_rel] = new_root_i
    else:
        old_root = roots[old_root_i]
        old_path = old_root / path_rel
        if is_dir(old_path) and is_dir(new_path):
            merges.add(path_rel)
            for child_path in old_path.iterdir():
                child_path_rel = child_path.relative_to(old_root)
                assert child_path_rel not in paths
                paths[child_path_rel] = old_root_i
            for child_path in new_path.iterdir():
                add_path(roots, paths, merges, new_root_i, child_path)
        else:
            print('warning: {} shadows {}'.format(new_path, old_path))
            paths[path_rel] = new_root_i



def add(new_root_i, new_path):
    add_path(roots, paths, merges, new_root_i, new_path)

x=list(roots[1].iterdir())
add(1, x[0])

