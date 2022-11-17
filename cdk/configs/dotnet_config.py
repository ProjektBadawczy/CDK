from aws_cdk.aws_ecs import Ec2TaskDefinition


def configure_dotnet_microservices(task_definition: Ec2TaskDefinition, graphs_type: str):
    # TODO implement me!
    # You need to create all of your containers and all needed links
    # Link allows you to make calls to other containers using their names
    # If you need to call graph_service from edmonds_karp_service add line
    # edmonds_karp_service.add_link(graph_service, "graph_service")
    pass
