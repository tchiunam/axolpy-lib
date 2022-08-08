from __future__ import annotations

from abc import ABC
from typing import Any, Dict

from axolpy.kubernetes import Cluster


class AWSRegion(object):
    """
    A region in AWS cloud platform.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize an object for a region in AWS cloud platform.

        :param name: Region name.
        :type name: str
        """

        self._name: str = name
        self._eks_clusters: Dict[str, Cluster] = dict()
        self._ecs_clusters: Dict[str, ECSCluster] = dict()
        self._rds_databases: Dict[str, RDSDatabase] = dict()

    @property
    def name(self) -> str:
        return self._name

    @property
    def eks_clusters(self) -> Dict[str, Cluster]:
        return self._eks_clusters.copy()

    def eks_cluster(self, name: str) -> Cluster:
        return self._eks_clusters[name]

    def add_eks_cluster(self, cluster: Cluster) -> None:
        """
        Add a cluster to this region.

        :param cluster: A EKS Cluster.
        :type cluster: :class:`Cluster`
        """

        self._eks_clusters[cluster.name] = cluster

    @property
    def ecs_clusters(self) -> Dict[str, ECSCluster]:
        return self._ecs_clusters.copy()

    def ecs_cluster(self, name: str) -> ECSCluster:
        return self._ecs_clusters[name]

    def add_ecs_cluster(self, cluster: ECSCluster) -> None:
        """
        Add a cluster to this region.

        :param cluster: A ECS Cluster.
        :type cluster: :class:`ECSCluster`
        """

        self._ecs_clusters[cluster.name] = cluster

    @property
    def rds_databases(self) -> Dict[str, RDSDatabase]:
        return self._rds_databases.copy()

    def rds_database(self, id: str) -> RDSDatabase:
        return self._rds_databases[id]

    def add_rds_database(self, database: RDSDatabase) -> None:
        """
        Add a database to this region.

        :param database: A RDS Database.
        :type database: :class:`RDSDatabase`
        """

        self._rds_databases[database.id] = database

    def __str__(self) -> str:
        return f"{__class__.__name__}(name: {self._name}, {len(self._eks_clusters)} EKS clusters" + \
            f", {len(self._ecs_clusters)} ECS clusters, {len(self._rds_databases)} RDS Databases)"


class ECSCluster(object):
    def __init__(
            self,
            name: str,
            region: AWSRegion) -> None:
        """
        A ECS Cluster in AWS.

        :param name: The name of ECS Cluster.
        :param name: str
        :param region: The region that this ECS Cluster is in.
        :param region: :class:`AWSRegion`
        """

        self._name: str = name
        self._region: AWSRegion = region
        self._services: Dict[str, ECSService] = dict()

        self._region.add_ecs_cluster(cluster=self)

    @property
    def name(self) -> str:
        return self._name

    @property
    def region(self) -> AWSRegion:
        return self._region

    @property
    def services(self) -> Dict[str, ECSService]:
        return self._services.copy()

    def service(self, name: str) -> ECSService:
        return self._services[name]

    def add_service(self, service: ECSService) -> None:
        self._services[service.name] = service

    def __str__(self) -> str:
        return f"{__class__.__name__}(name: {self._name}, {len(self._services)} services)"


class AbstractECSServicePatchable(ABC):
    def __init__(self, desired_count: int) -> None:
        self._desired_count: str = desired_count

    @property
    def desired_count(self) -> str:
        return self._desired_count


class ECSServicePatch(AbstractECSServicePatchable):
    def __init__(self, desired_count: str = None) -> None:
        super().__init__(desired_count=desired_count)

    def __str__(self) -> str:
        return f"{__class__.__name__}(desired_count: {self._desired_count})"


class ECSService(AbstractECSServicePatchable):
    def __init__(self,
                 name: str,
                 cluster: ECSCluster,
                 desired_count: int = 0,
                 patch: ECSServicePatch = None,
                 **kwargs) -> None:
        """
        A ECS Service in ECS cluster.

        :param name: The name of ECS Service.
        :type name: str
        :param cluster: The cluster this ECS Service is in.
        :type cluster: :class: `ECSCluster`
        :param patch: The patch of ECS Service.
        :type patch: :class:`ECSServicePatch`
        """

        self._name: str = name
        self._cluster: Cluster = cluster
        self._desired_count: int = desired_count
        self._patch: ECSServicePatch = patch
        # Properties is used to store the properties of this ECS Service
        # which are not the standard attributes of it.
        self._properties: dict = dict()
        for k, v in kwargs.items():
            self.add_property(name=k, value=v)

        self._cluster.add_service(service=self)

    @property
    def name(self) -> str:
        return self._name

    @property
    def cluster(self) -> ECSCluster:
        return self._cluster

    @property
    def patch(self) -> ECSServicePatch:
        return self._patch

    @patch.setter
    def patch(self, patch: ECSServicePatch) -> None:
        self._patch = patch

    def add_property(self, name: str, value: Any) -> None:
        self._properties[name] = value

    def property(self, name) -> Any:
        return self._properties.get(name, None)

    def __str__(self) -> str:
        return f"{__class__.__name__}(name: {self._name}, desired_count: {self._desired_count}" + \
            f", {len(self._properties)} properties)"


