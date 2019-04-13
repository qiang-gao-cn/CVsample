##################################################
# Name: Video(Volo) as a Service
# Version: v1.0.0
# Author: harry.ma@dao-lab.com
##################################################

import json;
import time;
import datetime;
import os;
import uuid;
import base64;
import boto3;

def returnResponse(errmsg, resBody = {}) :
    ErrorMsg = {
            "ok": {"statusCode": 200, "errorCode": 0, "errorMessage": "OK"},
            "no": {"statusCode": 500, "errorCode": 1, "errorMessage": "Internal Server Error"},
            "NoEnv": {"statusCode": 500, "errorCode": 2, "errorMessage": "AWS Env is not set"},
            "NoSupport":  {"statusCode": 400, "errorCode": 3, "errorMessage": "request is not supported"},
            "ReqBodyErr": {"statusCode": 400, "errorCode": 4, "errorMessage": "Fail to parse request body to JSON object."},
        };

    try :
        err = ErrorMsg[errmsg];
    except :
        err = ErrorMsg["no"];

    resBody["errorCode"] = err["errorCode"];
    resBody["errorMessage"] = err["errorMessage"];

    response = {};
    response["statusCode"] = err["statusCode"];
    response["headers"] = {};
    response["headers"]["Content-Type"] = "application/json";
    response["headers"]["Access-Control-Allow-Origin"] = "*";
    response["headers"]["Access-Control-Allow-Headers"] = "x-api-key";
    response["headers"]["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS";
    response["body"] = json.dumps(resBody, sort_keys=True);#json.dumps 字典=>json

    return response;


def getenv(vars) :
    env = {};

    for var in vars :
        try :
            env[var] = os.environ[var];
        except :
            env[var] = None;

    return env;

def parse_dyanmodb_fmt(obj) :
    r = {};
    for k in obj :
        r[k] = obj[k]["S"];

    return r;

def search_job(q) :
    envs = getenv(["VAAS_REGION", "AWS_KEY_ID", "AWS_KEY_VL", "AWS_DYNAMODB"]);
    #boto3.client aws api
    dynamodb = boto3.client("dynamodb",
                            region_name = envs["VAAS_REGION"],
                            aws_access_key_id = envs["AWS_KEY_ID"],
                            aws_secret_access_key = envs["AWS_KEY_VL"]);

    if q == {} :
        r = dynamodb.scan(TableName = envs["AWS_DYNAMODB"]);#dynamodb.scan scan扫描全表
    elif "JobID" in q :
        r = dynamodb.get_item(TableName = envs["AWS_DYNAMODB"], Key = {"JobID": {"S": q["JobID"]}});
    else :
        r = {}


    try :
        if r["ResponseMetadata"]["HTTPStatusCode"] == 200 :
            records = []
            if "Items" in r :
                for i in r["Items"] :
                    records.append(parse_dyanmodb_fmt(i));
            elif "Item" in r :
                # records.append(parse_dyanmodb_fmt(r["Item"]));
                return(parse_dyanmodb_fmt(r["Item"]));
            else :
                pass

            return({"items": records});
    except :
        return({"items": []});


def update_db(job) :
    envs = getenv(["VAAS_REGION", "AWS_KEY_ID", "AWS_KEY_VL", "AWS_DYNAMODB"]);

    dynamodb = boto3.client("dynamodb",
                            region_name = envs["VAAS_REGION"],
                            aws_access_key_id = envs["AWS_KEY_ID"],
                            aws_secret_access_key = envs["AWS_KEY_VL"]);

    expr = "";
    attrName = {};
    attrValue = {};
    for k in job :
        if k != "JobID" :
            if len(expr) > 0 :
                expr += ", ";
            else :
                expr = "SET ";
            expr += "#" + k + " = :" + k;

            attrName["#" + k] = k;
            if isinstance(job[k], str) :
                attrValue[":" + k] = {"S": job[k]};
            elif isinstance(job[k], dict) :
                attrValue[":" + k] = {"SS": job[k]};

    for i in range(5) :
        r = dynamodb.update_item(TableName = envs["AWS_DYNAMODB"],
                                 Key = {"JobID": {'S': job["JobID"]}},
                                 UpdateExpression = expr,
                                 ExpressionAttributeNames = attrName,
                                 ExpressionAttributeValues = attrValue,
                                 ReturnValues = 'UPDATED_NEW');
        if r["ResponseMetadata"]["HTTPStatusCode"] == 200 :
            return parse_dyanmodb_fmt(r["Attributes"]);

    return {};


def write_s3(job, key) :
    envs = getenv(["AWS_KEY_ID", "AWS_KEY_VL", "AWS_S3_BUCKET"]);

    s3 = boto3.client('s3',
                      aws_access_key_id = envs["AWS_KEY_ID"],
                      aws_secret_access_key = envs["AWS_KEY_VL"]);
    r = s3.put_object(Bucket = envs["AWS_S3_BUCKET"], Body = json.dumps(job), Key = key);

def read_s3(key) :
    envs = getenv(["AWS_KEY_ID", "AWS_KEY_VL", "AWS_S3_BUCKET"]);

    s3 = boto3.client('s3',
                      aws_access_key_id = envs["AWS_KEY_ID"],
                      aws_secret_access_key = envs["AWS_KEY_VL"]);
    r = s3.get_object(Bucket = envs["AWS_S3_BUCKET"], Key = key);
    if r["ResponseMetadata"]["HTTPStatusCode"] == 200 :
        return json.loads(r['Body'].read().decode('utf-8'));
    else :
        return {};


def list_s3(key) :
    envs = getenv(["AWS_KEY_ID", "AWS_KEY_VL", "AWS_S3_BUCKET"]);

    s3 = boto3.client('s3',
                      aws_access_key_id = envs["AWS_KEY_ID"],
                      aws_secret_access_key = envs["AWS_KEY_VL"]);

    r = {"profile":[]};
    for k in s3.list_objects(Bucket = envs["AWS_S3_BUCKET"], Prefix = key)['Contents']:
        r["profile"].append(k["Key"].lstrip(key));

    return r;

def send_sqs(job) :
    envs = getenv(["VAAS_REGION", "AWS_KEY_ID", "AWS_KEY_VL", "AWS_SQS"]);

    sqs = boto3.client('sqs',
                       region_name = envs["VAAS_REGION"],
                       aws_access_key_id = envs["AWS_KEY_ID"],
                       aws_secret_access_key = envs["AWS_KEY_VL"]);

    queueUrl = sqs.get_queue_url(QueueName=envs["AWS_SQS"])["QueueUrl"];

    for i in range(5) :
        r = sqs.send_message(QueueUrl = queueUrl, MessageBody = json.dumps(job));
        if r["ResponseMetadata"]["HTTPStatusCode"] == 200 :
            break;

def get_sqs() :
    envs = getenv(["VAAS_REGION", "AWS_KEY_ID", "AWS_KEY_VL", "AWS_SQS"]);

    sqs = boto3.client('sqs',
                       region_name = envs["VAAS_REGION"],
                       aws_access_key_id = envs["AWS_KEY_ID"],
                       aws_secret_access_key = envs["AWS_KEY_VL"]);

    queueUrl = sqs.get_queue_url(QueueName=envs["AWS_SQS"])["QueueUrl"];

    for i in range(5) :
        r = sqs.receive_message(QueueUrl = queueUrl, MaxNumberOfMessages = 1);
        if r["ResponseMetadata"]["HTTPStatusCode"] == 200 :
            try :
                msg = json.loads(r["Messages"][0]["Body"]);

                # sqs.delete_message(QueueUrl = queueUrl, ReceiptHandle = r["Messages"][0]["ReceiptHandle"]);
            except :
                msg = {};

            return msg;

def launch_ec2() :
    envs = getenv(["VAAS_REGION", "AWS_KEY_ID", "AWS_KEY_VL", "AWS_SQS", "VAAS_LABEL"]);

    ec2 = boto3.client('ec2',
                       region_name = envs["VAAS_REGION"],
                       aws_access_key_id = envs["AWS_KEY_ID"],
                       aws_secret_access_key = envs["AWS_KEY_VL"]);

    # r = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values":["vaas-am730"]}]);
    r = ec2.describe_instances();
    cnt = 0;
    for i in r["Reservations"] :
        for j in i["Instances"] :
            if j["State"]["Name"] == "running" :
                cnt += 1;

    if cnt <= 100 :
        r = ec2.run_instances(ImageId = "ami-053d389d4eb50048d",
                              InstanceType = "t3.micro",
                              # CreditSpecification = {"CpuCredits": "unlimited"},
                              InstanceInitiatedShutdownBehavior = "terminate",
                              UserData = "#!/bin/bash\nexport AWS_ACCESS_KEY_ID=\""
                                            + os.environ["AWS_KEY_ID"]
                                            + "\"\nexport AWS_SECRET_ACCESS_KEY=\""
                                            + os.environ["AWS_KEY_VL"]
                                            + "\"\nexport AWS_DEFAULT_REGION=\""
                                            + os.environ["VAAS_REGION"]
                                            + "\"\nexport AWS_SQS=\""
                                            + os.environ["AWS_SQS"]
                                            + "\"\nexport AWS_SNS=\""
                                            + os.environ["AWS_SNS"]
                                            + "\"\nexport API_GATEWAY_URL=\""
                                            + os.environ["API_GATEWAY_URL"]
                                            + "\"\nexport API_GATEWAY_KEY=\""
                                            + os.environ["API_GATEWAY_KEY"]
                                            + "\"\naws s3 cp s3://"
                                            + os.environ["AWS_BUCKET"]
                                            + "/install/run.bash .\nbash run.bash &\n",
                              TagSpecifications = [{"ResourceType": "instance",
                                                    "Tags": [{"Key": "Name", "Value": "VaaS"},
                                                             {"Key": "Client", "Value": "Turner"},
                                                             {"Key": "Version", "Value": "0.1"}]}],
                              MinCount = 1,
                              KeyName = "harry-dev",
                              MaxCount = 1);

def create_job(job) :
    send_sqs(job);
    update_db(job);
    # launch_ec2();

def main(event, context) :
    isS3 = False;
    isGateway = False;

    try :
        if event["Records"][0]["eventSource"] == "aws:s3" and event["Records"][0]["eventName"].startswith("ObjectCreated") :
            isS3 = True;
    except :
        pass;

    try :
        if event['httpMethod'] :
            isGateway = True;
    except :
        pass;

    if isS3 :
        num = 0;
        for record in event["Records"] :
            bucket = record["s3"]["bucket"]["name"];
            objKey = record["s3"]["object"]["key"];

            # print("bucket: " + bucket + " key:" + objKey + " ext:" + objKey.split(".")[-1].lower());

            if not objKey.startswith("upload/record/") and objKey.split(".")[-1].lower() in ["ts", "mxf", "mp4"] :
                str_timestamp = time.strftime("%Y%m%d%H%M%S");
                str_uuid = str(uuid.uuid1()).replace("-", "");
                jobID = str_timestamp + "-" + str_uuid;

                for i in range(1) :
                    job = {"JobID" : jobID + "-" + str(i) + "-0",
                           "Input": "s3://" + bucket + "/" + objKey,
                           "HLSSegTime": "10",
                           "VideoGOP": "250",
                           "Format": "hls",
                           "VideoCodec": "h264",
                           "AudioCodec": "aac",
                           "AudioBitrate": "64",
                           "AudioChannel": "2",
                           "State": "Queue",
                           "LastUpdate": str_timestamp,
                           "Enable": "True"};

                    outName = "s3://" + bucket + "/" + "output" + objKey.lstrip("upload").split(".")[0];

                    if i == 0 :
                        job["VideoSize"] = "640x360";
                        job["VideoBitrate"] = "300";
                        job["Output"] = outName + "_360p.m3u8";
                    elif i == 1 :
                        job["VideoSize"] = "854x480";
                        job["VideoBitrate"] = "500";
                        job["Output"] = outName + "_480p.m3u8";
                    elif i == 2 :
                        job["VideoSize"] = "1280x720";
                        job["VideoBitrate"] = "800";
                        job["Output"] = outName + "_720p.m3u8";
                    # print(job)

                    create_job(job);
                    num = num + 1;

        return returnResponse("ok", {"num":num});
    elif isGateway :
        if event['httpMethod'] == "POST" or event['httpMethod'] == "PUT" :
            try:
                if "isBase64Encoded" in event and event["isBase64Encoded"]:
                    req = json.loads(base64.b64decode(event["body"]));
                else:
                    req = json.loads(event["body"]);
            except :
                return returnResponse("ReqBodyErr");

            path = event["path"].rstrip("/");
            if path == "/profile" :
                profile_name = "default"
                if "name" in req :
                    profile_name = req["name"];

                write_s3(req, "profile/" + profile_name + ".json");
                return returnResponse("ok", req);
            elif path == "/bin" :
                if "name" in req :
                    profile_name = req["name"];
                    write_s3(req, "bin/" + profile_name + ".bash");
                    return returnResponse("ok", req);
                else :
                    return returnResponse("no");

        if event['httpMethod'] == "POST" :
            str_timestamp = time.strftime("%Y%m%d%H%M%S");
            str_uuid = str(uuid.uuid1()).replace("-", "");
            jobID = str_timestamp + "-" + str_uuid + "-0-0";

            if "JobID" in req :
                return returnResponse("no");

            req["JobID"] = jobID;
            req["LastUpdate"] = str_timestamp;

            if "profile" in req :
                p = read_s3("profile/" + req["profile"] + ".json");
                for k in p.keys() :
                    req[k] = p[k];

            if not "option" in req :
                opt_str = "-i input.mxf -f mxf -y " + req["output"];
                print(opt_str)
                req["option"] = base64.b64encode(opt_str.encode("ascii")).decode('ascii');

            print(req)
            # create_job(req);

            # return returnResponse("ok", search_job({"JobID": req["JobID"]}));
            return returnResponse("ok", req);

            pass
        elif event['httpMethod'] == "PUT" :
            if "JobID" in req :
                r = update_db(req);
                return returnResponse("ok", r);
            else :
                return returnResponse("no");
        elif event['httpMethod'] == "GET" :
            path = event["path"].rstrip("/");

            if path == "/queue" :
                r = get_sqs();
            elif path == "/job" :
                q = {};
                if "queryStringParameters" in event and event["queryStringParameters"] and "JobID" in event["queryStringParameters"] :
                    q["JobID"] = event["queryStringParameters"]["JobID"];

                r = search_job(q);
            elif path == "/profile" :
                q = {};
                if "queryStringParameters" in event and event["queryStringParameters"] and "name" in event["queryStringParameters"] :
                    r = read_s3("profile/" + event["queryStringParameters"]["name"] + ".json");
                else :
                    r = list_s3("profile/");
            elif path == "/bin" :
                q = {};
                if "queryStringParameters" in event and event["queryStringParameters"] and "name" in event["queryStringParameters"] :
                    r = read_s3("bin/" + event["queryStringParameters"]["name"] + ".bash");
                else :
                    r = list_s3("bin/");
            else :
                r = {};

            return returnResponse("ok", r);
        elif event['httpMethod'] == "DELETE" :
            path = event["path"].rstrip("/");

            if path == "/job" :
                r = get_sqs();
            else :
                r = {};

            return returnResponse("ok", r);
        elif event['httpMethod'] == "OPTIONS" :
            return returnResponse("ok");
        else :
            return returnResponse("MethodNotAllowed");
    else :
        return returnResponse("NoSupport");

