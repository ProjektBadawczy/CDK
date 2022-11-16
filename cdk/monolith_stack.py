import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
import aws_cdk.aws_ecs as ecs


class MonolithStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)
        cluster = ecs.Cluster(self, 'EcsMonolithCluster', vpc=vpc)
        cluster.add_capacity('Default', instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.SMALL))
        task_definition = ecs.Ec2TaskDefinition(self, 'Task')
        container = task_definition.add_container("monolith",
                                                  image=ecs.ContainerImage.from_registry("piotrszymanski/monolithjava_app:big-dense"),
                                                  port_mappings=[ecs.PortMapping(container_port=8001, host_port=8001, protocol=ecs.Protocol.TCP)],
                                                  memory_limit_mib=1900,
                                                  logging=ecs.LogDrivers.aws_logs(stream_prefix="monolith"))
        service = ecs.Ec2Service(self, "Service", cluster=cluster, task_definition=task_definition)
        lb = elbv2.ApplicationLoadBalancer(self, "LB", vpc=vpc, internet_facing=True)
        listener = lb.add_listener("PublicListener", port=8001, open=True, protocol=elbv2.ApplicationProtocol.HTTP)
        listener.add_targets('ECS', port=8001, protocol=elbv2.ApplicationProtocol.HTTP,
                             targets=[service.load_balancer_target(
                                 container_name="monolith",
                                 container_port=8001)])

        cdk.CfnOutput(self, 'LoadBalancerDNS', value=lb.load_balancer_dns_name)
