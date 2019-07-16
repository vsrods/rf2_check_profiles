import json
import os

# Load config file in object
with open("config.json", "r") as jsonFile:
  config = json.load(jsonFile)

models_dir=config['config']['models_dir']
#up = '{"Multiplayer Server Options":{"Admin Functionality":2,"Admin Password":"YES"}}'
#x = json.loads(up)
#with open("Multiplayer_model.JSON", "r") as jsonFile:
#    modeldata = json.load(jsonFile)

# For each check to be done
for check_profile in config['check_profiles']:
  # path to files of the profile to update
  profile_multiplayer=config['config']['rf2_install_dir'] + "\\UserData\\" + check_profile['profile'] + "\\Multiplayer.JSON"
  profile_player=config['config']['rf2_install_dir'] + "\\Userdata\\" + check_profile['profile'] + "\\" + check_profile['profile'] + ".JSON"

  for model_to_check in check_profile['models']:
    for model_file in config['models'][model_to_check]['files']:
      (model_prefix,model_type) = str.split(str(model_file),'-')

      with open(models_dir + model_file, 'r') as jsonFile:
          modeldata = json.load(jsonFile)
      
      if model_type == 'player.json':
        with open(profile_player, 'r') as jsonFile:
          data = json.load(jsonFile)
          loaded_file = profile_player

      elif model_type == 'multiplayer.json':
        with open(profile_multiplayer, 'r') as jsonFile:
          data = json.load(jsonFile)
          loaded_file = profile_multiplayer

      for model_key_first, model_value_first in modeldata.items():
        if isinstance(model_value_first, dict):
          for model_key_sub, model_value_sub in model_value_first.items():
            #print (model_file,model_key_first,model_key_sub,model_value_sub)
            for data_key_first, data_value_first in data.items():
              if isinstance(data_value_first, dict):
                for data_key_sub, data_value_sub in data_value_first.items():
                  if model_key_first == data_key_first and model_key_sub == data_key_sub and model_value_sub != data_value_sub:
                    data[data_key_first][data_key_sub]=model_value_sub
                    print ("updated:"+data_key_first+"/"+data_key_sub+"/ from: "+str(data_value_sub)+" to: "+str(model_value_sub))
              else:
                print ("not a dict:"+data_key_first+"/"+data_key_sub)
        else:
          print ("not a dict:"+data_key_first)

      with open(loaded_file, "w") as jsonFile:
        json.dump(data, jsonFile, sort_keys=True,indent=2, separators=(',', ':'))
