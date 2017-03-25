import logging
import _winreg


class RegistryUtils(object):
  ROOT_KEYS = ['hklm (for HKEY_LOCAL_MACHINE)',
               'hkcr (for HKEY_CLASSES_ROOT)',
               'hkcu (for HKEY_CURRENT_USER)',
               'hku (for HKEY_USERS)',
               'hkpd (for HKEY_PERFORMANCE_DATA)',
               'hkcc (for HKEY_CURRENT_CONFIG)'
               ]

  @staticmethod
  def get_data(rootkey, key, value):
    """This method acts as a wrapper for the internal __get_data method.

    Args:
      root_key (str): The root key as abbreviated string.
                      Valid values: [hklm, hkcr, hkcu, hku, hkpd, hkcc].
      key (str): The subkey starting from the root key.
              e.g.: SYSTEM\CurrentControlSet\Services\Tcpip\Parameters
      value (str): The value to query.
              e.g.: DhcpNameServer

    Returns:
      str. It returns the retrieved data if the value is correct,
          or an empty string otherwise.
    """
    rks = [rk.split()[0] for rk in RegistryUtils.ROOT_KEYS]
    if rootkey == rks[0]:
      return RegistryUtils.__get_data(_winreg.HKEY_LOCAL_MACHINE, key, value)
    elif rootkey == rks[1]:
      return RegistryUtils.__get_data(_winreg.HKEY_CLASSES_ROOT, key, value)
    elif rootkey == rks[2]:
      return RegistryUtils.__get_data(_winreg.HKEY_CURRENT_USER, key, value)
    elif rootkey == rks[3]:
      return RegistryUtils.__get_data(_winreg.HKEY_USERS, key, value)
    elif rootkey == rks[4]:
      return RegistryUtils.__get_data(_winreg.HKEY_PERFORMANCE_DATA, key, value)
    elif rootkey == rks[5]:
      return RegistryUtils.__get_data(_winreg.HKEY_CURRENT_CONFIG, key, value)
    else:
      logging.error('Incorrect registry root key value: {0}. Valid values: {1}'.format(rootkey, RegistryUtils.ROOT_KEYS))
    return ''

  @staticmethod
  def get_key_values(rootkey, key):
    """This method acts as a wrapper for the internal __get_key_values method.

    Args:
      root_key (str): The root key as abbreviated string.
                      Valid values: [hklm, hkcr, hkcu, hku, hkpd, hkcc].
      key (str): The subkey starting from the root key.
              e.g.: SYSTEM\CurrentControlSet\Services\Tcpip\Parameters

    Returns:
      list. It returns the retrieved values and subkeys
      or an empty list if data could not be retrieved.
    """
    rks = [rk.split()[0] for rk in RegistryUtils.ROOT_KEYS]
    if rootkey == rks[0]:
      return RegistryUtils.__get_key_values(_winreg.HKEY_LOCAL_MACHINE, key)
    elif rootkey == rks[1]:
      return RegistryUtils.__get_key_values(_winreg.HKEY_CLASSES_ROOT, key)
    elif rootkey == rks[2]:
      return RegistryUtils.__get_key_values(_winreg.HKEY_CURRENT_USER, key)
    elif rootkey == rks[3]:
      return RegistryUtils.__get_key_values(_winreg.HKEY_USERS, key)
    elif rootkey == rks[4]:
      return RegistryUtils.__get_key_values(_winreg.HKEY_PERFORMANCE_DATA, key)
    elif rootkey == rks[5]:
      return RegistryUtils.__get_key_values(_winreg.HKEY_CURRENT_CONFIG, key)
    else:
      logging.error('Incorrect registry root key value: {0}. Valid values: {1}'.format(rootkey, RegistryUtils.ROOT_KEYS))
    return []

  @staticmethod
  def __get_data(root_key, key, value):
    """This method gets the data from the given key and value under the root
    key.

    Args:
      root_key (str): The root key as abbreviated string.
                      Valid values: [hklm, hkcr, hkcu, hku, hkpd, hkcc].
      key (str): The subkey starting from the root key.
              e.g.: SYSTEM\CurrentControlSet\Services\Tcpip\Parameters
      value (str): The value to query.

    Returns:
      Str. It returns the retrieved data, or an empty string if data could not be retrieved.
    """
    data = ''
    try:
      hkey = _winreg.OpenKey(root_key, key, 0, _winreg.KEY_READ)
      data, regtype = _winreg.QueryValueEx(hkey, value)
      _winreg.CloseKey(hkey)
    except WindowsError as e:
      logging.error('Error occurred getting registry data: {0}'.format(e))
    return data

  @staticmethod
  def __get_key_values(root_key, key):
    """This method gets the values and subkeys from the given key under the
    root key.

    Args:
      root_key (str): The root key as abbreviated string.
                      Valid values: [hklm, hkcr, hkcu, hku, hkpd, hkcc].
      key (str): The subkey starting from the root key.
              e.g.: SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\interfaces
    Returns:
      list. It returns the retrieved values and subkeys
      or an empty list if data could not be retrieved.
    """
    values = []
    i = 0
    try:
      hkey = _winreg.OpenKey(root_key, key, 0, _winreg.KEY_READ)
    except WindowsError as e:
      logging.error('Key ({0}) could not be opened: {1}'.format(key, e))
      return values

    while True:
      try:
        value = _winreg.EnumKey(hkey, i)
        values.append(value)
        i += 1
      except WindowsError:
        logging.info('No more values. Total values: {0}'.format(i))
        if hkey:
            _winreg.CloseKey(hkey)
        break  # no more values
    return values
