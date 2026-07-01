# pod-ft Internal API Contracts

## Crawler → Parser

```
POST /api/v1/parse/html
Content-Type: application/json

{
    "url": "https://www.fedsfm.ru/news/7338",
    "html_content": "<html>...",
    "document_title": "Памятка для субъектов статьи 7.1"
}
```

Response 200:
```json
{
    "document_id": "uuid",
    "document_title": "Памятка...",
    "fragments": [
        {
            "fragment_id": "uuid",
            "fragment_no": 1,
            "section_path": "#content",
            "paragraph_label": "п. 1",
            "fragment_text": "...",
            "citation_label": "п. п. 1",
            "token_count": 42
        }
    ],
    "fragment_count": 42
}
```

## Parser → Versioning

```
POST /api/v1/documents/register
Content-Type: application/json

{
    "canonical_url": "https://www.fedsfm.ru/news/7338",
    "document_title": "Памятка для субъектов статьи 7.1",
    "document_kind": "memo",
    "content_hash": "sha256hex...",
    "regulator_code": "rosfinmonitoring"
}
```

Response 201:
```json
{
    "document_id": "uuid",
    "version_id": "uuid",
    "is_new_version": true,
    "version_label": "v1",
    "is_current": true
}
```

## Answer → Verification

Defined in spec section 11.3.

## Evidence trail

Every answer carries:
- source domain + URL
- document version + fragment citation
- prompt hash + verifier model + verifier result
- rules engine result (sufficiency policy decision)
