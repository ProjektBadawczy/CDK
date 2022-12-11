from aws_cdk.aws_ecs import Ec2TaskDefinition


def configure_cpp_microservices(task_definition: Ec2TaskDefinition, graphs_type: str):
    prefix = "quetzonarch/researchprojectmicroservicescpp_"
    suffix = "_sparse" if graphs_type=="small-sparse" else ""
    env_vars = {["INSIDE_DOCKER"]: "1"}
    api_gateway = create_container(task=task_definition, container_name="apigateway",
                                   image_path=prefix+"apigateway"+, memory_limit=1024,
                                   port_mapping=PortMapping(container_port=8001, host_port=8001,
                                                            protocol=Protocol.TCP),
                                   env=env_vars)
    graph_service = create_container(task=task_definition, container_name="graphservice",
                                     image_path=prefix+"graphservice"+suffix,
                                     memory_limit=2048, env=env_vars)
    bfs_service = create_container(task=task_definition, container_name="bfsservice",
                                   image_path=prefix+"bfsservice", memory_limit=1024,
                                   env=env_vars)
    edmonds_karp_service = create_container(task=task_definition, container_name="edmondskarpservice",
                                            image_path=prefix+"edmondskarpservice"+,
                                            memory_limit=1024, env=env_vars)
    push_relabel_service = create_container(task=task_definition, container_name="pushrelabelservice",
                                            image_path=prefix+"pushrelabelservice",
                                            memory_limit=1024, env=env_vars)

    api_gateway.add_link(graph_service, "graphservice")
    api_gateway.add_link(bfs_service, "bfsservice")
    api_gateway.add_link(edmonds_karp_service, "edmondskarpservice")
    api_gateway.add_link(push_relabel_service, "pushrelabelservice")
    bfs_service.add_link(graph_service, "graphservice")
    edmonds_karp_service.add_link(graph_service, "graphservice")
    edmonds_karp_service.add_link(bfs_service, "bfsservice")
    push_relabel_service.add_link(graph_service, "graphservice")
    push_relabel_service.add_link(bfs_service, "bfsservice")

