import re

def parsing_top_output(top_cmd_output):
    top_dict = []
    pid_info_list = [] 
    with open(top_cmd_output) as f:
        data = f.read()
#         print(data)

        patterns = [
        { 'regexp' : re.compile(
                    r'(?P<PID>(\d+))\s+'
                    r'(?P<COMMAND>([\w.]+\s?[\w.]+))\s+'
                    r'(?P<CPU>([0-9]+\.[0-9]+))(\s+\S+){4}\s+'
                    r'(?P<MEMORY>(\w+[-+]?))(\s+\S+){3}\s+'
                    r'(?P<PPID>(\d+))\s+'
                    r'(?P<STATE>(\S+))'
                    r'.*')
            }
        ]


        for line in data.splitlines():
            for item in patterns:
                match = item['regexp'].match(line)
                if match:
                    top_dict.append(match.groupdict())

        for item in top_dict:
            new_dict = { item['PID'] : { 'COMMAND' : item['COMMAND'], 
                                    'CPU' : item['CPU'], 
                                    'MEMORY' : item['MEMORY'], 
                                    'PPID' : item['PPID'],
                                    'STATE' : item['STATE']
                                   }
                                   }

            pid_info_list.append(new_dict)
            
    return pid_info_list


pid_info_list = parsing_top_output('top_command_output.txt')
