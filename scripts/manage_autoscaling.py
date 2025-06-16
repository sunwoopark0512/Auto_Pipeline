import os
import logging
from datetime import datetime
import boto3

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def get_env(name, default=None, required=False):
    value = os.getenv(name, default)
    if required and not value:
        logging.error(f"환경 변수 누락: {name}")
        exit(1)
    return value


ASG_NAME = get_env("ASG_NAME", required=True)
AMI_ID = get_env("AMI_ID", required=True)
INSTANCE_TYPE = get_env("INSTANCE_TYPE", required=True)
KEY_NAME = get_env("KEY_NAME", required=True)
SECURITY_GROUPS = [sg.strip() for sg in get_env("SECURITY_GROUPS", "").split(',') if sg.strip()]
SUBNETS = [sn.strip() for sn in get_env("SUBNETS", "").split(',') if sn.strip()]
MIN_SIZE = int(get_env("MIN_SIZE", "1"))
MAX_SIZE = int(get_env("MAX_SIZE", "1"))
DESIRED_CAPACITY = int(get_env("DESIRED_CAPACITY", str(MIN_SIZE)))
LAUNCH_CONFIG_NAME = get_env("LAUNCH_CONFIG_NAME", f"{ASG_NAME}-lc")
IAM_INSTANCE_PROFILE = get_env("IAM_INSTANCE_PROFILE")

asg = boto3.client('autoscaling')


def get_asg():
    resp = asg.describe_auto_scaling_groups(AutoScalingGroupNames=[ASG_NAME])
    groups = resp.get('AutoScalingGroups', [])
    return groups[0] if groups else None


def get_launch_config(name):
    resp = asg.describe_launch_configurations(LaunchConfigurationNames=[name])
    lcs = resp.get('LaunchConfigurations', [])
    return lcs[0] if lcs else None


def launch_config_needs_update(lc):
    if not lc:
        return True
    if lc['ImageId'] != AMI_ID:
        return True
    if lc['InstanceType'] != INSTANCE_TYPE:
        return True
    if lc.get('KeyName') != KEY_NAME:
        return True
    if set(lc.get('SecurityGroups', [])) != set(SECURITY_GROUPS):
        return True
    if IAM_INSTANCE_PROFILE and lc.get('IamInstanceProfile') != IAM_INSTANCE_PROFILE:
        return True
    return False


def create_launch_config(name):
    params = {
        'LaunchConfigurationName': name,
        'ImageId': AMI_ID,
        'InstanceType': INSTANCE_TYPE,
        'KeyName': KEY_NAME,
        'SecurityGroups': SECURITY_GROUPS,
    }
    if IAM_INSTANCE_PROFILE:
        params['IamInstanceProfile'] = IAM_INSTANCE_PROFILE
    asg.create_launch_configuration(**params)
    logging.info(f"런치 구성 생성: {name}")


def create_asg(lc_name):
    asg.create_auto_scaling_group(
        AutoScalingGroupName=ASG_NAME,
        LaunchConfigurationName=lc_name,
        MinSize=MIN_SIZE,
        MaxSize=MAX_SIZE,
        DesiredCapacity=DESIRED_CAPACITY,
        VPCZoneIdentifier=','.join(SUBNETS)
    )
    logging.info(f"ASG 생성 완료: {ASG_NAME}")


def update_asg(lc_name=None):
    params = {'AutoScalingGroupName': ASG_NAME}
    group = get_asg()
    if group is None:
        return
    changed = False
    if group['MinSize'] != MIN_SIZE:
        params['MinSize'] = MIN_SIZE
        changed = True
    if group['MaxSize'] != MAX_SIZE:
        params['MaxSize'] = MAX_SIZE
        changed = True
    if group['DesiredCapacity'] != DESIRED_CAPACITY:
        params['DesiredCapacity'] = DESIRED_CAPACITY
        changed = True
    if lc_name and group.get('LaunchConfigurationName') != lc_name:
        params['LaunchConfigurationName'] = lc_name
        changed = True
    if changed:
        asg.update_auto_scaling_group(**params)
        logging.info("ASG 업데이트 완료")
    else:
        logging.info("ASG 설정 변경 없음")


def main():
    group = get_asg()
    if not group:
        create_launch_config(LAUNCH_CONFIG_NAME)
        create_asg(LAUNCH_CONFIG_NAME)
        return

    lc_name = group.get('LaunchConfigurationName')
    lc = get_launch_config(lc_name) if lc_name else None
    if launch_config_needs_update(lc):
        new_lc_name = f"{LAUNCH_CONFIG_NAME}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        create_launch_config(new_lc_name)
        lc_name = new_lc_name
    update_asg(lc_name)


if __name__ == '__main__':
    main()
