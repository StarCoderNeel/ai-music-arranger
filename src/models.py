import logging
import re
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MusicNote(BaseModel):
    """Represents a single musical note with pitch, duration, and timing."""
    pitch: str
    duration: float
    timing: float

    @validator('pitch')
    def validate_pitch(cls, value):
        """Validate that the pitch is in a standard format (e.g., 'C4', 'A#3')."""
        if not isinstance(value, str):
            raise ValueError("Pitch must be a string")
        if not re.match(r'^[A-G][#b]?[0-9]+$', value):
            raise ValueError(f"Invalid pitch format: {value}")
        return value

class ChordProgression(BaseModel):
    """Represents a sequence of chords with associated musical notes."""
    notes: List[MusicNote]
    key: str

    @validator('key')
    def validate_key(cls, value):
        """Validate that the key is a non-empty string."""
        if not isinstance(value, str):
            raise ValueError("Key must be a string")
        if not value.strip():
            raise ValueError("Key cannot be empty")
        return value

class RhythmicPattern(BaseModel):
    """Represents a rhythmic pattern with beat durations and tempo."""
    beats: List[float]
    tempo: float

    @validator('tempo')
    def validate_tempo(cls, value):
        """Validate that the tempo is a positive number."""
        if value <= 0:
            raise ValueError("Tempo must be a positive number")
        return value

def validate_music_data(data: Dict) -> Dict:
    """
    Validate and convert raw music data into Pydantic models.
    Returns a dictionary with validated notes, chords, and rhythm.
    """
    logger.info("Validating music data")
    try:
        notes = [MusicNote(**note) for note in data.get('notes', [])]
        chords = [ChordProgression(**chord) for chord in data.get('chords', [])]
        rhythm = RhythmicPattern(**data.get('rhythm', {}))
        return {
            'notes': notes,
            'chords': chords,
            'rhythm': rhythm
        }
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise ValueError(f"Invalid music data: {e}")

def notes_to_array(notes: List[MusicNote]) -> np.ndarray:
    """
    Convert a list of MusicNote objects to a numpy array for TensorFlow processing.
    Each row contains pitch, duration, and timing values.
    """
    logger.info("Converting notes to numpy array")
    if not notes:
        return np.array([])
    pitches = [note.pitch for note in notes]
    durations = [note.duration for note in notes]
    timings = [note.timing for note in notes]
    return np.array([pitches, durations, timings]).T