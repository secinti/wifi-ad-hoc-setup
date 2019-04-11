## Ad-hoc Setup Python script

Clone the github project.

`git clone  https://github.com/secinti/wifi-ad-hoc-setup`

`cd wifi-ad-hoc-setup`

#### ToDo List

1. Get your wifi interface name. Run the following command in bash shell.

`iwconfig`

Example Output:


>>      enp3s0    no wireless extensions.
>>      wlx000f55a91b12  IEEE 802.11  ESSID:off/any  
>>           Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm   
>>           Retry short  long limit:2   RTS thr:off   Fragment thr:off
>>           Power Management:off
>>       lo        no wireless extensions.


2. Update the related line in **config.py** file.

  @line 9 `"device_name": "wlx000f55a91b12",`

  - 2a. Also, change the IP value to avoid conflicts during the experiment.

      @line 11 `"IP": "10.10.1.14",`

3. Run the script.

`python setup-adhoc-link.py`


4. Check the configuration.

`iwconfig`


Example Output:



>>     enp3s0    no wireless extensions.
>>     wlx000f55a91b12  IEEE 802.11  ESSID:"ISE-19"  
>>           Mode:Ad-Hoc  Frequency:2.437 GHz  Cell: 02:12:34:56:78:9D   
>>           Tx-Power=20 dBm   
>>           Retry short  long limit:2   RTS thr:off   Fragment thr:off
>>           Power Management:off  
>>     lo        no wireless extensions.


P.S.:  After the experiment, you should restart the network manager.

`sudo service network-manager start`
