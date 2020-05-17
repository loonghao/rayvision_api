"""Test rayvision_api.tag.Tag functions."""

# pylint: disable=import-error
import pytest

from rayvision_api.exception import RayvisionAPIError
from rayvision_api.operators import ProjectSettings


@pytest.fixture()
def fixture_project(rayvision_connect):
    """Get a Tag object."""
    return ProjectSettings(rayvision_connect)


# pylint: disable=redefined-outer-name
def test_add_project(fixture_project, mock_requests, mocker):
    """Test if code ``504`` error we can get the corresponding error return."""
    return_value = {
        'code': 200, 'data': {},
    }
    mock_requests(return_value)
    new_name = "my_test_project"
    mock_project = mocker.patch.object(fixture_project, "get_projects")
    mock_project.return_value = [
        {u'projectId': 361971, u'projectName': u'my_test_project'},
        {u'projectId': 258871, u'projectName': u'build_test'}]
    new_project = fixture_project.create_project(new_name)
    assert new_project["projectName"] == new_name


def test_delete_project(fixture_project, mock_requests):
    """Test if code ``404`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 200, 'data': {},
            'message': 'Delete lable failed.'
        }
    )
    assert fixture_project.delete_project("my_render_project")


def test_get_project_list(fixture_project, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {"projectNameList": [
             {"projectId": 3671,
              "projectName": "myLabel"
              }
         ]}}
    )
    assert fixture_project.get_projects()[0]['projectId'] == 3671
    assert fixture_project.get_projects()[0]['projectName'] == 'myLabel'
