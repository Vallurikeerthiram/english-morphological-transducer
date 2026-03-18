# English Morphology Rule Note

## Scope

This note aims to collect the largest practical catalog of English morphological rule families for base-word analysis.

Important limitation:

- There is no single finite, universally agreed list of "all English rules".
- English is open-ended, keeps borrowing new forms, and has many irregular lexical exceptions.
- So the best realistic target is a very large catalog of rule families, not a mathematically complete final list.

This note therefore separates:

1. high-confidence inflectional and spelling rules
2. broader productive derivational rule families
3. classical and learned alternations
4. prefix families
5. morphophonemic stem-alternation families
6. irregular and suppletive exceptions

## Current Project Count

In the current project codebase, the active implemented reverse-rule inventory is `101` rules.

Those `101` implemented rules are:

### Implemented y/i and vowel alternation rules

- `iness_to_y`
- `iest_to_y`
- `ier_to_y`
- `ied_to_ie`
- `ied_to_y`
- `ies_to_ie`
- `ies_to_y`
- `ily_to_y`
- `ying_to_ie`

### Implemented progressive and past reversal rules

- `king_to_c`
- `ing_undouble`
- `ing_add_e`
- `ing_strip`
- `ked_to_c`
- `ed_undouble`
- `ed_add_e`
- `ed_strip`

### Implemented comparative and superlative reversal rules

- `ker_to_c`
- `er_undouble`
- `er_add_e`
- `er_strip`
- `est_undouble`
- `est_add_e`
- `est_strip`

### Implemented plural and classical plural reversal rules

- `ves_to_f`
- `ves_to_fe`
- `men_to_man`
- `ses_to_sis`
- `ices_to_ex`
- `ices_to_ix`
- `i_to_us`
- `a_to_um`
- `a_to_on`
- `ae_to_a`
- `eaux_to_eau`
- `es_strip`
- `s_strip`

### Implemented core derivational reversal rules

- `ability_to_able`
- `ibility_to_ible`
- `ity_to_e`
- `ity_strip`
- `ization_to_ize`
- `isation_to_ise`
- `ized_to_ize`
- `ised_to_ise`
- `izing_to_ize`
- `ising_to_ise`
- `izer_to_ize`
- `iser_to_ise`
- `ation_to_ate`
- `ness_strip`
- `ment_strip`
- `ship_strip`
- `hood_strip`
- `dom_strip`
- `ful_strip`
- `less_strip`
- `ical_to_ic`
- `ably_to_able`
- `ibly_to_ible`
- `ly_strip`

### Implemented expanded derivational and learned reversal rules

- `icity_to_ic`
- `osity_to_ous`
- `ality_to_al`
- `ivity_to_ive`
- `ousness_to_ous`
- `fulness_to_ful`
- `lessness_to_less`
- `ance_strip`
- `ence_strip`
- `ism_strip`
- `ist_strip`
- `age_strip`
- `ee_strip`
- `or_strip`
- `ster_strip`
- `ling_strip`
- `let_strip`
- `en_strip`
- `ward_strip`
- `wise_strip`
- `ically_to_ical`
- `ally_to_al`
- `ally_to_ic`
- `able_add_e`
- `able_strip`
- `ible_strip`
- `ion_strip`
- `tion_to_t`
- `tion_to_te`
- `sion_to_se`
- `sion_to_de`
- `al_strip`
- `ic_strip`
- `ous_strip`
- `ious_to_y`
- `eous_to_e`
- `ary_strip`
- `ant_strip`
- `ent_strip`

### Implemented fallback rule

- `identity`

## A. Highest-Confidence Inflectional Rule Families

These are the safest rules for a rule-based base extractor.

### Number and agreement

