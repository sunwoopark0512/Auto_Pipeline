"""
GPU 사용량 추적 및 비용 최적화 (Spot Instance)
"""

import psutil
import boto3
import os

# EC2 Spot 사용 추적
ec2 = boto3.client('ec2', region_name=os.getenv('AWS_REGION'))

def get_gpu_usage() -> float:
    """현재 GPU 사용량 반환 (예: NVIDIA-SMI)"""
    gpu_data = psutil.sensors_temperatures()
    return gpu_data.get('gpu')

def get_spot_instance_price() -> float:
    """AWS Spot 인스턴스의 현재 가격 추적"""
    response = ec2.describe_instance_type_offerings(
        LocationType='availability-zone',
        Filters=[{'Name': 'instance-type', 'Values': ['p3.2xlarge']}]
    )
    return response.get('SpotPrice')

def optimize_cost():
    gpu_usage = get_gpu_usage()
    spot_price = get_spot_instance_price()
    if gpu_usage and gpu_usage > 80:
        print(f"🔴 높은 GPU 사용량 ({gpu_usage}%) - Spot 인스턴스 종료 및 예약")
    else:
        print(f"🟢 GPU 사용량 정상 ({gpu_usage}%) - Spot 인스턴스 유지 중")

if __name__ == '__main__':
    optimize_cost()
