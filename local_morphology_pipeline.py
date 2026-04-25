from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from english_words import get_english_words_set
from wordfreq import top_n_list


WORD_RE = re.compile(r"^[a-z]+$")
LONG_REPEAT_RE = re.compile(r"(.)\1{3,}")
CONSONANTS = set("bcdfghjklmnpqrstvwxyz")
PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "full_english_morphology_outputs"
NLTK_DATA_DIR = PROJECT_DIR / "nltk_data"
DEFAULT_WORDFREQ_TOP_N = 500000


@dataclass
class WordEntry:
    word: str
    definitions: list[str]
    pos_tags: list[str]
    sources: list[str]


@dataclass
class ResolutionStep:
    source: str
    target: str
    rule: str


@dataclass
class ResolutionResult:
    word: str
    final_base: str
    steps: list[ResolutionStep]
    known_word: bool


RULE_INVENTORY = [
    {"priority": 1, "rule": "iness_to_y", "suffix": "iness", "replacement": "y", "description": "Reverse iness to y.", "examples": ["happiness->happy", "airiness->airy"]},
    {"priority": 2, "rule": "iest_to_y", "suffix": "iest", "replacement": "y", "description": "Reverse iest to y.", "examples": ["happiest->happy", "easiest->easy"]},
    {"priority": 3, "rule": "ier_to_y", "suffix": "ier", "replacement": "y", "description": "Reverse ier to y.", "examples": ["happier->happy", "earlier->early"]},
    {"priority": 4, "rule": "ied_to_ie", "suffix": "ied", "replacement": "ie", "description": "Reverse ied to ie.", "examples": ["tied->tie", "untied->untie"]},
    {"priority": 5, "rule": "ied_to_y", "suffix": "ied", "replacement": "y", "description": "Reverse ied to y.", "examples": ["studied->study", "tried->try"]},
    {"priority": 6, "rule": "ies_to_ie", "suffix": "ies", "replacement": "ie", "description": "Reverse ies to ie.", "examples": ["ties->tie", "unties->untie"]},
    {"priority": 7, "rule": "ies_to_y", "suffix": "ies", "replacement": "y", "description": "Reverse ies to y.", "examples": ["studies->study", "tries->try"]},
    {"priority": 8, "rule": "ily_to_y", "suffix": "ily", "replacement": "y", "description": "Reverse ily to y.", "examples": ["easily->easy", "happily->happy"]},
    {"priority": 9, "rule": "ying_to_ie", "suffix": "ying", "replacement": "ie", "description": "Reverse ying to ie.", "examples": ["tying->tie", "dying->die"]},
    {"priority": 10, "rule": "king_to_c", "suffix": "cking", "replacement": "c", "description": "Reverse c->ck before ing.", "examples": ["panicking->panic", "mimicking->mimic"]},
    {"priority": 11, "rule": "ing_undouble", "suffix": "ing", "replacement": "undouble consonant", "description": "Reverse doubled-consonant ing.", "examples": ["running->run", "stopping->stop"]},
    {"priority": 12, "rule": "ing_add_e", "suffix": "ing", "replacement": "+e", "description": "Restore final e after ing.", "examples": ["making->make", "driving->drive"]},
    {"priority": 13, "rule": "ing_strip", "suffix": "ing", "replacement": "", "description": "Plain ing removal.", "examples": ["jumping->jump", "reading->read"]},
    {"priority": 14, "rule": "ked_to_c", "suffix": "cked", "replacement": "c", "description": "Reverse c->ck before ed.", "examples": ["panicked->panic", "frolicked->frolic"]},
    {"priority": 15, "rule": "ed_undouble", "suffix": "ed", "replacement": "undouble consonant", "description": "Reverse doubled-consonant ed.", "examples": ["stopped->stop", "planned->plan"]},
    {"priority": 16, "rule": "ed_add_e", "suffix": "ed", "replacement": "+e", "description": "Restore final e after ed.", "examples": ["loved->love", "baked->bake"]},
    {"priority": 17, "rule": "ed_strip", "suffix": "ed", "replacement": "", "description": "Plain ed removal.", "examples": ["marked->mark", "called->call"]},
    {"priority": 18, "rule": "ker_to_c", "suffix": "cker", "replacement": "c", "description": "Reverse c->ck before er.", "examples": ["panicker->panic", "mimicker->mimic"]},
    {"priority": 19, "rule": "er_undouble", "suffix": "er", "replacement": "undouble consonant", "description": "Reverse doubled-consonant er.", "examples": ["runner->run", "bigger->big"]},
    {"priority": 20, "rule": "er_add_e", "suffix": "er", "replacement": "+e", "description": "Restore final e after er.", "examples": ["closer->close", "admirer->admire"]},
    {"priority": 21, "rule": "er_strip", "suffix": "er", "replacement": "", "description": "Plain er removal.", "examples": ["player->play", "teacher->teach"]},
    {"priority": 22, "rule": "est_undouble", "suffix": "est", "replacement": "undouble consonant", "description": "Reverse doubled-consonant est.", "examples": ["biggest->big", "fattest->fat"]},
    {"priority": 23, "rule": "est_add_e", "suffix": "est", "replacement": "+e", "description": "Restore final e after est.", "examples": ["nicest->nice", "largest->large"]},
    {"priority": 24, "rule": "est_strip", "suffix": "est", "replacement": "", "description": "Plain est removal.", "examples": ["darkest->dark", "fastest->fast"]},
    {"priority": 25, "rule": "ves_to_f", "suffix": "ves", "replacement": "f", "description": "Reverse ves to f.", "examples": ["wolves->wolf", "leaves->leaf"]},
    {"priority": 26, "rule": "ves_to_fe", "suffix": "ves", "replacement": "fe", "description": "Reverse ves to fe.", "examples": ["knives->knife", "wives->wife"]},
    {"priority": 27, "rule": "men_to_man", "suffix": "men", "replacement": "man", "description": "Reverse men to man.", "examples": ["firemen->fireman", "policemen->policeman"]},
    {"priority": 28, "rule": "ses_to_sis", "suffix": "ses", "replacement": "sis", "description": "Reverse ses to sis.", "examples": ["analyses->analysis", "crises->crisis"]},
    {"priority": 29, "rule": "ices_to_ex", "suffix": "ices", "replacement": "ex", "description": "Reverse ices to ex.", "examples": ["indices->index", "vertices->vertex"]},
    {"priority": 30, "rule": "ices_to_ix", "suffix": "ices", "replacement": "ix", "description": "Reverse ices to ix.", "examples": ["appendices->appendix", "matrices->matrix"]},
    {"priority": 31, "rule": "i_to_us", "suffix": "i", "replacement": "us", "description": "Reverse i to us.", "examples": ["cacti->cactus", "stimuli->stimulus"]},
    {"priority": 32, "rule": "a_to_um", "suffix": "a", "replacement": "um", "description": "Reverse a to um.", "examples": ["data->datum", "bacteria->bacterium"]},
    {"priority": 33, "rule": "a_to_on", "suffix": "a", "replacement": "on", "description": "Reverse a to on.", "examples": ["phenomena->phenomenon", "criteria->criterion"]},
    {"priority": 34, "rule": "ae_to_a", "suffix": "ae", "replacement": "a", "description": "Reverse ae to a.", "examples": ["formulae->formula", "larvae->larva"]},
    {"priority": 35, "rule": "ability_to_able", "suffix": "ability", "replacement": "able", "description": "Reverse ability to able.", "examples": ["ability->able", "adaptability->adaptable"]},
    {"priority": 36, "rule": "ibility_to_ible", "suffix": "ibility", "replacement": "ible", "description": "Reverse ibility to ible.", "examples": ["possibility->possible", "flexibility->flexible"]},
    {"priority": 37, "rule": "ity_to_e", "suffix": "ity", "replacement": "e", "description": "Reverse ity to e.", "examples": ["activity->active", "sensitivity->sensitive"]},
    {"priority": 38, "rule": "ity_strip", "suffix": "ity", "replacement": "", "description": "Plain ity removal when valid.", "examples": ["fecundity->fecund", "morbidity->morbid"]},
    {"priority": 39, "rule": "ization_to_ize", "suffix": "ization", "replacement": "ize", "description": "Reverse ization to ize.", "examples": ["realization->realize", "organization->organize"]},
    {"priority": 40, "rule": "isation_to_ise", "suffix": "isation", "replacement": "ise", "description": "Reverse isation to ise.", "examples": ["organisation->organise", "civilisation->civilise"]},
    {"priority": 41, "rule": "ized_to_ize", "suffix": "ized", "replacement": "ize", "description": "Reverse ized to ize.", "examples": ["realized->realize", "organized->organize"]},
    {"priority": 42, "rule": "ised_to_ise", "suffix": "ised", "replacement": "ise", "description": "Reverse ised to ise.", "examples": ["organised->organise", "civilised->civilise"]},
    {"priority": 43, "rule": "izing_to_ize", "suffix": "izing", "replacement": "ize", "description": "Reverse izing to ize.", "examples": ["realizing->realize", "organizing->organize"]},
    {"priority": 44, "rule": "ising_to_ise", "suffix": "ising", "replacement": "ise", "description": "Reverse ising to ise.", "examples": ["organising->organise", "civilising->civilise"]},
    {"priority": 45, "rule": "izer_to_ize", "suffix": "izer", "replacement": "ize", "description": "Reverse izer to ize.", "examples": ["organizer->organize", "realizer->realize"]},
    {"priority": 46, "rule": "iser_to_ise", "suffix": "iser", "replacement": "ise", "description": "Reverse iser to ise.", "examples": ["organiser->organise", "advertiser->advertise"]},
    {"priority": 47, "rule": "ation_to_ate", "suffix": "ation", "replacement": "ate", "description": "Reverse ation to ate.", "examples": ["activation->activate", "creation->create"]},
    {"priority": 48, "rule": "ness_strip", "suffix": "ness", "replacement": "", "description": "Remove ness.", "examples": ["kindness->kind", "sadness->sad"]},
    {"priority": 49, "rule": "ment_strip", "suffix": "ment", "replacement": "", "description": "Remove ment.", "examples": ["development->develop", "agreement->agree"]},
    {"priority": 50, "rule": "ship_strip", "suffix": "ship", "replacement": "", "description": "Remove ship.", "examples": ["friendship->friend", "leadership->leader"]},
    {"priority": 51, "rule": "hood_strip", "suffix": "hood", "replacement": "", "description": "Remove hood.", "examples": ["childhood->child", "brotherhood->brother"]},
    {"priority": 52, "rule": "dom_strip", "suffix": "dom", "replacement": "", "description": "Remove dom.", "examples": ["freedom->free", "kingdom->king"]},
    {"priority": 53, "rule": "ful_strip", "suffix": "ful", "replacement": "", "description": "Remove ful.", "examples": ["hopeful->hope", "careful->care"]},
    {"priority": 54, "rule": "less_strip", "suffix": "less", "replacement": "", "description": "Remove less.", "examples": ["hopeless->hope", "careless->care"]},
    {"priority": 55, "rule": "ical_to_ic", "suffix": "ical", "replacement": "ic", "description": "Reverse ical to ic.", "examples": ["logical->logic", "magical->magic"]},
    {"priority": 56, "rule": "ably_to_able", "suffix": "ably", "replacement": "able", "description": "Reverse ably to able.", "examples": ["notably->notable", "comfortably->comfortable"]},
    {"priority": 57, "rule": "ibly_to_ible", "suffix": "ibly", "replacement": "ible", "description": "Reverse ibly to ible.", "examples": ["possibly->possible", "visibly->visible"]},
    {"priority": 58, "rule": "eaux_to_eau", "suffix": "eaux", "replacement": "eau", "description": "Reverse eaux to eau.", "examples": ["tableaux->tableau", "bureaux->bureau"]},
    {"priority": 59, "rule": "icity_to_ic", "suffix": "icity", "replacement": "ic", "description": "Reverse icity to ic.", "examples": ["electricity->electric", "authenticity->authentic"]},
    {"priority": 60, "rule": "osity_to_ous", "suffix": "osity", "replacement": "ous", "description": "Reverse osity to ous.", "examples": ["curiosity->curious", "generosity->generous"]},
    {"priority": 61, "rule": "ality_to_al", "suffix": "ality", "replacement": "al", "description": "Reverse ality to al.", "examples": ["normality->normal", "formality->formal"]},
    {"priority": 62, "rule": "ivity_to_ive", "suffix": "ivity", "replacement": "ive", "description": "Reverse ivity to ive.", "examples": ["productivity->productive", "creativity->creative"]},
    {"priority": 63, "rule": "ousness_to_ous", "suffix": "ousness", "replacement": "ous", "description": "Reverse ousness to ous.", "examples": ["graciousness->gracious", "seriousness->serious"]},
    {"priority": 64, "rule": "fulness_to_ful", "suffix": "fulness", "replacement": "ful", "description": "Reverse fulness to ful.", "examples": ["helpfulness->helpful", "carefulness->careful"]},
    {"priority": 65, "rule": "lessness_to_less", "suffix": "lessness", "replacement": "less", "description": "Reverse lessness to less.", "examples": ["carelessness->careless", "hopelessness->hopeless"]},
    {"priority": 66, "rule": "ance_strip", "suffix": "ance", "replacement": "", "description": "Remove ance.", "examples": ["performance->perform", "attendance->attend"]},
    {"priority": 67, "rule": "ence_strip", "suffix": "ence", "replacement": "", "description": "Remove ence.", "examples": ["existence->exist", "difference->differ"]},
    {"priority": 68, "rule": "ism_strip", "suffix": "ism", "replacement": "", "description": "Remove ism.", "examples": ["realism->real", "idealism->ideal"]},
    {"priority": 69, "rule": "ist_strip", "suffix": "ist", "replacement": "", "description": "Remove ist.", "examples": ["artist->art", "novelist->novel"]},
    {"priority": 70, "rule": "age_strip", "suffix": "age", "replacement": "", "description": "Remove age.", "examples": ["postage->post", "breakage->break"]},
    {"priority": 71, "rule": "ee_strip", "suffix": "ee", "replacement": "", "description": "Remove ee.", "examples": ["employee->employ", "escapee->escape"]},
    {"priority": 72, "rule": "or_strip", "suffix": "or", "replacement": "", "description": "Remove or.", "examples": ["actor->act", "sailor->sail"]},
    {"priority": 73, "rule": "ster_strip", "suffix": "ster", "replacement": "", "description": "Remove ster.", "examples": ["youngster->young", "songster->song"]},
    {"priority": 74, "rule": "ling_strip", "suffix": "ling", "replacement": "", "description": "Remove ling.", "examples": ["duckling->duck", "gosling->goose"]},
    {"priority": 75, "rule": "let_strip", "suffix": "let", "replacement": "", "description": "Remove let.", "examples": ["booklet->book", "leaflet->leaf"]},
    {"priority": 76, "rule": "en_strip", "suffix": "en", "replacement": "", "description": "Remove en.", "examples": ["wooden->wood", "golden->gold"]},
    {"priority": 77, "rule": "ward_strip", "suffix": "ward", "replacement": "", "description": "Remove ward.", "examples": ["homeward->home", "eastward->east"]},
    {"priority": 78, "rule": "wise_strip", "suffix": "wise", "replacement": "", "description": "Remove wise.", "examples": ["clockwise->clock", "moneywise->money"]},
    {"priority": 79, "rule": "ically_to_ical", "suffix": "ically", "replacement": "ical", "description": "Reverse ically to ical.", "examples": ["magically->magical", "logically->logical"]},
    {"priority": 80, "rule": "ally_to_al", "suffix": "ally", "replacement": "al", "description": "Reverse ally to al.", "examples": ["formally->formal", "accidentally->accidental"]},
    {"priority": 81, "rule": "ally_to_ic", "suffix": "ally", "replacement": "ic", "description": "Reverse ally to ic.", "examples": ["basically->basic", "logically->logic"]},
    {"priority": 82, "rule": "able_add_e", "suffix": "able", "replacement": "+e", "description": "Restore final e after able.", "examples": ["lovable->love", "blamable->blame"]},
    {"priority": 83, "rule": "able_strip", "suffix": "able", "replacement": "", "description": "Remove able.", "examples": ["readable->read", "adaptable->adapt"]},
    {"priority": 84, "rule": "ible_strip", "suffix": "ible", "replacement": "", "description": "Remove ible.", "examples": ["accessible->access", "digestible->digest"]},
    {"priority": 85, "rule": "ion_strip", "suffix": "ion", "replacement": "", "description": "Remove ion when valid.", "examples": ["adoption->adopt", "action->act"]},
    {"priority": 86, "rule": "tion_to_t", "suffix": "tion", "replacement": "t", "description": "Reverse tion to t.", "examples": ["action->act", "adoption->adopt"]},
    {"priority": 87, "rule": "tion_to_te", "suffix": "tion", "replacement": "te", "description": "Reverse tion to te.", "examples": ["relation->relate", "deletion->delete"]},
    {"priority": 88, "rule": "sion_to_se", "suffix": "sion", "replacement": "se", "description": "Reverse sion to se.", "examples": ["revision->revise", "explosion->explode?"]},
    {"priority": 89, "rule": "sion_to_de", "suffix": "sion", "replacement": "de", "description": "Reverse sion to de.", "examples": ["decision->decide", "division->divide"]},
    {"priority": 90, "rule": "al_strip", "suffix": "al", "replacement": "", "description": "Remove al.", "examples": ["national->nation", "formal->form"]},
    {"priority": 91, "rule": "ic_strip", "suffix": "ic", "replacement": "", "description": "Remove ic.", "examples": ["heroic->hero", "atomic->atom"]},
    {"priority": 92, "rule": "ous_strip", "suffix": "ous", "replacement": "", "description": "Remove ous.", "examples": ["dangerous->danger", "poisonous->poison"]},
    {"priority": 93, "rule": "ious_to_y", "suffix": "ious", "replacement": "y", "description": "Reverse ious to y.", "examples": ["mysterious->mystery", "injurious->injury"]},
    {"priority": 94, "rule": "eous_to_e", "suffix": "eous", "replacement": "e", "description": "Reverse eous to e.", "examples": ["advantageous->advantage", "outrageous->outrage"]},
    {"priority": 95, "rule": "ary_strip", "suffix": "ary", "replacement": "", "description": "Remove ary.", "examples": ["planetary->planet", "imaginary->imagine?"]},
    {"priority": 96, "rule": "ant_strip", "suffix": "ant", "replacement": "", "description": "Remove ant.", "examples": ["assistant->assist", "claimant->claim"]},
    {"priority": 97, "rule": "ent_strip", "suffix": "ent", "replacement": "", "description": "Remove ent.", "examples": ["dependent->depend", "resident->reside"]},
    {"priority": 98, "rule": "ly_strip", "suffix": "ly", "replacement": "", "description": "Remove ly.", "examples": ["quickly->quick", "calmly->calm"]},
    {"priority": 99, "rule": "es_strip", "suffix": "es", "replacement": "", "description": "Remove es when valid.", "examples": ["wishes->wish", "goes->go"]},
    {"priority": 100, "rule": "s_strip", "suffix": "s", "replacement": "", "description": "Remove s when valid.", "examples": ["runs->run", "cats->cat"]},
    {"priority": 101, "rule": "identity", "suffix": "", "replacement": "", "description": "Keep the word unchanged.", "examples": ["run->run", "happy->happy"]},
]
RULE_PRIORITY = {item["rule"]: item["priority"] for item in RULE_INVENTORY}


