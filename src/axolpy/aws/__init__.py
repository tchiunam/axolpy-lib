from typing import Dict

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
