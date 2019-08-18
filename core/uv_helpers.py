"""
module information : collection UV light functions

Author: Shanmugathas Vigneswaran
email: shanmugathas.vigneswaran@outlook.fr

Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
Licence:  https://creativecommons.org/licenses/by-nc/4.0/

"""

UV_INDEX: list = ['UV1',
                  'UV2',
                  'UV3',
                  'UV4',
                  'UV5',
                  'UV6',
                  'UV7',
                  'UV8',
                  'UV10']


def get_uv_index(milli_volt: float) -> str:
    """
    get light UV index
    for analog sensors: SENS-43UV
    :param milli_volt:
    :return:
    """
    assert isinstance(milli_volt, float)
    offset: float = 5.

    if milli_volt < 227-offset:
        raise ValueError('Value < {val} milliVolt'.format(val=227-offset))
    elif 227-offset < milli_volt < 227+offset:
        return UV_INDEX[0]
    elif 318-offset < milli_volt < 318+offset:
        return UV_INDEX[1]
    elif 408-offset < milli_volt < 408+offset:
        return UV_INDEX[2]
    elif 503-offset < milli_volt < 503+offset:
        return UV_INDEX[3]
    elif 606-offset < milli_volt < 606+offset:
        return UV_INDEX[4]
    elif 696-offset < milli_volt < 696+offset:
        return UV_INDEX[5]
    elif 795-offset < milli_volt < 795+offset:
        return UV_INDEX[6]
    elif 881-5 < milli_volt < 881+offset:
        return UV_INDEX[7]
    elif 976-offset < milli_volt < 976+offset:
        return UV_INDEX[8]
    elif 1170-offset < milli_volt < 1170+offset:
        return UV_INDEX[9]
    elif milli_volt > 1170+offset:
        raise ValueError('Value > {val} milliVolt'.format(val=1170-offset))