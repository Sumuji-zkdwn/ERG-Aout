# HMDG concept patch proposal

target: `Module.End.iSup_genEigenspace_restrict_eq_top`
path_length: 10
node_count: 13
edge_count: 18

## Concept bridge nodes

### C001_kernel_to_criterion `kernel_to_criterion`

status: candidate
phase_edge: `kernel setup` -> `criterion bridge`
role_shift: kernel -> criterion
score: 7
question: Why does the kernel statement become an injectivity/disjointness criterion?
shared_tags: transfer
lost_tags: kernel
gained_tags: constraint,criterion

token_tasks:
- ker: track the zero-preimage condition
- restrict: check what changes under restriction
- injective: translate kernel-zero into injectivity
- iff: split the equivalence into both directions
- disjoint: identify which subobjects must intersect trivially

### C002_criterion_to_constraint `criterion_to_constraint`

status: candidate
phase_edge: `criterion bridge` -> `constraint bridge`
role_shift: criterion -> constraint
score: 7
question: How is the criterion converted into structural side conditions such as disjointness, kernel equality, or lattice conditions?
shared_tags: constraint,transfer
lost_tags: criterion
gained_tags: kernel,lattice_operation

token_tasks:
- injective: translate kernel-zero into injectivity
- restrict: check what changes under restriction
- iff: split the equivalence into both directions
- disjoint: identify which subobjects must intersect trivially
- comap: follow the pullback/comap operation
- eq: identify the equality to prove
- sup: track join/supremum operations
- ker: track the zero-preimage condition

### C003_constraint_to_eigenspace `constraint_to_eigenspace`

status: candidate
phase_edge: `constraint bridge` -> `eigenspace conclusion`
role_shift: constraint -> eigenspace
score: 7
question: How do the kernel/disjointness constraints become a statement about generalized eigenspace decomposition?
shared_tags: lattice_operation
lost_tags: constraint,kernel
gained_tags: eigenspace

token_tasks:
- ker: track the zero-preimage condition
- noncommProd: track product of endomorphisms without assuming commutativity
- eq: identify the equality to prove
- supIndep: track independence of a family of subobjects
- inf: track meet/infimum operations
- iSup: track indexed supremum over components
- genEigenspace: connect constraints to generalized eigenspaces

## Typed edge list

- `D001:LinearMap.ker` -[main_path_edge]-> `D002:LinearMap.ker_codRestrict`
- `D002:LinearMap.ker_codRestrict` -[main_path_edge]-> `D003:LinearMap.ker_restrict`
- `D003:LinearMap.ker_restrict` -[main_path_edge]-> `D004:LinearMap.injective_restrict_iff_disjoint`
- `D004:LinearMap.injective_restrict_iff_disjoint` -[main_path_edge]-> `D005:LinearMap.comap_eq_sup_ker_of_disjoint`
- `D005:LinearMap.comap_eq_sup_ker_of_disjoint` -[main_path_edge]-> `D006:LinearMap.ker_comp_eq_of_commute_of_disjoint_ker`
- `D006:LinearMap.ker_comp_eq_of_commute_of_disjoint_ker` -[main_path_edge]-> `D007:LinearMap.ker_noncommProd_eq_of_supIndep_ker`
- `D007:LinearMap.ker_noncommProd_eq_of_supIndep_ker` -[main_path_edge]-> `D008:Submodule.inf_iSup_genEigenspace`
- `D008:Submodule.inf_iSup_genEigenspace` -[main_path_edge]-> `D009:Submodule.eq_iSup_inf_genEigenspace`
- `D009:Submodule.eq_iSup_inf_genEigenspace` -[main_path_edge]-> `D010:Module.End.iSup_genEigenspace_restrict_eq_top`
- `D003:LinearMap.ker_restrict` -[needs_bridge]-> `C001_kernel_to_criterion:kernel_to_criterion`
- `C001_kernel_to_criterion:kernel_to_criterion` -[bridges_to]-> `D004:LinearMap.injective_restrict_iff_disjoint`
- `D003:LinearMap.ker_restrict` -[original_boundary_edge]-> `D004:LinearMap.injective_restrict_iff_disjoint`
- `D004:LinearMap.injective_restrict_iff_disjoint` -[needs_bridge]-> `C002_criterion_to_constraint:criterion_to_constraint`
- `C002_criterion_to_constraint:criterion_to_constraint` -[bridges_to]-> `D005:LinearMap.comap_eq_sup_ker_of_disjoint`
- `D004:LinearMap.injective_restrict_iff_disjoint` -[original_boundary_edge]-> `D005:LinearMap.comap_eq_sup_ker_of_disjoint`
- `D007:LinearMap.ker_noncommProd_eq_of_supIndep_ker` -[needs_bridge]-> `C003_constraint_to_eigenspace:constraint_to_eigenspace`
- `C003_constraint_to_eigenspace:constraint_to_eigenspace` -[bridges_to]-> `D008:Submodule.inf_iSup_genEigenspace`
- `D007:LinearMap.ker_noncommProd_eq_of_supIndep_ker` -[original_boundary_edge]-> `D008:Submodule.inf_iSup_genEigenspace`

## Import note

This patch is intentionally marked as candidate. Accepting a concept bridge requires mathematical review or another expansion pass.
