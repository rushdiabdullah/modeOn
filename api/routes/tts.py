from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.auth import require_api_key
from api.models.schemas import SpeakersResponse, SpeakerInfo, TTSRequest
from tts.config import get_settings

router = APIRouter(prefix="/v1", tags=["tts"])


def get_engine():
    from api.main import get_tts_engine

    return get_tts_engine()


@router.get("/speakers", response_model=SpeakersResponse)
def list_speakers(_: None = Depends(require_api_key)) -> SpeakersResponse:
    return SpeakersResponse(speakers=[SpeakerInfo(id="default", label="Default voice")])


@router.post("/tts")
def synthesize(
    body: TTSRequest,
    _: None = Depends(require_api_key),
    engine=Depends(get_engine),
) -> Response:
    settings = get_settings()
    if len(body.text) > settings.max_text_chars:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"text exceeds max length ({settings.max_text_chars} chars)",
        )

    try:
        audio = engine.synthesize(
            body.text,
            speaker_id=body.speaker_id,
            language=body.language,
            speed=body.speed,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)) from e

    return Response(content=audio, media_type="audio/wav")
