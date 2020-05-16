"""Set the rendering environment configuration."""

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

from rayvision_api.constants import SoftWare


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
        try:
            return SoftWare[app_name].value
        except KeyError:
            err = ("No rendering configuration found for '{}'\n"
                   "Currently supporting: {}".format(app_name,
                                                     SoftWare.items()))
            raise ValueError(err)

    def create_render_config(self, app_name, app_version, config_name, ):
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

    def update_render_config(self, data):
        """Modify the user rendering environment configuration.

        Args:
            data (dict): Rendering environment configuration.
                e.g.:
                    {
                        'cgId': "2000",
                        'cgName': 'Maya',
                        'cgVersion': '2018',
                        'renderLayerType': 0,
                        'editName': 'tests',
                        'renderSystem': '1',
                        'pluginIds': 2703,
                    }.

        """
        return self._connect.post(self._connect.url.updateRenderEnv,
                                  data)

    def delete_render_config(self, config_name):
        """Delete user rendering environment configuration.

        Args:
            config_name (str): Rendering environment custom name.

        """
        data = {
            "editName": config_name
        }
        return self._connect.post(self._connect.url.deleteRenderEnv, data)

    def set_default_render_config(self, config_name):
        """Set the default render environment configuration.

        Args:
            config_name (str): Rendering environment custom name.

        """
        data = {
            'editName': config_name
        }
        return self._connect.post(self._connect.url.setDefaultRenderEnv, data)

    @lru_cache(maxsize=2)
    def get_render_config(self, name, config_name=None):
        """Get the user rendering environment configuration.

        Args:
            name (str): The name of the DCC.
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
        post_data = {"cgId": self._get_id_by_app_name(name)}
        return_data = self._connect.post(self._connect.url.getRenderEnv,
                                         post_data)
        data = {
            info["editName"]: info
            for info in return_data}
        return data.get(config_name, return_data)
