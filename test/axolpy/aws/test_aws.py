import pytest
from axolpy.aws import AWSRegion, ECSCluster, ECSService


class TestAWSRegionModel(object):
    def test_aws_region(self):
        """
        Test using AWSRegion.
        """

        region_name = "us-east-1"

        region = AWSRegion(name=region_name)
        pytest.test_aws_region_model_region: AWSRegion = region

        assert region.name == region_name
        assert region.eks_clusters == {}
        assert region.ecs_clusters == {}

        assert str(
            region) == f"{region.__class__.__name__}(name: {region_name}, 0 EKS clusters, 0 ECS clusters)"

    def test_ecs_cluster(self):
        """
        Test using ECSCluster.
        """

        region: AWSRegion = pytest.test_aws_region_model_region
        cluster_name = "test-cluster"

        cluster = ECSCluster(name=cluster_name, region=region)
        pytest.test_aws_region_model_ecs_cluster: ECSCluster = cluster

        actual_cluster = region.ecs_cluster(name=cluster_name)

        assert actual_cluster.name == cluster_name
        assert actual_cluster.region.name == region.name
        assert actual_cluster.services == {}

        assert str(
            actual_cluster) == f"{actual_cluster.__class__.__name__}(name: {cluster_name}, 0 services)"
        assert str(
            region) == f"{region.__class__.__name__}(name: {region.name}, 0 EKS clusters, 1 ECS clusters)"

    def test_ecs_service(self):
        """
        Test using ECSService.
        """

        cluster: ECSCluster = pytest.test_aws_region_model_ecs_cluster
        service_name = "test-service"
        desired_count = 5

        service = ECSService(
            name=service_name,
            cluster=cluster,
            desired_count=desired_count,
            foo="bar")
        service.add_property(name="priority", value=2)

        actual_service = cluster.service(name=service_name)

        assert actual_service.name == service_name
        assert actual_service.cluster == cluster
        assert actual_service.desired_count == desired_count
        assert actual_service.property("foo") == "bar"
        assert actual_service.property("priority") == 2

        assert str(
            actual_service) == f"{service.__class__.__name__}(name: {service_name}, desired_count: {desired_count}, 2 properties)"
        assert str(
            cluster) == f"{cluster.__class__.__name__}(name: {cluster.name}, 1 services)"
