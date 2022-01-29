
from atlassian.bitbucket import Cloud
from atlassian.bitbucket.cloud.repositories import Repository
from atlassian.bitbucket.cloud.workspaces import Workspace


class Bitbucket(Cloud):
    def __init__(self, username: str, password: str, *args, **kwargs):
        """
        This is a Bitbucket instance for the Bitbucket Cloud operations.

        :param username: string: Login username.
        :type username: str
        :param password: string: Login password.
        :type password: str
        :param *args: list: The fixed arguments for the AtlassianRestApi.
        :param **kwargs: dict: The keyword arguments for the AtlassianRestApi.
        """

        super(Bitbucket, self).__init__(
            username=username, password=password, *args, **kwargs)

    def get_workspace(self, name: str) -> Workspace:
        """
        Get a workspace with *name*.

        :param name: Workspace name.
        :type name: str

        :return: :class:`Workspace`
        """

        return self.workspaces.get(workspace=name)

    def get_repository(self, name: str, workspace_name: str) -> Repository:
        """
        Get a repository with *name*.

        :param name: Repository name.
        :type name: str
        :param workspace_name: Workspace name.
        :type name: str

        :return: :class:`Repository`
        """

        if workspace_name:
            return self.get_workspace(name=workspace_name).repositories.get(repository=name)


def get_deployment_environments(repository: Repository) -> dict:
    """
    Get all environments of a *repository*.

    :param repository: A repository.
    :type repository: :class:`Repository`

    :return: REST call response.
    :rtype: dict
    """

    return repository.get(path="environments", trailing=True)


def get_deployment_environment_variables(repository: Repository, environment_uuid: str, params: dict = None) -> dict:
    """
    Get all environments of a *repository*.

    :param environment_uuid: Environment UUID.
    :type environment_uuid: str
    :param repository: A repository.
    :type repository: :class:`Repository`
    :param params: REST call parameters.
    :type params: dict

    :return: REST call response.
    :rtype: dict
    """

    return repository.get(path=f"deployments_config/environments/{environment_uuid}/variables", params=params)
