# Cレベル向けPV-LJT設計仕様書 v1

状態: 設計仕様書。まだproduction刺激セットではない。

目的: CEFR C1中心の高熟達度英語学習者を対象に、英語句動詞
(phrasal verbs; PVs) の自動化された音声語彙知識と文脈内使用知識を
測定する48ターゲット・複数リスト型の音声LJTを開発する。

この文書は `c_level_pv_ljt_design_spec_v1.md` の日本語版である。
レビュー入力用の採点表は `c_level_pv_ljt_item_review_rubric_v1.tsv` を使う。

## 1. 測定構成概念

このLJTが測るべきものは、学習者が短い音声文の中でPVを聞き取り、
そのPVが当該文脈で意味的・コロケーション的に適切かを素早く判断
できるかである。

測定対象ではないもの:

- 書字提示によるPV意味認識
- 孤立音声PVの既知/未知判断
- 明示的な翻訳知識
- 広い意味での文法性判断
- 不自然な名詞、あり得ない出来事、一般常識違反の検出

測定対象:

- PV音声形式の認識
- 意図されたPV senseの検索
- 文脈内使用知識: 意味適合性、コロケーション制約、項構造、レジスター、
  局所談話への適合
- リスニング条件下での十分に速く安定した検索

Uchihara et al. (2025) では、LJTはmeaning recognitionやmeaning recall
とは異なる、自動化された音声語彙知識の指標として位置づけられている。
ただしPVでは多義性が強く、unacceptable文が単なる名詞カテゴリ異常で
解けてしまう危険が大きいため、単語版LJTよりも構成概念の絞り込みを
厳しくする必要がある。

## 2. 文献からの設計原則

### Uchihara et al. (2025)

指定論文は、音声提示された短文を一度聞き、ターゲット語が文脈内で
意味的に適切かを判断するLJTを開発している。LJTはTOEIC Listeningを
meaning recognition/recallよりよく予測し、宣言的知識ではなく自動化
された音声語彙知識を反映すると解釈されている。

PV-LJTへの含意:

- 書字ではなく音声提示にする。
- 文は短くする。
- ターゲットPVを文頭に置かない。
- 非ターゲット語彙は易しく保つ。
- 複雑な構文を避け、文法テスト化しない。
- acceptable/unacceptableの両条件を作る。
- native/expert reviewでキーが明確になるまで改稿する。
- 主指標は正答性、RTや再生回数は副次的プロセス指標とする。

### LJTの発展研究

Saito et al. (2024) のトレーニング研究や、Saito et al. (2026) の
timed/untimed LJT研究は、use-in-contextの語彙知識がリスニングに近い
測定対象であることを補強している。時間制限は自動化解釈を支えるが、
妥当性は厳しい時間制限そのものより、音声・文脈・項目品質に依存する。

設計上は、main trialでは一度だけ音声を提示し、長い熟考を避ける。
ただし締切秒数は事前pilotで決めるべきで、恣意的に短くしない。

### Judgment task方法論

Plonsky et al. (2020) と Ionin & Zyzik (2014) は、judgment taskの得点が
提示モダリティ、timing、文脈、尺度、報告方法に左右されることを示す。
したがってPV-LJTでは、項目数、条件バランス、反応時間測定、練習試行、
ランダム化、信頼性、項目レビューを明示的に記録する。

### Aural PV knowledge

Cheng et al. (2022) は、音声PV知識がL2リスニング理解と関連し、単語知識
に加えて説明力を持つことを示している。PV選定では、頻度、意味の不透明性、
sense選定、音声提示が重要である。

PV-LJTへの含意:

- PV formではなくPV senseを選ぶ。
- 透明な方向・身体動作だけで解けるsenseは避ける。
- できる限りcontiguous formを使い、提示形式を標準化する。
- rater reference documentで正答senseを明文化する。

### PV頻度・sense・多義性

Gardner & Davies (2007), Liu (2011), Garnier & Schmitt (2015), Sonbul et al.
(2020) から、PVはform単位ではなくsense単位で扱う必要がある。
高頻度PVでも、対象senseが低頻度だったり、短文内で安定して切り出せない
場合はLJTターゲットとして不適切である。

## 3. C1対象者に合わせた難易度方針

