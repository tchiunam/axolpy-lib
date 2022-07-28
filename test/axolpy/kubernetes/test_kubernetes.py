import pytest
from axolpy.aws import AWSRegion
from axolpy.kubernetes import (AWSClusterRef, Cluster, Deployment,
                               DeploymentPatch, Namespace, StatefulSet)


class TestKubernetesModel(object):
    def test_cluster(self):
        """
        Test using Cluster.
        """

        cluster_name = "starwars"
        cluster = Cluster(name=cluster_name)
        pytest.test_kubernetes_model_cluster: Cluster = cluster

        assert cluster.name == cluster_name

    def test_namespace(self):
        """
        Test using Namespace.
        """

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
        """
        Test using Deployment.
        """

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
        """
        Test using StatefulSet.
        """

        statefulset_name = "profiler"
        replicas = 10

        namespace = pytest.test_kubernetes_model_namespace
        s = StatefulSet(name=statefulset_name,
                        namespace=namespace,
                        replicas=replicas,
                        foo="bar")
        s.add_property(name="priority", value=2)

        actual_statefulset = namespace.stateful_set(
            statefulset_name)

        assert actual_statefulset.name == statefulset_name
        assert actual_statefulset.namespace == namespace
        assert actual_statefulset.replicas == replicas
        assert actual_statefulset.property("foo") == "bar"
        assert actual_statefulset.property("priority") == 2
        assert str(
            actual_statefulset) == f"{actual_statefulset.__class__.__name__}" + \
            f"(name: {statefulset_name}, replicas: {replicas}, 2 properties)"

    def test_namespace_after_adding_resources(self):
        """
        Test namespace after resources are added.
        """

        namespace = pytest.test_kubernetes_model_namespace
        assert str(
            namespace) == f"{namespace.__class__.__name__}" + \
            f"(name: {namespace.name}, 1 stateful_sets, 1 deployments)"


def test_aws_cluster_ref():
    """
    Test using AWSClusterRef.
    """

    aws_region = AWSRegion(name="us-east-1")
    aws_cluster_ref = AWSClusterRef(region=aws_region)

    cluster_name = "starwars"
    cluster = Cluster(name=cluster_name, platform_ref=aws_cluster_ref)

    assert cluster.platform_ref.region.name == aws_region.name
    assert cluster.platform_ref.region.eks_cluster(cluster_name) == cluster


def test_deployment_patch_model():
    """
    Test deployment patch model.
    """

    patch_replicas = 4

    patch = DeploymentPatch(replicas=patch_replicas)

    assert patch.replicas == patch_replicas
    assert str(patch) == f"{patch.__class__.__name__}" + \
        f"(replicas: {patch_replicas})"

    d = Deployment(name="test-deployment",
                   namespace=Namespace(name="test-namespace",
                                       cluster=Cluster(name="test-cluster")),
                   replicas=1)

    d.patch = patch

    assert d.patch.replicas == patch_replicas
