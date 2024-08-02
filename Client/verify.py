import re
# r = re.compile(r"^\d*[.,]?\d*$")
# r = re.compile(r'\d{4}:(B|S):(\w{3}/\w{3}):\d{4}:^\d*[.,]?\d*$:(SPOT|FWD):(Y|N)')
# r = re.compile(r'\w* \w* \w* \d{4}:(B|S):(\w{3}/\w{3}):(\d*):\d*[.,]?\d*:(SPOT|FWD):(Y|N)')
r = re.compile(r'amend trade \d{7} with rate \d*[.,]?\d*')
if r.match('amend trade 1234567 with rate 1.008'): 
    print ('it matches')
else:
    print('Wrong')

# if r.match('1111'): 
#     print ('it matches')
# else:
#     print('Wrong')

# if r.match('0.abc'): 
#     print ('it matches 0.abc ')
 
# if r.match('0.123'): 
#     print ('it matches 0.123')