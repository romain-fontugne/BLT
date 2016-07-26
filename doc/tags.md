
# Message tags:

- Duplicate: All information from the message are already in the routing table.
 (could be an update or a withdrawn)
- Flap: The message correspond to the previous state in the routing table.

# Path tags:

- Path Change: The path to the announce prefix changed.
- Origin Change: The origin AS have changed.
- Prepending: The path contains several times the same AS.


# Prefix tags:

- New prefix: Prefix not in the routing table
- Lonely: a prefix that does not overlap with any other prefix.
- Top: a prefix that covers one or more smaller prefix blocks, but is not itself
covered by a less specific.
- Deaggregated: a prefix that is covered by a less specific prefix, and this less 
specific is originated by the same AS as the deaggregated prefix.
- Delegated: a prefix that is covered by a less specific, and this less specific 
is not originated by the same AS as the delegated prefix.