class AbstractRDSDatabasePatchable(ABC):
    def __init__(
            self,
            engine_version: str,
            class_type: str) -> None:
        self._engine_version: str = engine_version
        self._class_type: str = class_type

    @property
    def engine_version(self) -> str:
        return self._engine_version

    @property
    def class_type(self) -> str:
        return self._class_type


class RDSDatabasePatch(AbstractRDSDatabasePatchable):
    def __init__(
            self,
            engine_version: str = None,
            class_type: str = None) -> None:
        super().__init__(
            engine_version=engine_version,
            class_type=class_type)

    def __str__(self) -> str:
        return f"{__class__.__name__}" + \
            f"(engine_version: {self._engine_version}" + \
            f", class_type: {self._class_type})"


class RDSDatabase(AbstractRDSDatabasePatchable):
    """
    A database Amazon Relational Databases Service.
    """

    def __init__(self,
                 id: str,
                 region: AWSRegion,
                 type: str,
                 host: str,
                 port: int = -1,
                 engine_type: str = "postgresql",
                 engine_version: str = None,
                 class_type: str = None,
                 dbname: str = None,
                 patch: RDSDatabasePatch = None) -> None:
        """
        Initialize a RDS Database.

        :param id: RDS database identifier.
        :type id: str
        :param region: AWS Region that this RDS database is in.
        :type region: :class:`AWSRegion`
        :param type: Type of RDS database. Choices: 'instance' or 'cluster'.
        :type type: str
        :param host: RDS database hostname.
        :type host: str
        :param port: RDS database port.
        :type port: int
        :param engine_type: Engine Type. Choice: 'postgresql' or 'mysql'.
        :type engine_type: str
        :param engine_version: Engine Version.
        :type engine_version: str
        :param class_type: Class Type.
        :type class_type: str
        :param dbname: Database name in the engine. Default is id.
        :type dbname: str
        :param patch: The patch of RDS Database.
        :type patch: :class:`RDSDatabasePatch`
        """

        assert type in ["instance",
                        "cluster"], "type must be instance or cluster"
        assert engine_type in ["postgresql",
                               "mysql"], "engine_type must be postgresql or mysql"

        super().__init__(engine_version=engine_version, class_type=class_type)

        self._id: str = id
        self._region: AWSRegion = region
        self._type: str = type
        self._host: str = host
        self._port: int = port if port != -1 else \
            {'postgresql': 5432, 'mysql': 3306}[engine_type]
        self._engine_type: str = engine_type
        self._dbname: str = dbname if dbname else id
        self._patch: RDSDatabasePatch = patch

        self._region.add_rds_database(database=self)

    @property
    def id(self) -> str:
        return self._id

    @property
    def region(self):
        return self._region

    @property
    def type(self) -> str:
        return self._type

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def engine_type(self) -> str:
        return self._engine_type

    @property
    def dbname(self) -> str:
        return self._dbname

    @property
    def patch(self) -> RDSDatabasePatch:
        return self._patch

    @patch.setter
    def patch(self, patch: RDSDatabasePatch) -> None:
        self._patch = patch

    def is_postgresql(self) -> bool:
        """
        Check if this RDS database is PostgreSQL.

        :return: True if this RDS database is PostgreSQL.
        :rtype: bool
        """

        return self._engine_type == "postgresql"

    def is_mysql(self) -> bool:
        """
        Check if this RDS database is MySQL.

        :return: True if this RDS database is MySQL.
        :rtype: bool
        """

        return self._engine_type == "mysql"

    def __str__(self) -> str:
        return f"RDSDatabase(id: {self._id}, type: {self._type}" + \
            f", host: {self._host}, port: {self._port}" + \
            f", engine_type: {self._engine_type}, engine_version: {self._engine_version}" + \
            f", class_type: {self._class_type}, dbname: {self._dbname})"
