// --- 1. Morphological Transducer (FST) Rule Inventory ---
const fstRuleLayers = [
    [{ suffix: "iness", replace: "y", name: "iness -> y" }, { suffix: "iest", replace: "y", name: "iest -> y" }, { suffix: "ier", replace: "y", name: "ier -> y" }, { suffix: "ily", replace: "y", name: "ily -> y" }],
    [{ suffix: "ied", replace: "y", name: "ied -> y" }, { suffix: "ied", replace: "ie", name: "ied -> ie" }, { suffix: "ies", replace: "y", name: "ies -> y" }, { suffix: "ies", replace: "ie", name: "ies -> ie" }, { suffix: "ying", replace: "ie", name: "ying -> ie" }],
    [{ suffix: "ing", replace: "", name: "ing -> ''", undouble: true, addE: true }, { suffix: "ed", replace: "", name: "ed -> ''", undouble: true, addE: true }, { suffix: "king", replace: "c", name: "king -> c" }, { suffix: "ked", replace: "c", name: "ked -> c" }],
    [{ suffix: "er", replace: "", name: "er -> ''", undouble: true, addE: true }, { suffix: "est", replace: "", name: "est -> ''", undouble: true, addE: true }, { suffix: "ves", replace: "f", name: "ves -> f" }, { suffix: "ves", replace: "fe", name: "ves -> fe" }, { suffix: "men", replace: "man", name: "men -> man" }, { suffix: "ses", replace: "sis", name: "ses -> sis" }, { suffix: "ices", replace: "ex", name: "ices -> ex" }, { suffix: "ices", replace: "ix", name: "ices -> ix" }, { suffix: "i", replace: "us", name: "i -> us" }, { suffix: "a", replace: "um", name: "a -> um" }, { suffix: "a", replace: "on", name: "a -> on" }, { suffix: "ae", replace: "a", name: "ae -> a" }, { suffix: "eaux", replace: "eau", name: "eaux -> eau" }],
    [{ suffix: "ability", replace: "able", name: "ability -> able" }, { suffix: "ibility", replace: "ible", name: "ibility -> ible" }, { suffix: "ization", replace: "ize", name: "ization -> ize" }, { suffix: "isation", replace: "ise", name: "isation -> ise" }, { suffix: "ized", replace: "ize", name: "ized -> ize" }, { suffix: "ised", replace: "ise", name: "ised -> ise" }, { suffix: "izing", replace: "ize", name: "izing -> ize" }, { suffix: "ising", replace: "ise", name: "ising -> ise" }, { suffix: "izer", replace: "ize", name: "izer -> ize" }, { suffix: "iser", replace: "ise", name: "iser -> ise" }, { suffix: "ation", replace: "ate", name: "ation -> ate" }, { suffix: "ness", replace: "", name: "ness -> ''" }, { suffix: "ment", replace: "", name: "ment -> ''" }, { suffix: "ship", replace: "", name: "ship -> ''" }, { suffix: "hood", replace: "", name: "hood -> ''" }, { suffix: "dom", replace: "", name: "dom -> ''" }, { suffix: "fully", replace: "ful", name: "fully -> ful" }, { suffix: "ful", replace: "", name: "ful -> ''" }, { suffix: "less", replace: "", name: "less -> ''" }, { suffix: "ical", replace: "ic", name: "ical -> ic" }, { suffix: "ably", replace: "able", name: "ably -> able" }, { suffix: "ibly", replace: "ible", name: "ibly -> ible" }, { suffix: "ly", replace: "", name: "ly -> ''" }, { suffix: "ity", replace: "e", name: "ity -> e" }, { suffix: "ity", replace: "", name: "ity -> ''" }],
    [{ suffix: "icity", replace: "ic", name: "icity -> ic" }, { suffix: "osity", replace: "ous", name: "osity -> ous" }, { suffix: "ality", replace: "al", name: "ality -> al" }, { suffix: "ivity", replace: "ive", name: "ivity -> ive" }, { suffix: "ousness", replace: "ous", name: "ousness -> ous" }, { suffix: "fulness", replace: "ful", name: "fulness -> ful" }, { suffix: "lessness", replace: "less", name: "lessness -> less" }, { suffix: "ance", replace: "", name: "ance -> ''" }, { suffix: "ence", replace: "", name: "ence -> ''" }, { suffix: "ism", replace: "", name: "ism -> ''" }, { suffix: "ist", replace: "", name: "ist -> ''" }, { suffix: "age", replace: "", name: "age -> ''" }, { suffix: "ee", replace: "", name: "ee -> ''" }, { suffix: "or", replace: "", name: "or -> ''" }, { suffix: "ster", replace: "", name: "ster -> ''" }, { suffix: "ling", replace: "", name: "ling -> ''" }, { suffix: "let", replace: "", name: "let -> ''" }, { suffix: "en", replace: "", name: "en -> ''" }, { suffix: "ward", replace: "", name: "ward -> ''" }, { suffix: "wise", replace: "", name: "wise -> ''" }, { suffix: "ically", replace: "ical", name: "ically -> ical" }, { suffix: "ally", replace: "al", name: "ally -> al" }, { suffix: "ally", replace: "ic", name: "ally -> ic" }, { suffix: "able", replace: "", name: "able -> ''", addE: true }, { suffix: "ible", replace: "", name: "ible -> ''" }, { suffix: "ion", replace: "", name: "ion -> ''" }, { suffix: "tion", replace: "t", name: "tion -> t" }, { suffix: "tion", replace: "te", name: "tion -> te" }, { suffix: "sion", replace: "se", name: "sion -> se" }, { suffix: "sion", replace: "de", name: "sion -> de" }, { suffix: "al", replace: "", name: "al -> ''" }, { suffix: "ic", replace: "", name: "ic -> ''" }, { suffix: "ous", replace: "", name: "ous -> ''" }, { suffix: "ious", replace: "y", name: "ious -> y" }, { suffix: "eous", replace: "e", name: "eous -> e" }, { suffix: "ary", replace: "", name: "ary -> ''" }, { suffix: "ant", replace: "", name: "ant -> ''" }, { suffix: "ent", replace: "", name: "ent -> ''" }],
    [{ suffix: "es", replace: "", name: "es -> ''" }, { suffix: "s", replace: "", name: "s -> ''" }]
];

