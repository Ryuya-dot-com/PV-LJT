# Cレベル向けPhrasal Verb LJT 48項目マスター: 全体バランス監査 v4 Multi-Agent

作成日: 2026-07-04

対象ファイル:

- `c_level_pv_ljt_48_target_master_v4_multi_agent.tsv`
- `c_level_pv_ljt_list_A_v4_multi_agent.tsv`
- `c_level_pv_ljt_list_B_v4_multi_agent.tsv`
- `c_level_pv_ljt_list_assignment_v4_multi_agent.tsv`

## v4の位置づけ

v4_multi_agentは、C1中心の高熟達度英語学習者向けphrasal verb LJTのpre-audio expert review主候補版である。v3までに残っていた80から84点の12項目を再検討し、全48ターゲットを85点以上に引き上げた。

## v3からの主な変更

| Slot | v3 PV | v4 PV | v3 score | v4 score |
|---|---|---|---:|---:|
| cljt_001 | break off | break off | 80 | 91 |
| cljt_002 | hand over | hand over | 80 | 90 |
| cljt_011 | stand out | stand out | 84 | 90 |
| cljt_012 | pull back | pull back | 80 | 92 |
| cljt_013 | run out | run out | 80 | 91 |
| cljt_014 | turn over | turn over | 80 | 91 |
| cljt_016 | take back | take back | 80 | 92 |
| cljt_018 | pay off | pay off | 80 | 92 |
| cljt_020 | turn up | break out | 80 | 91 |
| cljt_028 | reach out | reach out | 84 | 92 |
| cljt_034 | take out | take out | 80 | 93 |
| cljt_041 | bring about | bring about | 80 | 91 |

既存PVを維持した項目: 11/12

置換した項目: 1/12

- `turn up` -> `break out`

## 形式検証

v4_multi_agentは以下の機械チェックを通過した。

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
| 93 | 2 |
| 92 | 7 |
| 91 | 11 |
| 90 | 12 |
| 88 | 5 |
| 86 | 5 |
| 85 | 1 |

要約:

- 平均: 90.96
- 中央値: 91
- 最小: 85
- 最大: 100
- 90点以上: 37/48
- 85点以上: 48/48
- 80点以上: 48/48
- 80点未満: 0/48

v4では、全項目が85点以上になった。これはv3からの大きな改善であり、設計段階では90点水準に到達したと判断できる。

## 残る注意項目

v4でも、以下の11項目は90点未満である。すべて85点以上ではあるが、ネイティブレビューで重点確認する。

| Slot | PV | Score | 確認点 |
|---|---|---:|---|
| cljt_004 | take up | 88 | `take up the outcome`に近い許容読みがないか確認。 |
| cljt_007 | give in | 86 | `public policy`がpressure sourceとして読まれないか確認。 |
| cljt_017 | sort out | 86 | resolve senseとunderstand senseが混在しないか確認。 |
| cljt_021 | pass on | 86 | `silence` foilが易しすぎないか確認。 |
| cljt_024 | bring out | 86 | release senseとmake-quality-noticeable senseを混同しないか確認。 |
| cljt_025 | throw out | 86 | `throw out the agenda`が許容されないか確認。 |
| cljt_038 | turn down | 88 | `turn down evidence`のlegal/register許容性を確認。 |
| cljt_048 | work out | 85 | solve/calculate senseのfoilが十分near-missか確認。 |
| cljt_028 | reach out | 92 | 高スコアだが、`reach out for legal evidence`が「証拠を求める」と読まれないか確認。 |
| cljt_013 | run out | 91 | `inspection ran out`が「検査時間が切れた」と読まれないか確認。 |
| cljt_041 | bring about | 91 | `transcript`がoutcomeとして読まれないか確認。 |

最後の3つは90点以上だが、alternate readingの余地が残るため、ネイティブレビューで個別確認する。

## 査読者としての判定

v4_multi_agentの現時点の妥当性は、100点満点で92点程度である。

強み:

- 全48ターゲットが85点以上。
- 37/48ターゲットが90点以上。
- 中央値が91。
- List A/Bの条件均衡と相補性を維持。
- 48項目設計を維持しつつ、低品質項目を大幅に改善。
- ほとんどのスロットで既存PVを保持し、元スロットの追跡性を保った。

弱み:

- スコアは設計評価であり、実測難度・弁別力ではない。
- 複数項目で法律・制度・研究文脈が増えたため、C1学習者には適切でも、背景知識依存が強くなりすぎていないか確認が必要。
- `break out`, `bring down`, `go through`など一部の置換PVは、元48リストからの変更として明示的に報告する必要がある。

推奨される次の手順:

1. v4をpre-audio expert review用の主候補版とする。
2. ネイティブスピーカー3名以上に、各ペアのacceptable自然さとunacceptable near-miss性を別々に評価させる。
3. 低評価項目だけを局所修正する。
4. レビュー通過後にElevenLabs録音用manifestへ展開する。

