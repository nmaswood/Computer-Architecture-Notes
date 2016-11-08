# Caches
## Locate Data
1. Set index dtermiens cache set
2. Compare tag bits. If match proceed else, miss
3. Check valid bit

* Number of tag bits = l - b - s

## Loading Data

* Find starting and ending range of data
* N Locations in set associative cache
* Need LRU bits to track which block is the oldest


## Byte vs Word Addressing
* Address split into Block offset, set index and tag


## Questions
* How we actually keep track of blocks?
    * Do add until the cahce full and then pop the oldest, insert then ewst and incremen all the others
    * What if a block is already in the cache?
        * Do we just keep in twice?
* What is a dirty eviction?

