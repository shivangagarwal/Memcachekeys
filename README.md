Memcachekeys
============

Get all the keys of the memcached infra that you have. This is a wrapper which helps to get all the keys that are present in your Memcached servers. 
The code is written using Python threads to process the keys in parallel for different servers, thus increasing the performance.

Usage:
The usage is very straignforward:

server_array = [{'host':'192.168.0.1', 'port':'12211'}, {'host':'192.168.0.2', 'port':'12211'}] #list of dict of memcached servers

m = Memcachekeys(servers) #class init with the servers, if not provided it takes localhost as the default, with default memcached server port

m.get_all_keys() 
