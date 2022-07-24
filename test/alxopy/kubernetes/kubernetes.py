from axolpy.kubernetes import Deployment, StatefulSet


def test_eks_deployment():
    d = Deployment(name="test", replicas=1, foo="bar")
    d.add_property(name="priority", value=2)

    assert d.name == "test"
    assert d.replicas == 1
    assert d.property("foo") == "bar"
    assert d.property("priority") == 2
    assert str(
        d) == f"{d.__class__.__name__}(name: test, replicas: 1, 2 properties)"


def test_eks_statefulset():
    d = StatefulSet(name="test", replicas=1, foo="bar")
    d.add_property(name="priority", value=2)

    assert d.name == "test"
    assert d.replicas == 1
    assert d.property("foo") == "bar"
    assert d.property("priority") == 2
    assert str(
        d) == f"{d.__class__.__name__}(name: test, replicas: 1, 2 properties)"