対象者はC1中心であり、一般英語力・明示的語彙知識・多くの基本PV form
への親しみは高いと想定する。したがって、難しさはPV formの未知性では
なく、文脈内でのsense選択、collocation、register、argument structure
に置く。

設計方針:

- literal particle meaningだけで解ける項目を避ける。
- あり得ない名詞で解ける項目を避ける。
- academic/professional/institutional/interpersonalな文脈を優先する。
- 非ターゲット語彙は簡単にする。
- 文を長くしたり構文を複雑にしたりして難化しない。

## 4. ターゲット選定ルール

本番セットは48 scored PV targetsを維持する。ただし既存48 PVを無理に
保持する必要はない。Cレベル向け妥当性を優先し、弱いPVやsenseは差し替える。

各ターゲットに必要なメタデータ:

- `pv_id`
- `pv`
- `target_sense`
- `source`
- `raw_frequency_source`
- `sense_frequency_source`
- `opacity_or_transparency_rating`
- `register_focus`
- `polysemy_risk`
- `construct_fit`
- `replacement_status`
- `rationale`

優先ソース:

1. 現在のmaster listと既存audit
2. Sonbul/El-Dakhsのsense-level PVデータ
3. PHaVE Listとuser manual
4. Gardner & DaviesおよびLiuの頻度・register情報
5. 必要に応じた追加corpus check

保持条件:

- 意図senseが短文内で明確に特定できる。
- same-domainのunacceptable near-missが作れる。
- common alternate senseでunacceptable文がacceptableにならない。
- 特殊イントネーションに依存しない。
- C1に適切で、簡単すぎず、希少すぎない。
- 非ターゲット語彙を易しく保てる。

差し替え条件:

- discourse markerでprosodyがキーを決める。
- 多義性が強すぎ、短文で安定しない。
- unacceptable文が不可能名詞・非常識イベントでしか作れない。
- C1学習者がparticle directionalityだけで解ける。
- acceptable文が辞書例文のようで自然でない。
- native/expert ratersがキーに合意しない。

既存v6 auditに基づく差し替え優先PV:

- replace/rewrite: `give out`, `put in`, `take in`, `sit back`, `hold back`,
  `come along`, `get down`, `put out`, `clean up`, `keep up`, `look out`,
  `look back`, `go up`, `go down`, `come in`
- drop候補: `make out`, `come on`

## 5. 文作成仕様

各PVにはacceptable文とunacceptable文を1つずつ作る。したがって48 PVに
対して96文候補を作る。ただし1人の参加者が同一PVを2回見ることは避け、
各リストでは各PVを1条件のみ提示する。

### 文長

標準は5-9語。自然性が明確に上がる場合のみ4語または10語を許容する。
作業記憶や構文処理を測らないよう、文は短く保つ。

### ターゲット位置

PVを文頭に置かない。望ましい構造は以下:

- subject + PV + object/complement
- subject + auxiliary + PV + object/complement
- 必要に応じて短い前置詞句

避けるもの:

- 文頭2語以内のターゲット
- 最終語だけでキーが分かる配置
- 長いlead-in

### 構文

原則として1つのfinite clauseのみ。関係節、複雑な従属節、入れ子のidiom、
不必要な受動態を避ける。

### 非ターゲット語彙

C1には易しい語彙を使う。希少名詞、専門語、文化依存の固有知識で
難化しない。

### acceptable文

acceptable文は、意図senseで自然で、通常の英語として成立し、senseを
説明しすぎない。近くに同義語・パラフレーズを置かない。

### unacceptable文

unacceptable文は、対象PV senseが局所文脈に合わないために不適切で
なければならない。単なるナンセンスではなくnear-missにする。

良いnear-miss:

- 同じ研究領域内のtask vs proposition
- 同じ法的/学術領域内のevidence vs outcome
- 同じ制度文脈内のrole vs event
- 同じ情報提示文脈内のprocess vs document component

悪いnear-miss:

- person vs furniture
- event vs pencil
- `deadline` を汎用wrong objectとして反復
- 主語の有生性だけで解ける
- 不可能な物理行為
- 数値の上下だけで解けるincrease/decrease

### 禁止cue

以下は使わない:

- `but`, `although`, `however`
- `never`, `no`, `nothing`
- 明示的な反意語ペア
- 数量変化だけで解ける表現
- 皮肉・sarcasm・特殊イントネーション
- 談話の不連続性だけで答えが分かる文

