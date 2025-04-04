from __future__ import unicode_literals

import os
import json

import boto
import boto3
import boto.dynamodb2
import boto.iam
import boto.s3
import boto.s3.key
import boto.cloudformation
from boto.exception import BotoServerError
from freezegun import freeze_time
import sure  # noqa

import pytest
from moto.core import ACCOUNT_ID

from moto import (
    mock_cloudformation_deprecated,
    mock_s3_deprecated,
    mock_sns_deprecated,
    mock_sqs_deprecated,
    mock_route53_deprecated,
    mock_iam_deprecated,
    mock_dynamodb2_deprecated,
)
from moto.cloudformation import cloudformation_backends

dummy_template = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Description": "Stack 1",
    "Resources": {},
}

dummy_template2 = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Description": "Stack 2",
    "Resources": {},
}

# template with resource which has no delete attribute defined
dummy_template3 = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Description": "Stack 3",
    "Resources": {
        "VPC": {"Properties": {"CidrBlock": "192.168.0.0/16"}, "Type": "AWS::EC2::VPC"}
    },
}

dummy_template4 = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Resources": {
        "myDynamoDBTable": {
            "Type": "AWS::DynamoDB::Table",
            "Properties": {
                "AttributeDefinitions": [
                    {"AttributeName": "Name", "AttributeType": "S"},
                    {"AttributeName": "Age", "AttributeType": "S"},
                ],
                "KeySchema": [
                    {"AttributeName": "Name", "KeyType": "HASH"},
                    {"AttributeName": "Age", "KeyType": "RANGE"},
                ],
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
                "TableName": "Person",
            },
        }
    },
}

dummy_template_json = json.dumps(dummy_template)
dummy_template_json2 = json.dumps(dummy_template2)
dummy_template_json3 = json.dumps(dummy_template3)
dummy_template_json4 = json.dumps(dummy_template4)


@mock_cloudformation_deprecated
def test_create_stack():
    conn = boto.connect_cloudformation()
    conn.create_stack("test_stack", template_body=dummy_template_json)

    stack = conn.describe_stacks()[0]
    stack.stack_id.should.contain(
        "arn:aws:cloudformation:us-east-1:123456789:stack/test_stack/"
    )
    stack.stack_name.should.equal("test_stack")
    stack.get_template().should.equal(
        {
            "GetTemplateResponse": {
                "GetTemplateResult": {
                    "TemplateBody": dummy_template_json,
                    "ResponseMetadata": {
                        "RequestId": "2d06e36c-ac1d-11e0-a958-f9382b6eb86bEXAMPLE"
                    },
                }
            }
        }
    )


@mock_cloudformation_deprecated
def test_create_stack_with_other_region():
    conn = boto.cloudformation.connect_to_region("us-west-2")
    conn.create_stack("test_stack", template_body=dummy_template_json)

    stack = conn.describe_stacks()[0]
    stack.stack_id.should.contain(
        "arn:aws:cloudformation:us-west-2:123456789:stack/test_stack/"
    )
    stack.stack_name.should.equal("test_stack")
    stack.get_template().should.equal(
        {
            "GetTemplateResponse": {
                "GetTemplateResult": {
                    "TemplateBody": dummy_template_json,
                    "ResponseMetadata": {
                        "RequestId": "2d06e36c-ac1d-11e0-a958-f9382b6eb86bEXAMPLE"
                    },
                }
            }
        }
    )


@mock_cloudformation_deprecated
@mock_route53_deprecated
def test_create_stack_hosted_zone_by_id():
    conn = boto.connect_cloudformation()
    dummy_template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "Stack 1",
        "Parameters": {},
        "Resources": {
            "Bar": {
                "Type": "AWS::Route53::HostedZone",
                "Properties": {"Name": "foo.bar.baz"},
            }
        },
    }
    dummy_template2 = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "Stack 2",
        "Parameters": {"ZoneId": {"Type": "String"}},
        "Resources": {
            "Foo": {
                "Properties": {"HostedZoneId": {"Ref": "ZoneId"}, "RecordSets": []},
                "Type": "AWS::Route53::RecordSetGroup",
            }
        },
    }
    conn.create_stack(
        "test_stack1", template_body=json.dumps(dummy_template), parameters={}.items()
    )
    r53_conn = boto.connect_route53()
    zone_id = r53_conn.get_zones()[0].id
    conn.create_stack(
        "test_stack2",
        template_body=json.dumps(dummy_template2),
        parameters={"ZoneId": zone_id}.items(),
    )

    stack = conn.describe_stacks()[0]
    assert stack.list_resources()


