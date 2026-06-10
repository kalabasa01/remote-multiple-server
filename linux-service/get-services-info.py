from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

def linux_device(hostIP):
    server_config = {
        "device_type": "linux",
        "host": hostIP,
        "username": "admin",
        "password": "mypassword",
        "secret": "mypassword",
        "port": 22,
    }

    try:
        net_connect = ConnectHandler(**server_config)
        net_connect.enable()

        services = ["my-test.service","my-test2.service"]
        for service_name in services:
            is_enabled = net_connect.send_command(
                            f"systemctl is-enabled {service_name} || sudo systemctl enable --now {service_name}",
                            expect_string=r"\[sudo\] password|#|\$",
                        ).strip()
            is_active = net_connect.send_command(
                            f"systemctl is-active {service_name} || sudo systemctl start --now {service_name}",
                            expect_string=r"\[sudo\] password|#|\$",
                        ).strip()

        print(f"Server Host  : {hostIP}")
        print(f"Services     : {services}")
        print(f"Status       : \033[32mactive\033[0m")
        print(f"On-Boot      : \033[32menabled\033[0m\n")

        net_connect.disconnect()

    except NetmikoTimeoutException:
        print(f"Connection Timeout: Could not reach {server_config['host']}.\n")
    except NetmikoAuthenticationException:
        print(f"Authentication Failed: Check username/password for {server_config['host']}.\n")
    except Exception as e:
        print(f"An error occurred while processing {server_config['host']}: {e}\n")

# Execution
print("\n---- Script is running ----\n")
host_addresses = ["0.0.0.0", "1.1.1.1"]
for hostIP in host_addresses:
    linux_device(hostIP)

print("Script execution completed.\n\n")
