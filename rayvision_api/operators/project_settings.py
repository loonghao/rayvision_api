"""Provide a class for operating project."""

# Import built-in modules
from pprint import pformat

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache


class ProjectSettings(object):
    """The operator of the Project."""

    def __init__(self, connect):
        """Initialize instance.

        Args:
            connect (rayvision_api.connect.Connect): The connect instance.

        """
        self._connect = connect

    def create_project(self, project_name, status="0"):
        """Create a new project.

        Args:
            project_name (str): name of the render project.
            status (int, optional): The render project init status,
                0 or 1,default is 0.
                1: disable
                0: enable

        """
        data = {
            "newName": project_name,
            "status": status
        }
        return self._connect.post(self._connect.url.addLabel, data)

    def delete_project(self, project_name):
        """Delete the project by given name.

        Args:
            project_name (str): The name of the label to be deleted.

        """
        return self._connect.post(self._connect.url.deleteLabel,
                                  {"delName": project_name})

    @lru_cache(maxsize=None)
    def _get_project_list(self):
        """Get current exits projects.

        Returns:
            dict: The information about the projects.
                e.g.:
                    {
                        "projectNameList": [
                            {
                                "projectId": 3671,
                                "projectName": "myLabel"
                            }
                        ]
                    }

        """
        return self._connect.post(self._connect.url.getLabelList,
                                  validator=False)

    @lru_cache(maxsize=2)
    def get_projects(self):
        """Get current exits projects.

        Returns:
            list of dict: The information about the projects.
                e.g.:
                    [
                        {
                            "projectId": 3671,
                            "projectName": "myLabel"
                        }
                    ]

        """
        return self._get_project_list()["projectNameList"]

    def __str__(self):
        return pformat(self.get_projects())
