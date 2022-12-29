from aws_cdk.aws_ecs import Ec2TaskDefinition, PortMapping, Protocol
from cdk.factories.container_factory import create_container

def configure_dotnet_microservices(task_definition: Ec2TaskDefinition, graphs_type: str):
    api_gateway = create_container(task=task_definition, container_name="api-gateway",
                                   image_path="weronikapiotrowska/microservicesdotnet-api-gateway", memory_limit=1024,
                                   port_mapping=PortMapping(container_port=8001, host_port=8001,
                                                            protocol=Protocol.TCP))
    graph_service = create_container(task=task_definition, container_name="graph-service",
                                     image_path="weronikapiotrowska/microservicesdotnet-graph-service:" + graphs_type,
                                     memory_limit=2048)
    bfs_service = create_container(task=task_definition, container_name="bfs-service",
                                   image_path="weronikapiotrowska/microservicesdotnet-bfs-service", memory_limit=1024)
    edmonds_karp_service = create_container(task=task_definition, container_name="edmonds-karp-service",
                                            image_path="weronikapiotrowska/microservicesdotnet-edmonds-karp-service",
                                            memory_limit=1024)
    push_relabel_service = create_container(task=task_definition, container_name="push-relabel-service",
                                            image_path="weronikapiotrowska/microservicesdotnet-push-relabel-service",
                                            memory_limit=1024)

    api_gateway.add_link(graph_service, "graph-service")
    api_gateway.add_link(bfs_service, "bfs-service")
    api_gateway.add_link(edmonds_karp_service, "edmonds-karp-service")
    api_gateway.add_link(push_relabel_service, "push-relabel-service")
    bfs_service.add_link(graph_service, "graph-service")
    edmonds_karp_service.add_link(graph_service, "graph-service")
    edmonds_karp_service.add_link(bfs_service, "bfs-service")
    push_relabel_service.add_link(graph_service, "graph-service")
    push_relabel_service.add_link(bfs_service, "bfs-service")
