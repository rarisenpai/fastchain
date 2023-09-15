from base import Chunk
from docarray.typing import (
    NdArray,
    NdArrayEmbedding,
    AudioNdArray,
    VideoNdArray,
    AnyEmbedding,
    ImageUrl,
    AudioUrl,
    TextUrl,
    Mesh3DUrl,
    PointCloud3DUrl,
    VideoUrl,
    AnyUrl,
    ID,
    AnyTensor,
    ImageTensor,
    AudioTensor,
    VideoTensor,
    ImageNdArray,
    ImageBytes,
    VideoBytes,
    AudioBytes,
)
from pydantic import Field, ValidationError, validator
from typing import Optional, Tuple, Dict, List

from fastchain.chunker.utils import num_tokens_from_string
from fastchain.constants import MAX_CHUNK_SIZE_TOKENS


class TextChunk(Chunk):
    """Text Chunk class."""

    content_type: str = "plaintext"
    content: str = Field(default_factory=str)
    coordinates: Optional[Tuple]

    @validator("text")
    def validate_text_length(cls, text):
        NUM_TOKENS = num_tokens_from_string(text)
        if NUM_TOKENS > MAX_CHUNK_SIZE_TOKENS:
            raise ValidationError(
                f"Chunk size cannot be greater than MAX_CHUNK_SIZE_TOKENS: {MAX_CHUNK_SIZE_TOKENS}, NUM_TOKENS: {NUM_TOKENS}",
                loc="text",
            )
        return text

    def __str__(self):
        return self.content


class ImageChunk(Chunk):
    """Image Chunk class."""

    content_type: str = "image"
    content: ImageBytes = Field(default_factory=ImageBytes)
    embedding: Optional[NdArrayEmbedding]
    coordinates: Optional[Tuple]


class VideoChunk(Chunk):
    """Video Chunk class."""

    content_type: str = "video"
    content: VideoBytes = Field(default_factory=VideoBytes)
    embedding: Optional[NdArrayEmbedding]
    coordinates: Optional[Tuple]


class AudioChunk(Chunk):
    """Audio Chunk class."""

    content_type: str = "audio"
    content: AudioBytes = Field(default_factory=AudioBytes)
    embedding: Optional[NdArrayEmbedding]


class FigureCaptionChunk(TextChunk):
    """Figure caption existing or autogenerated (model)"""

    content_type: str = "caption"


class TranscribedAudioChunk(TextChunk):
    """Audio transcribed to text"""

    content_type: str = "audio"