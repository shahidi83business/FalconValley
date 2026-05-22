#raghelper.py
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import numpy as np

from openai import AsyncOpenAI


@dataclass
class DocChunk:
    id: str
    text: str
    meta: Dict[str, str]
    embedding: Optional[np.ndarray] = None


def _cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-12
    return float(np.dot(a, b) / denom)


class RAGHelper:
    """
    Minimal RAG:
      - add_documents(): chunks -> embeddings -> store in memory
      - query(): embed query -> top-k retrieve -> answer with citations
    """

    def __init__(
        self,
        *,
        embedding_model: str = "text-embedding-3-small",
        chat_model: str = "gpt-4.1-mini",
        top_k: int = 5,
    ):
        self.client = AsyncOpenAI()
        self.embedding_model = embedding_model
        self.chat_model = chat_model
        self.top_k = top_k
        self._store: List[DocChunk] = []

    async def embed_texts(self, texts: List[str]) -> List[np.ndarray]:
        # why: embeddings are the retrieval index
        resp = await self.client.embeddings.create(
            model=self.embedding_model,
            input=texts,
        )
        # resp.data[i].embedding is a list[float]
        return [np.array(item.embedding, dtype=np.float32) for item in resp.data]

    async def add_documents(
        self,
        chunks: List[DocChunk],
        *,
        batch_size: int = 64,
    ) -> None:
        # Embed in batches for speed + rate limits
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            embs = await self.embed_texts([c.text for c in batch])
            for c, e in zip(batch, embs):
                c.embedding = e
                self._store.append(c)

    def _retrieve(self, query_emb: np.ndarray, top_k: Optional[int] = None) -> List[Tuple[float, DocChunk]]:
        k = top_k or self.top_k
        scored: List[Tuple[float, DocChunk]] = []
        for c in self._store:
            if c.embedding is None:
                continue
            scored.append((_cosine_sim(query_emb, c.embedding), c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:k]

    async def query(
        self,
        user_query: str,
        *,
        system_prompt: str = "You are a helpful assistant. Use the provided context. If context is insufficient, say so.",
        top_k: Optional[int] = None,
        temperature: float = 0.2,
        max_context_chars: int = 8000,
    ) -> Dict:
        if not self._store:
            return {
                "answer": "No documents indexed yet. Add documents first.",
                "contexts": [],
            }

        q_emb = (await self.embed_texts([user_query]))[0]
        hits = self._retrieve(q_emb, top_k=top_k)

        # Build context with lightweight citations
        contexts = []
        ctx_parts = []
        total = 0
        for score, chunk in hits:
            cite = f"[{chunk.id}]"
            piece = f"{cite} {chunk.text.strip()}"
            if total + len(piece) > max_context_chars:
                break
            total += len(piece)
            ctx_parts.append(piece)
            contexts.append({
                "id": chunk.id,
                "score": score,
                "meta": chunk.meta,
                "text": chunk.text,
            })

        context_block = "\n\n".join(ctx_parts) if ctx_parts else "(no context retrieved)"

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    "Answer the question using ONLY the context below. "
                    "Cite sources inline like [chunk_id].\n\n"
                    f"CONTEXT:\n{context_block}\n\n"
                    f"QUESTION:\n{user_query}"
                ),
            },
        ]

        resp = await self.client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=temperature,
        )

        return {
            "answer": resp.choices[0].message.content,
            "contexts": contexts,
        }
