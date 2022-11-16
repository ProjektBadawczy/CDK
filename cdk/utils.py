from aws_cdk.aws_ecs import PortMapping, Ec2TaskDefinition, ContainerImage, LogDrivers, Ec2Service, Protocol
from aws_cdk.aws_elasticloadbalancingv2 import ApplicationProtocol, ApplicationLoadBalancer
from aws_cdk.aws_stepfunctions_tasks import ContainerDefinition


def create_containers(app_version: str, task_definition: Ec2TaskDefinition):
    match app_version:
        case "java":
            return configure_java_microservices(task_definition)
        case "dotnet":
            return configure_dotnet_microservices(task_definition)
        case "cpp":
            return configure_cpp_microservices(task_definition)


def configure_java_microservices(task_definition: Ec2TaskDefinition):
    api_gateway = create_container(task=task_definition, container_name="api-gateway",
                                   image_path="piotrszymanski/microservicesjava-api-gateway", memory_limit=1024,
                                   port_mapping=PortMapping(container_port=8001, host_port=8001,
                                                            protocol=Protocol.TCP))
    graph_service = create_container(task=task_definition, container_name="graph-service",
                                     image_path="piotrszymanski/microservicesjava-graph-service:big-dense",
                                     memory_limit=2048)
    bfs_service = create_container(task=task_definition, container_name="bfs-service",
                                   image_path="piotrszymanski/microservicesjava-bfs-service", memory_limit=1024)
    edmonds_karp_service = create_container(task=task_definition, container_name="edmonds-karp-service",
                                            image_path="piotrszymanski/microservicesjava-edmonds-karp-service",
                                            memory_limit=1024)
    push_relabel_service = create_container(task=task_definition, container_name="push-relabel-service",
                                            image_path="piotrszymanski/microservicesjava-push-relabel-service",
                                            memory_limit=1024)
    eureka_server = create_container(task=task_definition, container_name="eureka-server",
                                     image_path="piotrszymanski/microservicesjava-eureka-server", memory_limit=1024)

    api_gateway.add_link(graph_service, "graph-service")
    api_gateway.add_link(bfs_service, "bfs-service")
    api_gateway.add_link(edmonds_karp_service, "edmonds-karp-service")
    api_gateway.add_link(push_relabel_service, "push-relabel-service")
    api_gateway.add_link(eureka_server, "eureka-server")
    graph_service.add_link(eureka_server, "eureka-server")
    bfs_service.add_link(graph_service, "graph-service")
    bfs_service.add_link(eureka_server, "eureka-server")
    edmonds_karp_service.add_link(graph_service, "graph-service")
    edmonds_karp_service.add_link(bfs_service, "bfs-service")
    edmonds_karp_service.add_link(eureka_server, "eureka-server")
    push_relabel_service.add_link(graph_service, "graph-service")
    push_relabel_service.add_link(bfs_service, "bfs-service")
    push_relabel_service.add_link(eureka_server, "eureka-server")


def configure_dotnet_microservices(task_definition: Ec2TaskDefinition):
    # TODO implement me!
    # You need to create all of your containers and all needed links
    # Link allows you to make calls to other containers using their names
    # If you need to call graph_service from edmonds_karp_service add line
    # edmonds_karp_service.add_link(graph_service, "graph_service")
    pass


def configure_cpp_microservices(task_definition: Ec2TaskDefinition):
    # TODO implement me!
    # You need to create all of your containers and all needed links
    # Link allows you to make calls to other containers using their names
    # If you need to call graph_service from edmonds_karp_service add line
    # edmonds_karp_service.add_link(graph_service, "graph_service")
    pass


def create_listener(app_version: str, lb: ApplicationLoadBalancer, service: Ec2Service):
    match app_version:
        case "java":
            return inner_create_listener("api-gateway", lb, service)
        case "dotnet":
            # TODO fill me with real api gateway container name!
            return inner_create_listener("CHANGE ME!!!", lb, service)
        case "cpp":
            # TODO fill me with real api gateway container name!
            return inner_create_listener("CHANGE ME!!!", lb, service)


def inner_create_listener(api_gateway_container_name: str, lb: ApplicationLoadBalancer, service: Ec2Service):
    listener = lb.add_listener("PublicListener", port=8001, open=True, protocol=ApplicationProtocol.HTTP)
    listener.add_targets('ECS', port=8001, protocol=ApplicationProtocol.HTTP,
                         targets=[service.load_balancer_target(
                             container_name=api_gateway_container_name,
                             container_port=8001)])


def create_container(task: Ec2TaskDefinition, container_name: str, image_path: str, memory_limit: int,
                     port_mapping: PortMapping = None) -> ContainerDefinition:
    return task.add_container(container_name,
                       container_name=container_name,
                       image=ContainerImage.from_registry(image_path),
                       port_mappings=[port_mapping] if port_mapping is not None else None,
                       memory_limit_mib=memory_limit,
                       logging=LogDrivers.aws_logs(stream_prefix="microservices" + container_name))

