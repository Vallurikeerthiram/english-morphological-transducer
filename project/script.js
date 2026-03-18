// --- 1. Morphological Transducer (FST) Rule Inventory ---
// Based on ENGLISH_MORPHOLOGY_RULE_NOTE.md (101 Rules)
// Prioritized according to Project Documentation Draft: iest > ier > ies > ing > ed > s

const fstRuleLayers = [
    // LAYER 1: High-priority Superlative/Comparative y-alternations
    [
        { suffix: "iness", replace: "y", name: "iness -> y" },
        { suffix: "iest", replace: "y", name: "iest -> y" },
        { suffix: "ier", replace: "y", name: "ier -> y" },
        { suffix: "ily", replace: "y", name: "ily -> y" }
    ],
    // LAYER 2: Plurals and y-alternations
    [
        { suffix: "ied", replace: "y", name: "ied -> y" },
        { suffix: "ied", replace: "ie", name: "ied -> ie" },
        { suffix: "ies", replace: "y", name: "ies -> y" },
        { suffix: "ies", replace: "ie", name: "ies -> ie" },
        { suffix: "ying", replace: "ie", name: "ying -> ie" }
    ],
    // LAYER 3: Progressive and Past (with undoubling/silent-e)
    [
        { suffix: "ing", replace: "", name: "ing -> ''", undouble: true, addE: true },
        { suffix: "ed", replace: "", name: "ed -> ''", undouble: true, addE: true },
        { suffix: "king", replace: "c", name: "king -> c" },
        { suffix: "ked", replace: "c", name: "ked -> c" }
    ],
    // LAYER 4: Degree and Plurals
    [
        { suffix: "er", replace: "", name: "er -> ''", undouble: true, addE: true },
        { suffix: "est", replace: "", name: "est -> ''", undouble: true, addE: true },
        { suffix: "ves", replace: "f", name: "ves -> f" },
        { suffix: "ves", replace: "fe", name: "ves -> fe" },
        { suffix: "men", replace: "man", name: "men -> man" },
        { suffix: "ses", replace: "sis", name: "ses -> sis" }
    ],
    // LAYER 5: Core Derivational Reversal
    [
        { suffix: "ability", replace: "able", name: "ability -> able" },
        { suffix: "ibility", replace: "ible", name: "ibility -> ible" },
        { suffix: "ization", replace: "ize", name: "ization -> ize" },
        { suffix: "isation", replace: "ise", name: "isation -> ise" },
        { suffix: "ation", replace: "ate", name: "ation -> ate" },
        { suffix: "ness", replace: "", name: "ness -> ''" },
        { suffix: "ment", replace: "", name: "ment -> ''" },
        { suffix: "ship", replace: "", name: "ship -> ''" },
        { suffix: "hood", replace: "", name: "hood -> ''" },
        { suffix: "dom", replace: "", name: "dom -> ''" },
        { suffix: "fully", replace: "ful", name: "fully -> ful" },
        { suffix: "ful", replace: "", name: "ful -> ''" },
        { suffix: "less", replace: "", name: "less -> ''" },
        { suffix: "ical", replace: "ic", name: "ical -> ic" },
        { suffix: "ly", replace: "", name: "ly -> ''" },
        { suffix: "ity", replace: "e", name: "ity -> e" },
        { suffix: "ity", replace: "", name: "ity -> ''" }
    ],
    // LAYER 6: Basic Inflection
    [
        { suffix: "es", replace: "", name: "es -> ''" },
        { suffix: "s", replace: "", name: "s -> ''" }
    ]
];

