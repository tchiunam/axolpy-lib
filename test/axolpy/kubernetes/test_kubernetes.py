import pytest
from axolpy.aws import AWSRegion
from axolpy.kubernetes import (AWSClusterRef, Cluster, Deployment, Namespace,
                               StatefulSet)


class TestKubernetesModel(object):
    def test_cluster(self):
        cluster_name = "starwars"
        cluster = Cluster(name=cluster_name)
        pytest.test_kubernetes_model_cluster: Cluster = cluster

        assert cluster.name == cluster_name

    def test_namespace(self):
        cluster = pytest.test_kubernetes_model_cluster
        namespace_name = "general"
        namespace = Namespace(name=namespace_name, cluster=cluster)
        pytest.test_kubernetes_model_namespace: Namespace = namespace

        assert namespace.name == namespace_name
        assert namespace.cluster == cluster
        assert namespace.stateful_sets == {}
        assert namespace.deployments == {}

        assert cluster.namespace(namespace_name) == namespace
        assert str(cluster) == f"{cluster.__class__.__name__}" + \
            f"(name: {cluster.name}, {len(cluster.namespaces)} namespaces)"

    def test_deployment(self):
        deployment_name = "authentication"
        replicas = 4

        d = Deployment(name=deployment_name,
                       namespace=pytest.test_kubernetes_model_namespace,
                       replicas=replicas,
                       foo="bar")
        d.add_property(name="priority", value=2)

        actual_deployment = pytest.test_kubernetes_model_namespace.deployment(
            deployment_name)

        assert actual_deployment.name == deployment_name
        assert actual_deployment.namespace == pytest.test_kubernetes_model_namespace
        assert actual_deployment.replicas == replicas
        assert actual_deployment.property("foo") == "bar"
        assert actual_deployment.property("priority") == 2
        assert str(
            actual_deployment) == f"{actual_deployment.__class__.__name__}" + \
            f"(name: {deployment_name}, replicas: {replicas}, 2 properties)"

    def test_statefulset(self):
        statefulset_name = "profiler"
        replicas = 10

        s = StatefulSet(name=statefulset_name,
                        namespace=pytest.test_kubernetes_model_namespace,
                        replicas=replicas,
                        foo="bar")
        s.add_property(name="priority", value=2)

        actual_statefulset = pytest.test_kubernetes_model_namespace.stateful_set(
            statefulset_name)

        assert actual_statefulset.name == statefulset_name
        assert actual_statefulset.namespace == pytest.test_kubernetes_model_namespace
        assert actual_statefulset.replicas == replicas
        assert actual_statefulset.property("foo") == "bar"
        assert actual_statefulset.property("priority") == 2
        assert str(
            actual_statefulset) == f"{actual_statefulset.__class__.__name__}" + \
            f"(name: {statefulset_name}, replicas: {replicas}, 2 properties)"

    def test_namespace_after_adding_resources(self):
        assert str(
            pytest.test_kubernetes_model_namespace) == f"{pytest.test_kubernetes_model_namespace.__class__.__name__}" + \
            f"(name: {pytest.test_kubernetes_model_namespace.name}, 1 stateful_sets, 1 deployments)"


def test_aws_cluster_ref():
    aws_region = AWSRegion(name="us-east-1")
    aws_cluster_ref = AWSClusterRef(region=aws_region)

    cluster_name = "starwars"
    cluster = Cluster(name=cluster_name, platform_ref=aws_cluster_ref)

    assert cluster.platform_ref.region.name == aws_region.name
