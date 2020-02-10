#! python3

import os, sys, json, subprocess

#
# Config
#
path_to_keys = os.environ.get('AWS_KEY_PATH', '~/ssh/')

#
# Globals
#
DEBUG = False

#
# This could be something clever like reading JSON from Git or PostgreSQL
#
aws_out = subprocess.run('aws ec2 describe-instances --output json'.split(), capture_output=True)

#
# This could be something better
#
class Inst:
  def __init__(self):
    self.name=None
    self.apps=[]
    self.key=None
    self.dns=None
    self.ip =None
    self.env=None
    self.eks=False

  def is_good(self):
    return (not self.eks) and self.name and self.key and (self.dns or self.ip)

  def to_ssh(self):
    key_name = self.key + '.pem'
    key_location = os.path.join(path_to_keys, key_name)
    address = (self.dns or self.ip)
    return f"ssh -i '{key_location}' ubuntu@{address}"

  def to_config(self):
    key_name = self.key + '.pem'
    key_location = os.path.join(path_to_keys, key_name)
    address = (self.dns or self.ip)
    return f"{self.name})) ssh -i '{key_location}' ubuntu@{address} ;;"

  def __str__(self):
    role = self.eks and "EKS" or "ec2"
    return f"[{self.name}:{role}:{self.key}:{self.dns or self.ip}]"

#
# This could be functions
#
by_name = {}

if 0 != aws_out.returncode:
  print("Error! aws subprocess returned code", aws_out.returncode)
  print("Error message:", aws_out.stderr)
  sys.exit(aws_out.returncode)

ec2_json = json.loads( aws_out.stdout )

if not 'Reservations' in ec2_json:
  print("Error! Can't find key 'Reservations' in aws subprocess output.")
  print("Aborting.")
  sys.exit(-1)

ec2s = ec2_json['Reservations']

for ec2 in ec2s:
  insts = ec2['Instances']
  for inst in insts:
    i = Inst()
    #
    for tag in inst['Tags']:
      if 'Name' == tag['Key']:
        i.name = tag['Value']
      if 'Env' == tag['Key']:
        i.env = tag['Value']
      if 'Apps' == tag['Key']:
        i.apps = tag['Value']
      if 'alpha.eksctl.io/nodegroup-type' == tag['Key']:
        i.eks = True
    i.key = inst.get('KeyName')
    i.dns = inst.get('PublicDnsName')
    i.ip  = inst.get('PublicIpAddress')
    #
    if i.is_good():
      by_name[ i.name ] = i
    else:
      if DEBUG:
        print('not good:', i)
#
#
#
if DEBUG: print('by_name:', by_name)

for k,v in by_name.items():
  # change k to something smarter, like 'www.medly.link' -> 'www'
  # turn spaces into _ or something
  print(k, ')', v.to_ssh(), ';;')
