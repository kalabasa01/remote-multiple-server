from netmiko import ConnectHandler
import re

def linux_device(hostIP):
    try:
        net_connect = ConnectHandler(
            device_type="linux",
            host=hostIP,
            username="admin",
            password="mypassword",
            secret="mypassword"
        )
        net_connect.enable()

        print(f"\nServer Host: {hostIP}")
        print("FW Info:")

        for public_IP in ["2.2.2.2", "3.3.3.3"]:
            output = net_connect.send_command(
                f"sudo firewall-cmd --list-rich-rules | grep {public_IP}",
                expect_string=r"\[sudo\] password|#|\$"
            )

            matches = re.findall(rf'address="{public_IP}".*?port="([^"]+)".*?protocol="([^"]+)"', output)

            if matches:
                print(f"     Public IP: {public_IP}")
                for i, (port, proto) in enumerate(matches, 1):
                    print(f"     Port and Protocol ({i}): {port}/{proto}")
                print("")

        net_connect.disconnect()
        print("-" * 30)
    except Exception as e:
        print(f"Error on {hostIP}: {e}\n")

# Execution
host_addresses = ["0.0.0.0", "1.1.1.1"]
for hostIP in host_addresses:
    linux_device(hostIP)