class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.terminal = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            node = node.children.setdefault(char, TrieNode())
        node.terminal = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            node = node.children.get(char)
            if node is None:
                return False
        return node.terminal


def ensure_wordnet():
    import nltk

    NLTK_DATA_DIR.mkdir(parents=True, exist_ok=True)
    if str(NLTK_DATA_DIR) not in nltk.data.path:
        nltk.data.path.insert(0, str(NLTK_DATA_DIR))

    for resource in ("wordnet", "omw-1.4"):
        try:
            nltk.data.find(f"corpora/{resource}")
        except LookupError:
            nltk.download(resource, download_dir=str(NLTK_DATA_DIR), quiet=False)

    from nltk.corpus import wordnet as wn

    return wn


def normalize_word(raw_word: str) -> str | None:
    word = raw_word.replace("_", " ").lower().strip()
    if " " in word:
        return None
    if not WORD_RE.fullmatch(word):
        return None
    if LONG_REPEAT_RE.search(word):
        return None
    if len(word) < 2:
        return None
    return word


def build_wordnet_lexicon() -> dict[str, WordEntry]:
    wn = ensure_wordnet()
    entries: dict[str, dict[str, set[str]]] = {}

    for synset in wn.all_synsets():
        definition = synset.definition().strip()
        pos_tag = synset.pos()
        for lemma in synset.lemmas():
            word = normalize_word(lemma.name())
            if word is None:
                continue

            record = entries.setdefault(
                word,
                {"definitions": set(), "pos_tags": set(), "sources": set()},
            )
            if definition:
                record["definitions"].add(definition)
            record["pos_tags"].add(pos_tag)
            record["sources"].add("wordnet")

    lexicon: dict[str, WordEntry] = {}
    for word in sorted(entries):
        record = entries[word]
        lexicon[word] = WordEntry(
            word=word,
            definitions=sorted(record["definitions"]),
            pos_tags=sorted(record["pos_tags"]),
            sources=sorted(record["sources"]),
        )

    return lexicon


