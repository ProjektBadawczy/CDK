import aws_cdk as cdk
from aws_cdk.aws_elasticloadbalancingv2 import ApplicationLoadBalancer
from constructs import Construct
import aws_cdk.aws_ec2 as ec2
from aws_cdk.aws_ecs import Ec2Service, Ec2TaskDefinition, Cluster, NetworkMode

from cdk.factories.architecture_factory import create_microservices
from cdk.factories.listener_factory import create_microservices_listener


class MicroservicesStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)
        cluster = Cluster(self, 'EcsMicroservicesCluster', vpc=vpc)
        cluster.add_capacity('Default', instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.LARGE),
                             desired_capacity=1)
        task_definition = Ec2TaskDefinition(self, 'Task', network_mode=NetworkMode.BRIDGE)
        lb = ApplicationLoadBalancer(self, "LB", vpc=vpc, internet_facing=True)
        version = self.node.try_get_context("version")
        graphs_type = self.node.try_get_context("graphs")
        create_microservices(task_definition, version, graphs_type)
        service = Ec2Service(self, "Service", cluster=cluster, task_definition=task_definition)
        create_microservices_listener(version, lb, service)
        cdk.CfnOutput(self, 'LoadBalancerDNS', value=lb.load_balancer_dns_name)

