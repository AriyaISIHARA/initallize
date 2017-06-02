import os
import re


class Initallize(object):
    def __init__(self, dname):
        self._read_init(dname)

    def write(self, file):
        file.write(self._before_all)
        file.write(self._blank_lines)
        print("__all__ = (", file=file)
        for iden in self._gen_identifiers():
            print(f"    '{iden}',", file=file)
        print(")", file=file)

    def _read_init(self, dname):
        init_file = os.path.join(dname, '__init__.py')
        with open(init_file) as fin:
            buf = fin.read()
        m = re.search(r'^__all__\s*=', buf, re.MULTILINE)
        if m:
            before_all = buf[:m.start()]
            self._blank_lines = ''
        else:
            before_all = buf
            self._blank_lines = '\n\n'
        names = []
        code = re.sub(r'#.+$|\\\n', '', before_all, flags=re.MULTILINE)
        for m in re.finditer(
                r'^(?:from\s+\.?\w+\s+)?'
                r'import(?:\s+\.?\w+\s+as)?\s+\.?(\w+)\s*$',
                code, flags=re.MULTILINE
        ):
            names.append(m.group(1))
        for m_outer in re.finditer(
                r'^(?:from\s+\.?\w+\s+)?import\s+\(\s*(.+?)\s*\)',
                code, flags=(re.MULTILINE | re.DOTALL)
        ):
            for m in re.finditer(
                    r'(?:\.?\w+\s+as\s+)?\b\.?(\w+)\s*(?:,|$)',
                    m_outer.group(1), flags=re.MULTILINE
            ):
                names.append(m.group(1))
        self._before_all = before_all
        self._identifiers = names

    def _gen_identifiers(self):
        lowers = []
        camels = []
        uppers = []
        for iden in self._identifiers:
            if iden.islower():
                lowers.append(iden)
            elif iden.isupper():
                uppers.append(iden)
            else:
                camels.append(iden)
        yield from sorted(lowers)
        yield from sorted(camels)
        yield from sorted(uppers)


def proc_dir(dname):
    i = Initallize(dname)
    with open(os.path.join(dname, '__init__.py'), 'w') as fout:
        i.write(fout)


def proc_dirs(rootdir):
    for path, dirs, files in os.walk(rootdir):
        for dname in dirs:
            dpath = os.path.join(path, dname)
            inifile = os.path.join(dpath, '__init__.py')
            if not os.path.isfile(inifile):
                continue
            print('initallize', dpath, '...', end='', flush=True)
            proc_dir(dpath)
            print('ok')


if __name__ == '__main__':
    import sys
    proc_dirs(sys.argv[1])