def merge_source_words(
    lexicon: dict[str, WordEntry],
    words: set[str],
    source_name: str,
) -> None:
    for word in words:
        entry = lexicon.get(word)
        if entry is None:
            lexicon[word] = WordEntry(
                word=word,
                definitions=[],
                pos_tags=[],
                sources=[source_name],
            )
            continue

        if source_name not in entry.sources:
            entry.sources.append(source_name)
            entry.sources.sort()


def build_merged_lexicon(wordfreq_top_n: int) -> tuple[dict[str, WordEntry], dict[str, int]]:
    lexicon = build_wordnet_lexicon()

    web2_words = {
        normalized
        for raw_word in get_english_words_set(["web2"], lower=True)
        if (normalized := normalize_word(raw_word)) is not None
    }
    gcide_words = {
        normalized
        for raw_word in get_english_words_set(["gcide"], lower=True)
        if (normalized := normalize_word(raw_word)) is not None
    }
    wordfreq_words = {
        normalized
        for raw_word in top_n_list("en", wordfreq_top_n)
        if (normalized := normalize_word(raw_word)) is not None
    }

    merge_source_words(lexicon, web2_words, "web2")
    merge_source_words(lexicon, gcide_words, "gcide")
    merge_source_words(lexicon, wordfreq_words, "wordfreq")

    source_counts = {
        "wordnet_words": sum("wordnet" in entry.sources for entry in lexicon.values()),
        "web2_words": sum("web2" in entry.sources for entry in lexicon.values()),
        "gcide_words": sum("gcide" in entry.sources for entry in lexicon.values()),
        "wordfreq_words": sum("wordfreq" in entry.sources for entry in lexicon.values()),
        "defined_words": sum(bool(entry.definitions) for entry in lexicon.values()),
        "undefined_words": sum(not entry.definitions for entry in lexicon.values()),
    }
    return lexicon, source_counts


