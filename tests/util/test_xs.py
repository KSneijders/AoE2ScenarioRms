from AoE2ScenarioRms.util import XsUtil


def test_xs_bool():
    assert XsUtil.bool(True) == 'true'
    assert XsUtil.bool(False) == 'false'


def test_xs_constant():
    assert XsUtil.constant('my') == 'MY'
    assert XsUtil.constant('my_name') == 'MY_NAME'
    assert XsUtil.constant('my name') == 'MY_NAME'
    assert XsUtil.constant('my   name') == 'MY_NAME'
    assert XsUtil.constant('my name is') == 'MY_NAME_IS'
    assert XsUtil.constant('my name_IS') == 'MY_NAME_IS'
