from aws_cdk.aws_ecs import Ec2TaskDefinition, PortMapping, ContainerDefinition, ContainerImage, LogDrivers, Protocol

'''Invokes creation of monolith container in AWS ECS task
        :param task: Task in which you want to create a container. Pass task_definition parameter from your config 
        :param language: Programming language, should be read from program parameters. Possible values: java, dotnet, cpp
        :param graphs_type: Tag of monolith image that specifies graphs type, should be read from program parameters.
         Possible values: big-sparse, small-sparse, big-dense, small-dense
'''


def create_monolith_container(task: Ec2TaskDefinition, image_path: str, image_tag: str):
    create_container(task=task,
                     container_name="monolith",
                     image_path=image_path + ":" + image_tag,
                     memory_limit=7000,
                     port_mapping=PortMapping(container_port=8001, host_port=8001, protocol=Protocol.TCP))


'''Creates a container in AWS ECS task
        :param task: Task in which you want to create a container. Pass task_definition parameter from your config 
        :param container_name: Container name and id. Use the same value as in your local docker-compose file
        :param image_path: Path to your image in Docker Hub. The format is <USERNAME>/<IMAGE>:<TAG> e.g. piotrszymanski/monolithjava_app:big-dense
        : memory_limit_mib: Memory that will be provided for the container. Remember that all of the containers must use
         less than 7.5Gb of memory in total.
        :param port_mappings: Optional port mappings. Should be used only for api-gateway container
'''


def create_container(task: Ec2TaskDefinition, container_name: str, image_path: str, memory_limit: int,
                     port_mapping: PortMapping = None) -> ContainerDefinition:
    return task.add_container(container_name,
                              container_name=container_name,
                              image=ContainerImage.from_registry(image_path),
                              port_mappings=[port_mapping] if port_mapping is not None else None,
                              memory_limit_mib=memory_limit,
                              logging=LogDrivers.aws_logs(stream_prefix=container_name))
