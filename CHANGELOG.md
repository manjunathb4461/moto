Moto Changelog
===================

Unreleased
-----

2.2.7
-----
    General:
        * Performance improvements when using Moto in Server Mode.
          Only services that are actually used will now be loaded into memory, greatly reducing the waiting times when starting the server, making an initial request and calling the reset-api.

    New Services:
        * Firehose
            * create_delivery_stream()
            * delete_delivery_stream()
            * describe_delivery_stream()
            * list_delivery_streams()
            * list_tags_for_delivery_stream()
            * put_record()
            * put_record_batch()
            * tag_delivery_stream()
            * untag_delivery_stream()
            * update_destination()

    New Methods:
        * Autoscaling:
            * delete_lifecycle_hook()
            * describe_lifecycle_hooks()
            * put_lifecycle_hook()
        * EC2:
            * associate_subnet_cidr_block()
            * create_carrier_gateway()
            * delete_carrier_gateway()
            * describe_carrier_gateways()
            * describe_spot_price_history()
            * disassociate_subnet_cidr_block()
            * update_security_group_rule_descriptions_egress()
            * update_security_group_rule_descriptions_ingress()
        * Logs:
            * delete_metric_filter()
            * describe_metric_filters()
            * put_metric_filter()
        * SageMaker:
            * list_training_jobs()
        * Transcribe
            * create_vocabulary()
            * delete_transcription_job()
            * delete_vocabulary()
            * get_transcription_job()
            * get_vocabulary()
            * list_transcription_jobs()
            * start_transcription_job()

    Miscellaneous:
        * DynamoDB: Improved support for the ReturnConsumedCapacity-parameter across all methods
        * EC2:create_route() now supports the parameters CarrierGatewayId, DestinationPrefixListId
        * EC2:create_subnet() now supports the Ipv6CidrBlock-parameter
        * EC2:describe_nat_gateways() now supports the NatGatewayIds-parameter
        * EC2:describe_vpn_gateways() now supports the VpnGatewayIds-parameter
        * EC2:modify_network_interface_attribute() now supports the SourceDestCheck-parameter
        * EC2:replace_route() now supports the parameters DestinationIpv6CidrBlock, DestinationPrefixListId, NatGatewayId, EgressOnlyInternetGatewayId, TransitGatewayId
        * EC2:run_instances() now supports the InstanceMarketOptions.MarketType-parameter
        * Logs:put_log_events() now supports Firehose as a destination
        * Logs:put_subscription_filter() now supports Firehose as a destination
        * S3:create_bucket(): Improved error handling for duplicate buckets
        * S3:head_object() now validates incoming calls when using the `set_initial_no_auth_action_count`-decorator
        * SSM:put_parameter() now supports the DataType-parameter

2.2.6
-----
    General:
        * `pip install` will no longer log a warning when installing a service that does not have any dependencies
          Example: `pip install moto[acm]`

    New Services:
        ElasticTranscoder:
            * create_pipeline
            * delete_pipeline
            * list_pipelines
            * read_pipeline
            * update_pipeline

    New Methods:
        * DynamoDB:
            * describe_endpoints()

    Miscellaneous:
        * AWSLambda now sends logs to CloudWatch when Docker encounters an error, to make debugging easier
        * AWSLambda: For all methods, the FunctionName-parameter can be either the Lambda name or the Lambda ARN
        * AWSLambda:list_functions() now returns only the latest version by default
        * AWSLambda:invoke() now returns the correct Payload for invocations that resulted in an error
        * CloudFormation now supports the creation of type AWS::IAM::ManagedPolicy
        * CloudFormation now supports the deletion of type AWS::IAM::InstanceProfile
        * CloudFormation now supports the deletion of type AWS::IAM::Role
        * CloudWatch:create_log_group() now has proper validation for the length of the logGroupName-parameter
        * CloudWatch:describe_log_groups() now has proper validation for the limit-parameter
        * CloudWatch:describe_log_streams() now has proper validation for the limit-parameter
        * CloudWatch:get_log_events() now has proper validation for the limit-parameter
        * CloudWatch:filter_log_events() now has proper validation for the limit-parameter
        * DynamoDB:update_item(): fixed a bug where an item was created, despite throwing an error
        * DynamoDB:update_item() now throws an error when both UpdateExpression and AttributeUpdates are supplied
        * EC2:modify_instance_attribute() now supports Attribute="disableApiTermination"
        * S3 now supports direct uploads using the requests-library without having to specify the 'Content-Type' header
        * S3 now supports creating S3 buckets that start with a service name, i.e. `iot-bucket`
        * S3 now returns the RequestID in every response
        * S3:list_parts() now supports the MaxPart-parameter
        * SQS:get_queue_attributes() now behaves correctly when the AttributeNames-parameter is not provided
        * SQS:receive_message() no longer accepts queue-names for the QueueUrl-parameter, as per AWS' spec
        * SQS: The sqs.Queue-class no longer accepts queue-names, only queue-URLs, as per AWS' spec

2.2.5
-----
    General:
        * Python 3.9 is now officially supported

    Known bugs:
        * SQS:get_queue_attributes() throws an error when the AttributeNames-parameter is not provided

    New Methods:
        * DynamoDB (API v20111205, now deprecated)
            * UpdateItem
        * EC2:
            * modify_vpc_peering_connection_options()
        * Glue:
            * create_crawler()
            * delete_crawler()
            * get_crawler()
            * get_crawlers()
        * SSM:
            * describe_document_permission()
            * modify_document_permission()

    Miscellaneous:
        * CloudFormation:create_stack() now has validation for an empty Outputs-parameter
        * EC2 now returns errors in the correct format, fixing various bugs with `terraform destroy`
        * EC2:authorize_security_group_egress() now returns the securityGroupRuleSet-attribute
        * EC2:authorize_security_group_ingress() now returns the securityGroupRuleSet-attribute
        * EC2:create_route() now supports the EgressOnlyInternetGatewayId-parameter
        * EC2:create_route_table() now adds an IPv6-route when enabled
        * EC2:describe_security_groups() now returns the ipv6Ranges-attribute
        * EC2:describe_vpc_peering_connection() now supports the VpcPeeringConnectionIds-parameter
        * Organisations:detach_policy() now actually detaches a policy - before it was essentially a no-op
        * Route53:create_health_check() now supports the CallerReference-parameter
        * Route53:create_health_check() now support default values for integer-parameters such as Port/RequestInterval/FailureThreshold
        * Route53:create_health_check() now supports several additional parameters such as MeasureLatency/Inverted/Disabled/EnableSNI/ChildHealthChecks
        * SQS:create_queue() now supports the queue-attributes FifoThroughputLimit and DeduplicationScope


