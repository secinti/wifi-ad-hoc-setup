## Configuration parameters for the device
#

""" Fill out the following """
node = "name_of_network_node"

interfaces = [
    {
        "device_name": "wlx000f55a91b12",
        "type": "ad-hoc",
        "IP": "10.10.1.14",
        "Cell_ID": "02:12:34:56:78:9D",
        "SSID": "ISE-19",
        "Channel_Freq": "2437",
        "Channel_Num": "6",
        # not used - for the cases require overwriting MAC address
        "MAC_Address": "74:da:38:68:73:5f"
    },
    # setup-adhoc-link python module cannot handle the following mode,
    # it will raise an exception.
    {
        "device_name": "wlx000e8e878226",
        "type": "BATMAN",
        "IP": "10.10.0.14",
        "Cell_ID": "02:12:34:56:78:9C",
        "SSID": "CTLnetwork",
        "Channel_Freq": "2412",
        "Channel_Num": "1",

        # not used
        "BATMAN_MAC" : "",
        "MAC_Address": "00:0e:8e:87:82:26"
    }
]
