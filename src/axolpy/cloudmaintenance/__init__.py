from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List

import yaml

from ..aws import (AWSRegion, ECSCluster, ECSService, ECSServicePatch,
                   RDSDatabase, RDSDatabasePatch)
from ..kubernetes import (AWSClusterRef, Cluster, Deployment, DeploymentPatch,
                          Namespace, StatefulSet, StatefulSetPatch)


class ResourceDataLoader(object):
    """
    Load a collectiom of cloud resources from a file.
    """

    @classmethod
    def load_from_file(cls,
                       data_path: Path,
                       maintenance_id: str) -> Dict[str, AWSRegion]:
        """
        Load the resources from a file.

        :param data_path: Base path storing data files.
        :type data_path: :class:`Path`
        :param maintenance_id: Maintenance ID.
        :type maintenance_id: str

        :return: A dictionary of AWSRegions.
        :rtype: Dict[str, :class:`AWSRegion`]
        """

        database_optional_attrs = ["port",
                                   "engine_type",
                                   "engine_version",
                                   "class_type",
                                   "dbname"]
        database_patch_optional_attrs = ["engine_version", "class_type"]
        ecs_service_optional_props = ["restart_after_upgrade"]
        ecs_service_patch_optional_attrs = ["desired_count"]
        eks_statefulset_optional_props = ["restart_after_upgrade"]
        eks_statefulset_patch_optional_attrs = ["replicas"]
        eks_deployment_optional_props = ["restart_after_upgrade"]
        eks_deployment_patch_optional_attrs = ["replicas"]

        aws_regions: Dict[str, AWSRegion] = dict()

        resources_yaml = yaml.safe_load(
            data_path.joinpath(maintenance_id, "resource.yaml").read_text())
        for region_name, region_yaml in resources_yaml["regions"].items():
            region = AWSRegion(name=region_name)
            aws_regions[region_name] = region

            # Extract database resources
            # Lookup attributes needed for database object
            for database_yaml in region_yaml["databases"] if "databases" in region_yaml else []:
                db_attr = {"id": database_yaml["id"],
                           "region": region,
                           "type": database_yaml["type"],
                           "host": database_yaml["host"]}
                for attr in database_optional_attrs:
                    if attr in database_yaml:
                        db_attr[attr] = database_yaml[attr]

                # Lookup attributes needed for patching
                if "patch" in database_yaml:
                    patch_attr = dict()
                    for attr in database_patch_optional_attrs:
                        if attr in database_yaml["patch"]:
                            patch_attr[attr] = database_yaml["patch"][attr]
                    db_attr["patch"] = RDSDatabasePatch(**patch_attr)

                region.add_rds_database(database=RDSDatabase(**db_attr))

            # Extract ecs cluster resources
            for cluster_name, cluster_yaml in region_yaml["ecs"]["clusters"].items() \
                    if "ecs" in region_yaml and "clusters" in region_yaml["ecs"] else []:
                cluster = ECSCluster(
                    name=cluster_name,
                    region=region)

                for service_yaml in cluster_yaml["services"] if "services" in cluster_yaml else []:
                    svc_attr = {"name": service_yaml["name"],
                                "cluster": cluster,
                                "desired_count": service_yaml["desired_count"]}

                    # Lookup attributes needed for patching
                    if "patch" in service_yaml:
                        patch_attr = dict()
                        for attr in ecs_service_patch_optional_attrs:
                            if attr in service_yaml["patch"]:
                                patch_attr[attr] = service_yaml["patch"][attr]
                        svc_attr["patch"] = ECSServicePatch(
                            **patch_attr)
                    for prop in ecs_service_optional_props if "properties" in service_yaml else []:
                        if prop in service_yaml["properties"]:
                            svc_attr[prop] = service_yaml["properties"][prop]
                    cluster.add_service(service=ECSService(**svc_attr))

            # Extract eks resources
            for cluster_name, cluster_yaml in region_yaml["eks"]["clusters"].items() \
                    if "eks" in region_yaml and "clusters" in region_yaml["eks"] else []:
                cluster = Cluster(
                    name=cluster_name,
                    platform_ref=AWSClusterRef(region=region))

                for namespace_name, namespace_yaml in cluster_yaml["namespaces"].items():
                    namespace = Namespace(
                        name=namespace_name,
                        cluster=cluster)

                    # Extract StatefulSets
                    for sts_yaml in namespace_yaml["statefulsets"] if "statefulsets" in namespace_yaml else []:
                        sts_attr = {"name": sts_yaml["name"],
                                    "namespace": namespace,
                                    "replicas": sts_yaml["replicas"]}

                        # Lookup attributes needed for patching
                        if "patch" in sts_yaml:
                            patch_attr = dict()
                            for attr in eks_statefulset_patch_optional_attrs:
                                if attr in sts_yaml["patch"]:
                                    patch_attr[attr] = sts_yaml["patch"][attr]
                            sts_attr["patch"] = StatefulSetPatch(
                                **patch_attr)
                        for prop in eks_statefulset_optional_props if "properties" in sts_yaml else []:
                            if prop in sts_yaml["properties"]:
                                sts_attr[prop] = sts_yaml["properties"][prop]

                        namespace.add_statefulset(
                            statefulset=StatefulSet(**sts_attr))

                    # Extract deployments
                    for dpm_yml in namespace_yaml["deployments"] \
                            if "deployments" in namespace_yaml else []:
                        dpm_attr = {"name": dpm_yml["name"],
                                    "namespace": namespace,
                                    "replicas": dpm_yml["replicas"]}

                        # Lookup attributes needed for patching
                        if "patch" in dpm_yml:
                            patch_attr = dict()
                            for attr in eks_deployment_patch_optional_attrs:
                                if attr in dpm_yml["patch"]:
                                    patch_attr[attr] = dpm_yml["patch"][attr]
                            dpm_attr["patch"] = DeploymentPatch(
                                **patch_attr)
                        for prop in eks_deployment_optional_props \
                                if "properties" in dpm_yml else []:
                            if prop in dpm_yml["properties"]:
                                dpm_attr[prop] = dpm_yml["properties"][prop]

                        namespace.add_deployment(
                            deployment=Deployment(**dpm_attr))

        return aws_regions


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
        self._eks_statefulsets: List[StatefulSet] = list()

        self._data_loader: OperatorDataLoader = OperatorDataLoader(self)

    @property
    def id(self) -> str:
        return self._id

    @property
    def eks_deployments(self) -> Iterable[Deployment]:
        return self._eks_deployments

    @property
    def eks_statefulsets(self) -> Iterable[StatefulSet]:
        return self._eks_statefulsets

    @property
    def ecs_services(self) -> Iterable[ECSService]:
        return self._ecs_services

    @property
    def rds_databases(self) -> Iterable[RDSDatabase]:
        return self._rds_databases

    @property
    def data_loader(self) -> OperatorDataLoader:
        return self._data_loader

    def add_eks_deployment(self, deployment: Deployment) -> None:
        self._eks_deployments.append(deployment)

    def add_eks_statefulset(self, statefulset: StatefulSet) -> None:
        self._eks_statefulsets.append(statefulset)

    def add_ecs_service(self, service: ECSService) -> None:
        self._ecs_services.append(service)

    def add_rds_databases(self, database: RDSDatabase) -> None:
        self._rds_databases.append(database)


