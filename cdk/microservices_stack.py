import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecs as ecs
from cdk.utils import *


class MicroservicesStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)
        cluster = ecs.Cluster(self, 'EcsMicroservicesCluster', vpc=vpc)
        cluster.add_capacity('Default', instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.LARGE),
                             desired_capacity=1)
        task_definition = Ec2TaskDefinition(self, 'Task', network_mode=ecs.NetworkMode.BRIDGE)
        lb = ApplicationLoadBalancer(self, "LB", vpc=vpc, internet_facing=True)
        language = cdk.CfnParameter(self, "language", type="String")
        print(language)
        print(language.value_as_string)
        print(language.value)

        create_containers(language.value_as_string, task_definition)
        service = Ec2Service(self, "Service", cluster=cluster, task_definition=task_definition)
        create_listener("java", lb, service)
        cdk.CfnOutput(self, 'LoadBalancerDNS', value=lb.load_balancer_dns_name)

