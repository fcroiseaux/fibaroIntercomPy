# fibaroIntercomDoorPy

# Opening Fibaro Intercom managed portal door with Homeassistant

## Pyscript installation
This script needs to be used through the Homeassistant Pyscript integration. 
This script generates a service usable with `pyscript.open_portal`
More information here : https://hacs-pyscript.readthedocs.io/en/stable/index.html

## Usage
To use the script, copy the file `open_door.py` into `config/pyscript`
Create a file named intercom.ini in config directory with the following format.

````
[INTERCOM]
intercom_addr = xxx.yyy.zzz.ttt
user = intercomuseraddress
password = intercomuserpassword
````