@mock_cloudformation_deprecated
def test_creating_stacks_across_regions():
    west1_conn = boto.cloudformation.connect_to_region("us-west-1")
    west1_conn.create_stack("test_stack", template_body=dummy_template_json)

    west2_conn = boto.cloudformation.connect_to_region("us-west-2")
    west2_conn.create_stack("test_stack", template_body=dummy_template_json)

    list(west1_conn.describe_stacks()).should.have.length_of(1)
    list(west2_conn.describe_stacks()).should.have.length_of(1)


@mock_cloudformation_deprecated
@mock_sns_deprecated
@mock_sqs_deprecated
def test_create_stack_with_notification_arn():
    sqs_conn = boto.connect_sqs()
    queue = sqs_conn.create_queue("fake-queue", visibility_timeout=3)
    queue_arn = queue.get_attributes()["QueueArn"]

    sns_conn = boto.connect_sns()
    topic = sns_conn.create_topic("fake-topic")
    topic_arn = topic["CreateTopicResponse"]["CreateTopicResult"]["TopicArn"]

    sns_conn.subscribe(topic_arn, "sqs", queue_arn)

    conn = boto.connect_cloudformation()
    with freeze_time("2015-01-01 12:00:00"):
        conn.create_stack(
            "test_stack_with_notifications",
            template_body=dummy_template_json,
            notification_arns=topic_arn,
        )

    stack = conn.describe_stacks()[0]
    [n.value for n in stack.notification_arns].should.contain(topic_arn)

    with freeze_time("2015-01-01 12:00:01"):
        message = queue.read(1)

    msg = json.loads(message.get_body())
    msg["Message"].should.contain("StackId='{}'\n".format(stack.stack_id))
    msg["Message"].should.contain("Timestamp='2015-01-01T12:00:00.000Z'\n")
    msg["Message"].should.contain("LogicalResourceId='test_stack_with_notifications'\n")
    msg["Message"].should.contain("ResourceStatus='CREATE_IN_PROGRESS'\n")
    msg["Message"].should.contain("ResourceStatusReason='User Initiated'\n")
    msg["Message"].should.contain("ResourceType='AWS::CloudFormation::Stack'\n")
    msg["Message"].should.contain("StackName='test_stack_with_notifications'\n")
    msg.should.have.key("MessageId")
    msg.should.have.key("Signature")
    msg.should.have.key("SignatureVersion")
    msg.should.have.key("Subject")
    msg["Timestamp"].should.equal("2015-01-01T12:00:00.000Z")
    msg["TopicArn"].should.equal(topic_arn)
    msg.should.have.key("Type")
    msg.should.have.key("UnsubscribeURL")

    with freeze_time("2015-01-01 12:00:02"):
        message = queue.read(1)

    msg = json.loads(message.get_body())
    msg["Message"].should.contain("StackId='{}'\n".format(stack.stack_id))
    msg["Message"].should.contain("Timestamp='2015-01-01T12:00:00.000Z'\n")
    msg["Message"].should.contain("LogicalResourceId='test_stack_with_notifications'\n")
    msg["Message"].should.contain("ResourceStatus='CREATE_COMPLETE'\n")
    msg["Message"].should.contain("ResourceStatusReason='None'\n")
    msg["Message"].should.contain("ResourceType='AWS::CloudFormation::Stack'\n")
    msg["Message"].should.contain("StackName='test_stack_with_notifications'\n")
    msg.should.have.key("MessageId")
    msg.should.have.key("Signature")
    msg.should.have.key("SignatureVersion")
    msg.should.have.key("Subject")
    msg["Timestamp"].should.equal("2015-01-01T12:00:00.000Z")
    msg["TopicArn"].should.equal(topic_arn)
    msg.should.have.key("Type")
    msg.should.have.key("UnsubscribeURL")


