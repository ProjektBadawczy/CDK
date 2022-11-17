from aws_cdk.aws_ecs import Ec2TaskDefinition
from cdk.configs.cpp_config import configure_cpp_microservices
from cdk.configs.dotnet_config import configure_dotnet_microservices
from cdk.configs.java_config import configure_java_microservices
from cdk.factories.container_factory import create_monolith_container


def create_microservices(task_definition: Ec2TaskDefinition, app_version: str, graphs_type: str):
    match app_version:
        case "java":
            return configure_java_microservices(task_definition, graphs_type)
        case "dotnet":
            return configure_dotnet_microservices(task_definition, graphs_type)
        case "cpp":
            return configure_cpp_microservices(task_definition, graphs_type)


def create_monolith(task: Ec2TaskDefinition, app_version: str, graphs_type: str):
    match app_version:
        case "java":
            create_monolith_container(task=task, image_path="piotrszymanski/monolithjava_app", image_tag=graphs_type)
        case "dotnet":
            # TODO Change image path to real path to monolith image. Do not include any tags!
            create_monolith_container(task=task, image_path="CHANGE ME!!!", image_tag=graphs_type)
        case "cpp":
            # TODO Change image path to real path to monolith image. Do not include any tags!
            create_monolith_container(task=task, image_path="CHANGE ME!!!", image_tag=graphs_type)