## 6. 複数リスト設計

基本は2リスト設計とする。

- List A: 48 trials, acceptable 24 / unacceptable 24
- List B: 各PVについてList Aと逆条件
- 各参加者は各PVを1回だけ見る。
- List A/Bを合わせると全PVでacceptable/unacceptableの両方が観測される。

これはUchihara et al.のpaired scoringとは異なる。原典では同一ターゲット
のappropriate/inappropriate両方を得点に使うが、本設計では反復露出と疲労を
避けるためcounterbalanced PV-LJTとして実施する。論文・報告ではこの違いを
明記する。

リスト内制約:

- acceptable/unacceptable 24/24
- sourceとregisterをできるだけ均衡
- 同一反応は最大2連続
- 同じbase verbは可能なら8試行以上離す
- 同じparticleは可能なら4試行以上離す
- high-risk itemを連続させない

参加者割付:

- list A/B
- male/female voice
- F/J response mapping

本番版では、これらをparticipant IDから自動割付し、参加者に選ばせない。

## 7. 音声・タイミング

ElevenLabs TTSは継続使用する。ただしTTS出力はproduction-ready音声ではなく、
recording candidateとして扱う。

音声生成:

- male/female各1声
- model/output formatは固定
- manifestを保存
- API keyはmaterialsやmanifestに残さない
- file name/pathを固定

音声レビュー項目:

- 文が完全に読まれている
- clipping/noiseなし
- loudnessが概ね揃っている
- verbとparticleの間に不自然なpauseがない
- particleに不自然な強勢がない
- prosodyがacceptable/unacceptableを漏らさない
- PVの発音が曖昧でない
- 演技調で意味が変わらない

推奨pilot設定:

- main trialは1回再生
- replayは原則なし
- RTはaudio offsetから測る
- 6秒でsoft warning
- timeoutはpilot結果を見て10秒程度を検討

## 8. 練習試行

練習は手続きを教えるためのもので、解法方略を教えてはならない。

要件:

- 6-8 trials
- acceptable/unacceptableを均衡
- main target PVを使わない
- 同一PVのacceptable/unacceptableを連続提示しない
- real-real-real-foil-foilのようなパターンを作らない
- feedbackはpracticeのみ
- mainではfeedbackなし

## 9. 項目レビュー採点ルーブリック

各PVペアは100点で採点する。production候補は90点以上、かつcritical gate
を1つも失敗しないこと。

配点:

- PV-sense dependency: 25
- near-miss quality: 20
- cue control: 15
- polysemy and alternate-sense control: 15
- acceptable sentence naturalness: 10
- audio robustness: 10
- C1 suitability: 5

critical gate:

- common senseでunacceptable文がacceptableになるならreject
- absurd nounやimpossible eventで解けるならreject
- native/expert ratersがキーに合意しないならrevise/reject
- TTS prosodyでキーが反転し得るならreject/re-record

解釈:

- 90-100: production candidate
- 80-89: minor revision candidate
- 70-79: major revision candidate
- 70未満: targetまたはpairを作り直す

機械監査は必要条件であって十分条件ではない。語数、overt cue、target form
が合格でも、構成概念妥当性は保証されない。

## 10. native/expert validation

production freeze前の最低条件:

1. 英語母語話者2名が各文を独立評価する。
2. 応用言語学または語彙/PV研究者1名がpair rationaleを確認する。
3. 不一致は多数決でなく改稿で解決する。
4. 改稿後に再評価する。

文レベル評価:

- acceptable item naturalness
- unacceptable item unambiguity
- PV-sense dependency
- general cue risk
- alternate-sense risk
- audio suitability

pair-level decision:

- keep
- revise minor
- revise major
- replace target/sense
- drop

## 11. 参加者得点化

trial score:

- 1 = responseがkeyと一致
- 0 = incorrect, timeout, missing

person score:

- total correct out of 48
- percent correct

必ず別報告:

- acceptable accuracy
- unacceptable accuracy
- response bias
- correct no-replay trialsのmedian RT
- timeout rate
- replay/flag rate

pilot item analysis:

- item facility
- discrimination
- condition-specific accuracy
- RT distribution
- list effect
- voice effect
- response-key effect
- shared verb/particleによるlocal dependence

## 12. production freeze条件

