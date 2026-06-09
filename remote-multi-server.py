from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

def linux_device(hostIP):
    try:
        linux_server = {
            'device_type': "linux",
            'host': hostIP,
            'username': "username",
            'password': "password",
            'port': 22
        }

        # Open connection and send command
        open_connection = ConnectHandler(**linux_server)
        output = open_connection.send_command('echo "Service: sshd.service" &&  echo "On-boot: $(systemctl is-enabled sshd.service)" && echo "Status: $(systemctl is-active sshd.service)"')

        # Disconnect cleanly when done
        open_connection.disconnect()

        if output:
            print(output)
            print(f"Server IP: {hostIP}")
        else:
            print(f"Connection to {hostIP} succeeded, but no output was received.")

    # Specific exceptions must come first
    except NetmikoTimeoutException:
        print(f"\n[Error] Connection timed out on {hostIP}. Check the IP address and network connectivity.")
    except NetmikoAuthenticationException:
        print(f"\n[Error] Authentication failed on {hostIP}. Please check your username and password.")
    # Generic exception acting as a safety net at the end
    except Exception as e:
        print(f"\n[Error] An unexpected error occurred on {hostIP}: {e}")

print("--- Start of the Script ---")
# Host Addresses
addresses = ['127.0.0.1']

for ipv4 in addresses:
    linux_device(ipv4)

print("\n--- End of the Script ---")
