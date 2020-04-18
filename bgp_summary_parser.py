'''
This code parses the bgp summary output and 
outpus bgp_info and neighbors_dict
'''
import re
ip_addr = r'\b\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\b' 
ASN_REGEX = r'\d+'
neighbors_dict = []
bgp_info = []
with open('bgp_summary.txt') as f:
    bgp_data = f.read()
    router_id = re.search('BGP router identifier (?P<router_id>{})'.format(ip_addr), bgp_data)
    bgp_info.append(router_id.groupdict())
    local_as = re.search('local AS number (?P<local_as>\d+)', bgp_data)
    bgp_info.append(local_as.groupdict())
    patterns = [
        {'regexp' : re.compile(
                        r"(?P<remote_addr>{})"
                        r"\s+\d+\s+(?P<remote_as>{})(\s+\S+){{5}}\s+"
                        r"(?P<uptime>(never)|\d+\S+)"
                        r"\s+(?P<accepted_prefixes>\d+)".format(ip_addr, ASN_REGEX))},
        {'regexp' : re.compile(
                        r"(?P<remote_addr>({}))"
                        r"\s+\d+\s+(?P<remote_as>{})(\s+\S+){{5}}\s+"
                        r"(?P<uptime>(never)|\d+\S+)\s+(?P<state>\D.*)".format(ip_addr, ASN_REGEX))}
        
    ]
    
    for line in bgp_data.splitlines():
        for item in patterns:
            match = item['regexp'].match(line)
            if match:
                neighbors_dict.append(match.groupdict())

            
    print(bgp_info)
    print(neighbors_dict)