const suppletionMap = {
    "went": "go", "gone": "go", "was": "be", "were": "be", "is": "be", "am": "be", "are": "be", "been": "be",
    "has": "have", "had": "have", "does": "do", "did": "do", "done": "do", "made": "make", "took": "take",
    "taken": "take", "came": "come", "saw": "see", "seen": "see", "ate": "eat", "eaten": "eat", "wrote": "write",
    "written": "write", "spoke": "speak", "spoken": "speak", "broke": "break", "broken": "break", "drove": "drive",
    "driven": "drive", "sang": "sing", "sung": "sing", "rang": "ring", "rung": "ring", "drank": "drink",
    "drunk": "drink", "gave": "give", "given": "give", "knew": "know", "known": "know", "grew": "grow", "grown": "grow",
    "better": "good", "best": "good", "worse": "bad", "worst": "bad", "farther": "far", "further": "far",
    "farthest": "far", "furthest": "far", "mice": "mouse", "geese": "goose", "teeth": "tooth", "feet": "foot",
    "lice": "louse", "people": "person", "children": "child"
};

function generateCandidates(word, logCallback) {
    let candidates = [];
    if (suppletionMap[word]) {
        candidates.push({ word: suppletionMap[word], rule: "Irregular/Suppletion" });
        if(logCallback) logCallback(`Irregular Match: '${word}' -> '${suppletionMap[word]}'`);
    }
    for (let layer of fstRuleLayers) {
        for (let rule of layer) {
            if (word.endsWith(rule.suffix) && word.length > rule.suffix.length) {
                let stem = word.slice(0, -rule.suffix.length);
                let base = stem + rule.replace;
                candidates.push({ word: base, rule: rule.name });
                if(logCallback) logCallback(`Rule Match: '${word}' -> '${base}' (${rule.name})`);
                if (rule.undouble && stem.length >= 2 && stem[stem.length-1] === stem[stem.length-2]) {
                    let undoubled = stem.slice(0, -1);
                    candidates.push({ word: undoubled, rule: rule.name + " + Undouble" });
                    if(logCallback) logCallback(`Undouble Rule: '${word}' -> '${undoubled}'`);
                }
                if (rule.addE) {
                    let withE = stem + "e";
                    candidates.push({ word: withE, rule: rule.name + " + Add-E" });
                    if(logCallback) logCallback(`Silent-E Rule: '${word}' -> '${withE}'`);
                }
            }
        }
    }
    candidates.push({ word: word, rule: "Self" });
    const uniqueCandidates = []; const seen = new Set();
    for (let c of candidates) { if (!seen.has(c.word)) { uniqueCandidates.push(c); seen.add(c.word); } }
    return uniqueCandidates;
}

