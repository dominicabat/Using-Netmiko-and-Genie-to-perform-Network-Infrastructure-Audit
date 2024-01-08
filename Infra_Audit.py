from netmiko import *
import pprint

#edit updated_ver depending on audit requirements

updated_ver = '15.5(2)T'



#indicate devices in device_list.txt, show commands in sh_commands.txt
#this opens the files, reads, then turn them into a list.

with open('device_list.txt') as device_list:
	hosts = device_list.read().splitlines()

with open('sh_commands.txt', "r") as sh_cmd_list:
	sh_app_commands = sh_cmd_list.read().splitlines()

#iterating each host
#connect_param are the common parameters to be used by Netmiko, ConnectHandler to access the devices.

for host in hosts:
	try:
		connect_param = {
			'device_type': 'cisco_ios',
			'host': host,
			'port': 22,
			'username': 'cisco',
			'password': 'cisco123',
			'secret': 'cisco'
			}

		print(f"================={host}=================\n")

		#at the current device in iteration, the list of commands are iterated.
		#connect_param as argument to ConnectHandler
		#session_conn.enable() to go to privilege mode, secret is used. 

		for sh_app_command in sh_app_commands:
			session_conn = ConnectHandler(**connect_param)
			session_conn.enable()
			out = session_conn.send_command(sh_app_command, use_genie=True)
			#conditional, will perform a code block depending on what command in 'sh_app_command' is currently on the for loop iteration
			#print(out)
			if sh_app_command == 'show version':
				print(f"{out['version']['hostname']} IOS version is: {out['version']['version']}")
				print(f"Image ID is: {out['version']['image_id']}")
				if out['version']['version'] == updated_ver:
					print(f"{out['version']['hostname']} is currently running updated version {updated_ver}\n")
				else:
					print(f"Device version {out['version']['version']} outdated. Please update device version to {updated_ver}")
			elif sh_app_command == 'show interfaces':
				print("Router Interface Status:")
				for interface, info in out.items():
					if info['enabled'] == True:
						print(f"{interface}:  enabled")
					else:
						print(f"{interface}:  shutdown")

		print(f"\n===============================================\n\n\n")

	except (NetMikoTimeoutException, NetMikoAuthenticationException) as error:
		print(f"{error}\n")