- plural `-s`: `cat -> cats`
- plural `-es`: `box -> boxes`, `wish -> wishes`
- plural `-ies`: `study -> studies`
- plural `-ves`: `wolf -> wolves`, `knife -> knives`
- plural `-men`: `man -> men`, `fireman -> firemen`
- plural `-en`: `ox -> oxen`
- zero plural: `sheep -> sheep`, `deer -> deer`
- 3rd person singular `-s`: `run -> runs`
- 3rd person singular `-es`: `go -> goes`, `wash -> washes`
- 3rd person singular `-ies`: `try -> tries`

### Tense and aspect

- past `-ed`: `walk -> walked`
- past participle `-ed`: `paint -> painted`
- progressive `-ing`: `jump -> jumping`

### Degree

- comparative `-er`: `tall -> taller`
- comparative `-ier`: `happy -> happier`
- superlative `-est`: `fast -> fastest`
- superlative `-iest`: `happy -> happiest`

### Adverbial

- adverbial `-ly`: `quick -> quickly`
- adverbial `-ily`: `easy -> easily`

## B. Core Orthographic Repair Rules

These are the most important spelling transformations used when attaching or removing suffixes.

### Final consonant doubling

- double final consonant before vowel suffix: `run -> running`, `stop -> stopped`
- reverse undoubling: `running -> run`, `stopped -> stop`
- multisyllabic stress-sensitive doubling: `prefer -> preferred`, `admit -> admitted`
- non-doubling with unstressed final syllables: `open -> opening`
- non-doubling with final `w`, `x`, `y`: `snowing`, `boxed`, `playing`

### Silent e rules

- drop silent `e` before vowel-initial suffix: `make -> making`, `love -> loving`
- restore silent `e` in reverse: `making -> make`, `loved -> love`
- retain `e` before consonant-initial suffix in many cases: `safe -> safely`

### y and i alternations

- `y -> i` before many suffixes: `happy -> happier`, `study -> studied`
- reverse `i -> y`: `happier -> happy`, `studied -> study`
- no `y -> i` before `-ing`: `study -> studying`
- `ie -> y` before `-ing`: `tie -> tying`, `die -> dying`
- reverse `ying -> ie`: `tying -> tie`, `dying -> die`

### c and ck alternations

- `c -> ck` before `-ed`, `-ing`, `-er`: `panic -> panicked`, `mimic -> mimicking`
- reverse `ck -> c`: `panicked -> panic`, `panicker -> panic`

### Sibilant-triggered es

- add `-es` after `s`, `x`, `z`, `sh`, `ch`: `bus -> buses`, `watch -> watches`
- reverse `-es` removal when valid: `wishes -> wish`

## C. Regular Reverse Mapping Families

These are common reverse rules for spelling-based base extraction.

- `-iness -> y`: `happiness -> happy`
- `-iest -> y`: `happiest -> happy`
- `-ier -> y`: `happier -> happy`
- `-ied -> y`: `studied -> study`
- `-ies -> y`: `studies -> study`
- `-ied -> ie`: `tied -> tie`
- `-ies -> ie`: `ties -> tie`
- `-ily -> y`: `easily -> easy`
- `-ying -> ie`: `tying -> tie`
- `-ing -> base`
- `-ing -> base + e`
- `-ing -> undoubled base`
- `-ed -> base`
- `-ed -> base + e`
- `-ed -> undoubled base`
- `-er -> base`
- `-er -> base + e`
- `-er -> undoubled base`
- `-est -> base`
- `-est -> base + e`
- `-est -> undoubled base`
- `-ness -> base`
- `-ly -> base`
- `-es -> base`
- `-s -> base`

## D. Classical and Learned Plural Families

These matter a lot if you want broad English coverage.