@mock_cloudformation_deprecated
@mock_s3_deprecated
def test_create_stack_from_s3_url():
    s3_conn = boto.s3.connect_to_region("us-west-1")
    bucket = s3_conn.create_bucket("foobar", location="us-west-1")
    key = boto.s3.key.Key(bucket)
    key.key = "template-key"
    key.set_contents_from_string(dummy_template_json)
    key_url = key.generate_url(expires_in=0, query_auth=False)

    conn = boto.cloudformation.connect_to_region("us-west-1")
    conn.create_stack("new-stack", template_url=key_url)

    stack = conn.describe_stacks()[0]
    stack.stack_name.should.equal("new-stack")
    stack.get_template().should.equal(
        {
            "GetTemplateResponse": {
                "GetTemplateResult": {
                    "TemplateBody": dummy_template_json,
                    "ResponseMetadata": {
                        "RequestId": "2d06e36c-ac1d-11e0-a958-f9382b6eb86bEXAMPLE"
                    },
                }
            }
        }
    )


@mock_cloudformation_deprecated
def test_describe_stack_by_name():
    conn = boto.connect_cloudformation()
    conn.create_stack("test_stack", template_body=dummy_template_json)

    stack = conn.describe_stacks("test_stack")[0]
    stack.stack_name.should.equal("test_stack")


@mock_cloudformation_deprecated
def test_describe_stack_by_stack_id():
    conn = boto.connect_cloudformation()
    conn.create_stack("test_stack", template_body=dummy_template_json)

    stack = conn.describe_stacks("test_stack")[0]
    stack_by_id = conn.describe_stacks(stack.stack_id)[0]
    stack_by_id.stack_id.should.equal(stack.stack_id)
    stack_by_id.stack_name.should.equal("test_stack")


@mock_dynamodb2_deprecated
@mock_cloudformation_deprecated
def test_delete_stack_dynamo_template():
    conn = boto.connect_cloudformation()
    db_conn = boto.dynamodb2.connect_to_region("us-east-1")
    #
    conn.create_stack("test_stack", template_body=dummy_template_json4)
    db_conn.list_tables()["TableNames"].should.have.length_of(1)
    #
    conn.delete_stack("test_stack")
    db_conn.list_tables()["TableNames"].should.have.length_of(0)


@mock_cloudformation_deprecated
def test_describe_deleted_stack():
    conn = boto.connect_cloudformation()
    conn.create_stack("test_stack", template_body=dummy_template_json)

    stack = conn.describe_stacks("test_stack")[0]
    stack_id = stack.stack_id
    conn.delete_stack(stack.stack_id)
    stack_by_id = conn.describe_stacks(stack_id)[0]
    stack_by_id.stack_id.should.equal(stack.stack_id)
    stack_by_id.stack_name.should.equal("test_stack")
    stack_by_id.stack_status.should.equal("DELETE_COMPLETE")


@mock_cloudformation_deprecated
def test_get_template_by_name():
    conn = boto.connect_cloudformation()
    conn.create_stack("test_stack", template_body=dummy_template_json)

    template = conn.get_template("test_stack")
    template.should.equal(
        {
            "GetTemplateResponse": {
                "GetTemplateResult": {
                    "TemplateBody": dummy_template_json,
                    "ResponseMetadata": {
                        "RequestId": "2d06e36c-ac1d-11e0-a958-f9382b6eb86bEXAMPLE"
                    },
                }
            }
        }
    )


@mock_cloudformation_deprecated
def test_list_stacks():
    conn = boto.connect_cloudformation()
    conn.create_stack("test_stack", template_body=dummy_template_json)
    conn.create_stack("test_stack2", template_body=dummy_template_json)

    stacks = conn.list_stacks()
    stacks.should.have.length_of(2)
    stacks[0].template_description.should.equal("Stack 1")


@mock_cloudformation_deprecated
def test_list_stacks_with_filter():
    conn = boto.connect_cloudformation()
    conn.create_stack("test_stack", template_body=dummy_template_json)
    conn.create_stack("test_stack2", template_body=dummy_template_json)
    conn.update_stack("test_stack", template_body=dummy_template_json2)
    stacks = conn.list_stacks("CREATE_COMPLETE")
    stacks.should.have.length_of(1)
    stacks[0].template_description.should.equal("Stack 1")
    stacks = conn.list_stacks("UPDATE_COMPLETE")
    stacks.should.have.length_of(1)


