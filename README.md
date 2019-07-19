# rf2_check_profiles

* Lost in all the parameters of Multiplayer.json and player.json ? 

* Difficulties to administrate parameters of several rF2 dedicated servers ?

**rf2_check_profiles** is an answer bringing you configuration models to assign to your profiles. You can customize the models and apply to the needed user profiles. It also brings referenced configurations aspect.

**rf2_check_profiles** will check and update (if needed) values of the parameters contained in each models assigned to each user profile (available in Userdata)

# Usage

1. Shutdown the rFactor2 dedicated servers that need to be checked in order to value updates to be effective

2. Launch check_profiles.py script in windows terminal (cmd.exe or powershell)

```
python check_profiles.py
```

Updated parameters are given in the output of the command.

# Requirements

Python needs to be installed (https://www.python.org/downloads/)

# Installation

* You can git clone or download the archive of the last version: https://github.com/knackko/rf2_check_profiles/archive/master.zip

* Unzip in the folder you want

# Configuration
**config.json** contains list of models and the list of user profiles to check vs models.

* Configure rFactor install dir in config part

```
  "config":{
  
    "rf2_install_dir": "C:\\perso\\rf2_dedi",
 ```   
 

# Define models

  # From examples

Models examples are available in examples directory, you can copy those files in models directory.

  # Create new models

You can also define new models by creating models files in models directory:

1. Create model files in models directory, respecting the naming:
  - <model_name>-player.json : if the model contains player.json parameters to check
  - <model_name>-multiplayer.json : if the model contains multiplayer parameters to check

2. Edit models files content:

To edit the content, you can start from one of the examples.

3. Add the model in config.json in models part

```
  "models":{
  
      "<model_name>":{
      
        "files":["<model_name>-multiplayer.json"]
        
        }
 ```       

In the above example, the model have to check only parameters contained in multiplayer file.

Another example from examples dir checking player.json and multiplayer.json file is:

```
  "models":{
  
     "basics":{
     
        "files":["basics-multiplayer.json","basics-player.json"]
        
        }
```

# Assign models to profiles to check

* Add the user profiles to check in check_profiles part
example, for player and champ1 profiles:

```
  "check_profiles":[
  
    {
    
      "profile":"player",
      
      "models":["basics","quali_private"]
      
    },
    
        {
        
      "profile":"champ1",
      
      "models":["basics","quali_public"]
      
    }
    
  ]
```
..
