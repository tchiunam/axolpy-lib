from __future__ import annotations

from abc import ABC
from typing import Any, Dict


class ClusterCloudPlatformRef(ABC):
    """
    A reference to a cluster in a cloud platform.
    """

    pass


class AWSClusterRef(ClusterCloudPlatformRef):
    """
    AWS Cluster Ref for a cluster in AWS cloud platform.
    """

    def __init__(self, region: Any) -> None:
        """
        Initialize this Ref.

        :param region: The region of this cluster.
        :type region: :class:`AWSRegion`
        """

        self._region: Any = region

    @property
    def region(self) -> Any:
        return self._region


class Cluster(object):
    def __init__(self, name: str, platform_ref: ClusterCloudPlatformRef = None) -> None:
        """
        A Cluster in kubernetes.

        :param name: The name of Cluster.
        :type name: str
        :param platform_ref: Ref of cloud platform of this cluster is in.
        :type platform_ref: :class:`ClusterCloudPlatformRef`
        """

        self._name: str = name
        self._namespaces: Dict[str, Namespace] = dict()
        self._platform_ref: ClusterCloudPlatformRef = platform_ref

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespaces(self) -> Dict[str, Namespace]:
        return self._namespaces.copy()

    def namespace(self, name: str) -> Namespace:
        return self._namespaces[name]

    def add_namespace(self, namespace: Namespace) -> None:
        self._namespaces[namespace.name] = namespace

    @property
    def platform_ref(self) -> ClusterCloudPlatformRef:
        return self._platform_ref

    def __str__(self) -> str:
        return f"{__class__.__name__}(name: {self._name}, {len(self._namespaces)} namespaces)"


class Namespace(object):
    def __init__(
            self,
            name: str,
            cluster: Cluster) -> None:
        """
        A Namespace in kubernetes cluster.

        :param name: The name of Namespace.
        :type name: str
        :param cluster: The cluster this Namespace is in.
        :type cluster: :class:`Cluster`
        """

        self._name: str = name
        self._cluster: Cluster = cluster
        self._stateful_sets: Dict[str, StatefulSet] = dict()
        self._deployments: Dict[str, Deployment] = dict()

        cluster.add_namespace(namespace=self)

    @property
    def name(self) -> str:
        return self._name

    @property
    def cluster(self):
        return self._cluster

    @property
    def stateful_sets(self) -> Dict[str, StatefulSet]:
        return self._stateful_sets.copy()

    def stateful_set(self, name: str) -> StatefulSet:
        return self._stateful_sets[name]

    def add_stateful_set(self, stateful_set: StatefulSet) -> None:
        self._stateful_sets[stateful_set.name] = stateful_set

    @property
    def deployments(self) -> Dict[str, Deployment]:
        return self._deployments.copy()

    def deployment(self, name: str) -> Deployment:
        return self._deployments[name]

    def add_deployment(self, deployment: Deployment) -> None:
        self._deployments[deployment.name] = deployment

    def __str__(self) -> str:
        return f"{__class__.__name__}(name: {self._name}, {len(self._stateful_sets)} stateful_sets" + \
            f", {len(self._deployments)} deployments)"


class StatefulSet(object):
    def __init__(self,
                 name: str,
                 namespace: Namespace,
                 replicas: int,
                 **kwargs) -> None:
        """
        A StatefulSet in kubernetes cluster.

        :param name: The name of StatefulSet.
        :type name: str
        :param namespace: The namespace this Deployment is in.
        :type namespace: :class:`Namespace`
        :param replicas: The number of replicas of StatefulSet.
        :type replicas: int
        """

        self._name: str = name
        self._namespace: Namespace = namespace
        self._replicas: int = replicas
        # Properties is used to store the properties of this StatefulSet
        # which are not the standard attributes of k8s.
        self._properties: dict = dict()
        for k, v in kwargs.items():
            self.add_property(name=k, value=v)

        self._namespace.add_stateful_set(stateful_set=self)

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace(self) -> Namespace:
        return self._namespace

    @property
    def replicas(self) -> int:
        return self._replicas

    def add_property(self, name: str, value: Any) -> None:
        self._properties[name] = value

    def property(self, name) -> Any:
        return self._properties.get(name, None)

    def __str__(self) -> str:
        return f"{__class__.__name__}(name: {self._name}, replicas: {self._replicas}" + \
            f", {len(self._properties)} properties)"


class Deployment(object):
    def __init__(self,
                 name: str,
                 namespace: Namespace,
                 replicas: int,
                 **kwargs) -> None:
        """
        A Deployment in kubernetes cluster.

        :param name: The name of Deployment.
        :type name: str
        :param namespace: The namespace this Deployment is in.
        :type namespace: :class:`Namespace`
        :param replicas: The number of replicas of Deployment.
        :type replicas: int
        """

        self._name: str = name
        self._namespace: Namespace = namespace
        self._replicas: int = replicas
        # Properties is used to store the properties of this Deployment
        # which are not the standard attributes of k8s.
        self._properties: dict = dict()
        for k, v in kwargs.items():
            self.add_property(name=k, value=v)

        self._namespace.add_deployment(deployment=self)

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace(self) -> Namespace:
        return self._namespace

    @property
    def replicas(self) -> int:
        return self._replicas

    def add_property(self, name: str, value: Any) -> None:
        self._properties[name] = value

    def property(self, name) -> Any:
        return self._properties.get(name, None)

    def __str__(self) -> str:
        return f"{__class__.__name__}(name: {self._name}, replicas: {self._replicas}" + \
            f", {len(self._properties)} properties)"
