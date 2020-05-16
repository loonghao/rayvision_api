"""Interface to operate on the task."""
try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

from rayvision_api.exception import RayvisionError


class RenderJobs(object):
    """API task related operations."""

    TASK_PARAM = "taskIds"

    def __init__(self, connect):
        """Initialize instance.

        Args:
            connect (rayvision_api.connect.Connect): The connect instance.

        """
        self._connect = connect
        self._has_submit = False
        self._task_id = None

    def _create_task(self,
                     count=1,
                     task_user_level=50,
                     out_user_id=None,
                     labels=None):
        """Create a task ID.

        Args:
            count (int, optional): The quantity of task ID.
            task_user_level (int): Set the user's task level to either 50 or
                60, default is 50.
            out_user_id (int, optional): Non-required, external user ID, used
                to distinguish users accessing third parties.
            labels (list or tuple, optional): Custom task labels.

        Returns:
            dict: The information of the task.
                e.g.:
                    {
                        "taskIdList": [1658434],
                        "aliasTaskIdList": [2W1658434],
                        "userId": 100093088
                    }

        """
        data = {
            'count': count,
            'taskUserLevel': task_user_level
        }
        if out_user_id:
            data['outUserId'] = out_user_id
        if labels:
            data['labels'] = labels
        return self._connect.post(self._connect.url.createTask, data)

    def _generate_task_id(self):
        """Get task id.

        Example::

            task_id_info = {
                    "taskIdList": [1658434],
                    "aliasTaskIdList": [2W1658434],
                    "userId": 100093088
                }

        Returns:
            int: The ID number of the task.

        """
        if not self._has_submit and self._task_id:
            return self._task_id
        task_id_info = self._create_task(count=1, out_user_id=None)
        task_id_list = task_id_info.get("taskIdList")
        if not task_id_list:
            raise RayvisionError(1000000, 'Failed to create task number!')
        self._task_id = task_id_list[0]
        self._has_submit = False
        return self._task_id

    @property
    def task_id(self):
        """int: The ID number of the render task.

        Notes:
            As long as we do not initialize the class again or submit the task
            successfully, we can always continue to get the task id from the
            class instance.

        """
        return self._generate_task_id()

    def submit_task(self,
                    info,
                    asset_lsolation_model=None,
                    out_user_id=None,
                    only_id=False):
        """Submit a task to rayvision render farm.

        Args:
            task_id (int): Submit task ID.
            asset_lsolation_model (str): Asset isolation type, Optional value,
                default is null, optional value:'TASK_ID_MODEL' or 'OUT_USER_MODEL'.
            out_user_id (str): The asset isolates the user ID, Optional value,
                when asset_lsolation_model='OUT_USER_MODEL' ,'out_user_id'
                cant be empty.

        """
        data = {
            "taskId": self.task_id
        }
        if asset_lsolation_model:
            data["assetIsolationModel"] = asset_lsolation_model
        if out_user_id:
            data["outUserId"] = out_user_id.strip()
        data.update(info)
        task_info = self._connect.post(self._connect.url.submitTask, data)
        if only_id:
            return self.task_id
        self._has_submit = True
        return task_info

    def stop_task(self, task_param_list):
        """Stop the task.

        Args:
            task_param_list (list): Task ID list.

        """
        return self._connect.post(self._connect.url.stopTask,
                                  {self.TASK_PARAM: task_param_list})

    def start_task(self, task_param_list):
        """Start task.

        Args:
            task_param_list (list): Task ID list.

        """
        return self._connect.post(self._connect.url.startTask,
                                  {self.TASK_PARAM: task_param_list})

    def abort_task(self, task_param_list):
        """Give up the task.

        Args:
            task_param_list (list): Task ID list.

        """
        return self._connect.post(self._connect.url.abortTask,
                                  {self.TASK_PARAM: task_param_list})

    def delete_task(self, task_param_list):
        """Delete task.

        Args:
            task_param_list (list): Task ID list.

        """
        return self._connect.post(self._connect.url.deleteTask,
                                  {self.TASK_PARAM: task_param_list})

    def update_priority(self, task_id, priority):
        """Update the render priority for the task by given task id.

        Args:
            task_id (int): The ID number of the render task.
            priority (int): The priority for the current render task.

        """
        data = {
            "taskId": task_id,
            "taskUserLevel": priority,
        }
        self._connect.post(self._connect.url.updateTaskUserLevel, data)
        return True

    def set_job_overtime_top(self, task_id_list, overtime):
        """Set the task timeout stop time.

        Args:
            task_id_list (list of int): Task list.
            overtime (int or float): Timeout time, unit: second.
            Example:
                {
                    "taskIds":[485],
                    "overTime":1800
                }
        """
        data = {
            'taskIds': task_id_list,
            'overTime': overtime
        }
        return self._connect.post(self._connect.url.setOverTimeStop, data)

    def set_full_speed_render(self, task_id_list):
        """Full to render.

        Args:
            task_id_list (list of int): Task list.
            Example:
                {
                    "taskIds":[485],
                }
        """
        data = {
            'taskIds': task_id_list,
        }
        return self._connect.post(self._connect.url, data)

    @lru_cache(maxsize=2)
    def get_task_list(self, page_num=1, page_size=2, status_list=None,
                      search_keyword=None,
                      start_time=None, end_time=None):
        """Get task list.

        An old to the new row, the old one.

        Args:
            page_num (int): Required value, current page.
            page_size (int): Required value, numbers displayed per page.
            status_list (list of int): status code list, query the status of
                the task in the list.
            search_keyword (string): Optional, scenario name or job ID.
            start_time (string): Optional, search limit for start time.
            end_time (string): Optional, search limit for end time.

        Returns:
            dict: Task profile, please see the documentation for details.
                e.g.:
                    {
                        "pageCount": 32,
                        "pageNum": 1,
                        "total": 32,
                        "size": 1,
                        "items": [
                            {
                                "sceneName": "",
                                "id": 18278,
                                "taskAlias": "P18278",
                                "taskStatus": 0,
                                "statusText": "render_task_status_0",
                                "preTaskStatus": 25,
                                "preStatusText": "render_task_status_25",
                                "totalFrames": 0,
                                "abortFrames": null,
                                "executingFrames": null,
                            },
                        ]
                    }

        """
        data = {
            'pageNum': page_num,
            'pageSize': page_size
        }
        if status_list:
            data['statusList'] = status_list
        if search_keyword:
            data['searchKeyword'] = search_keyword
        if start_time:
            data['startTime'] = start_time
        if end_time:
            data['endTime'] = end_time
        return self._connect.post(self._connect.url.queryTaskFrames, data)

    @lru_cache(maxsize=2)
    def get_task_frames(self, task_id, page_num, page_size,
                        search_keyword=None):
        """Get task rendering frame details.

        Args:
            task_id (int): The task ID number,
                which is the unique identifier of the task, required field.
            page_num (int): Current page number.
            page_size (int): Displayed data size per page.
            search_keyword (str, optional): Is a string, which is queried
                according to the name of a multi-frame name of a machine
                rendering, optional.

        Returns:
            dict: Frames profile list, please see the documentation for details.
                e.g.:
                    {
                        "pageCount": 9,
                        "pageNum": 1,
                        "total": 17,
                        "size": 2,
                        "items": [
                            {
                                "id": 1546598,
                                "userId": null,
                                "framePrice": null,
                                "feeType": null,
                                "platform": null,
                                "frameIndex": "0-1",
                                "frameStatus": 4,
                                "feeAmount": 0.44,
                                "startTime": 1535960273000,
                                "endTime": 1535960762000,
                            },
                        ],
                    }

        """
        data = {
            'taskId': task_id,
            'pageNum': page_num,
            'pageSize': page_size
        }
        if search_keyword:
            data['searchKeyword'] = search_keyword
        return self._connect.post(self._connect.url.queryTaskFrames, data)

    @lru_cache(maxsize=2)
    def ge_all_job_frame_status(self):
        """Get the overview of task rendering frame.

        Returns:
            dict: Frames status profile.
                e.g.:
                    {
                        "executingFramesTotal": 1,
                        "doneFramesTotal": 308,
                        "failedFramesTotal": 2,
                        "waitingFramesTotal": 153,
                        "totalFrames": 577
                    }

        """
        return self._connect.post(self._connect.url.queryAllFrameStats,
                                  validator=False)

    def restart_failed_frames(self, task_param_list):
        """Re-submit the failed frame.

        Args:
            task_param_list (list of str): Task ID list.

        """
        data = {
            "taskIds": task_param_list
        }
        return self._connect.post(self._connect.url.restartFailedFrames, data)

    def restart_frame(self, task_id, select_all, ids_list=None):
        """Re-submit the specified frame.

        Args:
            task_id (int): Task ID number.
            ids_list (list, optional): Frame ID list, valid when select_all is
                0.
            select_all (int): Whether to re-request all,
                1 all re-raised, 0 specified frame re-request.

        """
        data = {
            'taskIds': task_id,
            'selectAll': select_all
        }
        if bool(ids_list):
            if isinstance(ids_list, list):
                data['ids'] = ids_list
            else:
                raise TypeError("ids_list must be list type")
        else:
            data['ids'] = []

        return self._connect.post(self._connect.url.restartFrame, data)

    @lru_cache(maxsize=2)
    def get_job_info(self, task_ids_list):
        """Get task details.

        Args:
            task_ids_list (list of int): Shell task ID list.

        Returns:
            dict: Task details.
                e.g.:
                    {
                        "pageCount": 1,
                        "pageNum": 1,
                        "total": 1,
                        "size": 100,
                        "items": [
                            {
                                "sceneName": "3d66.com_593362_2018.max",
                                "id": 19084,
                                "taskAlias": "P19084",
                                "taskStatus": 0,
                                "statusText": "render_task_status_0",
                                "preTaskStatus": 25,
                                "preStatusText": "render_task_status_25",
                                "totalFrames": 0,
                                "abortFrames": null,
                                "executingFrames": null,
                                "doneFrames": null,
                                "failedFrames": 0,
                                "framesRange": "0",
                                "projectName": "",
                                "renderConsume": null,
                                "taskArrears": 0,
                                "submitDate": 1535958477000,
                                "startTime": null,
                                "completedDate": null,
                                "renderDuration": null,
                                "userName": "xiaoguotu_ljian",
                                "producer": null,
                                "taskLevel": 60,
                                "taskUserLevel": 0,
                                "taskLimit": null,
                                "taskOverTime": null,
                                "userId": 10001520,
                                "outputFileName": null,
                                "munuTaskId": "",
                                "layerParentId": 0,
                                "cgId": 2001,
                                "taskKeyValueVo": {
                                    "tiles": null,
                                    "allCamera": null,
                                    "renderableCamera": null
                                }
                            }
                        "userAccountConsume": null
                    }

        """
        data = {
            'taskIds': task_ids_list
        }
        return self._connect.post(self._connect.queryTaskInfo, data)

    @lru_cache(maxsize=2)
    def error_detail(self, code, language='0'):
        """Get analysis error code.

        Args:
            code (int): Required value, error code.
                e.g.:
                    10010.
                    15000.
            language (str, optional): Not required, language,
                0: Chinese (default) 1: English.

        Returns:
            list of dict: Detailed list of error messages.
                e.g.:
                     [
                         {
                            "id": 5,
                            "code": "15000",
                            "type": 1,
                            "languageFlag": 0,
                            "desDescriptionCn": "",
                            "desSolutionCn": ""
                            "solutionPath": "",
                            "isRepair": 0,
                            "isDelete": 1,
                            "isOpen": 1,
                            "lastModifyAdmin": "",
                            "updateTime": 1534387709000
                         },
                     ]

        """
        data = {
            'code': code,
            'language': language
        }
        return self._connect.post(self._connect.url.queryErrorDetail, data)

    @lru_cache(maxsize=2)
    def get_task_processing_img(self, task_id, frame_type=None):
        """Get the task progress diagram,currently only Max software is supported.

        Args:
            task_id (int): Task id.
            frame_type (int): Apply colours to a drawing type, nonessential 2
                represents the photon frame, 5 gets the main picture progress,
                and returns the result dynamically according to the stage of
                the rendering task
            Example:
                {
                    "taskId":389406
                }

        Returns: Task progress diagram information
            dict:
                Example:
                    {
                        "block":16,
                        "currentTaskType":"Render",
                        "grabInfo":[
                            [
                                {
                                    "couponFee":"0.00",
                                    "frameIndex":"0",
                                    "renderInfo":"",
                                    "frameBlock":"1",
                                    "frameEst":"0",
                                    "grabUrl":"/mnt/output/d20/small_pic/10001500/10001834/389406/Render_2018110900083_0_frame_0[_]block_0[_]_STP00000_Renderbus_0000[-]tga.jpg",
                                    "feeAmount":"0.20",
                                    "frameUsed":"66",
                                    "frameStatus":"4",
                                    "framePercent":"100",
                                    "isMaxPrice":"0",
                                    "startTime":"2018-11-09 18:28:26",
                                    "endTime":"2018-11-09 18:29:32"
                                }
                            ]
                        ],
                        "height":1500,
                        "sceneName":"com_589250.max-Camera007",
                        "startTime":"2018-11-09 18:27:40",
                        "width":2000
                    }

        """
        data = {
            "taskId": task_id
        }
        if frame_type:
            data["frameType"] = frame_type
        return self._connect.post(self._connect.url.loadTaskProcessImg, data)

    @lru_cache(maxsize=2)
    def get_frame_thumbnall(self, frame_id, frame_status=4):
        """Load thumbnail.

        Args:
            frame_id (int): Frame id.
            frame_status (int): State of the frame, only complete with
                thumbnails.

        Returns:
            list: Thumbnail path.
                Example:
                    [
                        "small_pic\\100000\\100001\\138\\Render_264_renderbus_0008[-]jpg.jpg"
                    ]

        """
        data = {
            'id': frame_id,
            'frameStatus': frame_status
        }
        return self._connect.post(self._connect.url.loadingFrameThumbnail,
                                  data)
