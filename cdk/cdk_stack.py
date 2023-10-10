from aws_cdk import (
    Stack,
    aws_ec2 as ec2, 
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns
)
from constructs import Construct

class CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpc = ec2.Vpc(self, "MyVpc", max_azs=3)     # default is all AZs in region
        cluster = ecs.Cluster(self, "MyCluster", vpc=vpc, cluster_name="MyCluster")
        ecs_patterns.ApplicationLoadBalancedFargateService(self, "MyFargateService",
            cluster=cluster,            # Required
            service_name="MyFargateService",
            cpu=512,                    # Default is 256
            desired_count=6,            # Default is 1
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                family="CdkStackTaskDefinition",
                container_port=9092,
                image=ecs.ContainerImage.from_registry("ghcr.io/owenchenxy/example-hello-world:17")),
            memory_limit_mib=2048,      # Default is 512
            public_load_balancer=True,
            listener_port=80)  
