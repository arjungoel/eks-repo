from aws_cdk import (
    Stack,
    DefaultStackSynthesizer,
    aws_s3 as s3,
    RemovalPolicy
)
from constructs import Construct
from eks_repo.eks_cluster import EksClusterStack

class EksRepoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        assets_bucket = s3.Bucket(
            self, "AssetsBucket",
            bucket_name="aws-cdk-eks-learning-bootcamp",
            removal_policy=RemovalPolicy.DESTROY,  # Only for development purposes
            auto_delete_objects=True  # Only for development purposes
        )
        
        # Pass the bucket to the synthesizer
        # synthesizer = DefaultStackSynthesizer(
        #     file_assets_bucket_name=assets_bucket.bucket_name
        # )
        
        EksClusterStack(
            scope=self,
            construct_id='EksStack',
            stack_name='EksStack'
            # synthesizer = synthesizer
        )    
    