@mock_cloudformation_deprecated
def test_delete_stack_by_name():
    conn = boto.connect_cloudformation()
    conn.create_stack("test_stack", template_body=dummy_template_json)

    conn.describe_stacks().should.have.length_of(1)
    conn.delete_stack("test_stack")
    conn.describe_stacks().should.have.length_of(0)


@mock_cloudformation_deprecated
def test_delete_stack_by_id():
    conn = boto.connect_cloudformation()
    stack_id = conn.create_stack("test_stack", template_body=dummy_template_json)

    conn.describe_stacks().should.have.length_of(1)
    conn.delete_stack(stack_id)
    conn.describe_stacks().should.have.length_of(0)
    with pytest.raises(BotoServerError):
        conn.describe_stacks("test_stack")

    conn.describe_stacks(stack_id).should.have.length_of(1)


@mock_cloudformation_deprecated
def test_delete_stack_with_resource_missing_delete_attr():
    conn = boto.connect_cloudformation()
    conn.create_stack("test_stack", template_body=dummy_template_json3)

    conn.describe_stacks().should.have.length_of(1)
    conn.delete_stack("test_stack")
    conn.describe_stacks().should.have.length_of(0)


@mock_cloudformation_deprecated
def test_bad_describe_stack():
    conn = boto.connect_cloudformation()
    with pytest.raises(BotoServerError):
        conn.describe_stacks("bad_stack")


@mock_cloudformation_deprecated()
def test_cloudformation_params():
    dummy_template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "Stack 1",
        "Resources": {},
        "Parameters": {
            "APPNAME": {
                "Default": "app-name",
                "Description": "The name of the app",
                "Type": "String",
            }
        },
    }
    dummy_template_json = json.dumps(dummy_template)
    cfn = boto.connect_cloudformation()
    cfn.create_stack(
        "test_stack1",
        template_body=dummy_template_json,
        parameters=[("APPNAME", "testing123")],
    )
    stack = cfn.describe_stacks("test_stack1")[0]
    stack.parameters.should.have.length_of(1)
    param = stack.parameters[0]
    param.key.should.equal("APPNAME")
    param.value.should.equal("testing123")


@mock_cloudformation_deprecated
def test_cloudformation_params_conditions_and_resources_are_distinct():
    dummy_template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "Stack 1",
        "Conditions": {
            "FooEnabled": {"Fn::Equals": [{"Ref": "FooEnabled"}, "true"]},
            "FooDisabled": {
                "Fn::Not": [{"Fn::Equals": [{"Ref": "FooEnabled"}, "true"]}]
            },
        },
        "Parameters": {
            "FooEnabled": {"Type": "String", "AllowedValues": ["true", "false"]}
        },
        "Resources": {
            "Bar": {
                "Properties": {"CidrBlock": "192.168.0.0/16"},
                "Condition": "FooDisabled",
                "Type": "AWS::EC2::VPC",
            }
        },
    }
    dummy_template_json = json.dumps(dummy_template)
    cfn = boto.connect_cloudformation()
    cfn.create_stack(
        "test_stack1",
        template_body=dummy_template_json,
        parameters=[("FooEnabled", "true")],
    )
    stack = cfn.describe_stacks("test_stack1")[0]
    resources = stack.list_resources()
    assert not [
        resource for resource in resources if resource.logical_resource_id == "Bar"
    ]


@mock_cloudformation_deprecated
def test_stack_tags():
    conn = boto.connect_cloudformation()
    conn.create_stack(
        "test_stack",
        template_body=dummy_template_json,
        tags={"foo": "bar", "baz": "bleh"},
    )

    stack = conn.describe_stacks()[0]
    dict(stack.tags).should.equal({"foo": "bar", "baz": "bleh"})


