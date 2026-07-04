# Cレベル向けPV-LJT: マルチエージェント候補統合メモ v3

作成日: 2026-07-04

目的: v3_multi_agentで80から84点に残っていた最後の12項目を再検討し、可能な限り既存PVを維持しながら、C1中心のaural phrasal verb LJTとして90点水準へ近づける。

## 対象項目

| Slot | v3 PV | v3 score | 主な問題 |
|---|---|---:|---|
| cljt_001 | break off | 80 | `proposal`が交渉文脈でやや許容されうる。 |
| cljt_002 | hand over | 80 | prisoner/arrestがやや人物/出来事の粗い差に寄る。 |
| cljt_011 | stand out | 84 | 比較集合の制御が弱く、一般意味で解ける可能性がある。 |
| cljt_012 | pull back | 80 | `approval`が抽象的すぎ、near-missとして不安定。 |
| cljt_013 | run out | 80 | samples/findingsはresource cueが強い。 |
| cljt_014 | turn over | 80 | records/permissionは目的語制限がやや粗い。 |
| cljt_016 | take back | 80 | lead/lossはスポーツ結果の対比がやや表層的。 |
| cljt_018 | pay off | 80 | investment/invoiceはintransitive/transitive senseの競合が残る。 |
| cljt_020 | turn up | 80 | arrival senseが透明で、increase/found readingsも競合する。 |
| cljt_028 | reach out | 84 | patients/symptomsは人/非人の手がかりが強い。 |
| cljt_034 | take out | 80 | mortgage/receiptはliteral removal readingが残る。 |
| cljt_041 | bring about | 80 | reforms/changeは一般的すぎ、target senseをほぼ言い換えている。 |

## 採用した改稿

| Slot | v4 PV | v4 score | Acceptable | Unacceptable | 採用理由 |
|---|---|---:|---|---|---|
| cljt_001 | break off | 91 | The union broke off negotiations before arbitration. | The union broke off concessions before arbitration. | negotiations/concessionsで同一交渉domainを維持しつつ、終了可能な活動と交渉条件を分けた。 |
| cljt_002 | hand over | 90 | The agency handed over the investigation to prosecutors. | The agency handed over the verdict to prosecutors. | responsibility transferとlegal outcomeを同一法務domainで対比。 |
| cljt_011 | stand out | 90 | One bid stood out among tenders. | One bid stood out among invoices. | procurement documents内で、比較集合として成立するものと成立しにくいものを対比。 |
| cljt_012 | pull back | 92 | The investors pulled back from the funding round. | The investors pulled back from the valuation. | finance-deal domainで、withdrawal対象の活動/commitmentと評価値を対比。 |
| cljt_013 | run out | 91 | The permit ran out during the audit. | The inspection ran out during the audit. | resource depletionからexpiry/validity senseへ変更し、透明性を下げた。 |
| cljt_014 | turn over | 91 | The suspect turned over evidence to police. | The suspect turned over charges to police. | authority-transfer senseで、possessed materialとlegal actionを対比。 |
| cljt_016 | take back | 92 | The party took back the seat. | The party took back the turnout. | election domainで、regain可能なpositionとresult measureを対比。 |
| cljt_018 | pay off | 92 | The firm paid off the loan after restructuring. | The firm paid off the forecast after restructuring. | debt-settlement senseに固定し、payable obligationとestimateを対比。 |
| cljt_020 | break out | 91 | A dispute broke out during mediation. | A settlement broke out during mediation. | `turn up`を置換。arrival senseが透明すぎるため、event-onset senseへ変更。 |
| cljt_028 | reach out | 92 | The client reached out for legal advice. | The client reached out for legal evidence. | contactable-recipient cueを避け、help-seeking complementに変更。 |
| cljt_034 | take out | 93 | The landlord took out a flood policy. | The landlord took out a flood claim. | insurance domainで、obtained productとfiled claimを対比。 |
| cljt_041 | bring about | 91 | The ruling brought about a retrial. | The ruling brought about a transcript. | legal cause-result frameで、institutional outcomeとrecordを対比。 |

## 置換判断

今回、既存PVを置換したのは1項目のみである。

| Slot | v3 PV | v4 PV | 理由 |
|---|---|---|---|
| cljt_020 | turn up | break out | `turn up`はarrival senseが透明で、appear/increase/foundなどのsense競合も強い。`break out`は候補プール内にあり、mediation domainで同一ドメインnear-missを作れる。 |

## 採用しなかった候補

| 候補 | 理由 |
|---|---|
| `draw up` for cljt_014 | 高品質だが候補プール外。`turn over`を91点水準まで改善できたため保留。 |
| `pan out` for cljt_018 | 高品質だが候補プール外。`pay off`をdebt-settlement senseで92点まで改善できたため保留。 |
| `roll out` for cljt_020 | 高品質だが候補プール外。候補プール内の`break out`で十分に改善できたため不採用。 |
| `iron out` for cljt_041 | 高品質だが候補プール外。`bring about`をlegal outcome frameで91点まで改善できたため保留。 |
| `close down`などの安定した置換候補 | 既存PVを維持できる項目が多く、リスト全体の元スロット追跡性を優先した。 |

## v4の到達点

出力ファイル:

- `c_level_pv_ljt_48_target_master_v4_multi_agent.tsv`
- `c_level_pv_ljt_list_assignment_v4_multi_agent.tsv`
- `c_level_pv_ljt_list_A_v4_multi_agent.tsv`
- `c_level_pv_ljt_list_B_v4_multi_agent.tsv`

検証結果:

- 48ターゲット / 96文
- List A: acceptable 24 / unacceptable 24
- List B: acceptable 24 / unacceptable 24
- A/Bは全ターゲットで相補的
- ターゲットPVは全項目で第3語以降
- 文長は全項目で5から10語
- 同一条件の連続は各リスト最大3試行
- 機械検証上の問題は0件

スコア改善:

- v3平均: 88.29
- v4平均: 90.96
- v3中央値: 90
- v4中央値: 91
- v3の90点以上: 25/48
- v4の90点以上: 37/48
- v3の85点以上: 36/48
- v4の85点以上: 48/48

査読者としての評価:

v4は、設計段階では90点水準の主候補版として扱える。全項目が85点以上になり、90点以上も37/48まで増えた。残る課題は、机上評価ではなく、ネイティブスピーカーによるacceptable自然さとunacceptable near-miss性の実査読である。

