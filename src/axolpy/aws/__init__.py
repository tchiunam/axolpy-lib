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

    @property
    def name(self) -> str:
        return self._name

    @property
    def eks_clusters(self) -> Dict[str, Cluster]:
        return self._eks_clusters.copy()

    def add_eks_cluster(self, cluster: Cluster) -> None:
        """
        Add a cluster to this region.

        :param cluster: A EKS Cluster.
        :type cluster: :class:`Cluster`
        """

        self._eks_clusters[cluster.name] = cluster

    def __str__(self) -> str:
        return f"{__class__.__name__}(name: {self._name}, {len(self._eks_clusters)} EKS clusters)"


class ECSService(object):
    def __init__(self,
                 name: str,
                 desired_count: int = 0,
                 **kwargs) -> None:
        self._name: str = name
        self._desired_count: int = desired_count
        # Properties is used to store the properties of this ECS Service
        # which are not the standard attributes of it.
        self._properties: dict = dict()
        for k, v in kwargs.items():
            self.add_property(name=k, value=v)

    @property
    def name(self) -> str:
        return self._name

    @property
    def desired_count(self) -> int:
        return self._desired_count

    def add_property(self, name: str, value: Any) -> None:
        self._properties[name] = value

    def property(self, name) -> Any:
        return self._properties.get(name, None)

    def __str__(self) -> str:
        return f"{__class__.__name__}(name: {self._name}, desired_count: {self._desired_count}" + \
            f", patch: {self._patch})"
