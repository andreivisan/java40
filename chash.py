#!/usr/bin/env python3

from hashlib import md5
from typing import List

hash_ring = []
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
    hash_ring.append(cache_node.key)
    hash_ring = sorted(hash_ring)

def map_requests_to_cache_server(request: str):
    global request_map
    n = len(hash_ring)
    request_hash = _md5_hash(request)
    if n == 0 or request_hash > hash_ring[- 1]:
        request_map.setdefault(0, []).append(request_hash)
        return
    print(request_hash)
    def binary_search(ring: List[int], start: int, end: int):
        if start > end:
            if start >= len(hash_ring):
                # Wrap around to the first node
                start = 0
            request_map.setdefault(hash_ring[start], []).append(request_hash)
            return
        mid = start + (end - start) // 2
        if hash_ring[mid] == request_hash:
           request_map.setdefault(hash_ring[mid], []).append(request_hash)
           return
        elif hash_ring[mid] < request_hash:
            binary_search(ring, mid+1, end)
        else:
            binary_search(ring, start, mid-1)
    binary_search(hash_ring, 0, len(hash_ring) - 1)

def remove_node_from_ring(cache_node: CacheNode):
    global hash_ring
    hash_ring.remove(cache_node.key)

if __name__ == "__main__":
    add_node_hash_to_ring(CacheNode('Node1'))
    add_node_hash_to_ring(CacheNode('Node2'))
    add_node_hash_to_ring(CacheNode('Node3'))
    requests = ['Request1', 'Request2', 'Request3', 'Request4', 'Request5']
    initial_mappings = {}
    for req in requests:
        map_requests_to_cache_server(req)
        req_hash = _md5_hash(req)
        initial_mappings[req_hash] = request_map[req_hash]
    add_node_hash_to_ring(CacheNode('Node4'))
    remove_node_from_ring(CacheNode('Node2'))
    request_map.clear()
    updated_mappings = {}
    for req in requests:
        map_requests_to_cache_server(req)
        req_hash = _md5_hash(req)
        # Store the updated mapping
        updated_mappings[req_hash] = request_map[req_hash]
        remapped_count = 0
    for req in requests:
        if initial_mappings[req] != updated_mappings[req]:
            remapped_count += 1
    total_requests = len(requests)
    remapped_percentage = (remapped_count / total_requests) * 100
    print(f"{remapped_percentage}% of requests were remapped.")
