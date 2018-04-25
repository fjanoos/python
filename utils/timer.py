'''
timing utils
'''

import time


class Timer():
    FORMATTER = '{} took {:0.2f} seconds'.format


    def __init__(self, task='task', verbose=True):
        self.task=task
        self.verbose=verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.stop = time.time();
        self.elapsed = self.stop - self.start;
        if args and args[1]:
            (type, value, traceback) = args
            message = '''
            \t{task} : !!! EXCEPTION !!!
            \t{task} : : {value!r}
            '''.format(task=self.task, value=value);
            print(message);
            raise value;
        if self.verbose:
            print(self.FORMATTER(self.task, self.elapsed));
