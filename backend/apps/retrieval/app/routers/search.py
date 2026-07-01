__anchor__ = "retrieval"
# schema-ref: project-schema.yaml#/services/8

from fastapi import APIRouter

from backend.apps.retrieval.app.schemas.search import (
    FragmentResult,
    IndexFragmentsRequest,
    IndexFragmentsResponse,
    SearchRequest,
    SearchResponse,
)
from backend.apps.retrieval.app.services.retrieval_service import RetrievalService

router = APIRouter(tags=["retrieval"])
_service = RetrievalService()


@router.post("/search", response_model=SearchResponse)
async def search_fragments(payload: SearchRequest) -> SearchResponse:
    results = await _service.search(
        query=payload.query,
        subject_type=payload.subject_type,
        regulator=payload.regulator,
        top_k=payload.top_k,
        min_confidence=payload.min_confidence,
    )
    return SearchResponse(
        query=payload.query,
        results=[FragmentResult(**r) for r in results],
        total_count=len(results),
        anchor="retrieval",
    )


@router.post("/index", response_model=IndexFragmentsResponse)
async def index_fragments(payload: IndexFragmentsRequest) -> IndexFragmentsResponse:
    count = await _service.index_fragments(
        [f.model_dump() for f in payload.fragments]
    )
    return IndexFragmentsResponse(indexed_count=count, anchor="retrieval")


@router.get("/fragments", response_model=list[FragmentResult])
async def list_indexed_fragments() -> list[FragmentResult]:
    fragments = await _service.list_fragments()
    return [FragmentResult(**f) for f in fragments]


@router.delete("/fragments/{fragment_id}", status_code=204)
async def delete_fragment(fragment_id: str) -> None:
    await _service.remove_fragment(fragment_id)