2.2.4
-----
    New Methods:
        * ConfigService:
            * delete_config_rule()
            * describe_config_rule()
            * put_config_rule()
        * EC2:
            * create_egress_only_internet_gateway()
            * delete_egress_only_internet_gateway()
            * describe_egress_only_internet_gateways()
        * Fargate:
            * create_fargate_profile()
            * delete_fargate_profile()
            * describe_fargate_profile()
            * list_fargate_profiles()
        * IOT:
            * deprecate_thing_type()
        * S3:
            * get_object_lock_configuration()
            * put_object_legal_hold()
            * put_object_lock_configuration()
            * put_object_retention()

    Miscellaneous:
        * CloudFormation:describe_stack_resource() now throws an exception of the LogicalResourceId does not exist
        * CloudFormation: AWS::Events::Rule now supports the EventPattern-property
        * CloudFormation: Improved Parameter handling
        * EC2:describe_instances() now handles wildcards correctly when filtering by tags
        * EC2:terminate_instances() now throws an exception when trying to terminate a protected instance
        * ELBv2:describe_rules() now returns the correct value for the IsDefault-attribute
        * IOT:create_thing() now throws an exception if the thing type is deprecated
        * IOT:update_thing() now throws an exception if the thing type is deprecated
        * S3:create_bucket() now supports the ObjectLockEnabledForBucket-parameter
        * S3:putObject() is fixed for the Java SDK, which failed with a eTag-validation

2.2.3
-----
    New Methods:
        * EC2:
            * create_managed_prefix_list()
            * delete_managed_prefix_list()
            * describe_managed_prefix_lists()
            * describe_prefix_lists()
            * get_managed_prefix_list_entries()
            * delete_vpc_endpoints()
            * disassociate_transit_gateway_route_table()
            * modify_managed_prefix_list()
        * ECR:
            * delete_lifecycle_policy()
            * delete_registry_policy()
            * describe_image_scan_findings()
            * describe_registry()
            * get_lifecycle_policy()
            * get_registry_policy()
            * put_lifecycle_policy()
            * put_registry_policy()
            * put_replication_configuration()
            * start_image_scan()
        * CloudWatch:
            * list_tags_for_resource()
            * tag_resource()
            * untag_resource()

    Miscellaneous:
        * CloudWatch: put_metric_alarm() now supports the parameters ExtendedStatistic, TreatMissingData, EvaluateLowSampleCountPercentile, ThresholdMetricId, Tags 
        * CognitoIdentity: create_identity_pool() now supports the IdentityPoolTags-parameter
        * CognitoIDP: initiate_auth() now supports the 'USER_PASSWORD_AUTH'-flow
        * EC2: allocate_address()  now supports the TagSpecifications-parameter
        * EC2: create_route() now supports the TransitGatewayId-parameter
        * EC2: delete_route() now supports the DestinationIpv6CidrBlock-parameter
        * EC2: describe_nat_gateways() now returns the connectivityType-attribute
        * ECR: delete_repository() now supports the force-parameter
        * EventBridge: put_events() now supports ARN's for the EventBusName-parameter
        * EventBridge: put_rule() now supports the Tags-parameter
        * IOT: create_policy_version() now throws the VersionsLimitExceededException if appropriate


2.2.2
-----
    General:
        * Removed the dependency on pkg_resources that was broken in 2.2.1
        
    New Services:
        * WafV2:
            * create_web_acl()
            * list_web_acls()
        
    New Methods:
        * Autoscaling:
            * delete_tags()
            * resume_processes()
        * ConfigService:
            * list_tags_for_resource()
            * tag_resource()
            * untag_resource()
        * EC2:
            * accept_transit_gateway_peering_attachment()
            * create_transit_gateway_peering_attachment()
            * delete_transit_gateway_peering_attachment()
            * describe_transit_gateway_peering_attachments()
            * reject_transit_gateway_peering_attachment()
        * ECR:
            * delete_repository_policy()
            * get_repository_policy()
            * list_tags_for_resource()
            * put_image_tag_mutability()
            * put_image_scanning_configuration()
            * set_repository_policy()
            * tag_resource()
            * untag_resource()
        * KMS:
            * update_alias()
        * Logs:
            * delete_resource_policy()
            * describe_resource_policies()
        * RDS:
            * modify_db_subnet_group()

    Miscellaneous:
        * CloudFormation: Improved support for AWS::ECR::Repository
        * CloudFormation: execute_change_set() now properly updates the status of a stack
        * CognitoIDP: list_users() now supports username/status in the Filter-attribute
        * ECR: create_repository() now supports the parameters encryptionConfiguration, imageScanningConfiguration, imageTagMutability
        * Events: put_permission() now supports the Policy and Condition-parameters
        * Events: remove_permission() now supports the RemoveAllPermissions-parameter
        * Kinesis: create_delivery_stream() now supports the ElasticsearchDestinationConfiguration-parameter
        * SecretsManager: create_secret() now supports the KmsKeyId-parameter
        * SecretsManager: update_secret() now supports the KmsKeyId-parameter

2.2.1
-----
    Known bugs:
        * Moto still depends on setuptools (or more specifically pkg_resources), 
          but this module is not listed as a dependency.

    General:
        * We removed Py3.5 support
        * We removed some unnecessary dependencies for the EC2/SQS services.

    New Services:
        * EFS:
            * create_file_system
            * create_mount_target
            * delete_file_system
            * delete_mount_target
            * describe_backup_policy
            * describe_file_systems
            * describe_mount_target

    New Methods:
        * CognitoIDP:
            * admin_user_global_sign_out()
        * EC2:
            * associate_transit_gateway_route_table()
            * delete_transit_gateway_vpc_attachment()
            * disable_transit_gateway_route_table_propagation()
            * enable_transit_gateway_route_table_propagation()
            * modify_vpc_tenancy()
            * modify_transit_gateway_vpc_attachment()
        * Events:
            * update_connection()

    Miscellaneous:
        * EC2 - describe_route_tables() now returns the associationState-attribute
        * EKS - list_clusters() received a pagination bug fix
        * IOT - describe_certificate() now returns the validity-attribute
        * SQS - create_queue() now supports empty tags
        * SQS - set_queue_attributes() now supports setting an empty policy


