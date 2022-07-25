from __future__ import annotations

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

    def __str__(self) -> str:
        return f"{__class__.__name__}(name: {self._name}, {len(self._eks_clusters)} EKS clusters" + \
            f", {len(self._ecs_clusters)} ECS clusters)"


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


class ECSService(object):
    def __init__(self,
                 name: str,
                 cluster: ECSCluster,
                 desired_count: int = 0,
                 **kwargs) -> None:
        """
        A ECS Service in ECS cluster.

        : param name: The name of ECS Service.
        : type name: str
        : param cluster: The cluster this ECS Service is in.
        : type cluster: : class: `ECSCluster`
        """

        self._name: str = name
        self._cluster: Cluster = cluster
        self._desired_count: int = desired_count
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
    def desired_count(self) -> int:
        return self._desired_count

    def add_property(self, name: str, value: Any) -> None:
        self._properties[name] = value

    def property(self, name) -> Any:
        return self._properties.get(name, None)

    def __str__(self) -> str:
        return f"{__class__.__name__}(name: {self._name}, desired_count: {self._desired_count}" + \
            f", {len(self._properties)} properties)"
