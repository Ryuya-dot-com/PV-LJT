# Cレベル向けPV-LJT: マルチエージェント候補統合メモ v2

作成日: 2026-07-04

目的: v2_multi_agentで80から84点に残っていた優先項目を、複数査読者役の候補生成に基づいて再改稿し、90点以上の項目数を増やす。

## 対象項目

今回は以下10スロットを対象にした。

| Slot | v2 PV | v2 score | 主な問題 |
|---|---|---:|---|
| cljt_009 | get on | 80 | boarding senseが透明すぎ、C1向けには易しい。 |
| cljt_015 | put on | 80 | event/artifact contrastがやや粗い。 |
| cljt_019 | get off | 80 | leave-vehicle senseが透明すぎる。 |
| cljt_023 | bring in | 80 | consultant/consultationの名詞差がやや表層的。 |
| cljt_026 | set out | 80 | procedure/appendix contrastが文書部品の粗い差に寄る。 |
| cljt_027 | break down | 80 | sports play/whistle contrastが粗い。 |
| cljt_031 | turn around | 80 | improvement/reversal/work-speed readingsが競合する。 |
| cljt_032 | back up | 80 | conclusion/confusion contrastが粗い。 |
| cljt_044 | point out | 81 | point outは目的語範囲が広く、unacceptableを安定させにくい。 |
| cljt_046 | follow up | 84 | thermometer foilがやや具体物異常に寄る。 |

## 採用した改稿

| Slot | v3 PV | v3 score | Acceptable | Unacceptable | 採用理由 |
|---|---|---:|---|---|---|
| cljt_009 | get on | 90 | The researchers got on with the analysis. | The researchers got on with the finding. | 交通senseを捨て、task-continuation senseへ変更。process/outcome contrastでC1向けに改善。 |
| cljt_015 | put on | 91 | The gallery put on a retrospective exhibition. | The gallery put on a retrospective catalog. | arts-program domain内でevent/artifact contrastを精密化。 |
| cljt_019 | get off | 91 | The defendant got off with a warning. | The defendant got off with a conviction. | 交通senseを捨て、legal leniency senseへ変更。 |
| cljt_023 | bring in | 92 | The campaign brought in large donations. | The campaign brought in large expenses. | recruitment senseからincome/support senseへ変更し、campaign-finance domainに固定。 |
| cljt_026 | set out | 93 | The contract set out the payment terms. | The contract set out the payment receipts. | contract/payment domainでstipulated contentとrecordを対比。 |
| cljt_027 | break down | 91 | The manager broke down the project budget. | The manager broke down the project deadline. | project-management domainでdecomposable objectを問う。 |
| cljt_031 | go through | 91 | The amendment went through the committee. | The amendment went through the testimony. | `turn around`を置換。formal approval path senseの方が一文で制御しやすい。 |
| cljt_032 | back up | 92 | The results backed up the hypothesis. | The results backed up the questionnaire. | research domain内でclaim/instrument contrastに変更。 |
| cljt_044 | bring down | 90 | The scandal brought down the minister. | The scandal brought down the briefing. | `point out`を置換。political loss-of-position senseの方がunacceptableを安定させやすい。 |
| cljt_046 | follow up | 90 | The clinic followed up on the patient referral. | The clinic followed up on the patient brochure. | medical-admin domain内でcase-trigger/material contrastに変更。 |

## 採用しなかった主要候補

| Slot | 候補 | 理由 |
|---|---|---|
| cljt_009 | come around: committee/compromise vs minutes | C1向けには強いが、`come around to the minutes`が「議事録に話が回る」と読まれる可能性がある。今回は既存PV保持を優先。 |
| cljt_019 | come off: proposal/cautious vs fiscal | impression senseは良いが、`fiscal`がcontent-domain adjectiveとして自然すぎる可能性がある。 |
| cljt_027 | iron out: final details vs signatures | 強い案だが候補プール外。`break down`を91点水準まで改善できたため保留。 |
| cljt_027 | wind up: dispute/arbitration vs testimony | outcome senseは有望だが、`wind up`のclose-company/toy/literal sensesが残る。 |
| cljt_044 | draw on: interview data vs appointments | 強い案だが候補プール外。今回は候補プール内の`bring down`を採用。 |
| cljt_046 | lawyer/complaint vs statute | 法務domainとして良いが、`follow up on a statute`が「法令について追加確認する」と読まれる余地がある。 |

## 統合後の状態

出力ファイル:

- `c_level_pv_ljt_48_target_master_v3_multi_agent.tsv`
- `c_level_pv_ljt_list_assignment_v3_multi_agent.tsv`
- `c_level_pv_ljt_list_A_v3_multi_agent.tsv`
- `c_level_pv_ljt_list_B_v3_multi_agent.tsv`

機械検証結果:

- 48ターゲット / 96文
- List A: acceptable 24 / unacceptable 24
- List B: acceptable 24 / unacceptable 24
- A/Bは全ターゲットで相補的
- ターゲットPVは全項目で第3語以降
- 文長は全項目で5から10語
- 同一条件の連続は各リスト最大3試行
- 機械検証上の問題は0件

スコア改善:

- v2平均: 86.08
- v3平均: 88.29
- v2中央値: 86
- v3中央値: 90
- v2の90点以上: 15/48
- v3の90点以上: 25/48
- 80点未満: 0/48を維持

査読者としての評価:

v3は、C1中心のphrasal verb LJTとしてv2よりかなり説得力がある。とくに、交通系の透明な`get on/get off`を抽象・制度的senseに切り替えたこと、`point out`の広すぎる目的語範囲を避けたこと、文書・研究・法務・政治・医療管理domainでsame-domain near-missを作ったことが改善点である。

ただし、`get on with`, `follow up on`, `bring in`は依然として使用範囲が広い。ネイティブレビューでは、unacceptable文が「やや不自然」ではなく「意図senseでは明確に不適切」と判断されるかを重点確認する必要がある。

