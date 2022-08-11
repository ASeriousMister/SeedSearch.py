# SeedSearch.py
A python tool that scans files in directories and subdirectories hunting BIP39 mnemonic seeds.
It is part of the bigger project Anu₿itux: more info at https://anubitux.org.


## Overview
It allows the user to provide a path and then scans all the files looking for sequencies of words that could be BIP39 mnemonic seeds. Then it checks if the found sequencies are valid mnemonic seeds and prints it in the output.
When seeds are found, the tool asks the user if he wants to derive addresses and check if the seeds have been used.
### Warning
Running issued could be encountered due to APIs limits. To check only a few seeds that could be more valuable, use SeedCheck.py


## Installation
The tool was tested in Ubuntu 20.04 with Python3.8.
I suggest tu run the tool in his own virtual enviroment.
Python shoul be installed by default. If not so, update your repositories
```
sudo apt update
```
and type
```
sudo apt install python3
```
Then install pip, to easily install the dependencies
```
sudo apt install python3-pip
```
Now clone the github repository
```
git clone https://github.com/ASeriousMister/SeedSearch.py
```
and install python virtual enviroments
```
pip3 install virtualenv
```
Now move to SeedCheck.py's directory,
```
cd SeedCheck.py
```
create a virtual enviroment (in the example named scve, but you can choose your preferred name)
```
virtualenv ssve
```
and activate it
```
source ssve/bin/activate
```
The name of the virtual enviroment should appear, in brackets, on the left of your command line. 
Now you can install the dependencies
```
pip3 install -r requirements.txt
```
Finally, you are ready to run the tool
```
python3 seedsearch.py -d /directory/to/scan
```
Sometimes pip may not install the packages listed in requirements.txt in the proper way.
In this case, just install the missing package shown in the error message with
```
pip3 install {missing_package_name}
```


## Supported derivations
The tool supports the following coins with the indicated derivation paths:
### Bitcoin
- BIP39
  * m/44'/0'/0'/0
  * m/44'/0'/0'/0' (hardened addresses)
  * m/49'/0'/0'/0
  * m/49'/0'/0'/0' (hardened addresses)
  * m/84'/0'/0'/0
  * m/84'/0'/0'/0' (hardened addresses)
  * m/84'/00/2147483645'/0'/0 (Samourai wallet Premix)
  * m/84'/00/2147483646'/0'/0 (Samourai wallet Postmix)
### Ethereum
- BIP39
  * m/44'/60'/0'/0
  * m/44'/60'/0'/0' (hardened addresses)
### Litecoin
- BIP39
  * m/44'/2'/0'/0
  * m/44'/2'/0'/0' (hardened addresses)
  * m/49'/2'/0'/0
  * m/49'/2'/0'/0' (hardened addresses)
  * m/84'/2'/0'/0
  * m/84'/2'/0'/0' (hardened addresses)
### Dash
- BIP39
  * m/44'/5'/0'/0
  * m/44'/5'/0'/0' (hardened addresses)
### ZCash
- BIP39
  * m/44'/133'/0'/0
  * m/44'/133'/0'/0' (hardened addresses)


## Read more
- [BIPs](https://github.com/bitcoin/bips)
- [HD wallet](https://pypi.org/project/hdwallet/)

### Troubleshooting
The tool may encounter some issues running with Ubuntu 22.04, due to incompatibility with ripemd160 hashes used by the hdwallet library.
To solve this you need to edit the /etc/ssl/openssl.cnf file, making sure that it contains all the following lines:
```
openssl_conf = openssl_init

[openssl_init]
providers = provider_sect

[provider_sect]
default = default_sect
legacy = legacy_sect

[default_sect]
activate = 1

[legacy_sect]
activate = 1
```

## Disclaimer
SeedSearch.py aims to find seeds stored in files. Its cearch has not to be considered exhaustive, because mnemonic seeds can be easily hidden placed other words between the ones composing the mnemonic, scrambling letters, etc.

## Credits & Donations
If you appreciate this work visit https://anubitux.org and consider making a donation
- BTC: 1AnUbiYpuFsGrc1JFxFCh5K9tXFd1BXPg
- XMR: 87PTU58siKNb3WWXcP4Hq4CmCb7kMQUsEiUWFT7SvvMMUqVw9XXFGrJZqmnGvuJLGtLoRuEqovTG4SWqkPr8YLopTSxZkkL
