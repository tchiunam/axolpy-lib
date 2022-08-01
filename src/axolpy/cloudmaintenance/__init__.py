from abc import ABC, abstractmethod
from io import TextIOWrapper
from pathlib import Path
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


class CloudMaintenanceStep(ABC):
    """"
    An abstract class for a cloud maintenance step.
    """

    _file_step_name: str = NotImplemented
    _file_step_name_suffix: str = None
    _file_extension: str = NotImplemented

    _cmd: str = NotImplemented

    _content_header: List[str] = NotImplemented

    def __init__(self,
                 step_no: int,
                 operator: Operator,
                 dist_path: Path) -> None:
        """
        Initialize a cloud maintenance step.

        :param step_no: The step number.
        :type step_no: int
        :param operator: The operator.
        :type operator: :class:`Operator`
        :param dist_path: The path to the distribution directory.
        :type dist_path: Path
        """

        self._step_no: str = step_no
        self._operator: Operator = operator
        self._dist_path: Path = dist_path

    def filename(self) -> str:
        return "{operator}-{step_no}-{file_step_name}{file_step_name_suffix}.{file_extenstion}".format(
            operator=self._operator.id,
            step_no=self._step_no,
            file_step_name=self._file_step_name,
            file_step_name_suffix="" if self._file_step_name_suffix is None
            else "-" + self._file_step_name_suffix,
            file_extenstion=self._file_extension)

    def output_filepath(self) -> Path:
        return Path(self._dist_path, self.filename())

    @abstractmethod
    def eligible(self) -> bool:
        pass

    def write_file(self) -> None:
        if not self.eligible():
            return

        filepath = self.output_filepath()
        with filepath.open("w") as f:
            self._write_file_content(f)
        filepath.chmod(0o755)

    @abstractmethod
    def _write_file_content(self, file: TextIOWrapper) -> None:
        pass