2.2.0
-----
    General Changes:
        * Support for Python 2.7 has been removed.
          The last release with Python2 support is now 2.1.0

    New Methods:
        * API Gateway:
            * delete_domain_name()
            * delete_method()
            * update_domain_name()
            * update_method()
            * update_method_response()
        * CognitoIdentity:
            * update_identity_pool()
        * EC2:
            * create_transit_gateway()
            * create_transit_gateway_route()
            * create_transit_gateway_route_table()
            * create_transit_gateway_vpc_attachment()
            * delete_transit_gateway()
            * delete_transit_gateway_route()
            * delete_transit_gateway_route_table()
            * describe_transit_gateway_attachments()
            * describe_transit_gateway_route_tables()
            * describe_transit_gateway_vpc_attachments()
            * describe_transit_gateways()
            * modify_transit_gateway()
            * search_transit_gateway_routes()
        * Events:
            * delete_api_destination()
            * delete_connection()
            * describe_connection()
            * update_api_destination()
        * Logs:
            * put_resource_policy()
        * Organizations:
            * delete_organization()
        * S3:
            * delete_bucket_website()

    Miscellaneous:
        * API Gateway - add_integration() now supports the parameters integration_method, tls_config, cache_namespace
        * API Gateway - add_method() now supports the parameters request_models, operation_name, authorizer_id, authorization_scopes, request_validator_id
        * API Gateway - create_integration() now supports the parameters tls_config, cache_namespace
        * API Gateway - create_method() now supports the parameters request_models, operation_name, authorizer_id, authorization_scopes, request_validator_id
        * API Gateway - create_method_response() now supports the parameters response_models, response_parameters
        * API Gateway - create_response() now supports the parameters response_models, response_parameters
        * API Gateway - create_rest_api() now supports the parameters minimum_compression_size
        * API Gateway - create_stage() now supports the parameters tags, tracing_enabled
        * API Gateway - delete_stage() now throws a StageNotFoundException when appropriate
        * API Gateway - get_api_key() now throws a ApiKeyNotFoundException when appropriate
        * API Gateway - get_integration_response() now throws a NoIntegrationResponseDefined when appropriate
        * API Gateway - get_method() now throws a MethodNotFoundException when appropriate

        * ApplicationAutoscaling - put_scaling_policy() now correctly processes the policy_type and policy_body parameters when overwriting an existing policy

        * CloudFormation - now supports the creation of AWS::EC2::TransitGateway

        * CloudWatch - put_metric_alarm() now supports the parameter rule
        * CloudWatch - get_metric_statistics() now supports the parameter dimensions

        * EC2 - create_customer_gateway() now supports the parameter tags
        * EC2 - create_security_group() now supports the parameter tags
        * EC2 - create_vpn_connection() now supports the parameter transit_gateway_id, tags
        * EC2 - create_vpn_gateway() now supports the parameter amazon_side_asn, availability_zone, tags
        * EC2 - get_all_customer_gateways() now has improved support for the filter parameter

        * ECS - create_service() now has support for the parameter service_registries

        * ELBv2 - create_load_balancer() now has support for the parameter loadbalancer_type

        * Events - create_api_destination() now has support for the parameter invocation_rate_limit_per_second
        * Events - create_event_bus() now has support for the parameter tags

        * IAM - create_instance_profile() now has support for the parameter tags
        * IAM - create_policy() now has support for the parameter tags

        * Logs - create_log_group() now has support for the parameter kms_key_id

        * SecretsManager - list_secrets() now supports pagination

2.1.0
-----
    General Changes:
        * Reduced the default value of DEFAULT_KEY_BUFFER_SIZE (introduced in 2.0.9).
          In practice, this means that large S3 uploads will now be cached on disk, instead of in-memory.
        * Removes `cfn-lint` as a dependency for the SSM-module.

    New Methods:
        * Kinesis
            * decrease_stream_retention_period
            * increase_stream_retention_period

    Miscellaneous:
        * CognitoIDP:admin_create_user(): Fixed a bug where user-supplied attributes would be ignored/overwritten
        * ELBv2:create_rule(): Increased support for Condition-parameter, to also allow http-header/http-request-method/host-header/path-pattern/query-string/source-ip

2.0.11
------
    New Services:
        * MediaStoreData
            * delete_object
            * get_object
            * list_items
            * put_object

    New Methods:
        * CognitoIDP
            * get_user
        * MediaConnect
            * add_flow_outputs
            * add_flow_vpc_interfaces
            * remove_flow_output
            * remove_flow_vpc_interface

    Miscellaneous:
        * ApplicationAutoscaling:put_scaling_policy() now supports StepScaling
        * ApplicationAutoscaling:register_scalable_target() now supports custom resources
        * CloudFormation: Now resolves default SSM parameters (AWS::SSM::Parameter::Value<>)
        * DynamoDB:update_item(): Fix bug for Action:DELETE without value supplied
        * EC2:create_network_interface() now supports the TagSpecification-parameter
        * ELBv2:modify_listener(): improved behaviour for the Certificates-parameter
        * Lambda:invoke() now returns header: content-type=application/json
        * Logs:put_log_events() now returns the correct error message when the stream does not exist
        * IOT:update_thing_shadow() now properly maintains state
        * S3: Listing parts on an aborted upload now throws the correct error
        * S3:delete_objects() now correctly ignores unknown keys
        * S3:list_object_versions() now returns the Prefix-attribute
        * S3:upload_part() now throws the correct error when providing a negative part number
        * SES:verify_domain_identity() and verify_domain_identity() are now idempotent
        * SNS:create_platform_endpoint() now returns an existing endpoint if the token and attributes are the same
        * SQS:delete_message_batch() now throws an error when duplicate messages are supplied
        * SQS:send_messages() now throws an error for FIFO queues if the MessageGroupId-parameter is not supplied

2.0.10
------

    New Services:
        * EKS
            * create_cluster
            * create_nodegroup
            * delete_cluster
            * delete_nodegroup
            * list_clusters
            * list_nodegroup

    Miscellaneous:
        * DynamoDB: Fixed a bug where it's not possible to call update_item on a GSI
        * EMR: now supports clusters with multiple master nodes
        * EMR:terminate_job_flows() now throws an exception when trying to terminate; protected job flows
        * MediaPackage: Implement NotFoundExceptions for delete_channel/describe_origin_endpoint/delete_origin_endpoint/update_origin_endpoint
        * S3:list_users_response() now returns the IsTruncated-attribute

2.0.9
-----
    General Changes:
        * Introduction of a new environment variable: MOTO_S3_DEFAULT_KEY_BUFFER_SIZE
          This allows you to set the in-memory buffer size for multipart uploads. The default size is (and always was) 16MB.
          Exceeding this buffer size will cause the contents to be written/saved to a temporary file.

    New Methods:
        * API Gateway:
            * update_rest_api()
        * DynamoDB:
            * create_backup()
            * delete_backup()
            * describe_backup()
            * list_backups()
            * restore_table_from_backup()
        * Events:
            * create_api_destination()
            * create_connection()
            * describe_api_destination()
            * list_api_destinations()
            * list_connections()
        * Logs
            * start_query()
            
    Miscellaneous:
        * Batch:
            * Now uses the exit code of the Docker-container to decide job status
            * Supports job-dependencies
        * CloudFormation:
            * Create/Update support for AWS::ElasticLoadBalancingV2::ListenerRule
            * Update support for AWS::ElasticLoadBalancingV2::Listener
        * Glacier:
            * Vault names can now contain special characters
        * MediaPackage:
            * describe_channel() now throws a NotFoundException for unknown channels
        * Organisations:
            * Improve tagging support 
        * S3:
            * Now supports '.' as a metadata character
        * S3 Config:
            * Fixed the response format for ACLs
        * SSM:
            * get_parameter() now throws correct exception for unknown parameters/versions
            * get_parameters() can now fetch specific versions and labeled parameters
            * get_parameter_history() now supports pagination
            * Parameter-names can now contain hyphens
            * Only the last 100 parameter versions are now kept, as per AWS' behaviour

