import tensorflow as tf
from pydantic import BaseModel, Field
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)

class MusicInput(BaseModel):
    """Model representing user input for music generation."""
    melody: list[int] = Field(..., description="List of MIDI note values for the melody")
    chords: list[str] = Field(..., description="List of chord names (e.g., 'Cmaj7', 'G7')")
    tempo: int = Field(..., description="BPM value for the rhythm")

class MusicService:
    """Service class for generating music arrangements using TensorFlow models."""
    
    def __init__(self):
        """Initialize the service and load the TensorFlow model."""
        self.model = self._load_model()
    
    def _load_model(self):
        """Load the pre-trained TensorFlow model."""
        try:
            model = tf.keras.models.load_model("music_model.h5")
            logging.info("Model loaded successfully")
            return model
        except Exception as e:
            logging.error(f"Failed to load model: {e}")
            raise
    
    def _validate_input(self, input_data: MusicInput):
        """Validate the input data for consistency and completeness."""
        if not input_data.melody or len(input_data.melody) < 5:
            raise ValueError("Melody must contain at least 5 notes")
        if not input_data.chords or len(input_data.chords) < 2:
            raise ValueError("At least 2 chords are required")
        if input_data.tempo < 40 or input_data.tempo > 240:
            raise ValueError("Tempo must be between 40 and 240 BPM")
        return True
    
    def generate_harmony(self, input_data: MusicInput):
        """Generate harmony notes based on the provided musical input."""
        try:
            self._validate_input(input_data)
            logging.info("Generating harmony with input: %s", input_data)
            processed_input = self._process_input(input_data)
            prediction = self.model.predict(processed_input)
            harmony_notes = self._convert_to_notes(prediction)
            return harmony_notes
        except Exception as e:
            logging.error(f"Error generating harmony: {e}")
            raise
    
    def _process_input(self, input_data: MusicInput):
        """Convert input data to a format suitable for the model."""
        melody = np.array(input_data.melody, dtype=np.float32)
        chords = np.array([self._chord_to_vector(chord) for chord in input_data.chords], dtype=np.float32)
        tempo = np.array([input_data.tempo], dtype=np.float32)
        return np.concatenate([melody, chords, tempo])
    
    def _chord_to_vector(self, chord: str) -> np.ndarray:
        """Convert a chord name to a numerical vector."""
        chord_map = {
            "Cmaj7": [1, 0, 0, 0, 0, 0, 0],
            "G7": [0, 1, 0, 0, 0, 0, 0],
            "Am7": [0, 0, 1, 0, 0, 0, 0],
            "D7": [0, 0, 0, 1, 0, 0, 0],
            "Em7": [0, 0, 0, 0, 1, 0, 0],
            "A7": [0, 0, 0, 0, 0, 1, 0],
            "Fmaj7": [0, 0, 0, 0, 0, 0, 1]
        }
        return np.array(chord_map.get(chord, [0]*7), dtype=np.float32)
    
    def _convert_to_notes(self, prediction: np.ndarray) -> list[int]:
        """Convert model prediction to MIDI notes."""
        return [int(note) for note in prediction.flatten()]