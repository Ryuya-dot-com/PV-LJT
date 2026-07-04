# Cレベル向けPV-LJT: マルチエージェント候補統合メモ v1

作成日: 2026-07-04

目的: 低スコア項目を中心に、複数の査読者役から候補を出し合い、C1中心のaural phrasal verb LJTとしてより妥当な48項目マスターへ統合する。

## エージェント役割

| Agent | 主な観点 | 出力の扱い |
|---|---|---|
| Agent A | PV意味・多義性・near-missの意味論的妥当性 | 既存PVを保持した高スコア改稿案を主に採用 |
| Agent B | C1難度・同一ドメインfoil・手がかり制御 | `put up`と`cut off`の採用案に強く反映 |
| Agent C | 音声LJTとしての自然さ・短文性・実装リスク | 既存PVでは不安定な場合の全面置換バックアップ案として保持 |

## 統合方針

今回は、次の順で採用判断を行った。

1. 既存PVを保持したまま90点水準に近づけられる場合は、その案を優先する。
2. 既存PVの多義性が短い音声文で制御できない場合のみ、外部PVへの全面置換を検討する。
3. acceptable/unacceptableは同一ドメイン内で作り、粗い文法性・世界知識・具体物異常だけで解ける項目を避ける。
4. ターゲットPVは第3語以降に置き、文長は5から10語に収める。
5. List A/Bの条件割付は維持し、既存の複数リスト均衡を壊さない。

## 採用した改稿

| Slot | 採用PV | 旧スコア | 新スコア | Acceptable | Unacceptable | 採用理由 |
|---|---|---:|---:|---|---|---|
| cljt_010 | play out | 84 | 92 | The trial played out over two weeks. | The verdict played out over two weeks. | legal-domainのevent/outcome contrastにより、`agreement played out`の許容可能性を回避。 |
| cljt_022 | cut off | 76 | 91 | The lender cut off the credit line. | The lender cut off the credit rating. | speech interruptionではなくfinance/access terminationに切り替え、C1向けの同一ドメインnear-missを実現。 |
| cljt_030 | put up | 61 | 90 | The bidder put up the required deposit. | The bidder put up the required estimate. | display senseを捨て、money/security senseに切ることで`put up a brochure`問題を解消。 |
| cljt_033 | open up | 84 | 91 | The ruling opened up new appeal options. | The ruling opened up new appeal deadlines. | legal appeal frameでavailability senseを固定し、`objections`の曖昧性を低減。 |
| cljt_035 | fill in | 78 | 90 | The consultant filled in for the project chair. | The consultant filled in for the project meeting. | `fill someone in on X`はトピック範囲が広すぎるため、substitute-for senseへ変更。 |
| cljt_036 | hold up | 84 | 90 | The appeal held up the construction permit. | The appeal held up the construction blueprint. | `receipt`も遅延可能なため、permit process/document contrastへ変更。 |
| cljt_040 | come out | 76 | 90 | The senator came out against the proposal. | The senator came out against the evidence. | reveal senseのperson/literal readingを避け、public stance senseへ変更。 |

## 採用しなかったが保持するバックアップ案

Agent Cの全面置換案は、短文性と自然さは強い。ただし、既存候補プールとの出典連続性が弱くなるため、今回はバックアップに留めた。

| Slot | Backup PV | Acceptable | Unacceptable | 保留理由 |
|---|---|---|---|---|
| cljt_030 | draw up | The lawyer drew up the lease. | The lawyer drew up the verdict. | 強い案だが、既存`put up`を90点水準まで救済できたため保留。 |
| cljt_022 | call off | The council called off the hearing. | The council called off the permit. | 強い案だが、`cut off`のfinance案が同等以上に良く、元PVを保持できる。 |
| cljt_035 | spell out | The contract spelled out the payment terms. | The contract spelled out the signature page. | 使える案だが、document part mismatchがやや粗く、今回は`fill in`のsubstitute senseを採用。 |
| cljt_040 | phase out | The company phased out the product line. | The company phased out the product launch. | 高品質だが、`come out`のstance senseが90点水準に改善できるため保留。 |

## 棄却した旧案

| Slot | 旧案 | 棄却理由 |
|---|---|---|
| cljt_030 | The crew put up the banner/brochure. | `put up a brochure`が掲示・展示文脈で許容される。 |
| cljt_022 | The host cut off the caller/topic. | `cut off the topic`が「話題を打ち切る」として許容されうる。 |
| cljt_035 | The assistant filled in the director on the plan/chair. | `fill someone in on X`のXが広すぎ、`chair`は粗い具体物異常に寄る。 |
| cljt_040 | The secret/witness came out during trial. | `witness came out`がliteral/social readingを誘発する。 |
| cljt_010 | The negotiations/agreement played out in public. | `agreement played out`が文脈によって許容されうる。 |
| cljt_033 | The policy opened up opportunities/objections. | `opened up objections`が「反論を生じさせた」に近く読まれる恐れがある。 |
| cljt_036 | The error held up the payment/receipt. | `receipt`も遅延可能で、unacceptable keyが不安定。 |

## 統合後の状態

統合後の参照ファイル:

- `c_level_pv_ljt_48_target_master_v2_multi_agent.tsv`
- `c_level_pv_ljt_list_assignment_v2_multi_agent.tsv`
- `c_level_pv_ljt_list_A_v2_multi_agent.tsv`
- `c_level_pv_ljt_list_B_v2_multi_agent.tsv`

検証結果:

- 48ターゲット / 96文
- List A: acceptable 24 / unacceptable 24
- List B: acceptable 24 / unacceptable 24
- A/Bは全ターゲットで相補的
- ターゲットPVは全項目で第3語以降
- 文長は全項目で5から10語
- 同一条件の連続は各リスト最大3試行
- 80点未満の項目は0
- 90点以上の項目は15/48

査読者としての評価:

今回の統合で、明確なブロッカーだった4項目は解消された。v2_multi_agentは、v1よりもパイロット前レビューに出せる状態に近い。ただし、90点以上は15/48に留まるため、完成版として90点評価を狙うには、まだ80点台前半の既存v6保持項目を選択的に改稿する必要がある。

