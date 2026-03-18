"""
English Morphological Analysis API

FastAPI-based REST API for morphological analysis of English words.
Provides endpoints for analyzing individual words and batches of words.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn

from .morphological_analyzer import MorphologicalAnalyzer

# Initialize FastAPI app
app = FastAPI(
    title="English Morphological Analyzer API",
    description="API for morphological analysis and base word extraction from English words",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzer with default dictionary
analyzer = MorphologicalAnalyzer()

# Pydantic models
class AnalysisRequest(BaseModel):
    word: str
    include_logs: Optional[bool] = False

class BatchAnalysisRequest(BaseModel):
    words: List[str]
    include_logs: Optional[bool] = False

class DictionaryUpdateRequest(BaseModel):
    words: List[str]

class AnalysisResponse(BaseModel):
    input_word: str
    base_word: str
    rule_applied: str
    found_in_dictionary: bool
    candidates_checked: int
    dictionary_size: int
    logs: List[str]

class BatchAnalysisResponse(BaseModel):
    results: List[AnalysisResponse]
    total_words: int

class DictionaryInfoResponse(BaseModel):
    word_count: int
    sample_words: List[str]

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "English Morphological Analyzer API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "analyze_word": "/analyze",
            "batch_analyze": "/analyze/batch",
            "dictionary_info": "/dictionary",
            "update_dictionary": "/dictionary/update"
        }
    }

@app.get("/analyze", response_model=AnalysisResponse)
async def analyze_word(
    word: str = Query(..., description="Word to analyze morphologically"),
    include_logs: bool = Query(False, description="Include detailed processing logs")
):
    """
    Analyze a single word morphologically

    - **word**: The word to analyze (e.g., "running", "happiest", "studies")
    - **include_logs**: Whether to include detailed processing logs

    Returns the base word, rule applied, and analysis details.
    """
    try:
        result = analyzer.analyze_word(word, include_logs)
        return AnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze/batch", response_model=BatchAnalysisResponse)
async def analyze_words_batch(request: BatchAnalysisRequest):
    """
    Analyze multiple words in a single request

    - **words**: List of words to analyze
    - **include_logs**: Whether to include detailed processing logs for each word
    """
    try:
        results = analyzer.analyze_multiple_words(request.words, request.include_logs)
        return BatchAnalysisResponse(
            results=[AnalysisResponse(**result) for result in results],
            total_words=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")

@app.get("/dictionary", response_model=DictionaryInfoResponse)
async def get_dictionary_info():
    """Get information about the loaded dictionary"""
    try:
        info = analyzer.get_dictionary_info()
        return DictionaryInfoResponse(**info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dictionary info retrieval failed: {str(e)}")

@app.post("/dictionary/update")
async def update_dictionary(request: DictionaryUpdateRequest):
    """
    Add words to the dictionary

    - **words**: List of words to add to the dictionary
    """
    try:
        analyzer.update_dictionary(request.words)
        return {
            "message": f"Added {len(request.words)} words to dictionary",
            "new_word_count": len(analyzer.trie)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dictionary update failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "analyzer_ready": True}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)