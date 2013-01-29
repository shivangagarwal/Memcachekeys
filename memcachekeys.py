import re, telnetlib, sys, threading

class MemCacheKeys:
    _outlist = []
    _key_regex = re.compile(ur'ITEM (.*) \[(.*); (.*)\]')
    _slab_regex = re.compile(ur'STAT items:(.*):number')

    def __init__(self, memservers = [{'host':'localhost', 'port':'11211'}]):
	"""init call, it takes the servers which are needed to be spanned to get all the keys
	"""
	self._memservers = memservers

    def telnet(self, host, port):
	return telnetlib.Telnet(host, port)

    def command(self,telnet, cmd):
	"""
	Runs the command on the telnet connected
	"""
	telnet.write("%s\n" %cmd)
	return telnet.read_until('END')

    def get_all_keys(self):
	"""Function which connects to telnet and gets the keys"""
	threads = []
	threads = [self._get_threads(x['host'], x['port']) for x in self._memservers]
	for t in threads:
	    t.start()
	for t in threads:
	    t.join()
	return self._outlist
    
    def _get_keys(self, host, port):
	"""Connects to one server and gets the keys of that particular servers
	"""
	_telnet = self.telnet(host, port)
	cmd = 'stats cachedump %s 0'
	keys = [key for id in self._slab_ids(_telnet) for key in self._key_regex.findall(self.command(_telnet, cmd %id))]
	result =  [key[0] for key in keys]
	self._outlist = self._outlist + result

    def _get_threads(self, host, port):
	result = []
	thread = threading.Thread(target= self._get_keys, args=(host, port))
	return thread

    def _slab_ids(self, telnet):
	"""
	Gets all the slab_ids
	"""
	return self._slab_regex.findall(self.command(telnet, 'stats items'))


if __name__ == '__main__':
    import pprint
    m = MemCacheKeys()
    pprint.pprint(m.get_all_keys())