2.0.8
-----
    General Changes:
        * Moto is now compatible with Flask/werkzeug 2.0

    New Methods:
        * MediaStore:
            * delete_container()
            * list_tags_for_resource()
        * Resource Groups:
            * get_group_configuration()
            * put_group_configuration()

    Miscellaneous:
        * APIGateway:update_usage_plan() now also supports the '/name', '/description' and '/productCode' paths.
        * CloudWatch:get_metric_statistics() now supports the 'unit'-parameter
        * EC2:run_instances() now supports the 'KmsKeyId'-parameter
        * EC2:run_instances() now supports TagSpecifications with ResourceType: 'Volume'
        * SES:test_render_template() now throws an exception if not all attributes are supplied
        * SSM:put_parameter() now supports the 'tags'-parameter
        * SQS:change_message_visibility() now throws an exception if the VisibilityTimeout is too large (> 43200 seconds)
        * SQS:receive_messages() has a bugfix: it now calculates the MessageRetentionPeriod from when the message was send, rather than from when the queue was created


2.0.7
-----
    General Changes:
        * When running Moto Server inside Docker, it is now possible to specify the service you want to run, using an environment variable (MOTO_SERVICE)
        * CloudWatchLogs models now appear in the Moto API dashboard

    New Services:
        * DMS
            * create_replication_task()
            * delete_replication_task()
            * describe_replication_tasks()
            * start_replication_task()
            * stop_replication_task()

    New Methods:
        * AWSLambda:
            * update_secret_version_stage()
        * CognitoIDP:
            * get_user_pool_mfa_config()
            * set_user_pool_mfa_config()

    Miscellaneous:
        * CloudWatchLogs:filter_log_events() now supports pagination
        * CloudWatchLogs:describe_log_streams() now supports pagination
        * EC2:describe_network_acls() now supports the filter 'owner-id'
        * EC2:modify_network_interface_attribute() now allows multiple security groups to be specified
        * SecretsManager:rotate_secret() now triggers the Lambda that is specified


2.0.6
-----
    New Methods:
        * EMR
            * list_instances()

    Miscellaneous:
        * API Gateway:put_integration_response() - Fixed a bug where an error would be thrown if the responseTemplates-parameter was not specified
        * Autoscaling - Fixed a bug where creating an ASG would remove manually created EC2-instances
        * CloudFormation support for:
            * AWS::SageMaker::Endpoint
            * AWS::SageMaker::EndpointConfig
            * AWS::SageMaker::Model
            * AWS::SageMaker::NotebookInstanceLifecycleConfig
        * CloudWatchLogs:filter_log_events() now supports pagination
        * DynamoDB: Now enforces Hash and Range key size limits
        * ECS:register_task_definition() now persists the taskRoleArn and executionRoleArn-parameters
        * EMR:describe_cluster() now returns the ClusterArn-attribute
        * EMR:run_job_flow() now returns the ClusterArn-attribute
        * EMR:describe_job_flows() now returns the ClusterArn-attribute
        * IOT:list_principal_thigns() now returns the name, instead of the ARN
        * Route53:get_all_rrsets() now returns the record sets in the right sort order
        * S3:get_object() now returns the NoSuchVersion-exception when the versionId was not found (instead of the InvalidVersion)
        * SQS:send_message() now supports the MessageSystemAttributes-parameter

2.0.5
-----
    New Services:
        * MediaStore
            * create_container()
            * describe_container()
            * list_containers()
            * put_lifecycle_policy()
            * get_lifecycle_policy()
            * put_container_policy()
            * get_container_policy()
            * put_metric_policy()
            * get_metric_policy

    Miscellaneous:
        * ACM now supports the MOTO_ACM_VALIDATION_WAIT-environment variable, to configure the wait time before the status on new certificates move from PENDING_VALIDATION to ISSUED
        * CloudFormation support for AWS::SageMaker::NotebookInstance
        * EMR:run_job_flow() now creates the appropriate EC2 security groups in a private subnet
        * Events:put_events() has improved support for the EventPattern-parameter in create_archive/put_rule
        * Events:put_targets() now support SQS queues
        * IAM:get_user() now returns the Tags-attribute
        * Fixed a bug where Moto would break on systems with a default encoding other than UTF-8

2.0.4
-----
    Miscelleaneous:
        * Events:put_targets() now supports SQS queues
        * Support:describe_cases() no longer requires the caseIdList-parameter

2.0.3
-----
    New Methods:
        * Support
            * create_case
            * describe_cases
            * resolve_case
    Miscelleaneous:
        * CF now returns the PhysicalResourceId-attributes for AWS::EC2::NatGateway/AWS::EC2::Route/AWS::EC2::SubnetRouteTableAssociation
        * CognitoIDP:sign_up() now throws an UsernameExistsException if appropriate
        * DynamoDB now validates the case sensitivity for begins_with/between operators
        * EC2:associate_route_table() now supports the GatewayId-parameter
        * EC2:authorize_egress() now throws a InvalidPermission.Duplicate-exception if appropriate
        * EC2:authorize_security_group_egress() now throws a InvalidGroup.NotFound-exception
        * EC2:authorize_security_group_ingress() now throws a InvalidGroup.NotFound-exception
        * Events:describe_rule() now returns the ManagedBy/CreatedBy-parameters
        * Events:put_events() now supports providing an ARN for the EventBusName-parameter
        * Route53:list_hosted_zones_by_name() now returns the DNSName-parameter
        * S3:put_object_acl() now throws a NoSuchKey-exception if the object does not exist
        * SES:send_templated_email() now throws a TemplateDoesNotExist-exception if the template has not been created first
        * SSM:put_parameter() now throws an exception for empty values
    Known bugs:
        * Support:describe_cases() throws an exception when called without the caseIdList-parameter


2.0.2
-----
    General Changes:
        * New Osaka region is now supported

    New Services:
        * MediaPackage

    New Methods:
        * Redshift
            * authorize_cluster_security_group_ingress
        * Secrets Manager:
            * untag_resource

    Miscellaneous:
        * IAM:list_roles() now contains the MaxSessionDuration-attribute
        * Kinesis:get_records(): Fix formatting of the ApproximateArrivalTimestamp-parameter
        * SQS:receive_message(): Fix behaviour of the AttributeNames-parameter

2.0.1
-----
    New Services:
        * Media Connect

    New Methods:
        * API Gateway: 
            * update_usage_plan
        * Events
            * cancel_replay
            * describe_replay
            * start_replay
            * list_replays
        
    Miscellaneous:
        * ECS TaskDefinitions now have the 'status' attribute
        * Events: the put_rule now updates an existing rule, instead of removing the old one (and the associated targets)
        * IAM create_roles and list_roles now return the Description
        * SSM: put_parameter and describe_parameters now supports tags


