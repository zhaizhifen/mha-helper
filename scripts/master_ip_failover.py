#!/usr/bin/python

import sys
from optparse import OptionParser
from lib.mha_ip_failover_helper import MHA_IP_failover_helper

# Current master shutdown phase
# /usr/local/mha-helper/scripts/master_ip_failover.py
# --orig_master_host=master1 --orig_master_ip=10.100.23.10
# --orig_master_port=3306 --command=stopssh --ssh_user=root
# --ssh_options='-o ServerAliveInterval=60 -o ServerAliveCountMax=20 -o StrictHostKeyChecking=no -o ConnectionAttempts=5 -o PasswordAuthentication=no -i /root/.ssh/id_rsa'


# parse comand line arguments
parser = OptionParser()
parser.add_option('--command', type='string')
parser.add_option('--orig_master_host', type='string')
parser.add_option('--orig_master_ip', type='string')
parser.add_option('--orig_master_port', type='string')
parser.add_option('--new_master_host', type='string')
parser.add_option('--new_master_ip', type='string')
parser.add_option('--new_master_port', type='string')
parser.add_option('--ssh_user', type='string')
parser.add_option('--ssh_options', type='string')

(options, args) = parser.parse_args()

# do the actual work
exit_code = 1

if options.command is None:
    sys.exit(exit_code)

mha_ip_failover_helper = MHA_IP_failover_helper()

if options.command == 'stop' or options.command == 'stopssh':
    if (options.orig_master_ip is not None and
            options.ssh_user is not None and
            options.ssh_options is not None):
        return_val = mha_ip_failover_helper.execute_stop_command(orig_master_ip=options.orig_master_ip,
                                                ssh_user=options.ssh_user, 
                                                ssh_options=options.ssh_options)
        if return_val == True:
            exit_code = 0

elif options.command == 'start':
    if (options.orig_master_ip is not None and 
            options.new_master_ip is not None and
            options.ssh_user is not None and
            options.ssh_options is not None):
        return_val = mha_ip_failover_helper.execute_start_command(orig_master_ip=options.orig_master_ip,
                                                new_master_ip=options.new_master_ip,
                                                ssh_user=options.ssh_user,
                                                ssh_options=options.ssh_options)
        # TODO - tie in with the script here that changes the /etc/hosts file

        if return_val == True:
            exit_code = 0

elif options.command == 'status':
    # We do not need to do anything here
    exit_code = 0

# exit the script with the appropriate code
# if script exits with a 0 status code, MHA continues with the failover
sys.exit(exit_code)
