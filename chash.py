#!/usr/bin/env python3

from hashlib import md5
from typing import List

hash_ring = [0]
request_map = {}

def _md5_hash(key: str) -> int:
    """Returns a hash value in the range [0, 2^128 - 1]."""
    hash_value = int(md5(key.encode()).hexdigest(), 16)
    return hash_value

class CacheNode:
    def __init__(self, identifier):
        self.identifier = identifier
        self.key = _md5_hash(self.identifier)

def add_node_hash_to_ring(cache_node: CacheNode):
    global hash_ring
    while cache_node.key in hash_ring:
        cache_node.key += 1
    hash_ring.append(cache_node.key)
    hash_ring = sorted(hash_ring)

def _find_cache_server_for_request(request: str):
    global request_map
    request_hash = _md5_hash(request)
    print(request_hash)
    def binary_search(ring: List[int], start: int, end: int):
        if start > end:
            request_map[hash_ring[start]] = request_hash
            return
        mid = start + (end - start) // 2
        if hash_ring[mid] == request_hash:
           request_map[hash_ring[mid]] = request_hash
           return
        elif hash_ring[mid] < request_hash:
            binary_search(ring, mid+1, end)
        else:
            binary_search(ring, start, mid-1)
    binary_search(hash_ring, 0, len(hash_ring) - 1)

if __name__ == "__main__":
    nodeA = CacheNode("NodeA")
    nodeB = CacheNode("NodeB")
    nodeC = CacheNode("NodeC")
    add_node_hash_to_ring(nodeA)
    add_node_hash_to_ring(nodeB)
    add_node_hash_to_ring(nodeC)
    print(hash_ring)
    req1 = '123/bla'
    _find_cache_server_for_request(req1)
    print(request_map) 