2.0.0
----
Full list of PRs merged in this release:
https://github.com/spulec/moto/pulls?q=is%3Apr+is%3Aclosed+merged%3A2020-09-07..2021-02-23

    General Changes:
        * When installing, it is now required to specify the service you want to use:
          pip install moto[service1,service2]
          pip install moto[all]
          
          This will ensure that only the required dependencies are downloaded. 
          See the README for more information.
          
        * Moved CI to Github Actions
        
        * Moto no longer hogs the _default_mock from responses
        
        * Internal testing is now executed using Pytest (instead of Nose)
        
        * CORS is now enabled when running MotoServer

        * AWS Lambda and Batch now support Podman as an alternative to Docker
    
    New Services:
        * Forecast
        * MediaLive
        * Support
        * Transcribe
    
    New Methods:
        * Application Autoscaling
            * delete_scaling_policy
            * deregister_scalable_target
            * describe_scaling_policies
            * put_scaling_policy
        * Batch
            * batch_update_partition
        * Cognito IDP
            * admin_set_user_password
        * EC2
            * create_flow_logs
            * delete_flow_logs
            * describe_flow_logs
            * describe_instance_type_offerings
            * describe_vpc_endpoints
        * EMR
            * create_security_configuration
            * delete_security_configuration
            * get_security_configuration
            * modify_cluster
            * put_autoscaling_policy
            * remove_auto_scaling_policy
        * Events
            * create_archive
            * delete_archive
            * describe_archive
            * list_archives
            * update_archive
        * Lambda
            * get_function_configuration
            * get_layer_version
            * list_layers
            * publish_layer_version
        * IAM
            * associate_iam_instance_profile
            * delete_role_permissions_boundary
            * describe_iam_instance_profile_associations
            * disassociate_iam_instance_profile
            * put_role_permissions_boundary
            * replace_iam_instance_profile_association
            * set_default_policy_version
            * tag_user
            * untag_user
        * IOT
            * create_topic_rule
            * delete_topic_rule
            * disable_topic_rule
            * enable_topic_rule
            * get_topic_rule
            * list_topic_rules
            * replace_topic_rule
        * Redshift
            * get_cluster_credentials
        * Route53
            * get_change (dummy)
        * SageMaker
            * create_notebook_instance_lifecycle_config
            * delete_notebook_instance_lifecycle_config
            * describe_notebook_instance_lifecycle_config
        * Secrets Manager
            * tag_resource
        * SES
            * test_render_template
            * update_template
        * Step Functions
            * get_execution_history
            * tag_resource
            * untag_resource
            * update_state_machine

    General Changes:
        * ACM - import_certificate() now supports the Tags-parameter
        * ACM - request_certificate() now supports the Tags-parameter
        * CF - SSHIngressRule now supports CidrIp and Description
        * CF - Now fully supports:
             AWS::StepFunctions::StateMachine
        * CF - Now supports creation of:
             AWS::ApiGateway::Deployment
             AWS::ApiGateway::Method
             AWS::ApiGateway::Resource
             AWS::ApiGateway::RestApi
             AWS::Lambda::Permission
        * CF - Now supports S3 outputs: Arn, DomainName, DualStackDomainName, RegionalDomainName, WebsiteURL
        * CloudWatch - list_metrics() no longer returns duplicate entries
        * CloudWatch - put_metric_alarm() now supports the Metrics and DatapointsToAlarm parameters
        * Config - Now supports IAM (Role, Policy)
        * Cognito - admin_initiate_auth() now supports the ADMIN_USER_PASSWORD_AUTH-flow
        * CognitoIDP - list_users() now supports spaces in the Filter-parameter
        * DynamoDB - GSI's now support the ProjectionType=INCLUDE parameter
        * DynamoDB - put_item() now supports empty values (in non-key attributes)
        * DynamoDB - update_item() now supports the ADD operation to a list (using the AttributeUpdates-parameter)
        * DynamoDB - update_item() now supports the PUT operation to a StringSet (using the AttributeUpdates-parameter)
        * DynamoDB - update_item() now supports ReturnValues='UPDATED_NEW'
        * DynamoDB - update_item() now defaults to PUT if the action is not supplied
        * DynamoDB Streams - The event name for deletions has been corrected to REMOVE (was DELETE before)
        * EB - create()/describe_applications() now return a properly formatted ARN (that contains the application-name)
        * EC2 - copy_snapshot() now supports the TagSpecifications-parameter
        * EC2 - create_image() now supports the TagSpecifications-parameter
        * EC2 - create_internet_gateway() now supports the TagSpecifications-parameter
        * EC2 - create_nat_gateway() now supports the TagSpecification-parameter
        * EC2 - create_network_acl() now supports the TagSpecification-parameter
        * EC2 - create_route_table() now supports the TagSpecifications-parameter
        * EC2 - create_subnet() now supports the TagSpecifications-parameter
        * EC2 - create_subnet() now supports secondary CidrBlock-values 
        * EC2 - create_tags() now supports empty values
        * EC2 - create_volume() now supports the KmsKeyId-parameter
        * EC2 - create_vpc now supports the TagSpecifications-parameter
        * EC2 - create_vpc_endpoint() now properly handles private_dns_enabled-parameter in CF/TF
        * EC2 - create_vpn_endpoint() now supports the VpnGatewayId-parameter
        * EC2 - describe_addresses() now returns Tags
        * EC2 - describe_instances() now supports filtering by the subnet-id-attribute
        * EC2 - describe_subnets() now supports filtering by the state-attribute
        * ECR - list_images() now returns a proper value for the imageDigest-attribute
        * ECS - the default cluster is now used in a variety of methods, if the Cluster-parameter is not supplied
        * ECS - create_service() now supports the launchType-parameter
        * ECS - delete_service() now supports the force-parameter
        * ECS - describe_container_instances() now returns the registeredAt-attribute
        * ECS - list_tasks now supports the filters family/service_name/desired_status
        * ECS - register_scalable_target() now supports updates
        * ECS - register_task_definition() now returns some attributes that were missing before
        * ECS - run_task() now supports the tags-parameter
        * EMR - ReleaseLabel now respects semantic versioning
        * Events - Now supports the Go SDK
        * Events - list_rules() now returns the EventBusName-parameter
        * Events - put_events() now has basic input validation 
        * Glue - create_database() now returns some attributes that were missing before
        * IAM - create_user() now returns the Tags-attribute
        * IAM - list_roles() now supports the parameters PathPrefix/Marker/MaxItems
        * IOT - delete_thing_group() is now idempotent
        * Lambda - update_function_configuration() now supports the VpcConfig-parameter
        * RDS - create_db_parameter_group() now returns the DBParameterGroupArn-attribute
        * RDS - describe_db_instances() now returns the TagList-attribute
        * RDS - describe_db_instances() now supports the filters-parameter
        * RDS - describe_db_snapshots() now supports the filters-parameter
        * Redshift - modify_cluster() now checks for invalid ClusterType/NumberOfNodes combinations
        * ResourceGroupTagging: Now supports EC2 VPC resources
        * ResourceGroupTagging: Now supports RDS DBInstance, DBSnapshot resources
        * ResourceGroupTagging - get_resources() has improved support for the TagFilters-parameter
        * S3 - copy_object() now supports copying deleted and subsequently restored objects with storage class Glacier
        * S3 - get_object() now throws the correct error for an unknown VersionId
        * S3 - get_object() now supports an empty Range-parameter
        * S3 - get_object() now returns headers that were missing in some cases (ContentLength/ActualObjectSize/RangeRequested)
        * S3 - put_object/get_object now support the ServerSideEncryption/SSEKMSKeyId/BucketKeyEnabled parameters
        * S3 - list_object_versions now returns the object in the correct sort order (last modified time)
        * SecretsManager - describe_secret() now returns a persistent ARN
        * SecretsManager - get_secret_value() now requires a version to exist
        * SecretsManager - put_secret_value() now requires a secret to exist
        * SES - get-template() now returns the HtmlPart-attribute
        * SNS - Support KmsMasterKeyId-attribute
        * SNS - create_topic() no longer throws an error when creating a FIFO queue
        * SNS - delete_topic() now also deletes the corresponding subscriptions
        * SNS - delete_topic() now raises an appropriate exception if the supplied topic not exists
        * Step Functions - list_executions() now supports filtering and pagination
        * SQS - The MD5OfMessageAttributes is now computed correctly 
        * SQS - a message in the DLQ now no longer blocks other messages with that MessageGroupId
        * SQS - create_queue() now supports the MaximumMessageSize-attribute
        * SQS - receive_message() now supports MessageAttributeNames=["All"]
        * SQS - send_message() now deduplicates properly using the MessageDeduplicationId



