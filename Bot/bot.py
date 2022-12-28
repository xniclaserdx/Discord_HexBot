import os
import interactions

def _get_extensions():
    yield 'basiscalc'
    yield 'finance_module'
    yield 'mc_server_status'
    yield 'website_check'
    yield 'matrixmodule'


text_file = open(os.path.dirname(os.path.abspath(__file__))+"/TOKEN.txt", "r")
token = text_file.read()
text_file.close()
client = interactions.Client(token=token)
client.load('interactions.ext.files')
client.load('core_commands')

for i in _get_extensions():
    client.load(i)
    print("extension loaded: "+ i)
print("extensions loaded successfully")

# successful start
@client.event
async def on_ready():
    print('Logged in successfully')

client.start()