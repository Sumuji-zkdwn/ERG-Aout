# HMDG boundary expansion tasks

target: `Module.End.iSup_genEigenspace_restrict_eq_top`
path_length: 10
boundary_count: 3

### Boundary 1

score: 7
phase_edge: `kernel setup` -> `criterion bridge`
node_edge: `LinearMap.ker_restrict` -> `LinearMap.injective_restrict_iff_disjoint`
role_shift: kernel -> criterion
shared_tags: transfer
lost_tags: kernel
gained_tags: constraint,criterion

#### Expansion question

Why does the kernel statement become an injectivity/disjointness criterion?

#### Expansion tasks

1. State the exact source theorem/declaration in plain language.
2. State the exact target theorem/declaration in plain language.
3. Identify the operation that crosses the boundary.
4. Expand each token hint below into one sentence.
5. Decide whether an intermediate concept node is missing between the two declarations.

#### Token tasks

- ker: track the zero-preimage condition
- restrict: check what changes under restriction
- injective: translate kernel-zero into injectivity
- iff: split the equivalence into both directions
- disjoint: identify which subobjects must intersect trivially

#### Candidate missing concept node

`kernel_to_criterion`

### Boundary 2

score: 7
phase_edge: `criterion bridge` -> `constraint bridge`
node_edge: `LinearMap.injective_restrict_iff_disjoint` -> `LinearMap.comap_eq_sup_ker_of_disjoint`
role_shift: criterion -> constraint
shared_tags: constraint,transfer
lost_tags: criterion
gained_tags: kernel,lattice_operation

#### Expansion question

How is the criterion converted into structural side conditions such as disjointness, kernel equality, or lattice conditions?

#### Expansion tasks

1. State the exact source theorem/declaration in plain language.
2. State the exact target theorem/declaration in plain language.
3. Identify the operation that crosses the boundary.
4. Expand each token hint below into one sentence.
5. Decide whether an intermediate concept node is missing between the two declarations.

#### Token tasks

- injective: translate kernel-zero into injectivity
- restrict: check what changes under restriction
- iff: split the equivalence into both directions
- disjoint: identify which subobjects must intersect trivially
- comap: follow the pullback/comap operation
- eq: identify the equality to prove
- sup: track join/supremum operations
- ker: track the zero-preimage condition

#### Candidate missing concept node

`criterion_to_constraint`

### Boundary 3

score: 7
phase_edge: `constraint bridge` -> `eigenspace conclusion`
node_edge: `LinearMap.ker_noncommProd_eq_of_supIndep_ker` -> `Submodule.inf_iSup_genEigenspace`
role_shift: constraint -> eigenspace
shared_tags: lattice_operation
lost_tags: constraint,kernel
gained_tags: eigenspace

#### Expansion question

How do the kernel/disjointness constraints become a statement about generalized eigenspace decomposition?

#### Expansion tasks

1. State the exact source theorem/declaration in plain language.
2. State the exact target theorem/declaration in plain language.
3. Identify the operation that crosses the boundary.
4. Expand each token hint below into one sentence.
5. Decide whether an intermediate concept node is missing between the two declarations.

#### Token tasks

- ker: track the zero-preimage condition
- noncommProd: track product of endomorphisms without assuming commutativity
- eq: identify the equality to prove
- supIndep: track independence of a family of subobjects
- inf: track meet/infimum operations
- iSup: track indexed supremum over components
- genEigenspace: connect constraints to generalized eigenspaces

#### Candidate missing concept node

`constraint_to_eigenspace`
