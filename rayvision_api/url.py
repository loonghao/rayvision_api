# Import built-in modules
from enum import Enum

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache


@lru_cache(maxsize=2)
def assemble_api_url(domain, api_url, protocol_type='https'):
    """Assemble the requests api url.

    Args:
        domain (str): The domain of the render farm.
        api_url (str): The url of the operator.
        protocol_type (str, optional): The type of the protocol

    Returns:
        str: Assembled url address for the API.

    """
    return "{}://{}{}".format(protocol_type, domain, api_url)


class ApiUrl(str, Enum):
    """Enumeration type class related to API URL."""
    queryPlatforms = "/api/render/common/queryPlatforms"
    queryUserProfile = "/api/render/user/queryUserProfile"
    queryUserSetting = "/api/render/user/queryUserSetting"
    updateUserSetting = "/api/render/user/updateUserSetting"
    getTransferBid = '/api/render/task/getTransferBid'
    createTask = '/api/render/task/createTask'
    submitTask = '/api/render/task/submitTask'
    queryErrorDetail = '/api/render/common/queryErrorDetail'
    getTaskList = '/api/render/task/getTaskList'
    stopTask = '/api/render/task/stopTask'
    startTask = '/api/render/task/startTask'
    abortTask = '/api/render/task/abortTask'
    deleteTask = '/api/render/task/deleteTask'
    queryTaskFrames = '/api/render/task/queryTaskFrames'
    queryAllFrameStats = '/api/render/task/queryAllFrameStats'
    restartFailedFrames = '/api/render/task/restartFailedFrames'
    restartFrame = '/api/render/task/restartFrame'
    queryTaskInfo = '/api/render/task/queryTaskInfo'
    addLabel = '/api/render/common/addLabel'
    deleteLabel = '/api/render/common/deleteLabel'
    getLabelList = '/api/render/common/getLabelList'
    querySupportedSoftware = '/api/render/common/querySupportedSoftware'
    querySupportedPlugin = '/api/render/common/querySupportedPlugin'
    addRenderEnv = '/api/render/common/addRenderEnv'
    updateRenderEnv = '/api/render/common/updateRenderEnv'
    deleteRenderEnv = '/api/render/common/deleteRenderEnv'
    setDefaultRenderEnv = '/api/render/common/setDefaultRenderEnv'
    getRenderEnv = '/api/render/common/getRenderEnv'
    updateTaskUserLevel = "/api/rendering/task/renderingTask/updateTaskUserLevel"  # pylint: disable=line-too-long
    getRaySyncUserKey = '/api/render/user/getRaySyncUserKey'
    getTransferServerMsg = '/api/render/task/getTransferServerMsg'
    loadTaskProcessImg = "/api/render/task/loadTaskProcessImg"
    setOverTimeStop = "/api/render/task/setOverTimeStop"
    loadingFrameThumbnail = '/api/render/task/loadingFrameThumbnail'
    fullSpeed = '/api/render/task/fullSpeed'
