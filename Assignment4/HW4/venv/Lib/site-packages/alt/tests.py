import time
from alt.common import get_default_logger, format_time


def test_decorator(func):
    def test_executor(self, *args, **kwargs):
        logger = kwargs.get('logger', get_default_logger())
        if 'url' in kwargs:
            kwargs['url'] = kwargs['url'].format(**kwargs)
        if 'endpoint' in kwargs:
            kwargs['endpoint'] = kwargs['endpoint'].format(**kwargs)
        if 'baseurl' in kwargs:
            kwargs['baseurl'] = kwargs['baseurl'].format(**kwargs)
        test = Test(logger, kwargs.get('test_number', "?"), kwargs.get('param_set_number', "?"), func, self, args,
                    kwargs, skip=kwargs.get('skip_test', False), nickname=kwargs.get('nickname', None))
        test.execute()
        return test
    return test_executor


class Test:
    def __init__(self, logger, test_number, param_set_number, test_func, param_self, param_args, param_kwargs, skip=False, nickname=None):
        self.logger = logger
        self.test_func = test_func
        self.param_self = param_self
        self.param_args = param_args
        self.param_kwargs = param_kwargs
        self.test_suite = param_self.__class__.__name__
        self.test_name = test_func.__name__
        self.test_number = test_number
        self.param_set_number = param_set_number
        self.test_skipped = skip
        self.nickname = nickname
        self.executed = False
        self.elapsed_time = 0
        self.test_passed = False

    def execute(self):
        if self.test_skipped is True:
            self.logger.debug("Skipping test: {}".format(self))
            return
        if self.executed is True:
            raise ValueError("Test already executed")
        start = time.time()
        self.logger.debug("Starting test: {}".format(self))
        try:
            self.test_func(self.param_self, *self.param_args, **self.param_kwargs)
            self.test_passed = True
        except:
            self.logger.error("error", exc_info=True)
        self.executed = True
        self.elapsed_time = time.time() - start
        self.logger.debug("Finished test: {}".format(self))

    def __str__(self):
        test_prefix = "#{}.{} {} {}".format(self.test_number, self.param_set_number, self.test_suite, self.test_name)
        if self.nickname is not None:
            test_prefix += " ({})".format(self.nickname)
        if not self.executed:
            return "{} - Not Executed".format(test_prefix)
        else:
            return "{} - ({}) Result: {} ".format(test_prefix, format_time(self.elapsed_time),
                                                  'Passed' if self.test_passed is True else 'Failed')