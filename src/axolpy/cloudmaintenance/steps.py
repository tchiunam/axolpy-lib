from abc import ABC, abstractmethod
from io import TextIOWrapper
from pathlib import Path
from typing import List

from axolpy.cloudmaintenance import Operator


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
        filepath.parent.mkdir(mode=0o755,
                              parents=True,
                              exist_ok=True)
        with filepath.open("w") as f:
            self._write_file_content(file=f)
        filepath.chmod(0o755)

    @abstractmethod
    def _write_file_content(self, file: TextIOWrapper) -> None:
        pass


class UpdateECSTaskCount(CloudMaintenanceStep):
    """
    Generate a bash script to update the task count of an ECS service.
    """

    _file_step_name: str = "update-ecs-task-count"
    _file_step_name_suffix: str = "RESUME"
    _file_extension: str = "sh"

    _cmd: str = "# aws ecs update-service --region {region} --cluster {cluster} --service {name} --desired-count {count}"

    _content_header: List[str] = ["#!/bin/bash"]

    _zeroinfy: bool = False

    def __init__(self,
                 step_no: int,
                 operator: Operator,
                 dist_path: Path,
                 zeroinfy: bool = False) -> None:
        super().__init__(step_no=step_no, operator=operator, dist_path=dist_path)
        self._zeroinfy = zeroinfy
        if self._zeroinfy:
            self._file_step_name_suffix = "ZERO"

    def eligible(self) -> bool:
        return True if len(self._operator.ecs_services) > 0 else False

    def _write_file_content(self, file: TextIOWrapper) -> None:
        file.writelines(self._content_header)
        file.write("\n\n")
        for i, service in enumerate(self._operator.ecs_services):
            file.write(self._cmd.format(
                region=service.cluster.region.name,
                cluster=service.cluster.name,
                name=service.name,
                count=0 if self._zeroinfy else service.desired_count) + "\n")
            if i < len(self._operator.ecs_services) - 1:
                file.write("# sleep 2\n")


class UpdateK8sStatefulSetReplicas(CloudMaintenanceStep):
    """
    Generate a bash script to update the replicas of a k8s statefulset.
    """

    _file_step_name: str = "update-k8s-statefulset-replicas"
    _file_step_name_suffix: str = "RESUME"
    _file_extension: str = "sh"

    _cmd: str = "# kubectl scale -n {namespace} statefulsets {name} --replicas={replicas}"

    _content_header: List[str] = ["#!/bin/bash"]

    _zeroinfy: bool = False

    def __init__(self,
                 step_no: int,
                 operator: Operator,
                 dist_path: Path,
                 zeroinfy: bool = False) -> None:
        super().__init__(step_no=step_no, operator=operator, dist_path=dist_path)
        self._zeroinfy = zeroinfy
        if self._zeroinfy:
            self._file_step_name_suffix = "ZERO"

    def eligible(self) -> bool:
        for deployment in self._operator.eks_statefulsets:
            if not deployment.property("restart_after_upgrade"):
                return True

        return False

    def _write_file_content(self, file: TextIOWrapper) -> None:
        file.writelines(self._content_header)
        file.write("\n\n")

        for statefulset in self._operator.eks_statefulsets:
            if not statefulset.property("restart_after_upgrade"):
                file.write(self._cmd.format(
                    namespace=statefulset.namespace.name,
                    name=statefulset.name,
                    replicas=0 if self._zeroinfy else statefulset.replicas) + "\n")


class UpdateK8sDeploymentReplicas(CloudMaintenanceStep):
    _file_step_name: str = "apro-change-k8s-deployment-replicas"
    _file_step_name_suffix: str = "RESUME"
    _file_extension: str = "sh"

    _cmd: str = "# kubectl scale -n {namespace} deployment/{name} --replicas={replicas}"

    _content_header: List[str] = ["#!/bin/bash"]

    _zeroinfy: bool = False

    def __init__(self,
                 step_no: int,
                 operator: Operator,
                 dist_path: Path,
                 zeroinfy: bool = False) -> None:
        super().__init__(step_no=step_no, operator=operator, dist_path=dist_path)
        self._zeroinfy = zeroinfy
        if self._zeroinfy:
            self._file_step_name_suffix = "ZERO"

    def eligible(self) -> bool:
        for deployment in self._operator.eks_deployments:
            if not deployment.property("restart_after_upgrade"):
                return True

        return False

    def _write_file_content(self, file: TextIOWrapper) -> None:
        file.writelines(self._content_header)
        file.write("\n\n")

        for deployment in self._operator.eks_deployments:
            if not deployment.property("restart_after_upgrade"):
                file.write(self._cmd.format(
                    namespace=deployment.namespace.name,
                    name=deployment.name,
                    replicas=0 if self._zeroinfy else deployment.replicas) + "\n")