// --- 2. Trie Data Structure (DFA) ---
class TrieNode {
    constructor(char = '') {
        this.char = char;
        this.children = {};
        this.isEndOfWord = false;
        this.id = 'node_' + Math.random().toString(36).substr(2, 9);
    }
}

class Trie {
    constructor() {
        this.root = new TrieNode('START');
        this.wordCount = 0;
    }

    insert(word) {
        let current = this.root;
        for (let char of word) {
            if (!current.children[char]) {
                current.children[char] = new TrieNode(char);
            }
            current = current.children[char];
        }
        if (!current.isEndOfWord) {
            current.isEndOfWord = true;
            this.wordCount++;
        }
    }

    search(word, logCallback) {
        let current = this.root;
        let pathIds = [current.id];
        for (let char of word) {
            if (!current.children[char]) return { found: false, path: pathIds };
            current = current.children[char];
            pathIds.push(current.id);
        }
        return { found: current.isEndOfWord, path: pathIds };
    }

    getDynamicDFAView(wordsToTrace) {
        let nodesMap = new Map();
        let edges = [];

        nodesMap.set(this.root.id, {
            id: this.root.id, label: this.root.char, level: 0,
            color: { background: '#97c2fc', border: '#2b7ce9' },
            font: { color: '#000', size: 16, face: 'monospace', weight: 'bold' },
            shape: 'dot', size: 30, borderWidth: 3
        });

        const addChildrenToView = (parentNode, level) => {
            for (let char in parentNode.children) {
                let child = parentNode.children[char];
                if (!nodesMap.has(child.id)) {
                    nodesMap.set(child.id, {
                        id: child.id, label: child.char, level: level,
                        color: {
                            background: child.isEndOfWord ? '#7be141' : '#e0e0e0',
                            border: child.isEndOfWord ? '#41a906' : '#a0a0a0'
                        },
                        font: { color: '#333', size: 14 },
                        shape: 'dot', size: child.isEndOfWord ? 25 : 20, borderWidth: 2
                    });
                    edges.push({ from: parentNode.id, to: child.id, arrows: 'to', color: { color: '#cccccc', opacity: 0.5 } });
                }
            }
        };

        addChildrenToView(this.root, 1);

        wordsToTrace.forEach(word => {
            let current = this.root;
            for (let i = 0; i < word.length; i++) {
                let char = word[i];
                if (!current.children[char]) break;
                let nextNode = current.children[char];
                nodesMap.set(nextNode.id, {
                    id: nextNode.id, label: nextNode.char, level: i + 1,
                    color: {
                        background: nextNode.isEndOfWord ? '#7be141' : '#fb7e81',
                        border: nextNode.isEndOfWord ? '#41a906' : '#fa0a10'
                    },
                    font: { color: '#000', size: 18, weight: 'bold' },
                    shape: 'dot', size: 28, borderWidth: 4
                });
                edges.push({ from: current.id, to: nextNode.id, arrows: 'to', color: { color: '#848484', opacity: 1 }, width: 2 });
                addChildrenToView(nextNode, i + 2);
                current = nextNode;
            }
        });

        return { nodes: Array.from(nodesMap.values()), edges: edges };
    }
}

// --- 3. UI and Logic Integration ---
let fullDictionaryTrie = new Trie();
let customDictionaryTrie = new Trie();
let wordGroups = {};
let currentMode = 'model1';
let network = null;
let networkNodes = null;
let networkEdges = null;
let debounceTimer;

