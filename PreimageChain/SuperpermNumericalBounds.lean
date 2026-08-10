import PreimageChain.PathwiseFinalCore

/-!
# 最终超排列下界的直接数值推论

本模块把无条件全局定理与论文表 1 的精确数值等式直接组合，给出便于论文引用、
审稿与代码审计的 `Ssuper` 数值下界。
-/

namespace PreimageChain

open Hunter

private theorem superperm_numerical_bound_of_eq
    {k n : ℕ} (hk : 5 ≤ k) {hkNum : 5 ≤ k}
    (hnum : Numerics.hunterBound k + Numerics.gamma k hkNum = n) :
    n ≤ Ssuper k := by
  cases Subsingleton.elim hkNum hk
  exact hnum ▸ superperm_new_bound_closed hk

/-- 论文表 1 中 `k=5,…,14` 的无条件超排列长度下界。 -/
theorem superperm_numerical_bounds_closed :
    153 ≤ Ssuper 5 ∧
    869 ≤ Ssuper 6 ∧
    5892 ≤ Ssuper 7 ∧
    46118 ≤ Ssuper 8 ∧
    408418 ≤ Ssuper 9 ∧
    4033080 ≤ Ssuper 10 ∧
    43916235 ≤ Ssuper 11 ∧
    522610764 ≤ Ssuper 12 ∧
    6746523219 ≤ Ssuper 13 ∧
    93890256441 ≤ Ssuper 14 := by
  rcases Numerics.numerical_bounds with
    ⟨h5, h6, h7, h8, h9, h10, h11, h12, h13, h14⟩
  exact ⟨
    superperm_numerical_bound_of_eq (k := 5) (n := 153) (by omega) h5,
    superperm_numerical_bound_of_eq (k := 6) (n := 869) (by omega) h6,
    superperm_numerical_bound_of_eq (k := 7) (n := 5892) (by omega) h7,
    superperm_numerical_bound_of_eq (k := 8) (n := 46118) (by omega) h8,
    superperm_numerical_bound_of_eq (k := 9) (n := 408418) (by omega) h9,
    superperm_numerical_bound_of_eq (k := 10) (n := 4033080) (by omega) h10,
    superperm_numerical_bound_of_eq (k := 11) (n := 43916235) (by omega) h11,
    superperm_numerical_bound_of_eq (k := 12) (n := 522610764) (by omega) h12,
    superperm_numerical_bound_of_eq (k := 13) (n := 6746523219) (by omega) h13,
    superperm_numerical_bound_of_eq (k := 14) (n := 93890256441) (by omega) h14⟩

end PreimageChain
