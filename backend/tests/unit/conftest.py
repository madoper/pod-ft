__anchor__ = "tests"

import pytest


@pytest.fixture(autouse=True)
def _reset_retrieval_index() -> None:
    from backend.apps.retrieval.app.services.retrieval_service import RetrievalService
    RetrievalService.clear_index()
