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

    _content_header: List[str] = ["#!/bin/bash\n\n"]

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
        for i, service in enumerate(self._operator.ecs_services):
            count = service.desired_count
            if self._zeroinfy:
                count = 0
            elif service.patch and service.patch.desired_count > 0:
                count = service.patch.desired_count

            file.write(self._cmd.format(
                region=service.cluster.region.name,
                cluster=service.cluster.name,
                name=service.name,
                count=count) + "\n")
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

    _content_header: List[str] = ["#!/bin/bash\n\n"]

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
        for statefulset in self._operator.eks_statefulsets:
            if not statefulset.property("restart_after_upgrade"):
                file.write(self._cmd.format(
                    namespace=statefulset.namespace.name,
                    name=statefulset.name,
                    replicas=0 if self._zeroinfy else statefulset.replicas) + "\n")


class UpdateK8sDeploymentReplicas(CloudMaintenanceStep):
    _file_step_name: str = "change-k8s-deployment-replicas"
    _file_step_name_suffix: str = "RESUME"
    _file_extension: str = "sh"

    _cmd: str = "# kubectl scale -n {namespace} deployment/{name} --replicas={replicas}"

    _content_header: List[str] = ["#!/bin/bash\n\n"]

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
        for deployment in self._operator.eks_deployments:
            if not deployment.property("restart_after_upgrade"):
                file.write(self._cmd.format(
                    namespace=deployment.namespace.name,
                    name=deployment.name,
                    replicas=0 if self._zeroinfy else deployment.replicas) + "\n")


class DumpPgstats(CloudMaintenanceStep):
    _file_step_name: str = "dump-pgstats"
    _file_extension: str = "sh"

    _cmd: str = "psql -h {host} -p {port} -d {dbname} -U postgres -W -c 'select * from pg_stat_all_tables order by schemaname, relname' -o {id}-pg_stat-`date +%Y%m%d-%H%M%S`.csv"

    _content_header: List[str] = ["#!/bin/bash\n\n"]

    def __init__(self,
                 step_no: int,
                 operator: Operator,
                 dist_path: Path) -> None:
        super().__init__(step_no=step_no, operator=operator, dist_path=dist_path)

    def eligible(self) -> bool:
        for db in self._operator.rds_databases:
            if db.is_postgresql():
                return True

        return False

    def _write_file_content(self, file: TextIOWrapper) -> None:
        file.writelines(self._content_header)
        for db in self._operator.rds_databases:
            if db.is_postgresql():
                file.write(
                    "echo \"database id: {id}\"\n".format(id=db.id))
                file.write(self._cmd.format(
                    host=db.host, port=db.port, dbname=db.dbname, id=db.id) + "\n")


class DumpMysqlTableStatus(CloudMaintenanceStep):
    _file_step_name: str = "dump-mysqltablestatus"
    _file_extension: str = "sh"

    _cmd: str = "mysql -h {host} -p {port} -d {dbname} -U root -p -e 'show table status' -o {id}-tablestatus-`date +%Y%m%d-%H%M%S`.txt"

    _content_header: List[str] = ["#!/bin/bash\n\n"]

    def __init__(self,
                 step_no: int,
                 operator: Operator,
                 dist_path: Path) -> None:
        super().__init__(step_no=step_no, operator=operator, dist_path=dist_path)

    def eligible(self) -> bool:
        for db in self._operator.rds_databases:
            if db.is_mysql():
                return True

        return False

    def _write_file_content(self, file: TextIOWrapper) -> None:
        file.writelines(self._content_header)
        for db in self._operator.rds_databases:
            if db.is_mysql():
                file.write("echo \"database id: {id}\"\n".format(id=db.id))
                file.write(self._cmd.format(
                    host=db.host, port=db.port, dbname=db.dbname, id=db.id) + "\n")


class ModifyDatabaseEngineVersion(CloudMaintenanceStep):
    _file_step_name: str = "modify-database-engineversion"
    _file_extension: str = "sh"

    _cmd: str = "# aws rds modify-db-instance --region {region} --db-instance-identifier {id} --engine-version {version} --apply-immediately"

    _content_header: List[str] = ["#!/bin/bash\n\n"]

    def __init__(self,
                 step_no: int,
                 operator: Operator,
                 dist_path: Path) -> None:
        super().__init__(step_no=step_no, operator=operator, dist_path=dist_path)

    def eligible(self) -> bool:
        for db in self._operator.rds_databases:
            if db.patch and hasattr(db.patch, "engine_version"):
                return True

        return False

    def _write_file_content(self, file: TextIOWrapper) -> None:
        file.writelines(self._content_header)

        for i, db in enumerate(self._operator.rds_databases):
            if db.patch and db.patch.engine_version:
                file.write(self._cmd.format(
                    region=db.region.name,
                    id=db.id,
                    version=db.patch.engine_version) + "\n")
                if i < len(self._operator.rds_databases) - 1:
                    file.write("# sleep 2\n")
