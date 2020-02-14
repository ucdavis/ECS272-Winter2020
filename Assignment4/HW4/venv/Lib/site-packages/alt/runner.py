from alt.common import get_default_logger, format_time
import sys
import time


LINE_DELIMITER = "="*70


class AltRunner:
    def __init__(self, test_data, logger=None):
        self.test_data = test_data
        if logger is None:
            logger = get_default_logger()
        self.logger = logger

    @staticmethod
    def import_test_module(name):
        m = __import__(name)
        for n in name.split(".")[1:]:
            m = getattr(m, n)
        return m

    def run(self):
        self.logger.debug("Starting {}...".format(self.__class__.__name__))
        start = time.time()
        passed = []
        failed = []
        skipped = []
        test_num = 1
        for bvt in self.test_data['test_suites']:
            module = self.import_test_module(bvt['module_name'])
            class_ = getattr(module, bvt['class_name'])
            my_class = class_()
            tests = bvt['tests']
            for test in tests:
                sub_test_num = 1
                name = test['name']
                test_func = getattr(my_class, name)
                for data_set in test['data_points']:
                    invalid_args = {'logger', 'test_number', 'param_set_number'}.intersection(data_set)
                    if invalid_args:
                        raise ValueError('You cannot use the following arguments in tests: {}'.format(", ".join(invalid_args)))
                    try:
                        self.logger.debug("=" * 70)
                        data_set['test_number'] = test_num
                        data_set['param_set_number'] = sub_test_num
                        data_set['logger'] = self.logger
                        sub_test_num += 1
                        test_obj = test_func(**data_set)
                        if test_obj.test_skipped is True:
                            skipped.append(test_obj)
                        elif test_obj.test_passed is True:
                            passed.append(test_obj)
                        else:
                            failed.append(test_obj)
                    except Exception as e:
                        self.logger.error("Test failed", exc_info=True)
                        self.logger.error("Test failed: {}".format(e), file=sys.stderr)
                        sys.exit(1)
                test_num += 1
        self.logger.debug(LINE_DELIMITER)
        self.logger.debug(LINE_DELIMITER)
        total = len(passed) + len(failed) + len(skipped)
        self.logger.debug("{}/{} Passed: ".format(len(passed), total))
        for test in passed:
            self.logger.debug(test)
        self.logger.debug(LINE_DELIMITER)
        self.logger.debug("{}/{} Failed: ".format(len(failed), total))
        for test in failed:
            self.logger.debug(test)
        self.logger.debug(LINE_DELIMITER)
        self.logger.debug("{}/{} Skipped: ".format(len(skipped), total))
        for test in skipped:
            self.logger.debug(test)
        self.logger.debug(LINE_DELIMITER)
        self.logger.debug("Elapsed time: {}".format(format_time(time.time() - start)))