#!/usr/bin/env python
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


""" The following method is not required for this demo. """
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



def configure_wifi_interface(configuration_options):
    co = configuration_options

    """ Only work for ad-hoc network mode """
    if co.get('type') == 'ad-hoc':
        script = [
            "sudo ifconfig %s down" % co.get('device_name'),
            "sudo ip addr flush dev %s" %co.get('device_name'),
            "sudo iw dev %s set type ibss" % co.get('device_name'),
            "sudo rfkill unblock all",
            "sudo ifconfig %s up" % co.get('device_name'),
            "sudo iw dev %s ibss join %s %s HT20 fixed-freq %s" %
            (co.get('device_name'), co.get('SSID'), co.get('Channel_Freq'), co.get('Cell_ID'))
        ]

        """ Setup MTU size and IP configuration """
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
    else:
        # logging.error("Unexpected interface configuration mode given !")
        raise ValueError("Unexpected interface configuration mode given !")


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