def is_doubled_consonant(text: str) -> bool:
    return len(text) >= 2 and text[-1] == text[-2] and text[-1] in CONSONANTS


def add_candidate(
    candidates: list[tuple[str, str]],
    seen: set[str],
    candidate: str,
    rule_name: str,
) -> None:
    if len(candidate) < 2:
        return
    if not WORD_RE.fullmatch(candidate):
        return
    if candidate in seen:
        return
    seen.add(candidate)
    candidates.append((candidate, rule_name))


def generate_candidates(word: str) -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []
    seen: set[str] = set()

    if word.endswith("iness") and len(word) > 6:
        add_candidate(candidates, seen, word[:-5] + "y", "iness_to_y")

    if word.endswith("iest") and len(word) > 5:
        add_candidate(candidates, seen, word[:-4] + "y", "iest_to_y")

    if word.endswith("ier") and len(word) > 4:
        add_candidate(candidates, seen, word[:-3] + "y", "ier_to_y")

    if word.endswith("ied") and len(word) > 4:
        add_candidate(candidates, seen, word[:-3] + "ie", "ied_to_ie")

    if word.endswith("ied") and len(word) > 4:
        add_candidate(candidates, seen, word[:-3] + "y", "ied_to_y")

    if word.endswith("ies") and len(word) > 4:
        add_candidate(candidates, seen, word[:-3] + "ie", "ies_to_ie")

    if word.endswith("ies") and len(word) > 4:
        add_candidate(candidates, seen, word[:-3] + "y", "ies_to_y")

    if word.endswith("ily") and len(word) > 4:
        add_candidate(candidates, seen, word[:-3] + "y", "ily_to_y")

    if word.endswith("ying") and len(word) > 4:
        add_candidate(candidates, seen, word[:-4] + "ie", "ying_to_ie")

    if word.endswith("cking") and len(word) > 6:
        add_candidate(candidates, seen, word[:-5] + "c", "king_to_c")

    if word.endswith("ing") and len(word) > 5:
        stem = word[:-3]
        if is_doubled_consonant(stem):
            add_candidate(candidates, seen, stem[:-1], "ing_undouble")
        add_candidate(candidates, seen, stem + "e", "ing_add_e")
        add_candidate(candidates, seen, stem, "ing_strip")

    if word.endswith("cked") and len(word) > 5:
        add_candidate(candidates, seen, word[:-4] + "c", "ked_to_c")

    if word.endswith("ed") and len(word) > 4:
        stem = word[:-2]
        if is_doubled_consonant(stem):
            add_candidate(candidates, seen, stem[:-1], "ed_undouble")
        add_candidate(candidates, seen, stem + "e", "ed_add_e")
        add_candidate(candidates, seen, stem, "ed_strip")

    if word.endswith("cker") and len(word) > 5:
        add_candidate(candidates, seen, word[:-4] + "c", "ker_to_c")

    if word.endswith("er") and len(word) > 4:
        stem = word[:-2]
        if is_doubled_consonant(stem):
            add_candidate(candidates, seen, stem[:-1], "er_undouble")
        add_candidate(candidates, seen, stem + "e", "er_add_e")
        add_candidate(candidates, seen, stem, "er_strip")

    if word.endswith("est") and len(word) > 5:
        stem = word[:-3]
        if is_doubled_consonant(stem):
            add_candidate(candidates, seen, stem[:-1], "est_undouble")
        add_candidate(candidates, seen, stem + "e", "est_add_e")
        add_candidate(candidates, seen, stem, "est_strip")

    if word.endswith("ves") and len(word) > 4:
        add_candidate(candidates, seen, word[:-3] + "f", "ves_to_f")
        add_candidate(candidates, seen, word[:-3] + "fe", "ves_to_fe")

    if word.endswith("men") and len(word) > 4:
        add_candidate(candidates, seen, word[:-3] + "man", "men_to_man")

    if word.endswith("ses") and len(word) > 4:
        add_candidate(candidates, seen, word[:-2] + "is", "ses_to_sis")

    if word.endswith("ices") and len(word) > 5:
        add_candidate(candidates, seen, word[:-4] + "ex", "ices_to_ex")
        add_candidate(candidates, seen, word[:-4] + "ix", "ices_to_ix")

    if word.endswith("i") and len(word) > 3:
        add_candidate(candidates, seen, word[:-1] + "us", "i_to_us")

    if word.endswith("ae") and len(word) > 3:
        add_candidate(candidates, seen, word[:-2] + "a", "ae_to_a")

    if word.endswith("a") and len(word) > 3:
        add_candidate(candidates, seen, word[:-1] + "um", "a_to_um")
        add_candidate(candidates, seen, word[:-1] + "on", "a_to_on")

    if word.endswith("eaux") and len(word) > 5:
        add_candidate(candidates, seen, word[:-1], "eaux_to_eau")

    if word.endswith("ability") and len(word) > 6:
        add_candidate(candidates, seen, word[:-7] + "able", "ability_to_able")

    if word.endswith("ibility") and len(word) > 6:
        add_candidate(candidates, seen, word[:-7] + "ible", "ibility_to_ible")

    if word.endswith("icity") and len(word) > 6:
        add_candidate(candidates, seen, word[:-5] + "ic", "icity_to_ic")

    if word.endswith("osity") and len(word) > 6:
        add_candidate(candidates, seen, word[:-5] + "ous", "osity_to_ous")

    if word.endswith("ality") and len(word) > 6:
        add_candidate(candidates, seen, word[:-5] + "al", "ality_to_al")

    if word.endswith("ivity") and len(word) > 6:
        add_candidate(candidates, seen, word[:-5] + "ive", "ivity_to_ive")

    if word.endswith("ity") and len(word) > 5:
        add_candidate(candidates, seen, word[:-3] + "e", "ity_to_e")
        add_candidate(candidates, seen, word[:-3], "ity_strip")

    if word.endswith("ization") and len(word) > 8:
        add_candidate(candidates, seen, word[:-7] + "ize", "ization_to_ize")

    if word.endswith("isation") and len(word) > 8:
        add_candidate(candidates, seen, word[:-7] + "ise", "isation_to_ise")

    if word.endswith("ized") and len(word) > 5:
        add_candidate(candidates, seen, word[:-4] + "ize", "ized_to_ize")

    if word.endswith("ised") and len(word) > 5:
        add_candidate(candidates, seen, word[:-4] + "ise", "ised_to_ise")

    if word.endswith("izing") and len(word) > 6:
        add_candidate(candidates, seen, word[:-5] + "ize", "izing_to_ize")

    if word.endswith("ising") and len(word) > 6:
        add_candidate(candidates, seen, word[:-5] + "ise", "ising_to_ise")

    if word.endswith("izer") and len(word) > 5:
        add_candidate(candidates, seen, word[:-4] + "ize", "izer_to_ize")

    if word.endswith("iser") and len(word) > 5:
        add_candidate(candidates, seen, word[:-4] + "ise", "iser_to_ise")

    if word.endswith("ation") and len(word) > 6:
        add_candidate(candidates, seen, word[:-5] + "ate", "ation_to_ate")

    if word.endswith("ousness") and len(word) > 8:
        add_candidate(candidates, seen, word[:-7] + "ous", "ousness_to_ous")

    if word.endswith("fulness") and len(word) > 8:
        add_candidate(candidates, seen, word[:-7] + "ful", "fulness_to_ful")

    if word.endswith("lessness") and len(word) > 9:
        add_candidate(candidates, seen, word[:-8] + "less", "lessness_to_less")

    if word.endswith("ness") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4], "ness_strip")

    if word.endswith("ment") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4], "ment_strip")

    if word.endswith("ance") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4], "ance_strip")

    if word.endswith("ence") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4], "ence_strip")

    if word.endswith("ism") and len(word) > 5:
        add_candidate(candidates, seen, word[:-3], "ism_strip")

    if word.endswith("ist") and len(word) > 5:
        add_candidate(candidates, seen, word[:-3], "ist_strip")

    if word.endswith("age") and len(word) > 6:
        add_candidate(candidates, seen, word[:-3], "age_strip")

    if word.endswith("ee") and len(word) > 5:
        add_candidate(candidates, seen, word[:-2], "ee_strip")

    if word.endswith("or") and len(word) > 4:
        add_candidate(candidates, seen, word[:-2], "or_strip")

    if word.endswith("ster") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4], "ster_strip")

    if word.endswith("ling") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4], "ling_strip")

    if word.endswith("let") and len(word) > 5:
        add_candidate(candidates, seen, word[:-3], "let_strip")

    if word.endswith("en") and len(word) > 5:
        add_candidate(candidates, seen, word[:-2], "en_strip")

    if word.endswith("ward") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4], "ward_strip")

    if word.endswith("wise") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4], "wise_strip")

    if word.endswith("ship") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4], "ship_strip")

    if word.endswith("hood") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4], "hood_strip")

    if word.endswith("dom") and len(word) > 5:
        add_candidate(candidates, seen, word[:-3], "dom_strip")

    if word.endswith("ful") and len(word) > 5:
        add_candidate(candidates, seen, word[:-3], "ful_strip")

    if word.endswith("less") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4], "less_strip")

    if word.endswith("ical") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4] + "ic", "ical_to_ic")

    if word.endswith("ically") and len(word) > 8:
        add_candidate(candidates, seen, word[:-6] + "ical", "ically_to_ical")

    if word.endswith("ally") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4] + "al", "ally_to_al")
        add_candidate(candidates, seen, word[:-4] + "ic", "ally_to_ic")

    if word.endswith("ably") and len(word) > 5:
        add_candidate(candidates, seen, word[:-4] + "able", "ably_to_able")

    if word.endswith("ibly") and len(word) > 5:
        add_candidate(candidates, seen, word[:-4] + "ible", "ibly_to_ible")

    if word.endswith("able") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4] + "e", "able_add_e")
        add_candidate(candidates, seen, word[:-4], "able_strip")

    if word.endswith("ible") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4], "ible_strip")

    if word.endswith("sion") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4] + "se", "sion_to_se")
        add_candidate(candidates, seen, word[:-4] + "de", "sion_to_de")

    if word.endswith("tion") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4] + "t", "tion_to_t")
        add_candidate(candidates, seen, word[:-4] + "te", "tion_to_te")

    if word.endswith("ion") and len(word) > 5:
        add_candidate(candidates, seen, word[:-3], "ion_strip")

    if word.endswith("al") and len(word) > 6:
        add_candidate(candidates, seen, word[:-2], "al_strip")

    if word.endswith("ic") and len(word) > 5:
        add_candidate(candidates, seen, word[:-2], "ic_strip")

    if word.endswith("ious") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4] + "y", "ious_to_y")

    if word.endswith("eous") and len(word) > 6:
        add_candidate(candidates, seen, word[:-4] + "e", "eous_to_e")

    if word.endswith("ous") and len(word) > 6:
        add_candidate(candidates, seen, word[:-3], "ous_strip")

    if word.endswith("ary") and len(word) > 6:
        add_candidate(candidates, seen, word[:-3], "ary_strip")

    if word.endswith("ant") and len(word) > 6:
        add_candidate(candidates, seen, word[:-3], "ant_strip")

    if word.endswith("ent") and len(word) > 6:
        add_candidate(candidates, seen, word[:-3], "ent_strip")

    if word.endswith("ly") and len(word) > 4:
        add_candidate(candidates, seen, word[:-2], "ly_strip")

    if word.endswith("es") and len(word) > 4:
        add_candidate(candidates, seen, word[:-2], "es_strip")

    if word.endswith("s") and len(word) > 3 and not word.endswith(("ss", "us", "is")):
        add_candidate(candidates, seen, word[:-1], "s_strip")

    add_candidate(candidates, seen, word, "identity")
    return candidates


