from axolpy.aws import AWSRegion
from axolpy.kubernetes import Cluster


def test_aws_region():
    """
    Test using AWSRegion.
    """

    region = AWSRegion("us-east-1")
    assert region.name == "us-east-1"
    assert region.eks_clusters == {}

    region.add_eks_cluster(Cluster("test-cluster"))
    assert region.eks_clusters["test-cluster"].name == "test-cluster"
    assert str(
        region) == f"{region.__class__.__name__}(name: us-east-1, 1 EKS clusters)"
