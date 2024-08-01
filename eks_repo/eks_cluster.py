from aws_cdk import (
    Stack,
    aws_eks as eks,
    aws_ec2, 
    aws_iam
)
from constructs import Construct
from aws_cdk.aws_eks import Cluster, KubernetesVersion
from aws_cdk.lambda_layer_kubectl import KubectlLayer
from aws_cdk.aws_iam import Role, ServicePrincipal, ManagedPolicy
from aws_cdk.aws_ec2 import Vpc, SubnetType

class EksClusterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
      # Define the VPC
        vpc = Vpc(
            self, "EksVpc",
            max_azs=3,  # Default is all AZs in the region
            subnet_configuration=[
                {
                    "subnetType": SubnetType.PUBLIC,
                    "name": "Public",
                    "cidrMask": 24
                },
                {
                    "subnetType": SubnetType.PRIVATE_WITH_EGRESS,
                    "name": "Private",
                    "cidrMask": 24
                }
            ]
        )

       # Define the IAM role for the EKS cluster
        eks_role = Role(
            self, 'EksClusterRole',
            assumed_by=ServicePrincipal('eks.amazonaws.com'),
            managed_policies=[
                ManagedPolicy.from_aws_managed_policy_name('AmazonEKSClusterPolicy'),
                ManagedPolicy.from_aws_managed_policy_name('AmazonEKSServicePolicy')
            ],
            role_name="eks_service_role"
        )
        kubectl_layer = KubectlLayer(self, "KubectlLayer")
        
        cluster = eks.Cluster(
            self, "HelloEKS", 
            version=eks.KubernetesVersion.V1_30,
            kubectl_layer=kubectl_layer,
            cluster_name= "eks-cdk-cluster",
            masters_role=eks_role,
            vpc=vpc,
            default_capacity_instance=aws_ec2.InstanceType("t3.medium"),
            default_capacity=0
        )