function showLoading(show, message = "Building State Machine...") {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.style.display = show ? 'flex' : 'none';
        if (show) overlay.innerHTML = `<div style="text-align:center"><i class="fas fa-spinner fa-spin fa-2x"></i><p style="margin-top:10px">${message}</p></div>`;
    }
}

function initNetwork(visData) {
    const container = document.getElementById('network-container');
    if (!container) return;
    
    if (network) network.destroy();

    networkNodes = new vis.DataSet(visData.nodes);
    networkEdges = new vis.DataSet(visData.edges);
    
    const options = {
        layout: { hierarchical: { direction: 'UD', sortMethod: 'directed', nodeSpacing: 150, levelSeparation: 120, parentCentralization: true } },
        physics: { 
            enabled: true, 
            hierarchicalRepulsion: { nodeDistance: 160 }, 
            stabilization: { iterations: 100 } 
        },
        interaction: { dragNodes: true, zoomView: true, dragView: true, hover: true },
        nodes: { 
            shadow: { enabled: true, color: 'rgba(0,0,0,0.3)', size: 10, x: 5, y: 5 }
        },
        edges: { 
            smooth: { type: 'cubicBezier', forceDirection: 'vertical', roundness: 0.5 },
            shadow: { enabled: true, color: 'rgba(0,0,0,0.1)', size: 5, x: 2, y: 2 }
        }
    };
    
    network = new vis.Network(container, { nodes: networkNodes, edges: networkEdges }, options);
}

async function loadFullDictionary() {
    showLoading(true, "Downloading Lexicon...");
    try {
        const response = await fetch('words_alpha.txt');
        const text = await response.text();
        const words = text.split(/\r?\n/).map(w => w.trim().toLowerCase()).filter(w => w.length > 0);
        
        fullDictionaryTrie = new Trie();
        const total = words.length;
        const chunkSize = 25000;
        for (let i = 0; i < total; i += chunkSize) {
            words.slice(i, i + chunkSize).forEach(w => fullDictionaryTrie.insert(w));
            if (i % 50000 === 0) {
                showLoading(true, `Compiling States: ${Math.round((i/total)*100)}%`);
                await new Promise(r => setTimeout(r, 0));
            }
        }
        initNetwork(fullDictionaryTrie.getDynamicDFAView([]));
        showLoading(false);
    } catch (e) {
        showLoading(false);
        const fallback = ["happy", "happiness", "run", "running", "study", "studies"];
        fullDictionaryTrie = new Trie();
        fallback.forEach(w => fullDictionaryTrie.insert(w));
        initNetwork(fullDictionaryTrie.getDynamicDFAView([]));
    }
}

function highlightTriePath(pathIds) {
    if (!network || !networkNodes) return;
    const updates = [];
    networkNodes.getIds().forEach(id => {
        if (pathIds.includes(id)) {
            updates.push({ id: id, color: { background: '#ffff00', border: '#f39c12' }, size: 35, font: { size: 22, weight: 'bold' } });
        }
    });
    networkNodes.update(updates);
    
    // "Fly" to the final node for a 3D effect
    const lastId = pathIds[pathIds.length - 1];
    network.focus(lastId, {
        scale: 1.2,
        animation: { duration: 1000, easingFunction: 'easeInOutQuad' }
    });
}

function processWord(word, isModel1) {
    if (!word) {
        clearLog();
        document.getElementById('finalResult').innerText = '-';
        if (document.getElementById('meaningContainer')) document.getElementById('meaningContainer').style.display = 'none';
        return;
    }
    clearLog();
    const activeTrie = isModel1 ? fullDictionaryTrie : customDictionaryTrie;
    logToPanel('info', `LEXICAL ANALYSIS: "${word}"`);
    const candidates = generateCandidates(word, (msg) => logToPanel('candidate', msg));
    
    // Update graph dynamically
    initNetwork(activeTrie.getDynamicDFAView(candidates.map(c => c.word)));
    
    let finalBase = word; let found = false;
    setTimeout(() => {
        for (let cObj of candidates) {
            let candidate = cObj.word;
            logToPanel('check', `Searching DFA for: "${candidate}"`);
            let res = activeTrie.search(candidate);
            if (res.found) {
                finalBase = candidate; found = true;
                highlightTriePath(res.path);
                fetchMeaning(candidate);
                updateWordFamilies(candidate, word);
                break;
            }
        }
        const finalResEl = document.getElementById('finalResult');
        finalResEl.innerText = found ? finalBase : `"${word}" (Not Found)`;
        finalResEl.className = found ? 'result-display pop' : 'result-display error';
        if (!found) {
            if (document.getElementById('meaningContainer')) document.getElementById('meaningContainer').style.display = 'none';
            logToPanel('fail', `Lexical Error: "${word}" has no valid base form.`);
        }
    }, 200);
}

