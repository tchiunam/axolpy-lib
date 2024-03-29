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

    _cmd: List[str] = NotImplemented

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
    Generate a bash script to update the task count of ECS services.
    """

    _file_step_name: str = "update-ecs-task-count"
    _file_step_name_suffix: str = "RESUME"
    _file_extension: str = "sh"

    _cmd: List[str] = [
        "# aws ecs update-service --region {region} --cluster {cluster} --service {name} --desired-count {count}"]

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
            if not service.property("restart_after_upgrade"):
                count = service.desired_count
                if self._zeroinfy:
                    count = 0
                elif service.patch and service.patch.desired_count > 0:
                    count = service.patch.desired_count

                file.write(self._cmd[0].format(
                    region=service.cluster.region.name,
                    cluster=service.cluster.name,
                    name=service.name,
                    count=count) + "\n")
                if i < len(self._operator.ecs_services) - 1:
                    file.write("# sleep 2\n")


class UpdateK8sStatefulSetReplicas(CloudMaintenanceStep):
    """
    Generate a bash script to update the replicas of k8s statefulsets.
    """

    _file_step_name: str = "update-k8s-statefulset-replicas"
    _file_step_name_suffix: str = "RESUME"
    _file_extension: str = "sh"

    _cmd: List[str] = [
        "# kubectl scale -n {namespace} statefulsets {name} --replicas={replicas}"]

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
                replicas = statefulset.replicas
                if self._zeroinfy:
                    replicas = 0
                elif statefulset.patch and statefulset.patch.replicas > 0:
                    replicas = statefulset.patch.replicas

                file.write(self._cmd[0].format(
                    namespace=statefulset.namespace.name,
                    name=statefulset.name,
                    replicas=replicas) + "\n")


class UpdateK8sDeploymentReplicas(CloudMaintenanceStep):
    """
    Generate a bash script to update the replicas of k8s deployments.
    """

    _file_step_name: str = "change-k8s-deployment-replicas"
    _file_step_name_suffix: str = "RESUME"
    _file_extension: str = "sh"

    _cmd: List[str] = [
        "# kubectl scale -n {namespace} deployment/{name} --replicas={replicas}"]

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
                replicas = deployment.replicas
                if self._zeroinfy:
                    replicas = 0
                elif deployment.patch and deployment.patch.replicas > 0:
                    replicas = deployment.patch.replicas

                file.write(self._cmd[0].format(
                    namespace=deployment.namespace.name,
                    name=deployment.name,
                    replicas=replicas) + "\n")


class DumpPgstats(CloudMaintenanceStep):
    """
    Generate a bash script to dump pgstats.
    """

    _file_step_name: str = "dump-pgstats"
    _file_extension: str = "sh"

    _cmd: List[str] = [
        "psql -h {host} -p {port} -d {dbname} -U postgres -W -c 'select * from pg_stat_all_tables order by schemaname, relname' -o {id}-pg_stat-`date +%Y%m%d-%H%M%S`.csv"]

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
                file.write(self._cmd[0].format(
                    host=db.host, port=db.port, dbname=db.dbname, id=db.id) + "\n")


class DumpMysqlTableStatus(CloudMaintenanceStep):
    """
    Generate a bash script to dump mysql table status.
    """

    _file_step_name: str = "dump-mysqltablestatus"
    _file_extension: str = "sh"

    _cmd: List[str] = [
        "mysql -h {host} -p {port} -d {dbname} -U root -p -e 'show table status' -o {id}-tablestatus-`date +%Y%m%d-%H%M%S`.txt"]

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
                file.write(self._cmd[0].format(
                    host=db.host, port=db.port, dbname=db.dbname, id=db.id) + "\n")


class ModifyDatabaseEngineVersion(CloudMaintenanceStep):
    """
    Generate a bash script to modify the engine version of databases.
    """

    _file_step_name: str = "modify-database-engineversion"
    _file_extension: str = "sh"

    _cmd: List[str] = [
        "# aws rds modify-db-instance --region {region} --db-instance-identifier {id} --engine-version {version} --apply-immediately"]

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
                file.write(self._cmd[0].format(
                    region=db.region.name,
                    id=db.id,
                    version=db.patch.engine_version) + "\n")
                if i < len(self._operator.rds_databases) - 1:
                    file.write("# sleep 2\n")


class ModifyDatabaseClassType(CloudMaintenanceStep):
    """
    Generate a bash script to modify the class type of databases.
    """

    _file_step_name: str = "modify-database-classtype"
    _file_extension: str = "sh"

    _cmd: List[str] = [
        "# aws rds modify-db-instance --region {region} --db-instance-identifier {id} --db-instance-class {class_type} --apply-immediately"]

    _content_header: List[str] = ["#!/bin/bash\n\n"]

    def __init__(self,
                 step_no: int,
                 operator: Operator,
                 dist_path: Path) -> None:
        super().__init__(step_no=step_no, operator=operator, dist_path=dist_path)

    def eligible(self) -> bool:
        for db in self._operator.rds_databases:
            if db.patch and hasattr(db.patch, "class_type"):
                return True

        return False

    def _write_file_content(self, file: TextIOWrapper) -> None:
        file.writelines(self._content_header)
        for i, db in enumerate(self._operator.rds_databases):
            if db.patch and db.patch.class_type:
                file.write(self._cmd[0].format(
                    region=db.region.name,
                    id=db.id,
                    class_type=db.patch.class_type) + "\n")
                if i < len(self._operator.rds_databases) - 1:
                    file.write("# sleep 2\n")


class QueryDatabaseStatus(CloudMaintenanceStep):
    """
    Generate a bash script to query the status of databases.
    """

    _file_step_name: str = "query-database-status"
    _file_extension: str = "sh"

    _cmd: List[str] = [
        "aws rds describe-db-instances --region {region} --db-instance-identifier {id} --query 'DBInstances[*].{{DBInstanceIdentifier:DBInstanceIdentifier,DBInstanceClass:DBInstanceClass,Engine:Engine,DBInstanceStatus:DBInstanceStatus,DBName:DBName,Endpoint:Endpoint,EngineVersion:EngineVersion}}'"]

    _content_header: List[str] = ["#!/bin/bash\n\n"]

    def __init__(self,
                 step_no: int,
                 operator: Operator,
                 dist_path: Path) -> None:
        super().__init__(step_no=step_no, operator=operator, dist_path=dist_path)

    def eligible(self) -> bool:
        return True if len(self._operator.rds_databases) > 0 else False

    def _write_file_content(self, file: TextIOWrapper) -> None:
        file.writelines(self._content_header)
        for i, db in enumerate(self._operator.rds_databases):
            file.write(self._cmd[0].format(
                region=db.region.name,
                id=db.id) + "\n")
            if i < len(self._operator.rds_databases) - 1:
                file.write("sleep 2\n")


class RestartK8sDeployment(CloudMaintenanceStep):
    """
    Generate a bash script to restart k8s deployments.
    """

    _file_step_name: str = "restart-k8s-deployment"
    _file_extension: str = "sh"

    _cmd: List[str] = [
        "# kubectl rollout restart -n {namespace} deployment/{name}",
        "# kubectl scale -n {namespace} deployment/{name} --replicas={replicas}"]

    _content_header: List[str] = ["#!/bin/bash\n\n"]

    _zeroinfy: bool = False

    def __init__(self,
                 step_no: int,
                 operator: Operator,
                 dist_path: Path) -> None:
        super().__init__(step_no=step_no, operator=operator, dist_path=dist_path)

    def eligible(self) -> bool:
        for deployment in self._operator.eks_deployments:
            if deployment.property("restart_after_upgrade"):
                return True

        return False

    def _write_file_content(self, file: TextIOWrapper) -> None:
        file.writelines(self._content_header)
        for deployment in self._operator.eks_deployments:
            if deployment.property("restart_after_upgrade"):
                file.write(self._cmd[0].format(
                    namespace=deployment.namespace.name, name=deployment.name) + "\n")
                if deployment.patch and deployment.patch.replicas > 0:
                    file.write(self._cmd[1].format(
                        namespace=deployment.namespace.name,
                        name=deployment.name,
                        replicas=deployment.patch.replicas) + "\n")


class RestartECSService(CloudMaintenanceStep):
    """
    Create a bash script to restart ECS services.
    """

    _file_step_name: str = "restart-ecs-service"
    _file_extension: str = "sh"

    _cmd: List[str] = [
        "# aws ecs update-service --force-new-deployment --region {region} --cluster {cluster} --service {name}"]

    _content_header: List[str] = ["#!/bin/bash\n\n"]

    _zeroinfy: bool = False

    def __init__(self,
                 step_no: int,
                 operator: Operator,
                 dist_path: Path) -> None:
        super().__init__(step_no=step_no, operator=operator, dist_path=dist_path)

    def eligible(self) -> bool:
        for service in self._operator.ecs_services:
            if service.property("restart_after_upgrade"):
                return True

        return False

    def _write_file_content(self, file: TextIOWrapper) -> None:
        file.writelines(self._content_header)
        for i, service in enumerate(self._operator.ecs_services):
            if service.property("restart_after_upgrade"):
                file.write(self._cmd[0].format(
                    region=service.cluster.region.name,
                    cluster=service.cluster.name,
                    name=service.name) + "\n")
                if i < len(self._operator.ecs_services) - 1:
                    file.write("# sleep 2\n")


class QueryK8sDeploymentStatus(CloudMaintenanceStep):
    """
    Create a bash script to query the status of k8s deployments.
    """

    _file_step_name: str = "query-k8s-deployment-status"
    _file_extension: str = "sh"

    _cmd: List[str] = ["kubectl get deployments -n {namespace} {names}"]

    _content_header: List[str] = ["#!/bin/bash\n\n"]

    _zeroinfy: bool = False

    def __init__(self,
                 step_no: int,
                 operator: Operator,
                 dist_path: Path) -> None:
        super().__init__(step_no=step_no, operator=operator, dist_path=dist_path)

    def eligible(self) -> bool:
        return True if len(self._operator.eks_deployments) > 0 else False

    def _write_file_content(self, file: TextIOWrapper) -> None:
        file.writelines(self._content_header)
        namespace_dpms = dict()
        for dpm in self._operator.eks_deployments:
            if dpm.namespace.name not in namespace_dpms:
                namespace_dpms[dpm.namespace.name] = list()
            namespace_dpms[dpm.namespace.name].append(dpm)
        for namespace, deployments in namespace_dpms.items():
            file.write(self._cmd[0].format(
                namespace=namespace,
                names=" ".join([deployment.name for deployment in deployments])) + "\n")


class QueryECSTaskStatus(CloudMaintenanceStep):
    """
    Create a bash script to query the status of ECS tasks.
    """

    _file_step_name: str = "query-ecs-task-status"
    _file_extension: str = "sh"

    _cmd: List[str] = [
        "aws ecs describe-services --region {region} --cluster {cluster} --services {names} --query 'services[*].{{ServiceArn:serviceArn,ServiceName:serviceName,Status:status,DesiredCount:desiredCount,RunningCount:runningCount,PendingCount:pendingCount,Events:events[:2]}}'"]

    _content_header: List[str] = ["#!/bin/bash\n\n"]

    _zeroinfy: bool = False

    def __init__(self,
                 step_no: int,
                 operator: Operator,
                 dist_path: Path) -> None:
        super().__init__(step_no=step_no, operator=operator, dist_path=dist_path)

    def eligible(self) -> bool:
        return True if len(self._operator.ecs_services) > 0 else False

    def _write_file_content(self, file: TextIOWrapper) -> None:
        file.writelines(self._content_header)
        rc_services = dict()
        for service in self._operator.ecs_services:
            if service.cluster.region.name not in rc_services:
                rc_services[service.cluster.region.name] = dict()
            if service.cluster.name not in rc_services[service.cluster.region.name]:
                rc_services[service.cluster.region.name][service.cluster.name] = list()
            rc_services[service.cluster.region.name][service.cluster.name].append(
                service)
        for region_name, clusters in rc_services.items():
            for cluster_name, services in clusters.items():
                file.write(self._cmd[0].format(
                    region=region_name,
                    cluster=cluster_name,
                    names=" ".join([service.name for service in services])) + "\n")
