# CAP Theorem

The CAP Theorem, also known as Brewer's Theorem, outlines the fundamental trade-offs that must be considered when designing distributed applications and databases.

## What is the CAP Theorem?

The CAP Theorem states that a distributed data system can guarantee only two of the following three properties simultaneously:

1. Consistency (C):

    - Every read receives the most recent write or an error.

    - All nodes see the same data at the same time.

2. Availability (A):

    - Every request receives a (non-error) response, without the guarantee that it contains the most recent write.

    - The system remains operational 100% of the time.

3. Partition Tolerance (P):

    - The system continues to operate despite arbitrary partitioning due to network failures.
    
    - The system can handle communication breakdowns between nodes.