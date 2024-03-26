from LogDump import LogDump
from LogEntry import LogEntry

dump = LogDump("logs")

def pretty_print_dump(dump: LogDump):
    # Code here ...
    pass

pretty_print_dump(dump)
# pretty_print_dump(...) should print this to stdout:
# The spaces are important!
"""
conv1          
  conv1_f_var  
    FlexConv1_f
  conv1_b_var  
    FlexConv1_b

conv2          
  conv2_f_var  
    FlexConv2_f
  conv2_b_var  
    FlexConv2_b

dense1         
  dense1_w_var 
    FlexDense1_
  dense1_b_var 
    FlexDense1_
"""