@mock_cloudformation_deprecated
def test_update_stack():
    conn = boto.connect_cloudformation()
    conn.create_stack("test_stack", template_body=dummy_template_json)

    conn.update_stack("test_stack", dummy_template_json2)

    stack = conn.describe_stacks()[0]
    stack.stack_status.should.equal("UPDATE_COMPLETE")
    stack.get_template().should.equal(
        {
            "GetTemplateResponse": {
                "GetTemplateResult": {
                    "TemplateBody": dummy_template_json2,
                    "ResponseMetadata": {
                        "RequestId": "2d06e36c-ac1d-11e0-a958-f9382b6eb86bEXAMPLE"
                    },
                }
            }
        }
    )


@mock_cloudformation_deprecated
def test_update_stack_with_previous_template():
    conn = boto.connect_cloudformation()
    conn.create_stack("test_stack", template_body=dummy_template_json)
    conn.update_stack("test_stack", use_previous_template=True)

    stack = conn.describe_stacks()[0]
    stack.stack_status.should.equal("UPDATE_COMPLETE")
    stack.get_template().should.equal(
        {
            "GetTemplateResponse": {
                "GetTemplateResult": {
                    "TemplateBody": dummy_template_json,
                    "ResponseMetadata": {
                        "RequestId": "2d06e36c-ac1d-11e0-a958-f9382b6eb86bEXAMPLE"
                    },
                }
            }
        }
    )


@mock_cloudformation_deprecated
def test_update_stack_with_parameters():
    dummy_template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "Stack",
        "Resources": {
            "VPC": {
                "Properties": {"CidrBlock": {"Ref": "Bar"}},
                "Type": "AWS::EC2::VPC",
            }
        },
        "Parameters": {"Bar": {"Type": "String"}},
    }
    dummy_template_json = json.dumps(dummy_template)
    conn = boto.connect_cloudformation()
    conn.create_stack(
        "test_stack",
        template_body=dummy_template_json,
        parameters=[("Bar", "192.168.0.0/16")],
    )
    conn.update_stack(
        "test_stack",
        template_body=dummy_template_json,
        parameters=[("Bar", "192.168.0.1/16")],
    )

    stack = conn.describe_stacks()[0]
    assert stack.parameters[0].value == "192.168.0.1/16"


@mock_cloudformation_deprecated
def test_update_stack_replace_tags():
    conn = boto.connect_cloudformation()
    conn.create_stack(
        "test_stack", template_body=dummy_template_json, tags={"foo": "bar"}
    )
    conn.update_stack(
        "test_stack", template_body=dummy_template_json, tags={"foo": "baz"}
    )

    stack = conn.describe_stacks()[0]
    stack.stack_status.should.equal("UPDATE_COMPLETE")
    # since there is one tag it doesn't come out as a list
    dict(stack.tags).should.equal({"foo": "baz"})


@mock_cloudformation_deprecated
def test_update_stack_when_rolled_back():
    conn = boto.connect_cloudformation()
    stack_id = conn.create_stack("test_stack", template_body=dummy_template_json)

    cloudformation_backends[conn.region.name].stacks[
        stack_id
    ].status = "ROLLBACK_COMPLETE"

    with pytest.raises(BotoServerError) as err:
        conn.update_stack("test_stack", dummy_template_json)

    ex = err.value
    ex.body.should.match(r"is in ROLLBACK_COMPLETE state and can not be updated")
    ex.error_code.should.equal("ValidationError")
    ex.reason.should.equal("Bad Request")
    ex.status.should.equal(400)


