import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_ec2 as ec2
from aws_cdk.aws_elasticloadbalancingv2 import ApplicationLoadBalancer, ApplicationProtocol
import aws_cdk.aws_ecs as ecs

from cdk.factories.architecture_factory import create_monolith
from cdk.factories.listener_factory import create_monolith_listener


class MonolithStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)
        cluster = ecs.Cluster(self, 'EcsMonolithCluster', vpc=vpc)
        cluster.add_capacity('Default', instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.LARGE))
        task_definition = ecs.Ec2TaskDefinition(self, 'Task')
        lb = ApplicationLoadBalancer(self, "LB", vpc=vpc, internet_facing=True)
        version = self.node.try_get_context("version")
        graphs_type = self.node.try_get_context("graphs")
        create_monolith(task_definition, version, graphs_type)
        service = ecs.Ec2Service(self, "Service", cluster=cluster, task_definition=task_definition)
        create_monolith_listener(version, lb, service)

        cdk.CfnOutput(self, 'LoadBalancerDNS', value=lb.load_balancer_dns_name)
