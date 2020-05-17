"""Test rayvision_api.env.RenderEnv functions."""

# pylint: disable=import-error
import pytest

from rayvision_api.exception import RayvisionAPIError
from rayvision_api.operators import RenderConfig


# pylint: disable=redefined-outer-name
@pytest.fixture()
def fixture_render_config(rayvision_connect):
    """Initialize the user object."""
    return RenderConfig(rayvision_connect)


def test_add_render_env(fixture_render_config, render_env, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {
             'cgId': "2000",
             'cgName': 'Maya',
             'cgVersion': '2018',
             'renderLayerType': 0,
             'editName': 'my_test_render_config',
             'renderSystem': 1,
             'pluginIds': [2703]
         }})
    options = {'config_name': 'my_test_render_config',
               'app_version': '2018',
               "app_name": "maya"}
    assert fixture_render_config.create_render_config(**options)[
               'cgId'] == '2000'


def test_update_render_env(fixture_render_config, mocker, mock_requests):
    """Test if code ``404`` error we can get the corresponding error return."""
    mocker_config = mocker.patch.object(fixture_render_config,
                                        "get_render_config")
    mocker_config.return_value = {
        'cgId': "2000",
        'cgName': 'Maya',
        'cgVersion': '2018',
        'renderLayerType': 0,
        'editName': 'test_config',
        'renderSystem': 1,
        'pluginIds': [2703]}
    mock_requests({
        'code': 200,
        'data': {
            'cgId': "2000",
            'cgName': 'Maya',
            'cgVersion': '2019',
            'renderLayerType': 0,
            'editName': 'test_config',
            'renderSystem': 1,
            'pluginIds': [2703]},
        'message': 'Update render env failed.'
    })
    assert fixture_render_config.update_render_config(app_name="maya",
                                                      app_version="2019",
                                                      config_name="test",
                                                      plugin_ids=[1233])


def test_delete_render_config(fixture_render_config, mock_requests):
    """Test if we can delete is successful."""
    mock_requests(
        {
            'code': 200, 'data': {},
            'message': ''
        }
    )
    edit_name = 'test_ray'
    assert fixture_render_config.delete_render_config(edit_name)


def test_set_default_render_env(fixture_render_config, mock_requests):
    """Test if code ``600`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 600, 'data': {},
            'message': 'Set default render env failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        edit_name = 'test_ray'
        fixture_render_config.set_default_render_config(edit_name)
    assert 'Set default render env failed.' in str(err.value)


@pytest.mark.parametrize("test_data", [[{u'cgId': 2000,
                                         u'cgName': u'Maya',
                                         u'cgVersion': u'2018',
                                         u'editName': u'my_project',
                                         u'isDefault': 0,
                                         u'isMainUserId': 1,
                                         u'osName': 1,
                                         u'projectPath': u'',
                                         u'renderLayerType': 1,
                                         u'respUserPluginInfoVos': []},
                                        {u'cgId': 123,
                                         u'cgName': u'Maya',
                                         u'cgVersion': u'2018',
                                         u'editName': 'my_project_2',
                                         u'respUserPluginInfoVos': []}]])
def test_get_render_env(test_data, fixture_render_config, mock_requests):
    mock_requests(
        {
            "code": 200,
            "data": test_data,
        }
    )
    assert fixture_render_config.get_render_config("maya") == test_data
    data = fixture_render_config.get_render_config("maya",
                                                   config_name="my_project_2")
    assert data["cgId"] == 123


def test_get_render_env_failed(fixture_render_config):
    """Ensure we can catch the error message."""
    with pytest.raises(ValueError):
        fixture_render_config.get_render_config("test_name")


def test_supported_software(fixture_render_config, mock_requests):
    """Test get_supported_software this interface."""
    mock_requests(
        {
            "code": 200,
            'data': {u'cgPlugin': [],
                     u'cgVersion': [{u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_4.0_sp5b',
                                     u'id': 233},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_4.0_sp5',
                                     u'id': 213},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_4.0_sp4c',
                                     u'id': 211},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_4.0_sp4b',
                                     u'id': 203},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_4.0_sp4',
                                     u'id': 201},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_4.0_sp3',
                                     u'id': 190},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_4.0_sp2',
                                     u'id': 176},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_4.0_sp1',
                                     u'id': 165},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_4.0b',
                                     u'id': 157},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_3.6_sp9',
                                     u'id': 245},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_3.6_sp8',
                                     u'id': 149},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_3.6_sp7',
                                     u'id': 147},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_3.6_sp6',
                                     u'id': 145},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_3.6_sp5',
                                     u'id': 143},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_3.6_sp4',
                                     u'id': 141},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_3.6_sp2',
                                     u'id': 139},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_3.6_sp10',
                                     u'id': 243},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_3.6_sp1',
                                     u'id': 137},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_3.5_sp5',
                                     u'id': 186},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'clarisse_ifx_3.5_sp2',
                                     u'id': 163},
                                    {u'cgId': 2013,
                                     u'cgName': u'Clarisse',
                                     u'cgVersion': u'Clarisse_BUiLDER',
                                     u'id': 223}]}}
    )
    info = fixture_render_config.get_plugins("clarisse")
    assert isinstance(info["cgPlugin"], list)
    assert info["cgVersion"][0]["cgName"] == "Clarisse"
