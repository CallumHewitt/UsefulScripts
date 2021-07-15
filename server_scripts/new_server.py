from server_util import *
import yaml

def setup_server():
    config = get_config()
    commands = []

    # Setup sudo user
    sudo_user_config = config[SUDO_USER_FIELD]
    commands += sudo_user_commands(sudo_user_config[USERNAME_FIELD], sudo_user_config[PASSWORD_FIELD])

    # Configure firewall
    ufw_config = config[UFW_FIELD]
    commands += ufw_default_commands(ufw_config[INCOMING_UFW_FIELD], ufw_config[OUTGOING_UFW_FIELD])

    # Update packages
    commands += packages_update_commands()

    # Install starters
    starters = config.get(STARTERS_FIELD)
    if (starters != None):
        for start_commands in list(map(lambda name: starter_commands(name, config), starters)):
            commands += start_commands

    # Reboot command
    commands.append('reboot -f > /dev/null 2>&1 &')

    # Run commands
    ssh_config = config[SSH_FIELD]
    run_commands(commands, config[HOSTNAME_FIELD], ssh_config[KEY_LOCATION_FIELD], ssh_config[KEY_PASSPHRASE_FIELD])

def get_config():
    with open("config.yml", "r") as stream:
        return yaml.safe_load(stream)

if __name__ == '__main__':
    setup_server()