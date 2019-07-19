import json
import os
import logging
from logging.handlers import RotatingFileHandler
from logging import handlers

# Load config file in object
with open("config.json", "r") as jsonFile:
  config = json.load(jsonFile)

# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s %(message)s')

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

# create console handler and set level to debug
fh = handlers.RotatingFileHandler(config['config']['log_dir']+"checks.log", maxBytes=(1048576*5), backupCount=7)
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)

models_dir=config['config']['models_dir']

# For each check to be done
for check_profile in config['check_profiles']:
  # path to files of the profile to update
  profile_multiplayer=config['config']['rf2_install_dir'] + "\\UserData\\" + check_profile['profile'] + "\\Multiplayer.JSON"
  profile_player=config['config']['rf2_install_dir'] + "\\Userdata\\" + check_profile['profile'] + "\\" + check_profile['profile'] + ".JSON"

  logger.info ("< Begin   profile: "+check_profile['profile'])

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

      logger.info ("- Check   profile: "+check_profile['profile']+", filetype: "+model_type+", model: "+model_to_check)

      for model_key_first, model_value_first in modeldata.items():
        if isinstance(model_value_first, dict):
          for model_key_sub, model_value_sub in model_value_first.items():
            #print (model_file,model_key_first,model_key_sub,model_value_sub)
            for data_key_first, data_value_first in data.items():
              if isinstance(data_value_first, dict):
                for data_key_sub, data_value_sub in data_value_first.items():
                  if model_key_first == data_key_first and model_key_sub == data_key_sub and model_value_sub != data_value_sub:
                    data[data_key_first][data_key_sub]=model_value_sub
                    logger.info ("x Updated profile: "+check_profile['profile']+", filetype: "+model_type+", parameter: "+data_key_first+"/"+data_key_sub+", value from: "+str(data_value_sub)+" to: "+str(model_value_sub))
                  elif model_key_first == data_key_first and model_key_sub == data_key_sub and model_value_sub == data_value_sub:
                    logger.debug ("No change profile: "+check_profile['profile']+", filetype: "+model_type+", parameter: "+data_key_first+"/"+data_key_sub+", value from: "+str(data_value_sub)+" to: "+str(model_value_sub))
              else:
                logger.error (check_profile['profile']+": not a dict:"+data_key_first+"/"+data_key_sub)
        else:
          logger.error (check_profile['profile']+" not a dict:"+data_key_first)

      with open(loaded_file, "w") as jsonFile:
        json.dump(data, jsonFile, sort_keys=True,indent=2, separators=(',', ':'))

      #logger.info (">>> Checked profile: "+check_profile['profile']+", filetype: "+model_type)
  logger.info ("> End     profile: "+check_profile['profile'])