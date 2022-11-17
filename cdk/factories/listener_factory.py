from aws_cdk.aws_ecs import Ec2Service
from aws_cdk.aws_elasticloadbalancingv2 import ApplicationLoadBalancer, ApplicationProtocol


def create_microservices_listener(app_version: str, lb: ApplicationLoadBalancer, service: Ec2Service):
    match app_version:
        case "java":
            return inner_create_listener("api-gateway", lb, service)
        case "dotnet":
            # TODO fill me with real api gateway container name!
            return inner_create_listener("CHANGE ME!!!", lb, service)
        case "cpp":
            # TODO fill me with real api gateway container name!
            return inner_create_listener("CHANGE ME!!!", lb, service)


def create_monolith_listener(app_version: str, lb: ApplicationLoadBalancer, service: Ec2Service):
    match app_version:
        case "java":
            return inner_create_listener("monolith", lb, service)
        case "dotnet":
            # TODO fill me with real monolith container name!
            return inner_create_listener("CHANGE ME!!!", lb, service)
        case "cpp":
            # TODO fill me with real monolith container name!
            return inner_create_listener("CHANGE ME!!!", lb, service)


def inner_create_listener(internet_facing_container_name: str, lb: ApplicationLoadBalancer, service: Ec2Service):
    listener = lb.add_listener("PublicListener", port=8001, open=True, protocol=ApplicationProtocol.HTTP)
    listener.add_targets('ECS', port=8001, protocol=ApplicationProtocol.HTTP,
                         targets=[service.load_balancer_target(
                             container_name=internet_facing_container_name,
                             container_port=8001)])