- `-ves -> -f`: `wolves -> wolf`, `leaves -> leaf`
- `-ves -> -fe`: `knives -> knife`, `wives -> wife`
- `-men -> -man`: `firemen -> fireman`, `policemen -> policeman`
- `-ses -> -sis`: `analyses -> analysis`, `crises -> crisis`
- `-ices -> -ex`: `indices -> index`, `vertices -> vertex`
- `-ices -> -ix`: `appendices -> appendix`, `matrices -> matrix`
- `-i -> -us`: `cacti -> cactus`, `stimuli -> stimulus`
- `-a -> -um`: `bacteria -> bacterium`, `data -> datum`
- `-a -> -on`: `criteria -> criterion`, `phenomena -> phenomenon`
- `-ae -> -a`: `formulae -> formula`, `larvae -> larva`
- `-eaux -> -eau`: `tableaux -> tableau`
- `-ices -> -is` in some specialized words
- learned double plural options: `indexes/indices`, `appendixes/appendices`

## E. Productive Derivational Suffix Rule Families

These create new lexemes, so they are less safe than inflectional rules. They still matter if the project aims for broad base-word grouping.

### 1. Verb -> Noun

- `-ing`: `build -> building`
- `-er`: `teach -> teacher`
- `-or`: `act -> actor`
- `-ee`: `employ -> employee`
- `-ment`: `develop -> development`
- `-al`: `approve -> approval`
- `-ance`: `perform -> performance`
- `-ence`: `exist -> existence`
- `-tion`: `create -> creation`
- `-sion`: `revise -> revision`
- `-ion`: `permit -> permission`
- `-ation`: `activate -> activation`
- `-ization`: `realize -> realization`
- `-isation`: `organise -> organisation`
- `-age`: `post -> postage`
- `-ure`: `fail -> failure`
- `-ery`: `brew -> brewery`
- `-ry`: `husband -> husbandry`
- `-ent / -ant` in some learned patterns

### 2. Verb -> Adjective

- `-able`: `read -> readable`
- `-ible`: `access -> accessible`
- `-ive`: `act -> active`
- `-ative`: `talk -> talkative`
- `-ant`: `please -> pleasant` historically related
- `-ent`: `depend -> dependent`
- `-ed`: `talent -> talented` or participial adjective
- `-ing`: `amuse -> amusing`
- `-ory`: `observe -> observatory` type learned families

### 3. Verb -> Verb

- `-ize / -ise`
- `-ify`
- `-ate`
- `-en`

### 4. Adjective -> Noun

- `-ness`: `kind -> kindness`
- `-ity`: `active -> activity`
- `-ty`: `loyal -> loyalty`
- `-ism`: `ideal -> idealism`
- `-ity -> e` reverse families: `active <- activity`
- `-ability`: `adaptable <- adaptability`
- `-ibility`: `possible <- possibility`

### 5. Adjective -> Adverb

- `-ly`: `quick -> quickly`
- `-ily`: `easy -> easily`
- `-wise`: `clockwise`, `moneywise`
- `-ward / -wards`: `homeward`, `afterwards`

### 6. Adjective -> Verb

- `-en`: `weak -> weaken`
- `-ize / -ise`: `modern -> modernize`
- `-ify`: `simple -> simplify`

### 7. Noun -> Adjective

- `-al`: `nation -> national`
- `-ial`: `substance -> substantial`
- `-ic`: `atom -> atomic`
- `-ical`: `logic -> logical`
- `-ous`: `danger -> dangerous`
- `-ious`: `mystery -> mysterious`
- `-eous`: `advantage -> advantageous`
- `-ary`: `planet -> planetary`
- `-ory`: `memory -> memorial / advisory type families`
- `-less`: `hope -> hopeless`
- `-ful`: `care -> careful`
- `-y`: `cloud -> cloudy`
- `-ish`: `child -> childish`
- `-like`: `child -> childlike`
- `-esque`: `picture -> picturesque`
- `-en`: `wood -> wooden`
- `-ed`: `talent -> talented`

### 8. Noun -> Noun

- `-hood`: `child -> childhood`
- `-ship`: `friend -> friendship`
- `-dom`: `king -> kingdom`
- `-ism`: `hero -> heroism`
- `-ist`: `art -> artist`
- `-ess`: `actor -> actress`
- `-let`: `book -> booklet`
- `-ling`: `duck -> duckling`
- `-ster`: `gang -> gangster`
- `-ian`: `music -> musician`
- `-ite`: `Israel -> Israelite`, mineral and learned uses
- `-ry`: `jewel -> jewelry`
- `-ery`: `slavery`, `bravery`, place/type families