function fetchMeaning(word) {
    const meaningContainer = document.getElementById('meaningContainer');
    const definitionEl = document.getElementById('wordDefinition');
    const posEl = document.getElementById('partOfSpeech');
    meaningContainer.style.display = 'block';
    definitionEl.innerText = "Querying Lexicon...";
    fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`).then(r => r.json()).then(data => {
        const entry = data[0].meanings[0];
        definitionEl.innerText = entry.definitions[0].definition;
        posEl.innerText = entry.partOfSpeech;
        posEl.style.display = 'inline-block';
    }).catch(() => {
        definitionEl.innerText = "Definition unavailable.";
        posEl.style.display = 'none';
    });
}

function updateWordFamilies(base, original) {
    if (!wordGroups[base]) wordGroups[base] = new Set();
    wordGroups[base].add(original); wordGroups[base].add(base);
    let familyPanel = document.getElementById('wordFamilyList');
    if (!familyPanel) {
        const resultPanel = document.querySelector('.result-panel');
        const familyHeader = document.createElement('h3');
        familyHeader.innerHTML = '<i class="fas fa-users"></i> Word Family Grouping';
        familyHeader.style.marginTop = '20px';
        familyPanel = document.createElement('div');
        familyPanel.id = 'wordFamilyList';
        familyPanel.className = 'log-container';
        familyPanel.style.backgroundColor = '#fdfdfd'; familyPanel.style.color = '#444'; familyPanel.style.maxHeight = '150px';
        resultPanel.appendChild(familyHeader); resultPanel.appendChild(familyPanel);
    }
    familyPanel.innerHTML = '';
    for (let b in wordGroups) {
        let members = Array.from(wordGroups[b]).join(', ');
        let entry = document.createElement('div');
        entry.className = 'family-entry'; entry.style.fontSize = '0.8rem'; entry.style.marginBottom = '8px';
        entry.innerHTML = `<span style="color:#2980b9;font-weight:bold">${b}</span>: {${members}}`;
        familyPanel.appendChild(entry);
    }
}

function logToPanel(type, message) {
    const panel = document.getElementById('processLog');
    if (!panel) return;
    const placeholder = panel.querySelector('.placeholder-text');
    if (placeholder) placeholder.remove();
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    entry.innerText = `> ${message}`;
    panel.appendChild(entry);
    panel.scrollTop = panel.scrollHeight;
}

function clearLog() { const panel = document.getElementById('processLog'); if (panel) panel.innerHTML = ''; }

window.handleInputModel1 = () => { clearTimeout(debounceTimer); debounceTimer = setTimeout(() => processWord(document.getElementById('wordInput1').value.trim().toLowerCase(), true), 400); };
window.handleInputModel2 = () => { clearTimeout(debounceTimer); debounceTimer = setTimeout(() => processWord(document.getElementById('wordInput2').value.trim().toLowerCase(), false), 400); };
window.switchTab = (tabId) => {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    currentMode = tabId;
};

window.onload = () => {
    let checkVis = setInterval(() => { 
        if (typeof vis !== 'undefined') { 
            clearInterval(checkVis); 
            loadFullDictionary(); 
        } 
    }, 100);
    setTimeout(() => clearInterval(checkVis), 10000);
};

window.buildCustomTrie = () => {
    const dictStr = document.getElementById('dictInput').value;
    const words = dictStr.split(',').map(w => w.trim().toLowerCase()).filter(w => w.length > 0);
    customDictionaryTrie = new Trie();
    words.forEach(w => customDictionaryTrie.insert(w));
    initNetwork(customDictionaryTrie.getDynamicDFAView([]));
    document.getElementById('wordInput2').disabled = false;
};

window.buildDefaultTrie = () => { loadFullDictionary(); };
