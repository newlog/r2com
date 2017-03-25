from utils.registry_utils import RegistryUtils
import json

clsids_reg_keys = {
  r'hklm': 'SOFTWARE\Classes\CLSID',
  r'hkcu': 'SOFTWARE\Classes\CLSID'
}


def run():
  results = {}
  clsids = {}
  ru = RegistryUtils()
  for key, value in clsids_reg_keys.iteritems():
    clsids[key] = ru.get_key_values(key, value)
    for clsid in clsids[key]:
      default_clsid_value = ru.get_data(key, '{}\\{}'.format(clsids_reg_keys[key], clsid), '')
      results[clsid] =  '{}: {}'.format(clsid, default_clsid_value or 'No value')
  write_json_file(results)


def write_json_file(clsid_info):
  with open('clsids.json', "wb") as json_file:
    json.dump(clsid_info, json_file, indent=4)


if __name__ == '__main__':
  run()