def build_trie(lexicon: dict[str, WordEntry]) -> Trie:
    trie = Trie()
    for word in lexicon:
        trie.insert(word)
    return trie


def candidate_score(
    candidate: str,
    rule_name: str,
    lexicon: dict[str, WordEntry],
) -> tuple[int, int, int, int, int]:
    entry = lexicon.get(
        candidate,
        WordEntry(word=candidate, definitions=[], pos_tags=[], sources=[]),
    )
    return (
        len(entry.sources),
        int(bool(entry.definitions)),
        int("wordnet" in entry.sources),
        int("wordfreq" in entry.sources),
        -RULE_PRIORITY.get(rule_name, 999),
    )


def resolve_immediate_base(
    word: str,
    trie: Trie,
    lexicon: dict[str, WordEntry],
) -> tuple[str, str]:
    valid_candidates = [
        (candidate, rule_name)
        for candidate, rule_name in generate_candidates(word)
        if candidate != word and trie.search(candidate)
    ]
    if valid_candidates:
        candidate, rule_name = max(
            valid_candidates,
            key=lambda item: candidate_score(item[0], item[1], lexicon),
        )
        return candidate, rule_name
    if trie.search(word):
        return word, "identity"
    return word, "unresolved"


def resolve_base(
    word: str,
    trie: Trie,
    lexicon: dict[str, WordEntry],
    max_steps: int = 4,
) -> ResolutionResult:
    current = word
    visited = {word}
    steps: list[ResolutionStep] = []

    for _ in range(max_steps):
        candidate, rule_name = resolve_immediate_base(current, trie, lexicon)
        if candidate == current:
            break
        steps.append(ResolutionStep(source=current, target=candidate, rule=rule_name))
        current = candidate
        if current in visited:
            break
        visited.add(current)

    return ResolutionResult(
        word=word,
        final_base=current,
        steps=steps,
        known_word=trie.search(word),
    )


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_rule_inventory(output_dir: Path) -> None:
    rule_rows = [
        {
            "priority": str(item["priority"]),
            "rule": item["rule"],
            "suffix": item["suffix"],
            "replacement": item["replacement"],
            "description": item["description"],
            "examples": " | ".join(item["examples"]),
        }
        for item in RULE_INVENTORY
    ]
    write_csv(
        output_dir / "rule_inventory.csv",
        rule_rows,
        ["priority", "rule", "suffix", "replacement", "description", "examples"],
    )
    with (output_dir / "rule_inventory.json").open("w", encoding="utf-8") as handle:
        json.dump(RULE_INVENTORY, handle, indent=2)