class OperatorDataLoader(object):
    """
    A data loader to read operator data from a file.
    """

    def __init__(self,
                 operator: Operator) -> None:
        """
        Initialize a data loader.

        :param operator: The operator to load data for.
        :type operator: :class:`Operator`
        """

        self._operator = operator

    def load_from_file(self,
                       data_path: Path,
                       maintenance_id: str,
                       aws_regions: Dict[str, AWSRegion]) -> None:
        """
        Load the operator from a file.

        :param data_path: Base path storing data files.
        :type data_path: :class:`Path`
        :param maintenance_id: Maintenance ID.
        :type maintenance_id: str
        :param aws_regions: Data of all regions.
        :type aws_regions: Dict[str, :class:`AWSRegion`]
        """

        operator_yaml = yaml.safe_load(
            data_path.joinpath(maintenance_id,
                               "operator.yaml").read_text())

        for region_name, region_yaml in operator_yaml[self._operator.id].items():
            region = aws_regions[region_name]

            # Extract databases detail
            if "databases" in region_yaml:
                for database in region_yaml["databases"]:
                    self._operator.add_rds_databases(
                        region.rds_database(id=database["id"]))

            # Extract ecs servcies detail
            if "ecs" in region_yaml and "clusters" in region_yaml["ecs"]:
                for cluster_name, cluster_yaml in region_yaml["ecs"]["clusters"].items():
                    if "services" in cluster_yaml:
                        for service in cluster_yaml["services"]:
                            self._operator.add_ecs_service(
                                service=region.ecs_cluster(name=cluster_name).service(name=service["name"]))

            # Extract eks resources detail
            if "eks" in region_yaml and "clusters" in region_yaml["eks"]:
                for cluster_name, cluster_yaml in region_yaml["eks"]["clusters"].items():
                    if "namespaces" in cluster_yaml:
                        for namespace_name, namespace_yaml in cluster_yaml["namespaces"].items():
                            if "statefulsets" in namespace_yaml:
                                for statefulset in namespace_yaml["statefulsets"]:
                                    self._operator.add_eks_statefulset(
                                        statefulset=region.eks_cluster(name=cluster_name).namespace(name=namespace_name).statefulset(name=statefulset["name"]))
                            if "deployments" in namespace_yaml:
                                for deployment in namespace_yaml["deployments"]:
                                    self._operator.add_eks_deployment(
                                        deployment=region.eks_cluster(name=cluster_name).namespace(name=namespace_name).deployment(name=deployment["name"]))
