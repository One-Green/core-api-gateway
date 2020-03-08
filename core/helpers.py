"""
module information : collection of helper functions

Author: Shanmugathas Vigneswaran
email: shanmugathas.vigneswaran@outlook.fr

Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
Licence:  https://creativecommons.org/licenses/by-nc/4.0/

"""

from multiprocessing import Process


def run_parallel(*fns):
    """
    run multiprocessing function
    source = https://stackoverflow.com/questions/7207309/python-how-can-i-run-python-functions-in-parallel
    :param fns:
    :return:
    """
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()
