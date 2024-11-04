#!/usr/bin/env python3

from hashlib import md5
from struct import unpack_from
from typing import List

hash_ring = {}

def _md5_hash(key: str, num_nodes: int) -> int:
    # >I - using big endian to get the first 4 bytes
    hash_int = unpack_from('>I', md5(str(key).encode()).digest())[0]
    # Choose a prime number close to but larger than num_buckets
    prime_modulus = next_prime(num_nodes)
    return round(hash_int % prime_modulus % num_nodes)

def next_prime(n):
    def is_prime(n):
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    if n < 2:
        return 2
    prime = n
    while not is_prime(prime):
        prime += 1
    return prime

def test_md5_hash(num_keys=10, num_nodes=100):
    buckets = [0] * num_nodes
    for i in range(num_keys):
        bucket = _md5_hash(i, num_nodes)
        print(bucket)
        buckets[bucket] += 1
    # Calculate standard deviation to check uniformity
    expected = num_keys / num_nodes
    variance = sum((x - expected) ** 2 for x in buckets) / num_nodes
    std_dev = variance ** 0.5
    return std_dev / expected

def _add_notes_to_ring(num_keys: int, nodes: List[str]):
    num_nodes = len(nodes)
    for i in range(num_nodes):
        node_hash = _md5_hash(i, num_nodes)
        hash_ring.setdefault(node_hash, []).append(nodes[i])


if __name__ == "__main__":
    nodes = ['a', 'b', 'c']
    _add_notes_to_ring(nodes)
    print(hash_ring)
