import re
'''
output:
{'Ethernet1/5': {'ip': '192.0.2.1',
  'area': '0.0.0.10',
  'status': 'up',
  'Hello timer': '10',
  'cost': '4'},
 'Ethernet2/5': {'ip': '192.0.2.1',
  'area': '0.0.0.10',
  'status': 'up',
  'Hello timer': '10',
  'cost': '4'}}
'''
def separate_interface_data(ospf_data):
    '''
    this function separates each interface section
    '''
#     ospf_data = f2.read()
    ospf_data = re.split(r'(.+ is up, line protocol is \w)', ospf_data)
    ospf_data.pop(0)
    ospf_list = []
    while True:
        if len(ospf_data) >= 2:
            intf = ospf_data.pop(0)
            section = ospf_data.pop(0)

            # reunify because it was split up in the re.split
            ospf_string = intf + section
            ospf_list.append(ospf_string)

        else:
            break
                
    return ospf_list


def ospf_data(section):
    '''
    This function parses the section using regex
    '''
#     ospf = f.read()
    intf = re.findall(r'Ethernet\d+/\d+', section)[0]
    status = re.findall('Ethernet.* is (up|down),', section)[0]
    protocol_status = re.findall('line.* (up|down)', section)[0]
    interface_ip = re.findall(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', section)[0]
    area = re.findall(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', section)[1]
    hello_timer = re.findall('Hello (\d+)', section)[0]
    dead_timer = re.findall('Dead (\d+)', section)[0]
    cost = re.findall('cost (\d+)', section)[0]
    return intf, status, protocol_status, interface_ip, area, hello_timer, dead_timer, cost

if __name__ == '__main__':
    
    with open('ospf.txt') as f:
        ospf = f.read()
        d = {}
        ospf_sections = separate_interface_data(ospf)
        
        for section in ospf_sections: 
            intf, status, protocol_status, interface_ip, area, hello_timer, dead_timer, cost = ospf_data(section)
            d[intf] = {'ip': interface_ip, 'area': area, 'status': status, 'Hello timer': hello_timer,'cost': cost}