@mock_cloudformation_deprecated
def test_describe_stack_events_shows_create_update_and_delete():
    conn = boto.connect_cloudformation()
    stack_id = conn.create_stack("test_stack", template_body=dummy_template_json)
    conn.update_stack(stack_id, template_body=dummy_template_json2)
    conn.delete_stack(stack_id)

    # assert begins and ends with stack events
    events = conn.describe_stack_events(stack_id)
    events[0].resource_type.should.equal("AWS::CloudFormation::Stack")
    events[-1].resource_type.should.equal("AWS::CloudFormation::Stack")

    # testing ordering of stack events without assuming resource events will not exist
    # the AWS API returns events in reverse chronological order
    stack_events_to_look_for = iter(
        [
            ("DELETE_COMPLETE", None),
            ("DELETE_IN_PROGRESS", "User Initiated"),
            ("UPDATE_COMPLETE", None),
            ("UPDATE_IN_PROGRESS", "User Initiated"),
            ("CREATE_COMPLETE", None),
            ("CREATE_IN_PROGRESS", "User Initiated"),
        ]
    )
    try:
        for event in events:
            event.stack_id.should.equal(stack_id)
            event.stack_name.should.equal("test_stack")
            event.event_id.should.match(r"[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}")

            if event.resource_type == "AWS::CloudFormation::Stack":
                event.logical_resource_id.should.equal("test_stack")
                event.physical_resource_id.should.equal(stack_id)

                status_to_look_for, reason_to_look_for = next(stack_events_to_look_for)
                event.resource_status.should.equal(status_to_look_for)
                if reason_to_look_for is not None:
                    event.resource_status_reason.should.equal(reason_to_look_for)
    except StopIteration:
        assert False, "Too many stack events"

    list(stack_events_to_look_for).should.be.empty

    with pytest.raises(BotoServerError) as exp:
        conn.describe_stack_events("non_existing_stack")
    err = exp.value
    err.message.should.equal("Stack with id non_existing_stack does not exist")
    err.body.should.match(r"Stack with id non_existing_stack does not exist")
    err.error_code.should.equal("ValidationError")
    err.reason.should.equal("Bad Request")
    err.status.should.equal(400)


@mock_cloudformation_deprecated
def test_create_stack_lambda_and_dynamodb():
    conn = boto.connect_cloudformation()
    dummy_template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "Stack Lambda Test 1",
        "Parameters": {},
        "Resources": {
            "func1": {
                "Type": "AWS::Lambda::Function",
                "Properties": {
                    "Code": {"S3Bucket": "bucket_123", "S3Key": "key_123"},
                    "FunctionName": "func1",
                    "Handler": "handler.handler",
                    "Role": get_role_name(),
                    "Runtime": "python2.7",
                    "Description": "descr",
                    "MemorySize": 12345,
                },
            },
            "func1version": {
                "Type": "AWS::Lambda::Version",
                "Properties": {"FunctionName": {"Ref": "func1"}},
            },
            "tab1": {
                "Type": "AWS::DynamoDB::Table",
                "Properties": {
                    "TableName": "tab1",
                    "KeySchema": [{"AttributeName": "attr1", "KeyType": "HASH"}],
                    "AttributeDefinitions": [
                        {"AttributeName": "attr1", "AttributeType": "string"}
                    ],
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 10,
                        "WriteCapacityUnits": 10,
                    },
                    "StreamSpecification": {"StreamViewType": "KEYS_ONLY"},
                },
            },
            "func1mapping": {
                "Type": "AWS::Lambda::EventSourceMapping",
                "Properties": {
                    "FunctionName": {"Ref": "func1"},
                    "EventSourceArn": {"Fn::GetAtt": ["tab1", "StreamArn"]},
                    "StartingPosition": "0",
                    "BatchSize": 100,
                    "Enabled": True,
                },
            },
        },
    }
    validate_s3_before = os.environ.get("VALIDATE_LAMBDA_S3", "")
    try:
        os.environ["VALIDATE_LAMBDA_S3"] = "false"
        conn.create_stack(
            "test_stack_lambda_1",
            template_body=json.dumps(dummy_template),
            parameters={}.items(),
        )
    finally:
        os.environ["VALIDATE_LAMBDA_S3"] = validate_s3_before

    stack = conn.describe_stacks()[0]
    resources = stack.list_resources()
    assert len(resources) == 4


@mock_cloudformation_deprecated
def test_create_stack_kinesis():
    conn = boto.connect_cloudformation()
    dummy_template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "Stack Kinesis Test 1",
        "Parameters": {},
        "Resources": {
            "stream1": {
                "Type": "AWS::Kinesis::Stream",
                "Properties": {"Name": "stream1", "ShardCount": 2},
            }
        },
    }
    conn.create_stack(
        "test_stack_kinesis_1",
        template_body=json.dumps(dummy_template),
        parameters={}.items(),
    )

    stack = conn.describe_stacks()[0]
    resources = stack.list_resources()
    assert len(resources) == 1


def get_role_name():
    with mock_iam_deprecated():
        iam = boto.connect_iam()
        role = iam.create_role("my-role")["create_role_response"]["create_role_result"][
            "role"
        ]["arn"]
        return role
