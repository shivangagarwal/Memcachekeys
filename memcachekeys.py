import re, telnetlib, sys

class MemCacheKeys:
    _telnet = None
    _key_regex = re.compile(ur'ITEM (.*) \[(.*); (.*)\]')
    _slab_regex = re.compile(ur'STAT items:(.*):number')

    def __init__(self, memservers = [{'host':'localhost', 'port':'11211'}]):
	"""init call, it takes the servers which are needed to be spanned to get all the keys
	"""
	self._memservers = memservers

    def telnet(self, host, port):
	return telnetlib.Telnet(host, port)

    def command(self,cmd):
	"""
	Runs the command on the telnet connected
	"""
	self._telnet.write("%s\n" %cmd)
	return self._telnet.read_until('END')


    def get_all_keys(self):
	"""Function which connects to telnet and gets the keys"""
	keys = []
	for x in self._memservers:
	    self._telnet = self.telnet(x['host'], x['port'])
	    keys = keys + self._get_keys()
	return keys

    def _get_keys(self):
	"""Connects to one server and gets the keys of that particular servers
	"""
	cmd = 'stats cachedump %s 0'
	keys = [key for id in self._slab_ids() for key in self._key_regex.findall(self.command(cmd %id))]
	return [key[0] for key in keys]

    def _slab_ids(self):
	"""
	Gets all the slab_ids
	"""
	return self._slab_regex.findall(self.command('stats items'))


if __name__ == '__main__':
    import pprint
    m = MemCacheKeys()
    pprint.pprint(m.get_all_keys())

