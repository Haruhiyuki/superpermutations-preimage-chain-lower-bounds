# Beyond gain one: a general barrier and a mixed-transition program

This directory records a general upper-bound investigation prompted by the completed
preimage-chain lower-bound project. The purpose is not to optimize one small value of `n`, but
to identify which construction paradigm can still improve the general upper bound.

## Main conclusion

The familiar complete-2-cycle construction is not merely one convenient ansatz. It is forced by
bijectivity whenever the successor map uses only `T₁` and `T₂`. Moreover, consecutive weight-three
splices follow a deterministic macro-map of period `n-2`. These two facts imply that the verified
gain-one construction is optimal within the entire paradigm

> complete-2-cycle rooted forest + external component splicing.

Consequently, a genuine general improvement must place `T₃` (or higher transitions) inside the
balanced successor permutation itself. The next object is therefore a mixed-transition
circulation, not a larger collection of standard kernels.

The detailed theorem, ledger, and research program are in
[`MULTIKERNEL_BARRIER_AND_MIXED_TRANSITIONS.md`](MULTIKERNEL_BARRIER_AND_MIXED_TRANSITIONS.md).

## Reproducible degree-eight experiment

The script [`kernel_promotion_search.py`](kernel_promotion_search.py) reads the formally verified
`n=8` gain-one `.sprc` certificate from `urdvr/superpermutation-examples` and searches for a second
standard-kernel packet.

It finds:

* 6,720 distinct relabelled standard-kernel packets;
* three packets already present among the attachment rows;
* one exact balanced promotion replacing five attachment rows by four while promoting six rows;
* a rooted exact cover with 12 kernel rows, 826 attachment rows, and 838 total rows;
* but no all-weight-three splice chain through the resulting 12 kernel components.

Thus the row ledger alone reaches the candidate value `46203`, but the splice-period barrier
prevents it from becoming a superpermutation in this paradigm. This is a diagnostic certificate,
not a claimed new upper bound.

### Reproduction

```bash
python3 research/mixed_transition/kernel_promotion_search.py \
  path/to/46204-e1613d33.sprc \
  --output research/mixed_transition/results/n8_kernel_promotion.json
```

The upstream certificate is pinned at commit
`62958c6268f728828ed578a171486866b6fe4b20`, path
`n8/46204-e1613d33.sprc`.

## Status

This is an active research branch. No theorem in the main paper is changed, and no new upper bound
is claimed yet.