### 9. Noun -> Verb

- zero derivation: `hammer -> hammer`, `email -> email`
- `-ize / -ise`: `hospital -> hospitalize`
- `-ify`: `glory -> glorify`
- `-ate`: `origin -> originate`
- `en- / em-`: `slave -> enslave`

## F. Reverse Derivational Families Often Needed for Base Extraction

These are especially useful if the project wants lemma-like grouping beyond pure inflection.

- `-ability -> -able`
- `-ibility -> -ible`
- `-ity -> -e`
- `-ity -> base`
- `-ization -> -ize`
- `-isation -> -ise`
- `-ized -> -ize`
- `-ised -> -ise`
- `-izing -> -ize`
- `-ising -> -ise`
- `-izer -> -ize`
- `-iser -> -ise`
- `-ation -> -ate`
- `-ment -> base`
- `-ship -> base`
- `-hood -> base`
- `-dom -> base`
- `-ful -> base`
- `-less -> base`
- `-ical -> -ic`
- `-ably -> -able`
- `-ibly -> -ible`

## G. Prefix Rule Families

Prefixes usually keep the word class but change meaning.

### 1. Negation / opposite

- `un-`
- `in-`
- `im-`
- `il-`
- `ir-`
- `dis-`
- `non-`

### 2. Reversal / removal

- `de-`
- `un-`
- `dis-`

### 3. Repetition / again

- `re-`

### 4. Opposition / counteraction

- `anti-`
- `counter-`

### 5. Degree / excess / deficiency

- `over-`
- `under-`
- `super-`
- `sub-`
- `hyper-`
- `hypo-`
- `ultra-`
- `extra-`

### 6. Time / order

- `pre-`
- `post-`
- `fore-`

### 7. Number / quantity

- `mono-`
- `uni-`
- `bi-`
- `di-`
- `tri-`
- `multi-`
- `poly-`
- `semi-`
- `demi-`

### 8. Position / relation / movement

- `inter-`
- `intra-`
- `trans-`
- `sub-`
- `super-`
- `circum-`
- `peri-`
- `infra-`
- `retro-`

### 9. Identity / orientation

- `auto-`
- `pseudo-`
- `neo-`
- `pro-`
- `co-`
- `ex-`
- `vice-`
- `arch-`

### 10. Size / scale

- `micro-`
- `macro-`
- `mini-`
- `maxi-`

## H. Prefix Assimilation and Allomorphy

These are not new meanings, but important shape changes.

- `in- -> im-` before labials: `impossible`
- `in- -> il-` before `l`: `illegal`
- `in- -> ir-` before `r`: `irregular`
- `ad- -> ac-`: `accede`
- `ad- -> af-`: `affect`
- `ad- -> ag-`: `aggression`
- `ad- -> al-`: `allude`
- `ad- -> an-`: `announce`
- `ad- -> ap-`: `appoint`
- `ad- -> ar-`: `arrive`
- `ad- -> as-`: `assimilate`
- `ad- -> at-`: `attach`
- `con- -> com-`: `combine`
- `con- -> col-`: `collect`
- `con- -> cor-`: `correct`
- `sub- -> suf-`, `sug-`, `sup-`, `sus-`
- `ob- -> oc-`, `of-`, `op-`

## I. Morphophonemic Stem Alternation Families

These are real English morphological patterns, but they are much harder than simple suffix stripping.

- `describe -> description`
- `prescribe -> prescription`
- `revise -> revision`
- `decide -> decision`
- `expand -> expansion`
- `extend -> extension`
- `permit -> permission`
- `admit -> admission`
- `receive -> reception`
- `conceive -> conception`
- `resolve -> resolution`
- `derive -> derivation`
- `create -> creation`
- `sane -> sanity`
- `profane -> profanity`
- `clear -> clarity`
- `able <- ability`
- `possible <- possibility`
- `profound -> profundity`
- `long -> length`
- `strong -> strength`

