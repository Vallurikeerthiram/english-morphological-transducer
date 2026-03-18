// --- 1. Morphological Transducer Rules (FST Simulation) ---
const fstRules = [
    { suffix: "iest", replace: "y", name: "Superlative -> Base (iest -> y)" },
    { suffix: "ier", replace: "y", name: "Comparative -> Base (ier -> y)" },
    { suffix: "ies", replace: "y", name: "Plural/3rd Person -> Base (ies -> y)" },
    { suffix: "ing", replace: "", name: "Gerund -> Base (ing -> '')", handleDouble: true },
    { suffix: "ed", replace: "", name: "Past Tense -> Base (ed -> '')", handleDouble: true },
    { suffix: "er", replace: "", name: "Comparative -> Base (er -> '')", handleDouble: true },
    { suffix: "s", replace: "", name: "Plural -> Base (s -> '')" }
];

function generateCandidates(word, logCallback) {
    let candidates = [];
    for (let rule of fstRules) {
        if (word.endsWith(rule.suffix)) {
            let base = word.slice(0, -rule.suffix.length) + rule.replace;
            if (rule.handleDouble && rule.replace === "") {
                let stripped = word.slice(0, -rule.suffix.length);
                if (stripped.length >= 2 && stripped[stripped.length - 1] === stripped[stripped.length - 2]) {
                    let undoubled = stripped.slice(0, -1);
                    candidates.push({ word: undoubled, rule: rule.name + " + Undouble" });
                    logCallback(`Candidate: ${undoubled} (Rule: ${rule.name} + Undouble)`);
                }
            }
            candidates.push({ word: base, rule: rule.name });
            logCallback(`Candidate: ${base} (Rule: ${rule.name})`);
        }
    }
    candidates.push({ word: word, rule: "Self" });
    logCallback(`Candidate: ${word} (Self)`);
    return candidates;
}

// --- 2. Trie Logic ---
class TrieNode {
    constructor(char = '') {
        this.char = char;
        this.children = {};
        this.isEndOfWord = false;
    }
}
class Trie {
    constructor() { this.root = new TrieNode('ROOT'); }
    insert(word) {
        let current = this.root;
        for (let char of word) {
            if (!current.children[char]) current.children[char] = new TrieNode(char);
            current = current.children[char];
        }
        current.isEndOfWord = true;
    }
    search(word) {
        let current = this.root;
        for (let char of word) {
            if (!current.children[char]) return false;
            current = current.children[char];
        }
        return current.isEndOfWord;
    }
}

// --- 3. Manual Testing Script ---
const testDict = ["happy", "run", "study", "stop", "fast", "jump"];
const trie = new Trie();
testDict.forEach(w => trie.insert(w));

const testWords = ["happiest", "running", "studies", "stopped", "jumps", "faster"];

console.log("=== MANUAL LOGIC TEST RUNNER ===");
testWords.forEach(word => {
    console.log(`\nTesting Word: [${word}]`);
    const candidates = generateCandidates(word, (msg) => console.log("  - " + msg));
    
    let result = word;
    for (let cand of candidates) {
        if (trie.search(cand.word)) {
            result = cand.word;
            console.log(`  [SUCCESS] Match found in Trie: "${cand.word}"`);
            break;
        }
    }
    console.log(`  FINAL BASE WORD: ${result}`);
});
