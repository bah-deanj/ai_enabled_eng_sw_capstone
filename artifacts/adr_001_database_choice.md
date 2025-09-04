# Architectural Decision Record: Use PostgreSQL with pgvector

## Status
Accepted

## Context

The new hire onboarding tool requires storing and searching vector embeddings to enable semantic search and personalized recommendations. The primary backend options considered for this purpose were:

1. **PostgreSQL with the pgvector extension:** Enhances PostgreSQL to support vector datatypes and similarity search, allowing embeddings to be stored and queried alongside traditional relational data.
2. **Specialized vector databases** (such as ChromaDB, FAISS, Pinecone, Milvus): Purpose-built for efficient, large-scale vector search and related ML-centric features.

Key contextual factors influencing this decision include:

- The current infrastructure already uses PostgreSQL as the primary database.
- The expected scale of embeddings and query volume is moderate, aligning with an initial rollout or proof-of-concept rather than immediate large-scale production.
- Operational simplicity and ease of integration are prioritized to accelerate time-to-market.
- The engineering team has strong familiarity with PostgreSQL and its ecosystem.
- Cost control is important, especially in early development stages.

## Decision

We will **use PostgreSQL with the pgvector extension** as the backend for storing and searching vector embeddings in the new hire onboarding tool.

- Embeddings will be stored as vector columns in existing or new PostgreSQL tables.
- pgvector will enable similarity search (e.g., nearest neighbor queries) directly in SQL, allowing easy integration with existing user and onboarding data.
- This approach leverages our existing database infrastructure, tools, and operational workflows.

## Consequences

**Positive Effects:**

- **Simplicity and Speed:** Single database to operate, reducing the number of moving parts and accelerating development.
- **Integration:** Vector search can be combined with relational queries (e.g., filtering or joining with user metadata) using familiar SQL constructs.
- **Cost Efficiency:** No additional infrastructure cost or devops overhead, as PostgreSQL is already in use.
- **Maturity and Reliability:** PostgreSQL is a stable, ACID-compliant database with strong backup, monitoring, and tooling support.

**Negative Effects:**

- **Performance Limitations:** At scale (millions of vectors, high query throughput), vector search performance may not match that of specialized vector databases. Latency and throughput may become bottlenecks.
- **Scalability Constraints:** PostgreSQL is less suited for distributed, large-scale vector workloads. Scaling may require vertical scaling or basic sharding, which can be limiting.
- **Feature Gaps:** Lacks some advanced vector search features (e.g., hybrid search, advanced filtering, custom re-ranking) available in dedicated vector DBs.

**Follow-up Actions:**

- **Monitor Usage and Performance:** If embedding storage or query volume grows significantly, or advanced features are required, reevaluate adoption of a specialized vector database.
- **Stay Updated:** Monitor pgvector and PostgreSQL feature evolution for improvements in performance and capabilities.
- **Document Limitations:** Clearly document the limitations and potential migration paths for future scale.

---

**In summary:**  
PostgreSQL with pgvector is the optimal choice for the current onboarding tool’s needs, balancing ease of integration, operational simplicity, cost, and sufficient performance for the initial scale. This approach allows rapid prototyping and iteration, with a clear migration path to more specialized vector search infrastructure if future requirements demand it.