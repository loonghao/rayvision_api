"""A Python-based API for Using Renderbus cloud rendering service."""

import logging
import os
from rayvision_log import init_logger
import requests

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

from rayvision_api.connect import Connect
from rayvision_api.operators import RenderConfig
from rayvision_api.operators import ProjectSettings
from rayvision_api.operators import RenderJobs
from rayvision_api.operators import UserProfile
from rayvision_api.constants import PACKAGE_NAME
from rayvision_api.constants import DCC_ID_MAPPINGS
from rayvision_api.constants import SoftWare


class RayvisionAPI(object):
    """A Python-based API for Using Renderbus cloud rendering service.

    Examples:
        .. code-block:: python

            >>> from rayvision_api import RayvisionAPI
            >>> api_access_id = "xxxxxx"
            >>> api_access_key = "xxxxx"
            >>> ray = RayvisionAPI(access_id=api_access_id,
            ...                    access_key=api_access_key)
            # Print current user profiles.
            >>> print(ray.user_profile)
            # Access profile settings or info like a object.
            >>> print(ray.user_profile.user_name)
            >>> print(ray.user_profile.email)
            >>> print(ray.user_profile.user_id)

            # Add custom hooks.
            >>> def print_resp_url(resp, *args, **kwargs):
            ...     print(resp.url)

            >>> def check_for_errors(resp, *args, **kwargs):
            ...     resp.raise_for_status()

            >>> hooks = {'response': [print_resp_url, check_for_errors]}
            >>> ray = RayvisionAPI(access_id=api_access_id,
            ...                    access_key=api_access_key,
            ...                    hooks=hooks)

    """

    def __init__(self,
                 access_id=None,
                 access_key=None,
                 domain='task.renderbus.com',
                 render_platform='4',
                 protocol='https',
                 logger=None,
                 hooks=None):
        """Initialize the Rayvision API instance.

        Args:
            access_id (str, optional): The access id of API.
            access_key (str, optional): The access key of the API.
            domain (str, optional): The domain address of the API.
            render_platform (str, optional): The platform of renderFarm.
            protocol (str, optional): The requests protocol.
            logger (logging.Logger, optional): The logging logger instance.
            hooks (dict, optional): Advanced features that allow us to add
                custom hooks for post requests.
                e.g:
                    def print_resp_url(resp, *args, **kwargs):
                        print(resp.url)

                    def check_for_errors(resp, *args, **kwargs):
                        resp.raise_for_status()

                    hooks = {'response': [print_resp_url, check_for_errors]}

        References:
            https://alexwlchan.net/2017/10/requests-hooks/

        """
        self.logger = logger

        if not self.logger:
            init_logger(PACKAGE_NAME)
            self.logger = logging.getLogger(__name__)

        access_id = access_id or os.getenv("RAYVISION_API_ACCESS_ID")
        if not access_id:
            raise TypeError(
                'Required "access_id" not specified. Pass as argument or set '
                'in environment variable RAYVISION_API_ACCESS_ID.'
            )
        access_key = access_key or os.getenv("RAYVISION_API_KEY")
        if not access_id:
            raise TypeError(
                'Required "access_key" not specified. Pass as argument or set '
                'in environment variable RAYVISION_API_KEY.'
            )

        # Initialize the session instance.
        self._request = requests.Session()

        # Create a connection.
        self._connect = Connect(access_id,
                                access_key,
                                protocol,
                                domain,
                                render_platform,
                                session=self._request,
                                hooks=hooks)

        # Initialize all instances of api operators.
        self.user_profile = UserProfile(self._connect)
        self.render_jobs = RenderJobs(self._connect)
        self.project = ProjectSettings(self._connect)
        self.render_config = RenderConfig(self._connect)

    @property
    def connect(self):
        """rayvision.api.Connect: The current connect instance."""
        return self._connect

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._request.close()

    def software_list(self):
        pass

    @property
    @lru_cache(maxsize=None)
    def render_platforms(self):
        """Get the currently available rendering platform.

        Returns:
            list of dict: Platforms profile.
                e.g.:
                     [
                         {
                             "platform": 2,
                             "name": "query_platform_w2"
                         },
                     ]

        """
        zone = 1 if "renderbus" in self._connect.domain.lower() else 2
        return self._connect.post(self._connect.url.queryPlatforms,
                                  {'zone': zone})

    @property
    @lru_cache(maxsize=None)
    def supported_software(self):
        """Get supported rendering software.

        Returns:
            dict: Software profile.
                e.g.:
                    {
                        "isAutoCommit": 2,
                        "renderInfoList": [
                            {
                                "cgId": 2000,
                                "cgName": "Maya",
                                "cgType": "ma;mb",
                                "iconPath": "/img/softimage/maya.png",
                                "isNeedProjectPath": 3,
                                "isNeedAnalyse": 1,
                                "isSupportLinux": 1
                            }
                        ],
                        "defaultCgId": 2001
                    }

        """
        return self._connect.post(self._connect.url.querySupportedSoftware,
                                  validator=False)

    @property
    @lru_cache(maxsize=2)
    def default_render_software(self):
        """dict: The current default render software."""
        info_list = self.supported_software["renderInfoList"]
        for info in info_list:
            if info["cgId"] == self.supported_software["defaultCgId"]:
                return info

    @lru_cache(maxsize=2)
    def supported_plugin(self, name, os_name=None):
        """Get supported rendering software plugins.

        Args:
            name (str): The name of the DCC.
                e.g.:
                    maya,
                    houdini
            os_name (str): The platform of the OS.
                e.g:
                    windows
                    linux

        Returns:
            dict: Plugin profile.
                e.g.:
                    {
                        "cgPlugin": [
                            {
                                "cvId": 19,
                                "pluginName": "zblur",
                                "pluginVersions": [
                                    {
                                        "pluginId": 1652,
                                        "pluginName": "zblur",
                                        "pluginVersion": "zblur 2.02.019"
                                    }
                                ]
                            },
                        ],
                        "cgVersion": [
                            {
                                "id": 23,
                                "cgId": 2005,
                                "cgName": "CINEMA 4D",
                                "cgVersion": "R19"
                            }
                        ]
                    }

        """
        cg_id = DCC_ID_MAPPINGS[name.strip()]
        data = {'cgId': cg_id,
                'osName': os_name or self.connect.system_platform}
        return self._connect.post(self._connect.url.querySupportedPlugin, data)

    def submit(self, task_info, only_id=True):
        """Submit a task.

        Args:
            task_info (dict): Task id.

        """
        return self.render_jobs.submit_task(task_info)
