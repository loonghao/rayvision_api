"""Test rayvision_api.UserOperator.UserOperator functions."""

# pylint: disable=import-error
import pytest

from rayvision_api.exception import RayvisionAPIError
from rayvision_api.operators import UserProfile


@pytest.fixture()
def user_operator(rayvision_connect, mock_requests):
    """Get a UserOperator object."""
    return UserProfile(rayvision_connect, auto_login=False)


# pylint: disable=redefined-outer-name
def test_query_user_profile(user_operator, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {
             "UserID": 10001136,
             "UserName": "rayvision",
             "platform": 2,
             "phone": "15945467254",
         }})
    assert user_operator.query_user_profile()['UserID'] == 10001136
    assert user_operator.query_user_profile()['UserName'] == "rayvision"
    assert user_operator.query_user_profile()['platform'] == 2
    assert user_operator.query_user_profile()['phone'] == "15945467254"


def test_query_user_setting(user_operator, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {
             "taskOverTime": 1216165,
             "singleNodeRenderFrames": "1",
             "shareMainCapital": 0,
             "subDeleteTask": 0,
         }})
    assert user_operator.query_user_setting()['taskOverTime'] == 1216165
    assert user_operator.query_user_setting()['singleNodeRenderFrames'] == "1"
    assert user_operator.query_user_setting()['shareMainCapital'] == 0
    assert user_operator.query_user_setting()['subDeleteTask'] == 0


def test_update_user_setting(user_operator, mock_requests):
    """Test if code ``404`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 404, 'data': {},
            'message': 'Update UserOperator setting failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        task_over_time = 2582
        user_operator.update_user_setting(task_over_time)
    assert 'Update UserOperator setting failed.' in str(str(err.value))


# pylint: disable=redefined-outer-name
def test_platforms(user_operator, mock_requests):
    """Test query all render_platforms."""
    mock_requests({'code': 200,
                   'data': [{'platform': 2,
                             'name': 'platform2'},
                            {'platform': 3,
                             'name': 'platform3'}]})
    assert user_operator.platforms()[0]['platform'] == 2


def test_error_detail(user_operator, mock_requests):
    """Test we can get correct error message."""
    mock_requests({'code': 200, 'data': [{'code': 12345,
                                          'solutionPath': 'c:/tests.com'}]})
    details = user_operator.error_detail(12345)
    assert details[0]['code'] == 12345
    assert details[0]['solutionPath'] == 'c:/tests.com'


def test_get_task_list(user_operator, mock_requests):
    """Test if code ``404`` error we can get the corresponding error return."""
    mock_requests({'code': 404, 'data': {}, 'message': 'Get task failed.'})
    with pytest.raises(RayvisionAPIError) as err:
        user_operator.get_task_list()
    assert 'Get task failed.' in str(err.value)


def test_get_transfer_server_msg(user_operator, mock_requests):
    """Test get_supported_software this interface."""
    mock_requests(
        {'data': {
            'raysyncTransfer': {
                'port': 2542,
                'proxyIp': 'render.raysync.cn',
                'proxyPort': 32011,
                'serverIp': '127.0.0.1',
                'serverPort': 2121,
                'sslPort': 2543
            }
        }}
    )
    info = user_operator.get_transfer_server_config()['raysyncTransfer']
    assert info['port'] == 2542
    assert info['proxyIp'] == 'render.raysync.cn'
    assert info['proxyPort'] == 32011
    assert info['serverIp'] == '127.0.0.1'
    assert info['serverPort'] == 2121
    assert info['sslPort'] == 2543


def test_get_raysync_user_key(user_operator, mock_requests):
    """Test get_supported_software this interface."""
    mock_requests(
        {"code": 200,
         'data': {
             'raySyncUserKey': '8ccb94d67c1e4c17fd0691c02ab7f753cea64e3d',
             'userName': 'test',
             'platform': 2,
         }}
    )
    info = user_operator.get_raysync_user_key()
    assert info['raySyncUserKey'] == '8ccb94d67c1e4c17fd0691c02ab7f753cea64e3d'
    assert info['userName'] == 'test'
    assert info['platform'] == 2
