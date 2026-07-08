import streamlit as st
from components import render_session_header, render_prompt, render_explanation, render_technologies_used, render_key_concepts, render_what_you_built

render_session_header(3, "Cortex Search", "10:35 - 10:45 AM", "10 min", "Knowledge base, Cortex Search service, and RAG query pattern")

render_technologies_used([
    {"name": "Cortex Search Service", "description": "A managed hybrid search engine combining vector (semantic) and keyword search with automatic reranking. Created with a single SQL statement; handles embedding, indexing, and serving automatically.", "icon": "search"},
    {"name": "RAG (Retrieval Augmented Generation)", "description": "A pattern that retrieves relevant documents first, then passes them as context to an LLM for grounded answer generation. Reduces hallucination by anchoring responses in actual data.", "icon": "hub"},
    {"name": "SEARCH_PREVIEW", "description": "SQL function to query a Cortex Search Service. Supports text queries, column selection, filtering, and result limits. Returns JSON with ranked results.", "icon": "preview"},
])


PROMPT_3_1 = """In your workshop schema in HIIVE_COCO_HOL:

1. First, create a unified text table for search called MARKETPLACE_KNOWLEDGE_BASE that combines:
   - COMPLIANCE_REVIEWS: review_id as doc_id, 'compliance_review' as doc_type, findings_text as content, review_type as metadata_category, outcome as metadata_priority, review_date as doc_date
   - SUPPORT_TICKETS: ticket_id as doc_id, 'support_ticket' as doc_type, description_text || ' Resolution: ' || resolution_text as content, category as metadata_category, priority as metadata_priority, created_date as doc_date
   - REGULATORY_FILINGS: filing_id as doc_id, 'regulatory_filing' as doc_type, summary_text || ' Reviewer Notes: ' || reviewer_notes as content, filing_type as metadata_category, status as metadata_priority, filing_date as doc_date

2. Then create a Cortex Search Service:
   CREATE OR REPLACE CORTEX SEARCH SERVICE marketplace_knowledge_search
     ON content
     ATTRIBUTES metadata_category, metadata_priority, doc_type
     WAREHOUSE = HIIVE_COCO_HOL_WH
     TARGET_LAG = '1 hour'
     EMBEDDING_MODEL = 'snowflake-arctic-embed-l-v2.0'
     AS (
       SELECT doc_id, doc_type, content, metadata_category, metadata_priority, doc_date
       FROM MARKETPLACE_KNOWLEDGE_BASE
     );

Execute all SQL. Then verify the service is created by running SHOW CORTEX SEARCH SERVICES."""

render_prompt("Prompt 3.1", "Create Cortex Search Service", PROMPT_3_1)

render_explanation("What this prompt does", """
Two major steps: building a unified knowledge base and creating a search service.

**Step 1 — MARKETPLACE_KNOWLEDGE_BASE**: A UNION ALL table combining three document sources into a common schema:
- `doc_type` enables filtering by source (compliance vs. support vs. regulatory)
- `metadata_category` and `metadata_priority` become filter attributes
- Content is concatenated (description + resolution, summary + notes) for full context

**Step 2 — CREATE CORTEX SEARCH SERVICE**: This single SQL statement:

1. **Embeds** every row's `content` column using `snowflake-arctic-embed-l-v2.0`
2. **Indexes** both vector (semantic) and keyword (lexical) search
3. **Deploys** a low-latency serving endpoint
4. **Auto-refreshes** when source data changes (within TARGET_LAG)

**How hybrid search works**:
1. Query text is embedded into the same vector space
2. Vector similarity finds semantically similar documents
3. Keyword search finds lexically matching documents
4. A reranker combines and re-scores results
""")


PROMPT_3_2 = """In your workshop schema in HIIVE_COCO_HOL, query our marketplace_knowledge_search service using SEARCH_PREVIEW with these searches:

1. Search: "KYC verification failure" - show top 3 results
2. Search: "transfer delay settlement" - show top 3 results
3. Search: "SEC filing Form D" filtered to doc_type = 'regulatory_filing' - show top 3 results
4. Search: "accredited investor qualification" - show top 3 results

Use SEARCH_PREVIEW with the fully qualified service name in your schema for each query.

Execute all 4 searches and show results."""

render_prompt("Prompt 3.2", "Query the Search Service", PROMPT_3_2)

