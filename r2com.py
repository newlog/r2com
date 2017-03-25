import r2pipe
import json
import sys
import os


class R2COM(object):

    def __init__(self, binary):
        if binary:
          self.r2 = r2pipe.open(binary)
        else:
          self.r2 = r2pipe.open()

    def execute(self):
        success = False
        binary_clsid_info = self.get_cocreateinstance_clsids()  # format: {u'0x401022': {'clsid_addr': 4202584, 'clsid': '{01df0200-0000-0000-c000-000000000046}'}}
        if binary_clsid_info:
            clsid_data = self.read_win_clsid_db()
            success = self.set_clsid_comments(binary_clsid_info, clsid_data)
        return success

    def get_cocreateinstance_clsids(self):
        binary_clsid_info = {}
        cocreateinstance_offset = self.get_cocreateinstance_addr()
        if cocreateinstance_offset:
            call_offsets = self.get_cocreateinstance_xrefs(cocreateinstance_offset)
            if call_offsets:
                binary_clsid_info = self.get_clsids(call_offsets)
            else:
                print('CoCreateInstance function is imported in the binary but seems that has not been used')
        else:
            print('CoCreateInstance function is not used in the binary, its usage is ofuscated or a problem happened while finding function')
        return binary_clsid_info

    def get_cocreateinstance_addr(self):
        binary_imports = json.loads(self.r2.cmd("iij"))
        for binary_import in binary_imports:
            if binary_import.get('name', '') == 'ole32.dll_CoCreateInstance':
                return binary_import.get('plt', None)
        return None

    def get_cocreateinstance_xrefs(self, cocreateinstance_addr):
        self.r2.cmd('aa')
        call_offsets = []
        for xref in json.loads(self.r2.cmd('axtj {}'.format(cocreateinstance_addr))):
            if xref.get('type', '') == 'C':
                call_offset = xref.get('from', 0)
                if call_offset and not call_offset in call_offsets:
                    call_offsets.append(call_offset)
        return call_offsets

    def get_clsids(self, call_addrs):
        addrs_and_guids = {}
        for call_addr in call_addrs:
            push_addr, clsid_addr = self.get_clsid_addresses_from_call_addr(call_addr)
            if clsid_addr:
                clsid_value = self.get_clsid_value_from_clsid_addr(clsid_addr)
                if clsid_value:
                    addrs_and_guids[push_addr] = {'clsid_addr': clsid_addr, 'clsid': clsid_value}
                else:
                    print('Error: Cannot obtain CLSID value for CLSID address {} from call address {}'.format(clsid_addr, call_addr))
            else:
                print('Error: Cannot obtain CLSID address from call address {}'.format(call_addr))
        return addrs_and_guids

    def get_clsid_addresses_from_call_addr(self, call_addr):
        push_inst = self.get_previous_push_inst(call_addr)
        push_addr, clsid_addr = self.get_push_info(push_inst)
        return push_addr, clsid_addr

    def get_previous_push_inst(self, addr, max_backward_opcodes=10):
        push_inst = None
        for counter in range(max_backward_opcodes):
            instructions = json.loads(self.r2.cmd('pij 1 @ {} - {}'.format(addr, counter)))
            if instructions:
                if instructions[0] and 'push ' in instructions[0].get('opcode'):
                    push_inst = instructions[0]
                    break
        if not push_inst:
            print('Error: "push" instruction could not be found before call to CoCreate. Something is wrong')
        return push_inst

    @classmethod
    def get_push_info(cls, push_instruction):
        push_addr, pushed_addr = None, None
        if push_instruction and push_instruction.get('opcode'):
          push_opcode = push_instruction.get('opcode')
          pushed_addr = cls.get_hex_value_from_string(push_opcode.split('push ')[1])
          push_addr = push_instruction.get('offset')
        return push_addr, pushed_addr

    def get_clsid_value_from_clsid_addr(self, clsid_addr):
        clsid = None
        clsid_raw = self.r2.cmd('p8 16 @ {}'.format(clsid_addr)).strip()
        if len(clsid_raw) == 32:
            clsid_first_chunk = self.convert_hex_str_to_little_endian(clsid_raw[0:8])
            if clsid_first_chunk:
              clsid = '{' + '{}-{}-{}-{}-{}'.format(clsid_first_chunk, clsid_raw[8:12], clsid_raw[12:16], clsid_raw[16:20], clsid_raw[20:]) + '}'
        else:
            print('Error: expecting 32 characters after reading CLSID address {}, but {} characters found'.format(clsid_addr, len(clsid_raw)))
        return clsid

    @staticmethod
    def convert_hex_str_to_little_endian(hex_str):
      res = None
      try:
        res = hex_str.decode('hex')[::-1].encode('hex')
      except Exception as e:
        print('Hexadecimal string could not be transformend to little endian. CLSID will not be retrieved. Error: {}'.format(e))
      return res

    @staticmethod
    def get_hex_value_from_string(addr_string):
        value = None
        try:
            value = int(addr_string, 16)
        except ValueError:
            print('Error: cannot convert {} to int'.format(addr_string))
        return value

    @staticmethod
    def read_win_clsid_db():
        clsid_data = ''
        clsids_db_filename = os.path.join(os.path.dirname(__file__), 'clsids.json')
        try:
            with open(clsids_db_filename, 'rb') as fd:
                contents = fd.read()
                clsid_data = json.loads(contents)
        except IOError as e:
            print('Windows CLSID DB data could not be read. Does the clsids.json file exist? Error: {}'.format(e))
        return clsid_data

    def set_clsid_comments(self, binary_clsid_info, clsid_db):
        success = False
        for push_addr, clsid_info in binary_clsid_info.items():
            clsid_desc = self.find_clsid_desc(clsid_info['clsid'], clsid_db)
            if clsid_desc:
                success = True
                self.r2.cmd('CC {} @ {}'.format('COM CLSID ' + clsid_desc, push_addr))
                print('CLSID parameter at 0x{:02x}: {}'.format(push_addr, clsid_desc))
        return success

    @staticmethod
    def find_clsid_desc(clsid_value, clsid_db):
        clsid_desc = clsid_db.get(clsid_value.upper(), '') or clsid_db.get(clsid_value.lower(), '')
        if not clsid_desc:
            print('CLSID "{}" was not found in Windows CLSID DB'.format(clsid_value))
        return clsid_desc


if __name__ == "__main__":
    binary = sys.argv[1] if len(sys.argv) == 2 else None
    r2com = R2COM(binary)
    r2com.execute()