def analyze_lexicon(
    lexicon: dict[str, WordEntry],
    source_counts: dict[str, int],
    output_dir: Path,
    preview_groups: int,
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_rule_inventory(output_dir)

    trie = build_trie(lexicon)

    dictionary_rows: list[dict[str, str]] = []
    mapping_rows: list[dict[str, str]] = []
    groups: dict[str, list[str]] = defaultdict(list)
    selected_rule_counts: Counter[str] = Counter()
    valid_candidate_counts: Counter[str] = Counter()
    selected_rule_examples: dict[str, list[str]] = defaultdict(list)
    valid_candidate_examples: dict[str, list[str]] = defaultdict(list)

    for word, entry in lexicon.items():
        dictionary_rows.append(
            {
                "word": word,
                "sources": "|".join(sorted(entry.sources)),
                "pos_tags": "|".join(entry.pos_tags),
                "definitions": " | ".join(entry.definitions[:5]),
            }
        )

        seen_valid_rules: set[str] = set()
        for candidate, rule_name in generate_candidates(word):
            if candidate != word and trie.search(candidate):
                if rule_name not in seen_valid_rules:
                    valid_candidate_counts[rule_name] += 1
                    seen_valid_rules.add(rule_name)
                    if len(valid_candidate_examples[rule_name]) < 12:
                        valid_candidate_examples[rule_name].append(f"{word}->{candidate}")

        resolution = resolve_base(word, trie, lexicon)
        immediate_rule = resolution.steps[0].rule if resolution.steps else "identity"
        selected_rule_counts[immediate_rule] += 1
        if len(selected_rule_examples[immediate_rule]) < 12:
            selected_rule_examples[immediate_rule].append(
                f"{word}->{resolution.final_base}"
            )

        groups[resolution.final_base].append(word)
        mapping_rows.append(
            {
                "word": word,
                "final_base": resolution.final_base,
                "sources": "|".join(sorted(entry.sources)),
                "known_word": str(resolution.known_word),
                "step_count": str(len(resolution.steps)),
                "rule_chain": " > ".join(step.rule for step in resolution.steps) or "identity",
                "path": " > ".join(
                    f"{step.source}->{step.target}" for step in resolution.steps
                )
                or word,
                "definitions": " | ".join(entry.definitions[:3]),
            }
        )

    group_rows = []
    for base_word, words in sorted(groups.items()):
        sorted_words = sorted(words)
        group_rows.append(
            {
                "base_word": base_word,
                "group_size": str(len(sorted_words)),
                "words": "|".join(sorted_words),
            }
        )

    selected_rule_rows = [
        {
            "rule": rule_name,
            "selected_count": str(count),
            "examples": " | ".join(selected_rule_examples[rule_name]),
        }
        for rule_name, count in selected_rule_counts.most_common()
    ]

    valid_rule_rows = [
        {
            "rule": rule_name,
            "valid_candidate_count": str(count),
            "examples": " | ".join(valid_candidate_examples[rule_name]),
        }
        for rule_name, count in valid_candidate_counts.most_common()
    ]

    write_csv(
        output_dir / "dictionary_with_meanings.csv",
        dictionary_rows,
        ["word", "sources", "pos_tags", "definitions"],
    )
    write_csv(
        output_dir / "word_to_base.csv",
        mapping_rows,
        ["word", "final_base", "sources", "known_word", "step_count", "rule_chain", "path", "definitions"],
    )
    write_csv(
        output_dir / "base_groups.csv",
        group_rows,
        ["base_word", "group_size", "words"],
    )
    write_csv(
        output_dir / "selected_rule_summary.csv",
        selected_rule_rows,
        ["rule", "selected_count", "examples"],
    )
    write_csv(
        output_dir / "valid_candidate_summary.csv",
        valid_rule_rows,
        ["rule", "valid_candidate_count", "examples"],
    )

    with (output_dir / "base_groups.json").open("w", encoding="utf-8") as handle:
        json.dump(
            {base: sorted(words) for base, words in sorted(groups.items())},
            handle,
            indent=2,
            sort_keys=True,
        )

    preview = []
    for index, (base, words) in enumerate(sorted(groups.items())):
        if index >= preview_groups:
            break
        preview.append({"base": base, "size": len(words), "words": sorted(words)[:12]})

    sample_lookup_words = [
        "happy",
        "happier",
        "happiest",
        "happiness",
        "run",
        "running",
        "runner",
        "study",
        "studies",
        "studied",
        "making",
        "easily",
        "ties",
        "tying",
        "panicked",
        "wolves",
        "analyses",
        "realization",
        "ability",
    ]
    sample_resolutions = []
    for word in sample_lookup_words:
        resolution = resolve_base(word, trie, lexicon)
        sample_resolutions.append(
            {
                "word": word,
                "final_base": resolution.final_base,
                "rule_chain": [step.rule for step in resolution.steps] or ["identity"],
                "path": [f"{step.source}->{step.target}" for step in resolution.steps] or [word],
            }
        )

    summary = {
        "lexicon_size": len(lexicon),
        "group_count": len(groups),
        "source_counts": source_counts,
        "top_selected_rules": selected_rule_counts.most_common(15),
        "top_valid_candidate_rules": valid_candidate_counts.most_common(15),
        "sample_resolutions": sample_resolutions,
        "rule_count": len(RULE_INVENTORY),
        "preview_groups": preview,
        "coverage_note": (
            "This is a very large merged English lexicon from WordNet, WEB2, GCIDE, and wordfreq. "
            "It is broad but still not a mathematically complete list of every possible English word."
        ),
    }

    with (output_dir / "analysis_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    return summary


def run_lookups(
    words: list[str],
    lexicon: dict[str, WordEntry],
    output_dir: Path,
) -> list[dict[str, object]]:
    trie = build_trie(lexicon)
    results = []

    for raw_word in words:
        word = normalize_word(raw_word)
        if word is None:
            continue
        resolution = resolve_base(word, trie, lexicon)
        base_entry = lexicon.get(
            resolution.final_base,
            WordEntry(word=resolution.final_base, definitions=[], pos_tags=[], sources=[]),
        )
        results.append(
            {
                "word": word,
                "final_base": resolution.final_base,
                "base_sources": base_entry.sources,
                "rule_chain": [step.rule for step in resolution.steps] or ["identity"],
                "path": [f"{step.source}->{step.target}" for step in resolution.steps] or [word],
                "base_definitions": base_entry.definitions[:5],
            }
        )

    if results:
        with (output_dir / "lookup_results.json").open("w", encoding="utf-8") as handle:
            json.dump(results, handle, indent=2)

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a large local English morphology analysis with Trie validation and spelling rules."
    )
    parser.add_argument(
        "--wordfreq-top-n",
        type=int,
        default=DEFAULT_WORDFREQ_TOP_N,
        help="How many top English wordfreq entries to merge. Values above 500000 saturate at the package maximum.",
    )
    parser.add_argument(
        "--preview-groups",
        type=int,
        default=20,
        help="Number of grouped bases to preview in the JSON summary.",
    )
    parser.add_argument(
        "--lookup",
        nargs="*",
        default=[],
        help="Optional words to resolve directly against the merged Trie.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    lexicon, source_counts = build_merged_lexicon(wordfreq_top_n=args.wordfreq_top_n)
    summary = analyze_lexicon(
        lexicon=lexicon,
        source_counts=source_counts,
        output_dir=OUTPUT_DIR,
        preview_groups=args.preview_groups,
    )

    print(f"Lexicon size: {summary['lexicon_size']}")
    print(f"Group count: {summary['group_count']}")
    print("Source coverage:")
    for key, value in summary["source_counts"].items():
        print(f"  {key}: {value}")
    print("Top selected rules:")
    for rule_name, count in summary["top_selected_rules"][:10]:
        print(f"  {rule_name}: {count}")
    print("Sample resolutions:")
    for item in summary["sample_resolutions"]:
        print(
            f"  {item['word']} -> {item['final_base']} "
            f"via {' > '.join(item['rule_chain'])}"
        )
    if args.lookup:
        lookup_results = run_lookups(args.lookup, lexicon, OUTPUT_DIR)
        print("Lookup results:")
        for item in lookup_results:
            print(
                f"  {item['word']} -> {item['final_base']} "
                f"via {' > '.join(item['rule_chain'])}"
            )
    print(f"Rule inventory written to: {OUTPUT_DIR / 'rule_inventory.csv'}")
    print(f"Outputs written to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
