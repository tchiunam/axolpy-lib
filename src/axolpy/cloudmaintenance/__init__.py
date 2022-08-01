from typing import Iterable, List

from ..aws import ECSService, RDSDatabase
from ..kubernetes import Deployment, StatefulSet


class Operator(object):
    """
    An operator is a person who is responsible for performing
    maintenance on the system.
    """

    def __init__(self, id: str) -> None:
        """
        Initialize an operator.

        :param id: The ID of the operator.
        :type id: str
        """

        self._id = id
        self._rds_databases: List[RDSDatabase] = list()
        self._ecs_services: List[ECSService] = list()
        self._eks_deployments: List[Deployment] = list()
        self._eks_stateful_sets: List[StatefulSet] = list()

    @property
    def id(self) -> str:
        return self._id

    @property
    def eks_deployments(self) -> Iterable[Deployment]:
        return self._eks_deployments

    @property
    def eks_stateful_sets(self) -> Iterable[StatefulSet]:
        return self._eks_stateful_sets

    @property
    def ecs_services(self) -> Iterable[ECSService]:
        return self._ecs_services

    @property
    def rds_databases(self) -> Iterable[RDSDatabase]:
        return self._rds_databases

    def add_eks_deployment(self, deployment: Deployment) -> None:
        self._eks_deployments.append(deployment)

    def add_eks_stateful_set(self, stateful_set: StatefulSet) -> None:
        self._eks_stateful_sets.append(stateful_set)

    def add_ecs_service(self, service: ECSService) -> None:
        self._ecs_services.append(service)

    def add_rds_databases(self, database: RDSDatabase) -> None:
        self._rds_databases.append(database)
