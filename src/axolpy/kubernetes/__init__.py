from typing import Any


class Deployment(object):
    def __init__(self,
                 name: str,
                 replicas: int,
                 **kwargs) -> None:
        """
        A Deployment in kubernetest cluster.

        :param name: The name of Deployment.
        :type name: str
        :param replicas: The number of replicas of Deployment.
        :type replicas: int
        """

        self._name: str = name
        self._replicas: int = replicas
        # Propertise is used to store the properties of the deployment
        # which are not the standard attributes of k8s deployment.
        self._properties: dict = dict()
        for k, v in kwargs.items():
            self.add_property(name=k, value=v)

    @property
    def name(self) -> str:
        return self._name

    @property
    def replicas(self) -> int:
        return self._replicas

    def add_property(self, name: str, value: Any) -> None:
        self._properties[name] = value

    def property(self, name) -> Any:
        return self._properties.get(name, None)

    def __str__(self) -> str:
        return f"{__class__.__name__}(name: {self._name}, replicas: {self._replicas}, " + \
            f"{len(self._properties)} properties)"


class StatefulSet(object):
    def __init__(self,
                 name: str,
                 replicas: int,
                 **kwargs) -> None:
        """
        A StatefulSet in kubernetest cluster.

        :param name: The name of StatefulSet.
        :type name: str
        :param replicas: The number of replicas of StatefulSet.
        :type replicas: int
        """

        self._name: str = name
        self._replicas: int = replicas
        self._properties: dict = dict()
        for k, v in kwargs.items():
            self.add_property(name=k, value=v)

    @property
    def name(self) -> str:
        return self._name

    @property
    def replicas(self) -> int:
        return self._replicas

    def add_property(self, name: str, value: Any) -> None:
        self._properties[name] = value

    def property(self, name) -> Any:
        return self._properties.get(name, None)

    def __str__(self) -> str:
        return f"{__class__.__name__}(name: {self._name}, replicas: {self._replicas}, " + \
            f"{len(self._properties)} properties)"