以下を満たすまで新セットを`production`と呼ばない。

- 48 targetsの最終keep decisionがある。
- 96 sentence candidatesにexpert ratingsがある。
- 2 voices x 96 audio filesがaudio reviewを通過している。
- frozen item poolからList A/Bが生成されている。
- practice trialsがmain targetと独立している。
- production manifestが使用ファイルを一意に示す。
- READMEにcurrent production versionとanalysis join tableが1つだけ明記されている。
- 古いファイルはhistoricalとして区別されている。

推奨ファイル名:

- `aural_pv_ljt_items_v7_c_level_freeze.tsv`
- `aural_pv_ljt_list_A_v7_c_level_freeze.tsv`
- `aural_pv_ljt_list_B_v7_c_level_freeze.tsv`
- `pilot_trial_file_ljt_list_A_v7_c_level_freeze.tsv`
- `pilot_trial_file_ljt_list_B_v7_c_level_freeze.tsv`

## 13. 次の作業

1. 17個のweak/drop targetに対するreplacement candidate poolを作る。
2. frequency, opacity, register, C1 suitabilityで48 target sensesを再選定する。
3. 各targetにacceptable/unacceptable文を1つずつ作る。
4. 語数、target position、repeated nouns、overt cues、same-domain labels、
   list balanceを自動監査する。
5. `c_level_pv_ljt_item_review_rubric_v1.tsv` を使ってexpert review formを作る。
6. review通過後にのみElevenLabs音声を生成する。

## 参考文献

- Cheng, J., Matthews, J., Lange, K., & McLean, S. (2022). Aural single-word
  and aural phrasal verb knowledge and their relationships to L2 listening
  comprehension. TESOL Quarterly. https://doi.org/10.1002/tesq.3137
- Gardner, D., & Davies, M. (2007). Pointing out frequent phrasal verbs: A
  corpus-based analysis. TESOL Quarterly, 41(2), 339-359.
  https://doi.org/10.1002/j.1545-7249.2007.tb00062.x
- Garnier, M., & Schmitt, N. (2015). The PHaVE list: A pedagogical list of
  phrasal verbs and their most frequent meaning senses. Language Teaching
  Research, 19(6), 645-666. https://doi.org/10.1177/1362168814559798
- Ionin, T., & Zyzik, E. (2014). Judgment and interpretation tasks in second
  language research. Annual Review of Applied Linguistics, 34, 37-64.
  https://doi.org/10.1017/S0267190514000026
- Liu, D. (2011). The most frequently used English phrasal verbs in American
  and British English: A multicorpus examination. TESOL Quarterly, 45(4),
  661-688.
- Plonsky, L., Marsden, E., Crowther, D., Gass, S. M., & Spinner, P. (2020).
  A methodological synthesis and meta-analysis of judgment tasks in second
  language research. Second Language Research, 36(4), 583-621.
  https://doi.org/10.1177/0267658319828413
- Read, J. (2023). Towards a new sophistication in vocabulary assessment.
  Language Testing, 40(1), 40-46. https://doi.org/10.1177/02655322221125698
- Saito, K., Hosaka, I., Suzukida, Y., Takizawa, K., & Uchihara, T. (2026).
  Timed vs. untimed lexicosemantic judgement task for measuring automatized
  phonological vocabulary knowledge. Second Language Research.
  https://doi.org/10.1177/02676583261420616
- Saito, K., Uchihara, T., Takizawa, K., & Suzukida, Y. (2024). Declarative and
  automatized phonological vocabulary knowledge in L2 listening proficiency:
  A training study. Applied Psycholinguistics, 45(6), 1187-1218.
  https://doi.org/10.1017/S0142716424000468
- Sonbul, S., Salam El-Dakhs, D. A., & Al-Otaibi, H. (2020). Productive versus
  receptive L2 knowledge of polysemous phrasal verbs: A comparison of
  determining factors. System, 95, 102361.
  https://doi.org/10.1016/j.system.2020.102361
- Uchihara, T., Saito, K., Kurokawa, S., Takizawa, K., & Suzukida, Y. (2025).
  Declarative and automatized phonological vocabulary knowledge:
  Recognition, recall, lexicosemantic judgment, and listening-focused
  employability of second language words. Language Learning, 75(2), 458-492.
  https://doi.org/10.1111/lang.12668

