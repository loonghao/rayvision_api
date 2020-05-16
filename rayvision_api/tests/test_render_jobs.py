"""Test rayvision_api.task.Task functions."""

# pylint: disable=import-error
import pytest

from rayvision_api.exception import RayvisionAPIError
from rayvision_api.exception import RayvisionAPIParameterError
from rayvision_api.operators import RenderJobs


@pytest.fixture()
def fixture_render_jobs(rayvision_connect):
    """Get a Task object."""
    return RenderJobs(rayvision_connect)


# pylint: disable=redefined-outer-name
def test_create_task(fixture_render_jobs, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {
             "taskIdList": [1658434],
             "aliasTaskIdList": ['2W1658434'],
             "userId": 100093066
         }})
    assert fixture_render_jobs._create_task()['taskIdList'] == [1658434]
    assert fixture_render_jobs._create_task()['aliasTaskIdList'] == [
        '2W1658434']
    assert fixture_render_jobs._create_task()['userId'] == 100093066


def test_submit_task(fixture_render_jobs, mock_requests):
    """Test if code ``404`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 404, 'data': {},
            'message': 'Submit task failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        task_id = 564642
        fixture_render_jobs.submit_task(task_id)
    assert 'Submit task failed.' in str(err.value)


def test_stop_task(fixture_render_jobs, mock_requests):
    """Test if code ``604`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 604, 'data': {},
            'message': 'Stop task failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        task_param_list = ["336463", "469733"]
        fixture_render_jobs.stop_task(task_param_list)
    assert 'Stop task failed.' in str(err.value)


def test_start_task(fixture_render_jobs, mock_requests):
    """Test if code ``604`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 604, 'data': {},
            'message': 'Start task failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        task_param_list = ["456463", "469633"]
        fixture_render_jobs.start_task(task_param_list)
    assert 'Start task failed.' in str(err.value)


def test_abort_task(fixture_render_jobs, mock_requests):
    """Test if code ``604`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 604, 'data': {},
            'message': 'Abort task failed.'
        }
    )
    with pytest.raises(RayvisionAPIError) as err:
        task_param_list = ["456463", "462582"]
        fixture_render_jobs.abort_task(task_param_list)
    assert 'Abort task failed.' in str(err.value)


def test_delete_task(fixture_render_jobs, mock_requests):
    """Test if code ``601`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 601, 'data': {},
            'message': 'Delete task failed.'
        }
    )
    with pytest.raises(RayvisionAPIParameterError) as err:
        task_param_list = ["996463", "462582"]
        fixture_render_jobs.delete_task(task_param_list)
    assert 'Delete task failed.' in str(err.value)


@pytest.mark.parametrize('task_id, task_level', [
    (661616, 20),
    (661216, -20),
    (6616, 120),
    (6616, 500),
])
def test_update_job_priority(fixture_render_jobs, mock_requests, task_id,
                             task_level):
    """Test if code ``601`` error we can get the corresponding error return."""
    mock_requests(
        {
            'code': 200, 'data': {},
            'message': 'Update task level failed.'
        }
    )
    assert fixture_render_jobs.update_priority(task_id, task_level)


def test_all_frame_status(fixture_render_jobs, mock_requests):
    """Test that we can go to all frame states."""
    mock_requests(
        {'code': 200,
         'data': {
             'executingFramesTotal': 0, 'doneFramesTotal': 11,
             'failedFramesTotal': 230, 'waitingFramesTotal': 0,
             'totalFrames': 241,
         }})
    job_status = fixture_render_jobs.get_all_job_frame_status()
    assert job_status['totalFrames'] == 241
    assert job_status['waitingFramesTotal'] == 0