These are often better handled as learned alternation families or lexical mappings.

## J. Conversion / Zero-Derivation

English very often changes category without visible spelling change.

- noun -> verb: `email`, `hammer`, `host`
- verb -> noun: `run`, `walk`, `call`
- adjective -> verb: `clean`, `empty`
- adjective -> noun: `poor`, `rich`

These are morphological but cannot be reversed by spelling change alone.

## K. Irregular and Suppletive Families

These are not safe general rules. They need an exception lexicon.

### Irregular verb families

- `go -> went / gone`
- `be -> am / is / are / was / were / been`
- `have -> has / had`
- `do -> does / did / done`
- `say -> says / said`
- `make -> made`
- `take -> took / taken`
- `come -> came`
- `see -> saw / seen`
- `eat -> ate / eaten`
- `write -> wrote / written`
- `speak -> spoke / spoken`
- `break -> broke / broken`
- `drive -> drove / driven`
- `sing -> sang / sung`
- `ring -> rang / rung`
- `drink -> drank / drunk`
- `give -> gave / given`
- `know -> knew / known`
- `grow -> grew / grown`

### Suppletive adjective families

- `good -> better -> best`
- `bad -> worse -> worst`
- `far -> farther/further -> farthest/furthest`

### Irregular plural families

- `mouse -> mice`
- `goose -> geese`
- `tooth -> teeth`
- `foot -> feet`
- `louse -> lice`
- `person -> people`
- `child -> children`
- `brother -> brethren` in restricted use

## L. Practical Grouping of Rule Types for Your Project

If the project is about base-word extraction using spelling only, then the rule space should be divided into layers.

### Layer 1: safest active rules

- plural / 3rd person / past / progressive / comparative / superlative
- y/i alternations
- silent e restoration
- consonant undoubling
- c/ck repair

### Layer 2: moderately safe expansions

- `-ness`
- `-ly`
- `-ment`
- `-ship`
- `-hood`
- `-dom`
- `-ful`
- `-less`
- `-ation`
- `-ization`
- `-ability`
- `-ibility`

### Layer 3: high-ambiguity learned derivation

- `-tion`
- `-sion`
- `-ion`
- `-ity`
- `-ive`
- `-ous`
- `-al`
- `-ic`
- `-ical`
- Latinate stem alternations

### Layer 4: exceptions only

- irregular verbs
- suppletive comparatives
- irregular plurals
- lexicalized historical forms

## M. Bottom-Line Estimate

If you ask how many "possible rules" there are in a serious English morphology catalog, a realistic answer is:

- around `20-30` core inflection and spelling-repair rule families
- around `60-120+` productive derivational rule families
- around `25-40+` productive prefix families
- around `10-20+` classical plural and learned inflection families
- plus large irregular exception inventories

So English morphology is not a `61-rule` problem.

`61` can be a reasonable engineered active rule set, but the wider rule space is much larger.

## References

This note synthesizes standard English morphology using these accessible references:

- UFLI on suffix spelling changes such as doubling, drop-e, and y-to-i:
  https://ufli.education.ufl.edu/foundations/toolbox/107-110/
- Britannica on allomorphy and English plural/past allomorphs:
  https://www.britannica.com/topic/allomorph
- NYU MorphLab on derivational affix systems in English:
  https://wp.nyu.edu/morphlab/2020/09/15/stacking-derivational-affixes/
- Pressbooks chapter on English derivational morphology:
  https://udel.pressbooks.pub/language/chapter/5-5-derivational-morphology/
- Monmouth handout on prefix assimilation:
  https://department.monm.edu/classics/coursearchivetjs/clas224/Handouts/assimilation_of_prefixes.htm
- SIL glossary entry on morphology terminology:
  https://glossary.sil.org/node/13211
