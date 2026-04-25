# English Rule Space Notes

## Important truth

There is no finite, perfectly complete list of "all English morphological spelling rules" that can be enabled safely for automatic base-word extraction.

Reasons:

- English is open-ended and keeps adding new words.
- Borrowed classical forms create overlapping plural systems.
- Derivational morphology is highly ambiguous.
- Prefix stripping often changes meaning polarity rather than just spelling form.
- Many transformations are suppletive or irregular and need exceptions, not rules.

## Implemented active reverse rules

The current active rule inventory is exported in:

- `rule_inventory.csv`
- `rule_inventory.json`

These are the productive rules currently wired into the local transducer.

## Additional rule families that exist but are not safely exhaustive

### Prefix families

- `un-`
- `in- / im- / il- / ir-`
- `dis-`
- `mis-`
- `non-`
- `re-`
- `pre-`
- `post-`
- `anti-`
- `de-`
- `over-`
- `under-`
- `inter-`
- `trans-`
- `sub-`
- `super-`
- `semi-`
- `multi-`
- `micro-`
- `macro-`
- `auto-`
- `pseudo-`
- `neo-`
- `hyper-`
- `hypo-`
- `mono-`
- `bi-`
- `tri-`
- `co-`
- `counter-`
- `pro-`
- `ex-`

### High-ambiguity suffix families

- `-al`
- `-ial`
- `-ic`
- `-ical`
- `-ish`
- `-ous`
- `-ive`
- `-ative`
- `-ant`
- `-ent`
- `-ance`
- `-ence`
- `-ary`
- `-ory`
- `-age`
- `-ee`
- `-let`
- `-ling`
- `-ify`
- `-en`
- `-ism`
- `-ist`
- `-ity`
- `-ty`
- `-dom`
- `-hood`
- `-ship`
- `-ment`
- `-ness`
- `-less`
- `-ful`
- `-tion`
- `-sion`
- `-ion`
- `-ation`
- `-ization`
- `-isation`

### Classical plural pattern families

- `-ves -> -f / -fe`
- `-men -> -man`
- `-ses -> -sis`
- `-ices -> -ex / -ix`
- `-i -> -us`
- `-a -> -um / -on`
- `-ae -> -a`
- `-eaux -> -eau`

### Orthographic repair families

- `y <-> i`
- doubled consonant insertion/removal
- silent `e` deletion/restoration
- `c <-> ck` repair before `ed/ing/er`
- `ie <-> y` repair before `ing`

### Irregular exception families

These cannot be captured reliably with general spelling rules alone:

- `went -> go`
- `gone -> go`
- `better / best -> good`
- `worse / worst -> bad`
- `children -> child`
- `mice -> mouse`
- `geese -> goose`
- `teeth -> tooth`
- `feet -> foot`
- `women -> woman`
- `men -> man` is partly rule-like, but many irregular plurals still need explicit exceptions

## Practical conclusion

For a real system, the strongest design is:

1. a conservative active rule set
2. a broader catalog of possible rule families
3. an exception dictionary for irregulars
4. Trie validation and candidate scoring

That is the point where the system remains explainable without becoming too noisy.
