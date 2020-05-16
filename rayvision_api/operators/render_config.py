"""Set the rendering environment configuration."""

# Import built-in modules
from enum import Enum
from itertools import groupby
from operator import itemgetter

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache


class SoftWare(Enum):
    maya = "2000"
    max = "2001"
    lightwave = "2002"
    arnold = "2003"
    houdini = "2004"
    cinema4d = "2005"
    softimage = "2006"
    blender = "2007"
    vr_standalone = "2008"
    mr_standalone = "2009"
    sketchup = "2010"
    vue = "2011"
    keyshot = "2012"
    clarisse = "2013"
    octane_render = "2014"
    katana = "2016"

    @classmethod
    def items(cls):
        return cls._member_names_


class RenderConfig(object):
    """The rendering environment configuration."""

    def __init__(self, connect):
        """Initialize instance.

        Args:
            connect (rayvision_api.connect.Connect): The connect instance.

        """
        self._connect = connect

    @staticmethod
    def _get_id_by_app_name(app_name):
        """str: Get the ID by the render software.

        Args:
            app_name (str): The name of the render software.

        Raises:
            ValueError: No rendering configuration found.

        """
        try:
            return SoftWare[app_name].value
        except KeyError:
            err = ("No rendering configuration found for '{}'\n"
                   "Currently supporting: {}".format(app_name,
                                                     SoftWare.items()))
            raise ValueError(err)

    def create_render_config(self, app_name, app_version, config_name):
        """Adjust user rendering environment configuration.

        Args:
            app_name (str): The name of the DCC.
                .e.g:
                    - maya
                    - clarisse
                    - houdini
            app_version (str):
                    - 2018
                    - 17
            config_name (str): The name of the new config.

        Returns:
            dict: Render env profile.
                e.g.:
                    {
                        'editName': 'tests'
                    }

        """
        data = {
            "cgName": app_name,
            "cgVersion": app_version,
            "editName": config_name,
            "cgId": self._get_id_by_app_name(app_name)
        }
        return self._connect.post(self._connect.url.addRenderEnv, data)

    def update_render_config(self,
                             app_name,
                             app_version,
                             config_name,
                             render_layer_type=1,
                             render_system=None,
                             plugin_ids=[]):
        """Modify the user rendering environment configuration.

        Args:
            app_name (str): The name of the render software.
            app_version (str): The version of the render software.
            config_name (str): The name of the render configuration.
            render_layer_type (int): The type of the render layer.
                this option only support the job from maya.
            render_system (int): The type of the render os system.
                linux: 0
                windows: 1
            plugin_ids (list of int): The id list of the render plugins.
                we can use `get_plugin_versions` function to get the
                plugins id.

        """
        config = self.get_render_config(app_name, config_name)
        if not config:
            # The update renders config need to ensure the config already
            # exists.
            config = self.create_render_config(app_name, app_version,
                                               config_name)
        self._connect.post(self._connect.url.querySupportedPlugin)
        data = {
            'cgName': app_name,
            'cgVersion': app_version,
            'editName': config_name,
            'renderLayerType': render_layer_type or config["renderLayerType"],
            'renderSystem': render_system or config["renderSystem"],
            'pluginIds': plugin_ids or config["renderSystem"],
            "cgId": config["cgId"]
        }
        return self._connect.post(self._connect.url.updateRenderEnv,
                                  data)

    def delete_render_config(self, config_name):
        """Delete user rendering environment configuration.

        Args:
            config_name (str): The name of the render configuration.

        """
        data = {
            "editName": config_name
        }
        return self._connect.post(self._connect.url.deleteRenderEnv, data)

    def set_default_render_config(self, config_name):
        """Set the default render environment configuration.

        Args:
            config_name (str): The name of the render configuration.

        """
        data = {
            'editName': config_name
        }
        return self._connect.post(self._connect.url.setDefaultRenderEnv, data)

    @lru_cache(maxsize=2)
    def get_render_config(self, app_name, config_name=None):
        """Get the user rendering environment configuration.

        Args:
            app_name (str): The name of the render software.
            e.g.:
                maya,
                houdini,
                3dsmax
            config_name (str, optional): The name of the render env config.

        Return:
            list: Software profile.
                e.g.:
                     [
                        {
                            "cgId": 2000,
                            "editName": "testRenderEnv332",
                            "cgName": "Maya",
                            "cgVersion": "2020",
                            "osName": 0,
                            "renderLayerType": 0,
                            "isDefault": 0,
                            "respUserPluginInfoVos": [
                                {
                                    "pluginId": 1166,
                                    "pluginName": "wobble",
                                    "pluginVersion": "wobble 0.9.5"
                                }
                            ]
                        },
                        {
                            "cgId": 2000,
                            "editName": "testRenderEnv222",
                            "cgName": "Maya",
                            "cgVersion": "2020",
                            "osName": 0,
                            "renderLayerType": 0,
                            "isDefault": 0,
                            "respUserPluginInfoVos": [
                                {
                                    "pluginId": 1166,
                                    "pluginName": "wobble",
                                    "pluginVersion": "wobble 0.9.5"
                                }
                    ]

        """
        post_data = {"cgId": self._get_id_by_app_name(app_name)}
        return_data = self._connect.post(self._connect.url.getRenderEnv,
                                         post_data)
        data = {
            info["editName"]: info
            for info in return_data
        }
        return data.get(config_name, return_data)

    @lru_cache(maxsize=None)
    def get_supported_software(self):
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
        info_list = self.get_supported_software()["renderInfoList"]
        for info in info_list:
            if info["cgId"] == self.get_supported_software()["defaultCgId"]:
                return info

    @lru_cache(maxsize=2)
    def get_plugins(self, app_name, os_name=None):
        """Get supported rendering software plugins by the software.

        Args:
            app_name (str): The name of the render software.
                e.g.:
                    maya,
                    houdini
            os_name (str): The platform of the OS.
                e.g:
                    windows
                    linux

        Returns:
            dict: The information of the plugins.
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
        cg_id = self._get_id_by_app_name(app_name)
        data = {'cgId': cg_id,
                'osName': os_name or self._connect.system_platform}
        return self._connect.post(self._connect.url.querySupportedPlugin, data)

    def get_plugin_versions(self, app_name, plugin_name):
        """Get the plugins version by given render software name.

        Args:
            app_name (str): The name of the render software.
                e.g.:
                    maya
                    houdini
                    blender
            plugin_name (str): The plugin name of the render software.

        Returns:
            dict: The plugin info of the render software.

        """
        groups = groupby(self.get_plugins(app_name)["cgPlugin"],
                         key=itemgetter("pluginName"))
        for group_name, infos in groups:
            if group_name == plugin_name:
                return [info for info in infos]

    def get_render_software_versions(self, app_name):
        """Get versions for the given the rendering software.

        Args:
            app_name (str): The name of the render software.

        Returns:
            list of dict: The versions for the given the rendering software.
                e.g:
                    [
                        {
                        'cgId': 2000,
                        'cgName': 'Maya',
                        'cgVersion': u'2020',
                        'id': 227
                        },
                        {
                        'cgId': 2000,
                        'cgName': 'Maya',
                        'cgVersion': u'2019',
                        'id': 151
                        },
                    ]

        """
        return self.get_plugins(app_name)["cgVersion"]