render_explanation("What this prompt does", """
Four search queries demonstrating different capabilities:

1. **"KYC verification failure"** — Tests keyword + semantic overlap. Should find compliance reviews related to identity verification even if they use terms like "identity check" or "accreditation denial."

2. **"transfer delay settlement"** — Tests semantic search. Should find support tickets about trade settlement issues, share transfer delays, or ROFR processing time without needing exact term matches.

3. **"SEC filing Form D" with filter** — Tests **attribute filtering**:
```json
{
  "query": "SEC filing Form D",
  "columns": ["doc_id", "doc_type", "content"],
  "filter": {"@eq": {"doc_type": "regulatory_filing"}},
  "limit": 3
}
```

4. **"accredited investor qualification"** — Tests cross-document concept matching across compliance reviews and support tickets related to investor accreditation.

**Why hybrid search matters**: Pure keyword search misses synonyms ("KYC" vs "identity verification"). Pure vector search can return semantically similar but factually irrelevant results. Cortex Search combines both with reranking.
""")


PROMPT_3_3 = """In your workshop schema in HIIVE_COCO_HOL, implement a RAG pattern that:

1. Takes a user question: "What are the most common compliance issues on the HIIVE platform and what preventive measures have been effective?"

2. First retrieves the top 5 most relevant documents from your marketplace_knowledge_search service using SEARCH_PREVIEW

3. Then passes the retrieved context + question to SNOWFLAKE.CORTEX.COMPLETE() to generate a grounded answer. Use this CTE pattern:
   - search_results CTE: call SEARCH_PREVIEW on your service, get top 5 docs with columns doc_id, doc_type, content, metadata_category
   - context CTE: use LATERAL FLATTEN + LISTAGG to combine results into a single context string
   - Final SELECT: call CORTEX.COMPLETE with claude-sonnet-4-6, passing a system prompt that says "You are a compliance expert at HIIVE. Based ONLY on the following source documents, answer the user question. Cite specific documents by their doc_id."

Note: For the SEARCH_PREVIEW service name, use the fully qualified path: your database.schema.service_name (e.g., HIIVE_COCO_HOL.OLEG_OPS.marketplace_knowledge_search)

Execute and show the RAG response."""

render_prompt("Prompt 3.3", "RAG Pattern: Search + Generate", PROMPT_3_3)

render_explanation("What this prompt does", """
Implements the full **RAG (Retrieval Augmented Generation)** pattern in a single SQL query:

**Step 1 — Retrieve**: SEARCH_PREVIEW finds the 5 most relevant documents.

**Step 2 — Augment**: LATERAL FLATTEN + LISTAGG combines retrieved documents into a single context string.

**Step 3 — Generate**: CORTEX.COMPLETE() receives context + question and generates a grounded answer.

**RAG architecture**:
```
User Question
     |
     v
[Cortex Search] --> Top 5 documents
     |
     v
[Context Assembly] --> "SOURCE DOCUMENTS: doc1... doc2..."
     |
     v
[LLM (COMPLETE)] --> Grounded answer with citations
```

**Why RAG works better than raw LLM**:
- **Reduces hallucination**: LLM answers "ONLY" from provided documents
- **Provides citations**: "Cite specific documents by doc_id" enables traceability
- **Fresh data**: Search service reflects latest data; LLM knowledge is static
- **Domain-specific**: Your enterprise compliance and regulatory data isn't in the LLM's training set
""")


render_key_concepts([
    {"term": "Cortex Search Service", "definition": "A managed hybrid search engine created with SQL. Handles embedding, indexing (vector + keyword), reranking, and auto-refresh. Think of it as Elasticsearch-as-a-SQL-statement."},
    {"term": "RAG (Retrieval Augmented Generation)", "definition": "An AI pattern: (1) retrieve relevant documents from a knowledge base, (2) include them as context in an LLM prompt, (3) generate an answer grounded in the retrieved data. The standard pattern for enterprise AI chatbots."},
    {"term": "Hybrid Search", "definition": "Combining vector search (semantic similarity) with keyword search (exact/fuzzy text matching). Better than either alone because vector search catches synonyms while keyword search catches specific terms."},
    {"term": "LATERAL FLATTEN + LISTAGG", "definition": "LATERAL FLATTEN expands a JSON array into rows. LISTAGG concatenates row values into a single string. Together, they convert search result arrays into a context string for LLM prompts."},
])

render_what_you_built([
    "MARKETPLACE_KNOWLEDGE_BASE — unified document table from 3 sources (175 documents)",
    "marketplace_knowledge_search — Cortex Search service with hybrid search",
    "4 search queries demonstrating keyword, semantic, and filtered search",
    "Full RAG pipeline: retrieve + augment + generate in a single SQL query",
])
