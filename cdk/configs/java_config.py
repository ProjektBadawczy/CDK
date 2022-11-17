from cdk.factories.container_factory import create_container
from aws_cdk.aws_ecs import Ec2TaskDefinition, PortMapping, Protocol


def configure_java_microservices(task_definition: Ec2TaskDefinition, graphs_type: str):
    api_gateway = create_container(task=task_definition, container_name="api-gateway",
                                   image_path="piotrszymanski/microservicesjava-api-gateway", memory_limit=1024,
                                   port_mapping=PortMapping(container_port=8001, host_port=8001,
                                                            protocol=Protocol.TCP))
    graph_service = create_container(task=task_definition, container_name="graph-service",
                                     image_path="piotrszymanski/microservicesjava-graph-service:" + graphs_type,
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