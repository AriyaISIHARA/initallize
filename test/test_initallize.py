import os
from unittest import TestCase


def _request_new_dir(rootdir, prefix, trial=100):
    err = None
    for t in range(trial):
        dname = os.path.join(rootdir, f'{prefix}{t}')
        try:
            os.mkdir(dname)
            break
        except OSError as e:
            err = e
    else:
        raise err
    return dname


class InitallizeTest(TestCase):
    def test_with_all(self):
        self._test_initallize('with_all')

    def test_without_all(self):
        self._test_initallize('without_all')

    def _test_initallize(self, name):
        from io import StringIO
        import shutil

        from initallize import Initallize

        rootdir = os.path.dirname(__file__)
        in_src = os.path.join(rootdir, f'input_{name}_py.src')
        out_src = os.path.join(rootdir, f'output_{name}_py.src')
        module_dir = _request_new_dir(rootdir, 'tmp_module_')
        init_fpath = os.path.join(module_dir, '__init__.py')
        module_fpath = os.path.join(module_dir, 'inner_module.py')

        with open(out_src) as fin:
            expected_result = fin.read()

        shutil.copy(in_src, init_fpath)
        result = None
        with StringIO() as sio:
            Initallize(module_dir).write(sio)
            result = sio.getvalue()
        self.assertIsNotNone(result)

        self.maxDiff = None
        self.assertEqual(result, expected_result)