function generateCandidates(word, logCallback) {
    let candidates = [];
    
    // Identity check - word itself is always a candidate
    candidates.push({ word: word, rule: "Self" });

    for (let layer of fstRuleLayers) {
        for (let rule of layer) {
            if (word.endsWith(rule.suffix) && word.length > rule.suffix.length) {
                let stem = word.slice(0, -rule.suffix.length);
                
                // Base transformation
                let base = stem + rule.replace;
                candidates.push({ word: base, rule: rule.name });
                if(logCallback) logCallback(`Rule Match: '${word}' -> '${base}' (${rule.name})`);

                // Consonant Undoubling (runn-ing -> run)
                if (rule.undouble && stem.length >= 2 && stem[stem.length-1] === stem[stem.length-2]) {
                    let undoubled = stem.slice(0, -1);
                    candidates.push({ word: undoubled, rule: rule.name + " + Undouble" });
                    if(logCallback) logCallback(`Undouble Rule: '${word}' -> '${undoubled}'`);
                }

                // Silent E restoration (lov-ing -> love)
                if (rule.addE) {
                    let withE = stem + "e";
                    candidates.push({ word: withE, rule: rule.name + " + Add-E" });
                    if(logCallback) logCallback(`Silent-E Rule: '${word}' -> '${withE}'`);
                }
            }
        }
    }
    
    // Sort candidates to keep original prioritized layers
    // But pseudocode says Identity is usually checked last or prioritized by Trie
    // We will keep them in the order they were added but move Self to the end if desired.
    // Documentation says "First valid match (priority-based)".
    
    const uniqueCandidates = [];
    const seen = new Set();
    for (let c of candidates) {
        if (!seen.has(c.word)) {
            uniqueCandidates.push(c);
            seen.add(c.word);
        }
    }
    
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

    search(word, logCallback, highlightCallback) {
        let current = this.root;
        let pathIds = [current.id];
        
        for (let i = 0; i < word.length; i++) {
            let char = word[i];
            if (!current.children[char]) {
                if (logCallback) logCallback(`DFA Trace: No edge for '${char}' from state '${current.char}'`);
                return { found: false, path: pathIds };
            }
            current = current.children[char];
            pathIds.push(current.id);
            if (highlightCallback) highlightCallback(pathIds);
        }
        
        if (current.isEndOfWord) {
            if (logCallback) logCallback(`DFA Accept: '${word}' reached a final state.`);
            return { found: true, path: pathIds };
        } else {
            if (logCallback) logCallback(`DFA Sink: '${word}' reached a non-accepting state.`);
            return { found: false, path: pathIds };
        }
    }

    getDynamicDFAView(wordsToTrace) {
        let nodesMap = new Map();
        let edges = [];

        nodesMap.set(this.root.id, {
            id: this.root.id, label: this.root.char, level: 0,
            color: { background: '#97c2fc', border: '#2b7ce9' },
            font: { color: '#000', size: 16, face: 'monospace', weight: 'bold' },
            shape: 'ellipse', borderWidth: 3
        });

        const addChildrenToView = (parentNode, level) => {
            const sortedChars = Object.keys(parentNode.children).sort();
            for (let char of sortedChars) {
                let child = parentNode.children[char];
                if (!nodesMap.has(child.id)) {
                    nodesMap.set(child.id, {
                        id: child.id, label: child.char, level: level,
                        color: {
                            background: child.isEndOfWord ? '#7be141' : '#e0e0e0',
                            border: child.isEndOfWord ? '#41a906' : '#a0a0a0'
                        },
                        font: { color: child.isEndOfWord ? '#fff' : '#555', size: 12, face: 'monospace' },
                        shape: child.isEndOfWord ? 'box' : 'ellipse', borderWidth: 1
                    });
                    edges.push({ from: parentNode.id, to: child.id, arrows: 'to', color: { color: '#cccccc', opacity: 0.5 }, width: 1 });
                }
            }
        };

        addChildrenToView(this.root, 1);

        wordsToTrace.forEach(word => {
            let current = this.root;
            let level = 1;
            for (let i = 0; i < word.length; i++) {
                let char = word[i];
                if (!current.children[char]) break;
                let nextNode = current.children[char];
                nodesMap.set(nextNode.id, {
                    id: nextNode.id, label: nextNode.char, level: level,
                    color: {
                        background: nextNode.isEndOfWord ? '#7be141' : '#fb7e81',
                        border: nextNode.isEndOfWord ? '#41a906' : '#fa0a10'
                    },
                    font: { color: nextNode.isEndOfWord ? '#fff' : '#000', size: 16, face: 'monospace', weight: 'bold' },
                    shape: nextNode.isEndOfWord ? 'box' : 'ellipse', borderWidth: 3
                });
                edges.push({ from: current.id, to: nextNode.id, arrows: 'to', color: { color: '#848484', opacity: 1 }, width: 2 });
                addChildrenToView(nextNode, level + 1);
                current = nextNode;
                level++;
            }
        });

        return { nodes: Array.from(nodesMap.values()), edges: edges };
    }

    getVisData() {
        let nodes = [];
        let edges = [];
        const traverse = (node, parentId, level = 0) => {
            nodes.push({
                id: node.id, label: node.char, level: level,
                color: { background: node.char === 'START' ? '#97c2fc' : (node.isEndOfWord ? '#7be141' : '#fb7e81'), border: node.char === 'START' ? '#2b7ce9' : (node.isEndOfWord ? '#41a906' : '#fa0a10') },
                font: { color: (node.char === 'START' || !node.isEndOfWord) ? '#000' : '#fff', size: 14, face: 'monospace' },
                shape: node.isEndOfWord ? 'box' : 'ellipse', borderWidth: 2
            });
            if (parentId) edges.push({ from: parentId, to: node.id, arrows: 'to', color: { color: '#848484', opacity: 0.6 }, width: 1 });
            const sortedChars = Object.keys(node.children).sort();
            for (let char of sortedChars) traverse(node.children[char], node.id, level + 1);
        };
        traverse(this.root, null);
        return { nodes, edges };
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
    
    // Destroy old network to free memory
    if (network) {
        network.destroy();
        network = null;
    }

    networkNodes = new vis.DataSet(visData.nodes);
    networkEdges = new vis.DataSet(visData.edges);
    
    const options = {
        layout: { hierarchical: { direction: 'UD', sortMethod: 'directed', nodeSpacing: 120, levelSeparation: 100, parentCentralization: true } },
        physics: { enabled: false },
        interaction: { dragNodes: true, zoomView: true, dragView: true, hover: true },
        nodes: { shadow: true },
        edges: { smooth: { type: 'cubicBezier', forceDirection: 'vertical', roundness: 0.4 } }
    };
    
    network = new vis.Network(container, { nodes: networkNodes, edges: networkEdges }, options);
}

async function loadFullDictionary() {
    showLoading(true, "Downloading Lexicon...");
    try {
        const response = await fetch('words_alpha.txt');
        if (!response.ok) throw new Error("HTTP " + response.status);
        const text = await response.text();
        const words = text.split(/\r?\n/).map(w => w.trim().toLowerCase()).filter(w => w.length > 0);
        
        fullDictionaryTrie = new Trie();
        const total = words.length;
        const chunkSize = 25000;
        
        for (let i = 0; i < total; i += chunkSize) {
            const chunk = words.slice(i, i + chunkSize);
            chunk.forEach(w => fullDictionaryTrie.insert(w));
            
            if (i % 50000 === 0) {
                showLoading(true, `Compiling DFA States: ${Math.round((i/total)*100)}%`);
                await new Promise(r => setTimeout(r, 0));
            }
        }
        
        initNetwork(fullDictionaryTrie.getDynamicDFAView([]));
        showLoading(false);
        logToPanel('info', `✅ Compilation Complete: ${fullDictionaryTrie.wordCount.toLocaleString()} states loaded.`);
    } catch (error) {
        console.error("Dictionary Load Error:", error);
        showLoading(false);
        logToPanel('fail', 'Failed to load dictionary. falling back to sample set.');
        const fallback = ["happy", "happiness", "run", "running", "study", "studies", "stop", "stopped", "ram", "hconvert"];
        fullDictionaryTrie = new Trie();
        fallback.forEach(w => fullDictionaryTrie.insert(w));
        initNetwork(fullDictionaryTrie.getVisData());
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

function highlightTriePath(pathIds) {
    if (!networkNodes) return;
    const updateNodes = [];
    networkNodes.getIds().forEach(id => {
        const node = networkNodes.get(id);
        if (!node) return;
        let bgColor = node.label === 'START' ? '#97c2fc' : (node.shape === 'box' ? '#7be141' : '#fb7e81');
        if (pathIds.includes(id)) updateNodes.push({id: id, color: {background: '#ffff00', border: '#ff9900'}, borderWidth: 4});
        else updateNodes.push({id: id, color: {background: bgColor, border: node.color.border || '#000'}, borderWidth: 2});
    });
    networkNodes.update(updateNodes);
}

async function fetchMeaning(word) {
    const meaningContainer = document.getElementById('meaningContainer');
    const definitionEl = document.getElementById('wordDefinition');
    const posEl = document.getElementById('partOfSpeech');
    if (!meaningContainer || !definitionEl || !posEl) return;
    
    meaningContainer.style.display = 'block';
    definitionEl.innerText = "Querying WordNet...";
    posEl.style.display = 'none';
    
    try {
        const response = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`);
        if (!response.ok) throw new Error();
        const data = await response.json();
        const entry = data[0].meanings[0];
        definitionEl.innerText = entry.definitions[0].definition;
        posEl.innerText = entry.partOfSpeech;
        posEl.style.display = 'inline-block';
    } catch (e) {
        definitionEl.innerText = "Base word identified, but definition unavailable in this lexicon.";
        posEl.style.display = 'none';
    }
}

function updateWordFamilies(base, original) {
    if (!wordGroups[base]) wordGroups[base] = new Set();
    wordGroups[base].add(original);
    wordGroups[base].add(base);
    
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
        resultPanel.appendChild(familyHeader);
        resultPanel.appendChild(familyPanel);
    }
    
    familyPanel.innerHTML = '';
    for (let b in wordGroups) {
        let members = Array.from(wordGroups[b]).join(', ');
        let entry = document.createElement('div');
        entry.style.fontSize = '0.8rem'; entry.style.marginBottom = '8px';
        entry.innerHTML = `<span style="color:#2980b9;font-weight:bold">${b}</span>: {${members}}`;
        familyPanel.appendChild(entry);
    }
}

function processWord(word, isModel1) {
    if (!word) {
        clearLog();
        document.getElementById('finalResult').innerText = '-';
        if (document.getElementById('meaningContainer')) document.getElementById('meaningContainer').style.display = 'none';
        return;
    }
    
    clearLog();
    let activeTrie = isModel1 ? fullDictionaryTrie : customDictionaryTrie;
    
    if (isModel1 && activeTrie.wordCount === 0) {
        logToPanel('info', 'Wait: Dictionary still compiling...');
        return;
    }

    logToPanel('info', `LEXICAL ANALYSIS: "${word}"`);
    const candidates = generateCandidates(word, (msg) => logToPanel('candidate', msg));
    
    // Update graph with current candidate branches
    if (isModel1) initNetwork(activeTrie.getDynamicDFAView(candidates.map(c => c.word)));
    
    let finalBase = word;
    let found = false;
    
    // Use a slight delay to ensure the network is initialized before we start searching
    setTimeout(() => {
        // Try candidates in order
        for (let candidateObj of candidates) {
            let candidate = candidateObj.word;
            logToPanel('check', `Traversing DFA for: "${candidate}"`);
            let result = activeTrie.search(candidate, (msg) => logToPanel(msg.includes('Failed') ? 'fail' : 'success', msg));
            if (result.found) {
                finalBase = candidate;
                found = true;
                highlightTriePath(result.path);
                fetchMeaning(candidate);
                updateWordFamilies(candidate, word);
                break;
            }
        }
        document.getElementById('finalResult').innerText = finalBase;
    }, 50);
}

window.handleInputModel1 = () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        const val = document.getElementById('wordInput1').value.trim().toLowerCase();
        processWord(val, true);
    }, 400);
};

window.handleInputModel2 = () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        const val = document.getElementById('wordInput2').value.trim().toLowerCase();
        processWord(val, false);
    }, 400);
};

window.switchTab = (tabId) => {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    const btn = event.currentTarget;
    btn.classList.add('active');
    document.getElementById(tabId).classList.add('active');
    currentMode = tabId;
    if (tabId === 'model1') initNetwork(fullDictionaryTrie.getDynamicDFAView([]));
    else if (document.getElementById('dictInput').value) buildCustomTrie();
};

function buildCustomTrie() {
    const dictStr = document.getElementById('dictInput').value;
    const words = dictStr.split(',').map(w => w.trim().toLowerCase()).filter(w => w.length > 0);
    if (words.length === 0) return;
    customDictionaryTrie = new Trie();
    words.forEach(word => customDictionaryTrie.insert(word));
    initNetwork(customDictionaryTrie.getVisData());
    document.getElementById('wordInput2').disabled = false;
    logToPanel('info', `Manual Lexicon: ${words.length} entries.`);
}

function clearLog() {
    const panel = document.getElementById('processLog');
    if (panel) panel.innerHTML = '';
}

window.buildDefaultTrie = () => { if (currentMode === 'model1') loadFullDictionary(); else buildCustomTrie(); };

window.onload = () => {
    let checkVis = setInterval(() => { 
        if (typeof vis !== 'undefined') { 
            clearInterval(checkVis); 
            loadFullDictionary(); 
        } 
    }, 100);
    setTimeout(() => clearInterval(checkVis), 10000);
};