1.3.16
-----
Full list of PRs merged in this release:
https://github.com/spulec/moto/pulls?q=is%3Apr+is%3Aclosed+merged%3A2019-11-14..2020-09-07


    General Changes:
        * The scaffold.py-script has been fixed to make it easier to scaffold new services.
          See the README for an introduction.

    New Services:
        * Application Autoscaling
        * Code Commit
        * Code Pipeline
        * Elastic Beanstalk
        * Kinesis Video
        * Kinesis Video Archived Media
        * Managed BlockChain
        * Resource Access Manager (ram)
        * Sagemaker

    New Methods:
        * Athena:
            * create_named_query
            * get_named_query
            * get_work_group
            * start_query_execution
            * stop_query_execution
        * API Gateway:
            * create_authorizer
            * create_domain_name
            * create_model
            * delete_authorizer
            * get_authorizer
            * get_authorizers
            * get_domain_name
            * get_domain_names
            * get_model
            * get_models
            * update_authorizer
        * Autoscaling:
            * enter_standby
            * exit_standby
            * terminate_instance_in_auto_scaling_group
        * CloudFormation:
            * get_template_summary
        * CloudWatch:
            * describe_alarms_for_metric
            * get_metric_data
        * CloudWatch Logs:
            * delete_subscription_filter
            * describe_subscription_filters
            * put_subscription_filter
        * Cognito IDP:
            * associate_software_token
            * create_resource_server
            * confirm_sign_up
            * initiate_auth
            * set_user_mfa_preference
            * sign_up
            * verify_software_token
        * DynamoDB:
            * describe_continuous_backups
            * transact_get_items
            * transact_write_items
            * update_continuous_backups
        * EC2:
            * create_vpc_endpoint
            * describe_vpc_classic_link
            * describe_vpc_classic_link_dns_support
            * describe_vpc_endpoint_services
            * disable_vpc_classic_link
            * disable_vpc_classic_link_dns_support
            * enable_vpc_classic_link
            * enable_vpc_classic_link_dns_support
            * register_image
        * ECS:
            * create_task_set
            * delete_task_set
            * describe_task_set
            * update_service_primary_task_set
            * update_task_set
        * Events:
            * delete_event_bus
            * create_event_bus
            * list_event_buses
            * list_tags_for_resource
            * tag_resource
            * untag_resource
        * Glue:
            * get_databases
        * IAM:
            * delete_group
            * delete_instance_profile
            * delete_ssh_public_key
            * get_account_summary
            * get_ssh_public_key
            * list_user_tags
            * list_ssh_public_keys
            * update_ssh_public_key
            * upload_ssh_public_key
        * IOT:
            * cancel_job
            * cancel_job_execution
            * create_policy_version
            * delete_job
            * delete_job_execution
            * describe_endpoint
            * describe_job_execution
            * delete_policy_version
            * get_policy_version
            * get_job_document
            * list_attached_policies
            * list_job_executions_for_job
            * list_job_executions_for_thing
            * list_jobs
            * list_policy_versions
            * set_default_policy_version
            * register_certificate_without_ca
        * KMS:
            * untag_resource
        * Lambda:
            * delete_function_concurrency
            * get_function_concurrency
            * put_function_concurrency
        * Organisations:
            * describe_create_account_status
            * deregister_delegated_administrator
            * disable_policy_type
            * enable_policy_type
            * list_delegated_administrators
            * list_delegated_services_for_account
            * list_tags_for_resource
            * register_delegated_administrator
            * tag_resource
            * untag_resource
            * update_organizational_unit
        * S3:
            * delete_bucket_encryption
            * delete_public_access_block
            * get_bucket_encryption
            * get_public_access_block
            * put_bucket_encryption
            * put_public_access_block
        * S3 Control:
            * delete_public_access_block
            * get_public_access_block
            * put_public_access_block
        * SecretsManager:
            * get_resource_policy
            * update_secret
        * SES:
            * create_configuration_set
            * create_configuration_set_event_destination
            * create_receipt_rule_set
            * create_receipt_rule
            * create_template
            * get_template
            * get_send_statistics
            * list_templates
        * STS:
            * assume_role_with_saml
        * SSM:
            * create_documen
            * delete_document
            * describe_document
            * get_document
            * list_documents
            * update_document
            * update_document_default_version
        * SWF:
            * undeprecate_activity_type
            * undeprecate_domain
            * undeprecate_workflow_type

    General Updates:
        * API Gateway - create_rest_api now supports policy-parameter
        * Autoscaling - describe_auto_scaling_instances now supports InstanceIds-parameter
        * AutoScalingGroups - now support launch templates
        * CF - Now supports DependsOn-configuration
        * CF - Now supports FN::Transform AWS::Include mapping
        * CF - Now supports update and deletion of Lambdas
        * CF - Now supports creation, update and deletion of EventBus (Events)
        * CF - Now supports update of Rules (Events)
        * CF - Now supports creation, update and deletion of EventSourceMappings (AWS Lambda)
        * CF - Now supports update and deletion of Kinesis Streams
        * CF - Now supports creation of DynamoDB streams
        * CF - Now supports deletion of  DynamoDB tables
        * CF - list_stacks now supports the status_filter-parameter
        * Cognito IDP - list_users now supports filter-parameter
        * DynamoDB - GSI/LSI's now support ProjectionType=KEYS_ONLY
        * EC2 - create_route now supports the NetworkInterfaceId-parameter
        * EC2 - describe_instances now supports additional filters (owner-id)
        * EC2 - describe_instance_status now supports additional filters (instance-state-name, instance-state-code)
        * EC2 - describe_nat_gateways now supports additional filters (nat-gateway-id, vpc-id, subnet-id, state)
        * EC2 - describe_vpn_gateways now supports additional filters (attachment.vpc_id, attachment.state, vpn-gateway-id, type)
        * IAM - list_users now supports path_prefix-parameter
        * IOT - list_thing_groups now supports parent_group, name_prefix_filter, recursive-parameters
        * S3 - delete_objects now supports deletion of specific VersionIds
        * SecretsManager - list_secrets now supports filters-parameter
        * SFN - start_execution now receives and validates input
        * SNS - Now supports sending a message directly to a phone number
        * SQS - MessageAttributes now support labeled DataTypes

