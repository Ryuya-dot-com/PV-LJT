# Cレベル向けPhrasal Verb LJT 48項目マスター: 全体バランス監査 v3 Multi-Agent

作成日: 2026-07-04

対象ファイル:

- `c_level_pv_ljt_48_target_master_v3_multi_agent.tsv`
- `c_level_pv_ljt_list_A_v3_multi_agent.tsv`
- `c_level_pv_ljt_list_B_v3_multi_agent.tsv`
- `c_level_pv_ljt_list_assignment_v3_multi_agent.tsv`

## v2からの主な変更

v2で80から84点に残っていた10スロットをマルチエージェント方式で改稿した。

| Slot | v2 PV | v3 PV | v2 score | v3 score |
|---|---|---|---:|---:|
| cljt_009 | get on | get on | 80 | 90 |
| cljt_015 | put on | put on | 80 | 91 |
| cljt_019 | get off | get off | 80 | 91 |
| cljt_023 | bring in | bring in | 80 | 92 |
| cljt_026 | set out | set out | 80 | 93 |
| cljt_027 | break down | break down | 80 | 91 |
| cljt_031 | turn around | go through | 80 | 91 |
| cljt_032 | back up | back up | 80 | 92 |
| cljt_044 | point out | bring down | 81 | 90 |
| cljt_046 | follow up | follow up | 84 | 90 |

置換したPVは2つのみである。

- `turn around` -> `go through`
- `point out` -> `bring down`

その他8項目は、既存PVを維持しつつ、よりC1向けのsenseまたは文脈へ変更した。

## 形式検証

v3_multi_agentは以下の機械チェックを通過した。

- マスター行数: 96
- ターゲット数: 48
- マスター内条件: acceptable 48 / unacceptable 48
- List A: acceptable 24 / unacceptable 24
- List B: acceptable 24 / unacceptable 24
- List A/Bは全ターゲットで相補的
- 各リストは48ターゲットを1回ずつ提示
- 各リスト内で同一条件の連続は最大3試行
- ターゲットPV形は全センテンス内で検出可能
- ターゲットPV形は全項目で第3語以降に出現
- 文長は全項目で5から10語の範囲内
- 機械検証上の問題: 0件

## スコア分布

| スコア | ターゲット数 |
|---:|---:|
| 100 | 5 |
| 93 | 1 |
| 92 | 3 |
| 91 | 6 |
| 90 | 10 |
| 88 | 5 |
| 86 | 5 |
| 85 | 1 |
| 84 | 2 |
| 80 | 10 |

要約:

- 平均: 88.29
- 中央値: 90
- 最小: 80
- 最大: 100
- 90点以上: 25/48
- 85点以上: 36/48
- 80点以上: 48/48
- 80点未満: 0/48

v3では中央値が90に到達した。これは、C1中心LJTとしての設計妥当性がかなり改善したことを示す。ただし、まだ80点の項目が10ターゲット、84点の項目が2ターゲット残っている。

## v3で強くなった項目

| Slot | PV | 改善点 |
|---|---|---|
| cljt_009 | get on | transparentなboarding senseを捨て、task-continuation senseへ変更。 |
| cljt_015 | put on | theater/ticketからgallery/exhibition/catalogへ変更し、event/artifact contrastを精密化。 |
| cljt_019 | get off | leave-vehicle senseからlegal leniency senseへ変更。 |
| cljt_023 | bring in | consultant/consultationからdonations/expensesへ変更し、income/support senseに固定。 |
| cljt_026 | set out | procedure/appendixからpayment terms/receiptsへ変更し、document contentの制約を明確化。 |
| cljt_027 | break down | sports-domainからproject-management domainへ変更。 |
| cljt_031 | go through | turn aroundを置換し、formal approval path senseへ変更。 |
| cljt_032 | back up | conclusion/confusionからhypothesis/questionnaireへ変更。 |
| cljt_044 | bring down | point outを置換し、political loss-of-position senseへ変更。 |
| cljt_046 | follow up | thermometer foilからpatient referral/brochureへ変更。 |

## まだ重点レビューが必要な項目

v3で80から84点に残っている項目は以下である。

| Slot | PV | Score | 残るリスク |
|---|---|---:|---|
| cljt_001 | break off | 80 | `break off the proposal`が交渉・議論中断として許容されないか確認が必要。 |
| cljt_002 | hand over | 80 | custody/control transferの目的語制限が十分か確認が必要。 |
| cljt_012 | pull back | 80 | `pull back from approval`の不自然性が安定するか確認が必要。 |
| cljt_013 | run out | 80 | resource depletion cueが強く、C1には易しい可能性がある。 |
| cljt_014 | turn over | 80 | transfer/physical/read-through sensesの競合が残る。 |
| cljt_016 | take back | 80 | retract/return sensesの競合が残る。 |
| cljt_018 | pay off | 80 | loan/debt payoff senseとbenefit senseの切り分けが必要。 |
| cljt_020 | turn up | 80 | appear/increase/volume sensesの競合がある。 |
| cljt_034 | take out | 80 | obtain official service/document senseとremove/date sensesが競合する。 |
| cljt_041 | bring about | 80 | cause senseは安定しているが、結果名詞の選択がやや一般意味に寄る。 |
| cljt_011 | stand out | 84 | standout対象の選択が一般意味で処理される可能性がある。 |
| cljt_028 | reach out | 84 | contact senseが明確すぎ、C1ではやや易しい可能性がある。 |

次に改稿するなら、この12項目が対象になる。ただし、v3時点で中央値90、90点以上25/48に達しているため、全項目を無理に90点化するより、ネイティブレビューで低評価になりそうな項目を優先的に絞る方が効率的である。

## 査読者としての判定

v3_multi_agentの現時点の妥当性は、100点満点で90点程度である。

強み:

- 80点未満は0件を維持。
- 90点以上が25/48まで増加。
- 中央値が90に到達。
- List A/Bの形式バランスを維持。
- C1向けに、制度・法務・研究・政治・医療管理など抽象的domainの項目が増えた。

弱み:

- 80点ちょうどの項目がまだ10件残る。
- 一部の改稿項目は、ネイティブレビューでalternate readingが見つかる可能性がある。
- スコアは設計評価であり、実測の難度・弁別力ではない。

次の推奨手順:

1. v3をpre-audio expert review用の主候補版とする。
2. ただし、`break off`, `hand over`, `pull back`, `run out`, `turn over`, `take back`, `pay off`, `turn up`, `take out`, `bring about`, `stand out`, `reach out`は重点レビュー対象として明示する。
3. 90点化をさらに進めるなら、上記12項目から5から6項目だけを選び、第3ラウンドのマルチエージェント改稿を行う。
4. ElevenLabs録音は、少なくともネイティブレビューでacceptable自然さとunacceptable near-miss性を確認してから行う。

