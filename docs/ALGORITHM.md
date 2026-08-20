# RANGE-Ω v0.1

For a declared interval `[L,U]`, shard `i` of `m` receives an exact contiguous subrange with no overlap. The scanner computes `P=L·G` once and advances with `P←P+G`, avoiding a full scalar multiplication per candidate. Candidate public keys are serialized in compressed and uncompressed form and mapped to P2PKH for target comparison.

Checkpoint leaves bind the scalar and compressed public key. Leaves are hashed then reduced pairwise into a work root. This is an audit receipt, **not** a cryptographic proof that every candidate between checkpoints was evaluated.

Complexity for an address-only interval remains `O(N)` candidate checks. The project does not claim a shortcut where none is known.
