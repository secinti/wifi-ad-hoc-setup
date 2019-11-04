!/usr/bin/env python
import socket
import time
import subprocess
import logging
import os
import config


def configure_logger():
    logging.basicConfig(format='%(levelname)s:%(asctime)s::\n%(message)s',
                        # Python v3
                        # handlers=[
                        #    logging.FileHandler("{}.log".format("edimaxConf")),
                        #    logging.StreamHandler()
                        # ],
                        # Python v2
                        filename="{}.log".format("networkConfigurationLog"),  # Use of this attribute removes stdout
                        level=logging.NOTSET
                        )
    # Python v2
    logging.getLogger().addHandler(logging.StreamHandler())


def reinstall_batman_module():
    reinstall_module('batman-adv')


def reinstall_module(module_name):
    try:
        logging.info('Removing the module: {}'.format(module_name))
        subprocess.Popen(['sudo', 'rmmod', module_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
    except OSError as e:
        logging.error("Cannot remove driver module".format(e))

    try:
        logging.info('Installing the module: {}'.format(module_name))
        subprocess.Popen(['sudo', 'modprobe', module_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
    except OSError as e:
        logging.error("Cannot install driver module".format(e))
        return None


def check_and_reset_batman(interface_name):
    logging.info('Detecting batman compatibility of the interface:{}'.format(interface_name))
    if os.path.isdir("/sys/class/net/{}/batman_adv".format(interface_name)) is True:
        logging.info('The interface is already compatible')
    else:
        logging.info('The interface is NOT compatible')
        logging.info('Reinstalling batman module')
        reinstall_batman_module()


def configure_wifi_interface(configuration_options):

    co = configuration_options

    i_type = co.get(type)

    if i_type != 'BATMAN' and i_type != 'ad-hoc':
        raise ValueError("Unexpected interface configuration mode given !")
        return

    if i_type == 'BATMAN':
        check_and_reset_batman(co.get('device_name'))

    """Common configuration lines for both ad-hoc and batman"""
    script = [
        "sudo ifconfig %s down" % co.get('device_name'),
        "sudo ip addr flush dev %s" %co.get('device_name'),
        "sudo iw dev %s set type ibss" % co.get('device_name'),
        "sudo rfkill unblock all",
        "sudo ifconfig %s up" % co.get('device_name'),
        "sudo iw dev %s ibss join %s %s HT20 fixed-freq %s" %
        (co.get('device_name'), co.get('SSID'), co.get('Channel_Freq'), co.get('Cell_ID'))
    ]

    if co.get('type') == 'BATMAN':
        script.extend([
            "sudo ip link set mtu 1532 dev %s" % co.get('device_name'),
            "sudo batctl if add %s" % co.get('device_name'),
            "sudo ifconfig bat0 %s/24" % co.get('IP'),
            "sudo ifconfig bat0 up"
        ])
    else:
        script.extend([
            "sudo ip link set mtu 1500 dev %s" % co.get('device_name'),
            "sudo ifconfig %s %s/24" % (co.get('device_name'), co.get('IP')),
            ])

    for line in script:
        try:
            logging.info('Running: {}'.format(line))
            subprocess.Popen(line.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
        except OSError as e:
            logging.error("Cannot run the last line: {} ".format(e))


def main():
    configure_logger()

    logging.info("%d interfaces are defined" % len(config.interfaces))

    try:
        for interface in config.interfaces:
            configure_wifi_interface(interface)
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    main()
