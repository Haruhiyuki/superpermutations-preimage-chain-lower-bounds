import PreimageChain.Main

/-!
# 实际层下界到最终 `gamma` 修正
-/

namespace PreimageChain

open Hunter

/-- 任一实际层的 `s+G_s` 下界自动蕴含全局最优的 `gamma` 修正。 -/
theorem pathwiseNewBound_of_layer
    {k : ℕ} (hk : 5 ≤ k) (P : HPath k) (s : ℕ)
    (hlayer :
      Numerics.hunterBound k + (s + Numerics.G k s) ≤ P.wtP + k) :
    Numerics.hunterBound k + Numerics.gamma k hk ≤ P.wtP + k := by
  have hgamma := Numerics.gamma_le_objective (k := k) (s := s) hk
  exact (Nat.add_le_add_left hgamma (Numerics.hunterBound k)).trans hlayer

/-- 若每条 Hamilton 路径都产生一个可行层，则 `PathwiseNewBound` 无条件闭合。 -/
theorem pathwiseNewBound_of_layer_selector
    {k : ℕ} (hk : 5 ≤ k)
    (layer : HPath k → ℕ)
    (hlayer : ∀ P : HPath k, P.IsHamiltonian →
      Numerics.hunterBound k +
          (layer P + Numerics.G k (layer P)) ≤ P.wtP + k) :
    PathwiseNewBound k hk := by
  intro P hP
  exact pathwiseNewBound_of_layer hk P (layer P) (hlayer P hP)

end PreimageChain
