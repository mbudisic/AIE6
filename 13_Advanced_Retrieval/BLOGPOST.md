# Advanced Retrieval with LangChain: A Deep Dive ��

## Introduction

If you've worked with Retrieval Augmented Generation (RAG) systems, you might have wondered if your setup is achieving its full potential. Basic RAG is a good starting point, but there's a range of advanced techniques that can significantly improve performance. This article explores several of these advanced retrieval methods within the LangChain framework.

We will examine a notebook that evaluates various retrieval strategies using John Wick movie reviews as a dataset. This will allow us to cover different approaches, from Naive RAG to more complex methods like Parent Document Retrieval and Ensemble Retrievers. We'll also discuss the critical role of evaluation in understanding how well these strategies perform.

Let's begin our exploration of advanced retrieval.

## The Setup: Data, Embeddings, and Our Trusty RAG Chain 🛠️

Before comparing different retrieval strategies, a solid foundation is necessary. The notebook begins by preparing the environment:

1.  **Getting Dependencies**: Key libraries include `langchain`, `langchain-openai` (for LLMs and embedding models), `langchain-cohere` (for reranking), `rank_bm25` (for a keyword-based retrieval algorithm), and `qdrant-client` (for the vector database).
2.  **API Keys**: These are required to use OpenAI and Cohere services.
3.  **Data Collection and Preparation**: The dataset consists of reviews for the four John Wick movies, obtained from the [AI Maker Space Data Repository](https://github.com/AI-Maker-Space/DataRepository). Each review is loaded as a document. Metadata such as `Review_Date`, `Review_Title`, `Author`, `Rating`, and `Movie_Title` are added. A `last_accessed_at` field is also synthetically generated for illustrative purposes, though it's important to note that true time-weighting (e.g., in LangChain's `TimeWeightedRetriever`) is based on actual access times.
4.  **Vector Store Setup**: QDrant is used as the vector database, operating in-memory. OpenAI's `text-embedding-3-small` model generates document embeddings. A primary vector store named "JohnWick" is created.

With the data prepared and embedded, a standard RAG chain is built using LangChain Expression Language (LCEL). This chain's structure remains consistent across experiments; only the retriever component changes.

*   **Retrieval (R)**: This is the swappable component. Initially, a `naive_retriever` uses the QDrant vector store, fetching the top 10 most similar documents (`k=10`).
*   **Augmentation (A)**: A `ChatPromptTemplate` instructs the LLM to use the provided context to answer questions and to state "I don't know" if the answer isn't found in the context.
*   **Generation (G)**: `gpt-4o-mini` is the LLM. Since the focus is on retrieval evaluation, an efficient yet capable model is chosen.

This basic RAG chain serves as the baseline for comparison.

## Diving into Retrieval Strategies 🏊‍♂️

The notebook examines several retrieval methods, each offering a distinct approach to finding relevant information.

### 🧊 Naive RAG Chain

This is the control. The retriever performs a cosine similarity search across all review documents (each treated as an individual, un-chunked piece of context) and returns the top 10. This approach is straightforward but may not always yield the most focused or comprehensive results. Expected behavior is decent baseline performance, but it might struggle with nuanced queries or when relevant information is scattered across multiple smaller logical sections within a document.

### 🔢 Best-Matching 25 (BM25) Retriever

BM25 is a sparse retrieval algorithm, an alternative to dense vector embeddings. It relies on the bag-of-words model and ranks documents using term frequency and inverse document frequency (TF-IDF), focusing on keyword overlap. It's generally fast and can be effective when specific terms are vital. The `BM25Retriever` is initialized directly from the documents. We expect BM25 to perform well on queries with distinct keywords and potentially outperform vector search if the query terms are rare and discriminative. However, it might miss semantically similar content if keywords don't match exactly. The results often show BM25 as a strong contender, especially for its speed and simplicity.

### 🔄 Contextual Compression (Using Reranking)

The idea here is to retrieve a larger set of potentially relevant documents and then "compress" or filter them to a smaller, more precise set using a reranker.
1.  A base retriever (the `naive_retriever`) fetches an initial document set (e.g., top 10).
2.  A `CohereRerank` model (e.g., `rerank-english-v3.0`) re-evaluates these documents against the query, reordering them by relevance and providing a relevance score. Only the top N documents with high relevance are passed to the LLM.
This helps reduce noise and focus the LLM. Contextual compression is expected to improve precision by filtering out less relevant documents retrieved by the initial, broader search. The reranker should ideally pass only the most pertinent information, leading to more focused and accurate answers. The evaluation data often confirms this, showing higher precision-related scores.

### ❓ Multi-Query Retriever

The Multi-Query Retriever expands the original user query by using an LLM (the `chat_model`) to generate several variations or related sub-queries. It retrieves documents for each of these queries and then combines the unique documents to form the final context. This can capture different facets of user intent. This method is expected to improve recall, as different phrasings of a query might hit different relevant documents. However, it can sometimes reduce precision if the generated queries are too broad or off-topic. The notebook's results might show this trade-off, with increased context recall but potentially lower scores in faithfulness if irrelevant context is introduced.

### 👨‍👩‍👧 Parent Document Retriever (Small-to-Big)

This strategy balances precision and context. Small, focused text chunks often yield good similarity scores but may lack broader context. The Parent Document Retriever addresses this:
1.  **Parent Documents**: Original, larger documents (full movie reviews) are stored in an `InMemoryStore`.
2.  **Child Chunks**: These are split into smaller "child chunks" (e.g., using `RecursiveCharacterTextSplitter` with a 200-character chunk size), embedded, and stored in a separate vector store (a new QDrant collection "full_documents").
3.  **Retrieval Process**: Similarity search is performed against child chunks.
4.  **Returning Context**: Instead of small child chunks, their corresponding parent documents are returned.
The intuition is: find relevant small pieces but provide the LLM with their larger surrounding context. This approach is expected to improve faithfulness and answer quality by providing more complete context to the LLM, potentially leading to higher scores in metrics like `faithfulness` and `answer_relevancy`. The results often bear this out, showing that while initial retrieval is on small chunks, the larger context helps the LLM generate better answers.

### 🏛️ Ensemble Retriever

The Ensemble Retriever combines multiple retrievers.
1.  A list of retrievers is provided (e.g., `bm25_retriever`, `naive_retriever`, `parent_document_retriever`, `compression_retriever`, `multi_query_retriever`).
2.  Each fetches documents independently.
3.  Results are combined and reranked using an algorithm like Reciprocal Rank Fusion (RRF), which prioritizes documents highly ranked by multiple retrievers. Weights can be assigned to prioritize certain retrievers (equal weighting is used in the notebook).
This aims for robust, high-quality document sets by leveraging diverse signals. An ensemble is expected to provide more stable and often better overall performance by mitigating the weaknesses of individual retrievers. It might not top any single metric but should score consistently well across the board. The evaluation data usually supports this, showing the ensemble as a strong all-around performer.

### 🧩 Semantic Chunking (Not a Retriever, but a Chunking Strategy)

Semantic chunking is a preprocessing step that can improve retrieval. Instead of splitting documents by fixed character counts, it divides text based on semantic similarity.
1.  Embed all sentences in the corpus.
2.  Group adjacent sentences into chunks. A new chunk starts if semantic similarity between consecutive sentences drops below a threshold (the notebook uses `SemanticChunker` with the `percentile` method).
These semantically coherent chunks are stored in a new vector store ("JohnWickSemantic") and retrieved using a standard `naive_retriever`. This method is expected to create more meaningful chunks, leading to better context being fed to the LLM, and thus potentially improving all downstream metrics. If the semantic breaks align well with the information needs, retrieval metrics like `context_recall` and `context_precision` should improve compared to naive chunking.

## 📊 Evaluation: Measuring What Matters

Effective retrieval requires robust evaluation. The notebook uses Ragas, a framework for assessing RAG systems.

### 🌟 Creating a "Golden Dataset"

A "golden dataset" of questions and reference answers is essential. The notebook uses Ragas' `TestsetGenerator` to create this from the John Wick documents, generating:
*   `user_input`: Plausible user questions.
*   `reference_contexts`: Ideal context snippets for each question.
*   `reference`: Ideal human-like answers based on these contexts.
This dataset (18 samples in the notebook) is used to evaluate each RAG chain and is uploaded to LangSmith for detailed analysis.

### 🏃‍♀️ Running the Chains Asynchronously

To efficiently process the golden dataset, an asynchronous function `aapply_rag_chain` is used. It processes items in batches, invoking each chain's `ainvoke` method to get the `response` and `retrieved_contexts`. This speeds up data collection for evaluation. The notebook highlights this as an important practical consideration for speeding up evaluation workflows.

### 📈 The Metrics: Retriever vs. End-to-End

Now, we're going to run some metrics. Here are the interpretations that ChatGPT gives to a five year old 😀
The notebook uses two categories of metrics to assess different aspects of the RAG pipeline:

#### 🎯 Retriever Metrics (Quality of retrieved documents)

Let's imagine you have a big toy box full of picture cards, and you're playing a game where you need to find the right cards to answer a question. These three scores help you understand how good you are at picking cards:

1.  **Context Recall**: Recall measures how many of the right cards you found.
    "If there were 5 cards hiding the puppy picture, and I grabbed 3 of them, my Context Recall is like saying I found 3 out of the 5 puppy cards."
2.  **Context Entity Recall**: Entity Recall checks if you got at least one of the puppy cards.
    "If I'm looking for any card with a star on it, and I picked 1 star card (even if there were 10 in the pile), I get a thumbs-up—because I found at least one star."
3.  **Context Precision**: Precision measures how many of your grabbed cards were actually the ones you wanted.
    "I want to see puppy pictures. If I grab 5 cards but only 2 have puppies on them (and the other 3 are dinosaurs), my Precision is like saying only 2 out of my 5 cards were the right puppy cards."

#### 🏁 End-to-End Metrics (Quality of the final answer)

1.  **Response Relevancy**: "How much of my story is actually about the thing I was asked?"
    "If I tell a story with 10 sentences but only 8 of them talk about puppies (and 2 are about unicorns), Relevancy says I used 8 puppy sentences out of 10."
2.  **Factual Correctness (F1)**: "Of all the true puppy facts I could say, how many did I get right — and did I say any wrong ones?"
    "Imagine there are 3 true puppy facts: 'puppies bark,' 'puppies have fur,' 'puppies wag their tail.' I said 2 of them right, missed 1, and also told 1 wrong fact like 'puppies meow.' F1 scores me by balancing that I found 2 true facts but also made 1 mistake."
3.  **Faithfulness**: "Did I stick to only the cards I picked when telling my story, or did I invent extra stuff?"
    "If my cards only show a puppy, but I say 'and it can fly,' I'm not being faithful to my cards. Faithfulness checks I only talk about what my cards actually show."

Both metric types are vital. Good retriever metrics don't guarantee good answers if the LLM struggles. Conversely, an LLM might produce a decent answer with mediocre context, but this is less reliable. The notebook emphasizes that comprehensive evaluation looks at both aspects.

### ⚙️ Running the Evaluation

The `evaluate` function from Ragas applies these metrics to each chain's outputs (question, retrieved contexts, response, reference answer). This is done asynchronously. Results, including scores for each metric per data point, are stored.

## 🔬 Statistical Analysis: The Quest for "Best"

Determining the "best" retriever isn't simple. The notebook uses a detailed statistical analysis:

1.  **Summary Statistics**: For each retriever and metric, the mean and "StdDev" (standard deviation of the mean, via jackknife leave-one-out) are calculated. This StdDev indicates mean score stability relative to the dataset questions. Low StdDev means consistent performance.

2.  **Ranking**: Retrievers are ranked for each metric by mean score.

3.  **Score Standardization (Centering around Zero)**: Averaging ranks can be misleading if score differences are small. To better show relative performance, scores for each metric are standardized by subtracting the average score for that metric across all retrievers. This centers scores around zero, showing which retrievers are above or below average.

4.  **Aggregated Scores**:
    *   `retrieval_score`: Average of standardized scores for the three retriever metrics.
    *   `eoe_score` (End-of-End Score): Average of standardized scores for the three end-to-end metrics.
    *   An `average_score` across all six metrics is also computed.
    *   `score_variation`, `retrieval_var`, and `eoe_var` show the variance (stability) of these aggregated scores.

### 🤔 Why is Statistical Analysis Not Simple?

Comparing RAG systems involves several complexities:
*   **Dataset Dependency**: Performance is tied to the dataset and question types. A retriever excelling on movie reviews might not be best for technical documents.
*   **Metric Trade-offs**: No single retriever usually wins on all metrics. One might have high recall but lower precision; another might be faithful but miss context. The "best" depends on priorities.
*   **Small Sample Sizes**: Evaluation datasets are often small. Observed differences might not always be statistically significant. The jackknife standard deviation helps assess stability.
*   **Cost and Latency**: The highest-performing system might be too slow or expensive. These real-world factors (tracked by tools like LangSmith, though not directly in this part of the Ragas evaluation) are crucial.
*   **Subjectivity of "Good"**: Aspects like coherence or helpfulness beyond factual accuracy can be subjective.

The notebook's method of using multiple metrics, stability measures, and standardized scores offers a more nuanced comparison than simple averages.

## 📈 Final Interpretation of Tables

The notebook presents its statistical analysis in detailed Pandas DataFrames. Here's an interpretation of what these tables typically reveal, comparing expected behavior with potential outcomes:

*   **No Single Winner**: It's rare for one retriever to dominate all six metrics.
    *   *Expected*: Different strategies have different strengths.
    *   *Obtained*: `parent_document_retriever` might excel in `faithfulness` (due to complete context) and `context_recall`. `compression_retriever` (with Cohere Rerank) might achieve better `llm_context_precision_with_reference`. This aligns with expectations, as reranking specifically targets precision.
*   **BM25's Role**: `bm25` often performs well, especially in `context_entity_recall`.
    *   *Expected*: Strong for keyword-specific queries, fast.
    *   *Obtained*: Its good performance, particularly for entity recall, confirms its utility for queries where specific terms are key.
*   **Multi-Query's Performance**: `multi_query_retriever` can improve recall but sometimes at the cost of precision or by introducing noise.
    *   *Expected*: Better recall by covering more angles of a query. Risk of irrelevant information.
    *   *Obtained*: The tables might show higher `context_recall` but potentially lower `factual_correctness` or `faithfulness` if the LLM processes less relevant context, which is consistent with its mechanism.
*   **Ensemble Benefits**: `ensemble_retriever` often provides a good balance.
    *   *Expected*: More robust, well-rounded performance by combining strengths.
    *   *Obtained*: It may not top any single metric but often scores consistently well across many, acting as a safe, reliable option as anticipated.
*   **Semantic Chunking's Impact**: Comparing a naive retriever with semantically chunked documents versus standard chunking should show improvements.
    *   *Expected*: More meaningful chunks lead to better context.
    *   *Obtained*: Context-related metrics like `context_recall` and `llm_context_precision_with_reference` would likely improve if semantic breaks align well with information needs, confirming the benefit of context-aware chunking.
*   **Parent Document's Strength**: The `parent_document_retriever` is often strong in `faithfulness` and `context_recall`.
    *   *Expected*: Larger context reduces hallucination and improves information availability.
    *   *Obtained*: The results generally confirm this, as providing the LLM with broader context from parent documents helps in generating more grounded and comprehensive answers.
*   **Trade-offs Visible**: Standardized scores (`scores_wo_mean` table) and the final `aggregated_scores_df` highlight these trade-offs. A retriever might have a high positive `retrieval_score` but a slightly negative `eoe_score`, or vice-versa. This is expected as different strategies optimize for different parts of the RAG pipeline.

**Visualizing the Results**:
While the notebook uses tables, bar charts would be effective for visualization:
*   Grouped bar charts for each of the six basic metrics, with bars for each retriever.
*   Bar charts for aggregated scores (`retrieval_score`, `eoe_score`, `average_score`), possibly with error bars for `score_variation`.

A radar chart could also show how "balanced" each retriever's performance is across metrics.

For example, a hypothetical `average_score` bar chart might show:

```
Retriever      | Avg. Standardized Score
--------------------------------------------
Parent         | +0.025  (Slightly above average)
Ensemble       | +0.015
BM25           | +0.010
Naive          | -0.005
Semantic       | -0.008
Compression    | -0.012
Multi-Query    | -0.025  (Slightly below average)
```
*(These are illustrative values)*

This indicates that for this dataset, Parent Document Retrieval performed best overall. However, detailed metric scores are needed to understand *why*.

## 🏁 Conclusion: The Evolving RAG Landscape

Exploring advanced retrieval in LangChain reveals a rich toolkit for optimizing RAG systems. The "best" retriever depends on the specific use case, data, query types, and performance priorities.

Key takeaways:
*   **Experimentation is Key**: Test different strategies for your specific domain.
*   **Evaluation is Non-Negotiable**: Use frameworks like Ragas and comprehensive metrics.
*   **Understand Trade-offs**: Balance retrieval quality, end-to-end answer quality, cost, and latency.
*   **Async Operations**: Useful for speeding up evaluation and batch processing.
*   **Statistical Rigor**: Consider the stability and significance of results beyond simple averages.

The RAG field is dynamic. Understanding these advanced retrieval methods and using rigorous evaluation helps build more intelligent and effective RAG applications.
