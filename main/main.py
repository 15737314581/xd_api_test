import unittest
import os
from case.xdclass_api_test import XdclassTestCase

# def load_all_case():
#     """加载全部测试用例"""
#     case_path = os.path.join(os.getcwd(), "case")
#     discover = unittest.defaultTestLoader.discover(case_path, pattern="*Case.py", top_level_dir=None)
#     return discover
#
# if __name__ == '__main__':
#     runner = unittest.TextTestRunner(verbosity=2)
#     runner.run(load_all_case())

if __name__ == '__main__':
    app = XdclassTestCase()
    app.runAllCase("小滴课堂")