1.3.15
-----

This release broke dependency management for a lot of services - please upgrade to 1.3.16.

1.3.14
-----

    General Changes:
        * Support for Python 3.8
        * Linting: Black is now enforced.

    New Services:
        * Athena
        * Config
        * DataSync
        * Step Functions

    New methods:
        * Athena:
            * create_work_group()
            * list_work_groups()
        * API Gateway:
            * delete_stage()
            * update_api_key()
        * CloudWatch Logs
            * list_tags_log_group()
            * tag_log_group()
            * untag_log_group()
        * Config
            * batch_get_resource_config()
            * delete_aggregation_authorization()
            * delete_configuration_aggregator()
            * describe_aggregation_authorizations()
            * describe_configuration_aggregators()
            * get_resource_config_history()
            * list_aggregate_discovered_resources() (For S3)
            * list_discovered_resources() (For S3)
            * put_aggregation_authorization()
            * put_configuration_aggregator()
        * Cognito
            * assume_role_with_web_identity()
            * describe_identity_pool()
            * get_open_id_token()
            * update_user_pool_domain()
        * DataSync:
            * cancel_task_execution()
            * create_location()
            * create_task()
            * start_task_execution()
        * EC2:
            * create_launch_template()
            * create_launch_template_version()
            * describe_launch_template_versions()
            * describe_launch_templates()
        * ECS
            * decrypt()
            * encrypt()
            * generate_data_key_without_plaintext()
            * generate_random()
            * re_encrypt()
        * Glue
            * batch_get_partition()
        * IAM
            * create_open_id_connect_provider()
            * create_virtual_mfa_device()
            * delete_account_password_policy()
            * delete_open_id_connect_provider()
            * delete_policy()
            * delete_virtual_mfa_device()
            * get_account_password_policy()
            * get_open_id_connect_provider()
            * list_open_id_connect_providers()
            * list_virtual_mfa_devices()
            * update_account_password_policy()
        * Lambda
            * create_event_source_mapping()
            * delete_event_source_mapping()
            * get_event_source_mapping()
            * list_event_source_mappings()
            * update_configuration()
            * update_event_source_mapping()
            * update_function_code()
        * KMS
            * decrypt()
            * encrypt()
            * generate_data_key_without_plaintext()
            * generate_random()
            * re_encrypt()
        * SES
            * send_templated_email()
        * SNS
            * add_permission()
            * list_tags_for_resource()
            * remove_permission()
            * tag_resource()
            * untag_resource()
        * SSM
            * describe_parameters()
            * get_parameter_history()
        * Step Functions
            * create_state_machine()
            * delete_state_machine()
            * describe_execution()
            * describe_state_machine()
            * describe_state_machine_for_execution()
            * list_executions()
            * list_state_machines()
            * list_tags_for_resource()
            * start_execution()
            * stop_execution()
        SQS
            * list_queue_tags()
            * send_message_batch()

    General updates:
        * API Gateway:
            * Now generates valid IDs
            * API Keys, Usage Plans now support tags
        * ACM:
            * list_certificates() accepts the status parameter
        * Batch:
            * submit_job() can now be called with job name
        * CloudWatch Events
            * Multi-region support
        * CloudWatch Logs
            * get_log_events() now supports pagination
        * Cognito:
            * Now throws UsernameExistsException for known users
        * DynamoDB
            * update_item() now supports lists, the list_append-operator and removing nested items
            * delete_item() now supports condition expressions
            * get_item() now supports projection expression
            * Enforces 400KB item size
            * Validation on duplicate keys in batch_get_item()
            * Validation on AttributeDefinitions on create_table()
            * Validation on Query Key Expression
            * Projection Expressions now support nested attributes
        * EC2:
            * Change DesiredCapacity behaviour for AutoScaling groups
            * Extend list of supported EC2 ENI properties
            * Create ASG from Instance now supported
            * ASG attached to a terminated instance now recreate the instance of required
            * Unify OwnerIDs
        * ECS
            * Task definition revision deregistration: remaining revisions now remain unchanged
            * Fix created_at/updated_at format for deployments
            * Support multiple regions
        * ELB
            * Return correct response then describing target health of stopped instances
            * Target groups now longer show terminated instances
            * 'fixed-response' now a supported action-type
            * Now supports redirect: authenticate-cognito
        * Kinesis FireHose
            * Now supports ExtendedS3DestinationConfiguration
        * KMS
            * Now supports tags
        * Organizations
            * create_organization() now creates Master account
        * Redshift
            * Fix timezone problems when creating a cluster
            * Support for enhanced_vpc_routing-parameter
        * Route53
            * Implemented UPSERT for change_resource_records
        * S3:
            * Support partNumber for head_object
            * Support for INTELLIGENT_TIERING, GLACIER and DEEP_ARCHIVE
            * Fix KeyCount attribute
            * list_objects now supports pagination (next_marker)
            * Support tagging for versioned objects
        * STS
            * Implement validation on policy length
        * Lambda
            * Support EventSourceMappings for SQS, DynamoDB
            * get_function(), delete_function() now both support ARNs as parameters
        * IAM
            * Roles now support tags
            * Policy Validation: SID can be empty
            * Validate roles have no attachments when deleting
        * SecretsManager
            * Now supports binary secrets
        * IOT
            * update_thing_shadow validation
            * delete_thing now also removed principals
        * SQS
            * Tags supported for create_queue()


1.3.7
-----

    * Switch from mocking requests to using before-send for AWS calls

