from pydantic import BaseModel, Field


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to synthesize")
    speaker_id: str = Field(default="default", min_length=1)
    language: str = Field(default="ms", min_length=2, max_length=16)
    speed: float = Field(default=1.0, gt=0.25, le=2.0)


class SpeakerInfo(BaseModel):
    id: str
    label: str


class SpeakersResponse(BaseModel):
    speakers: list[SpeakerInfo]