1.3.6
-----

    * Fix boto3 pinning.

1.3.5
-----

    * Pin down botocore issue as temporary fix for #1793.
    * More features on secrets manager

1.3.4
------

    * IAM get account authorization details
    * adding account id to ManagedPolicy ARN
    * APIGateway usage plans and usage plan keys
    * ECR list images

1.3.3
------
    
    * Fix a regression in S3 url regexes
    * APIGateway region fixes
    * ECS improvements
    * Add @mock_cognitoidentity, thanks to @brcoding


1.3.2
------
The huge change in this version is that the responses library is no longer vendored. Many developers are now unblocked. Kudos to @spulec for the fix.

    * Fix route53 TTL bug
    * Added filtering support for S3 lifecycle
    * unvendoring responses

1.3.0
------

Dozens of major endpoint additions in this release. Highlights include:

    * Fixed AMI tests and the Travis build setup
    * SNS improvements
    * Dynamodb improvements
    * EBS improvements
    * Redshift improvements
    * RDS snapshot improvements
    * S3 improvements
    * Cloudwatch improvements
    * SSM improvements
    * IAM improvements
    * ELBV1 and ELBV2 improvements
    * Lambda improvements
    * EC2 spot pricing improvements
    * ApiGateway improvements
    * VPC improvements

1.2.0
------

    * Supports filtering AMIs by self
    * Implemented signal_workflow_execution for SWF
    * Wired SWF backend to the moto server
    * Added url decoding to x-amz-copy-source header for copying S3 files
    * Revamped lambda function storage to do versioning
    * IOT improvements
    * RDS improvements
    * Implemented CloudWatch get_metric_statistics
    * Improved Cloudformation EC2 support
    * Implemented Cloudformation change_set endpoints
    
1.1.25
-----

    * Implemented Iot and Iot-data
    * Implemented resource tagging API
    * EC2 AMIs now have owners
    * Improve codegen scaffolding
    * Many small fixes to EC2 support
    * CloudFormation ELBv2 support
    * UTF fixes for S3
    * Implemented SSM get_parameters_by_path
    * More advanced Dynamodb querying

1.1.24
-----

    * Implemented Batch
    * Fixed regression with moto_server dashboard
    * Fixed and closed many outstanding bugs
    * Fixed serious performance problem with EC2 reservation listing
    * Fixed Route53 list_resource_record_sets

1.1.23
-----

    * Implemented X-Ray
    * Implemented Autoscaling EC2 attachment
    * Implemented Autoscaling Load Balancer methods
    * Improved DynamoDB filter expressions

1.1.22
-----

    * Lambda policies
    * Dynamodb filter expressions
    * EC2 Spot fleet improvements

1.1.21
-----

    * ELBv2 bugfixes
    * Removing GPL'd dependency

1.1.20
-----

    * Improved `make scaffold`
    * Implemented IAM attached group policies
    * Implemented skeleton of Cloudwatch Logs
    * Redshift: fixed multi-params
    * Redshift: implement taggable resources
    * Lambda + SNS: Major enhancements

1.1.19
-----

    * Fixing regression from 1.1.15

1.1.15
-----

    * Polly implementation
    * Added EC2 instance info
    * SNS publish by phone number

1.1.14
-----

    * ACM implementation
    * Added `make scaffold`
    * X-Ray implementation

1.1.13
-----

    * Created alpine-based Dockerfile (dockerhub: motoserver/moto)
    * SNS.SetSMSAttributes & SNS.GetSMSAttributes + Filtering
    * S3 ACL implementation
    * pushing to Dockerhub on `make publish`

1.1.12
-----

    * implemented all AWS managed policies in source
    * fixing Dynamodb CapacityUnits format
    * S3 ACL implementation

1.1.11
-----

    * S3 authentication
    * SSM get_parameter
    * ELBv2 target group tagging
    * EC2 Security group filters

1.1.10
-----

    * EC2 vpc address filtering
    * EC2 elastic ip dissociation
    * ELBv2 target group tagging
    * fixed complexity of accepting new filter implementations

1.1.9
-----

    * EC2 root device mapping

1.1.8
-----

    * Lambda get_function for function created with zipfile
    * scripts/implementation_coverage.py

1.1.7
-----

    * Lambda invoke_async
    * EC2 keypair filtering

1.1.6
-----

    * Dynamo ADD and DELETE operations in update expressions
    * Lambda tag support

1.1.5
-----

    * Dynamo allow ADD update_item of a string set
    * Handle max-keys in list-objects
    * bugfixes in pagination

1.1.3
-----

    * EC2 vpc_id in responses

1.1.2
-----

    * IAM account aliases
    * SNS subscription attributes
    * bugfixes in Dynamo, CFN, and EC2

1.1.1
-----

    * EC2 group-id filter
    * EC2 list support for filters

1.1.0
-----

    * Add ELBv2
    * IAM user policies
    * RDS snapshots
    * IAM policy versions

1.0.1
-----

    * Add Cloudformation exports
    * Add ECR
    * IAM policy versions

1.0.0
-----

    BACKWARDS INCOMPATIBLE
    * The normal @mock_<service> decorators will no longer work with boto. It is suggested that you upgrade to boto3 or use the standalone-server mode. If you would still like to use boto, you must use the @mock_<service>_deprecated decorators which will be removed in a future release.
    * The @mock_s3bucket_path decorator is now deprecated. Use the @mock_s3 decorator instead.
    * Drop support for Python 2.6
    * Redshift server defaults to returning XML instead of JSON

    Added features
    * Reset API: a reset API has been added to flush all of the current data ex: `requests.post("http://motoapi.amazonaws.com/moto-api/reset")`
    * A dashboard is now available with moto_server at http://localhost:5000/moto-api/

0.4.31
------

    * ECS Cloudformation support
    * Cleaned up RDS XML/JSON issues
    * Boto==2.45
    * Add STS get_caller_identity
    * Turn on variable escaping in templates for S3 XML documents

0.4.30
------

    * Change spot requests to launch instances

0.4.29
------

    * Nest flask import so that it is not required globally

0.4.28
------

    * Add basic spot fleet support
    * IAM Managed Policies
    * Better EMR coverage
    * Basic KMS support for encrypt/decrypt

0.4.27
------

    *

0.4.25
------

    * ASG tags
    * ContainerInstance handling in ECS
    *

0.4.22
------

    * Add basic lambda endpoints
    * Support placement for EC2
    * Cleanup API versions


0.4.21
------

    * Fix bug with wrong response matches for S3

0.4.20
------

    * mock_s3 and mocks3bucket_path are now the same thing. The server decides
    which interface to is being used based on the request Host header. We will
    evetually deprecate mocks3bucket_path.
    * Basic ECS support
    * More Dynamo querying and indexes
    * Add Kinesis and ELB tags
    * Add JSON responses for EMR
    * Fix root instance volume to show up in other EBS volume calls
