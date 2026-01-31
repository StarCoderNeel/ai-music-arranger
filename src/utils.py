import logging
from typing import List, Optional
from pydantic import BaseModel
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Note(BaseModel):
    """Represents a musical note with pitch, accidental, and octave."""
    pitch: str
    accidental: Optional[str] = None
    octave: int

def parse_note(note_str: str) -> Note:
    """
    Parse a musical note string (e.g., 'C4', 'D#5', 'Eb2') into a Note model.
    
    Args:
        note_str (str): The note string to parse.
        
    Returns:
        Note: A Note model representing the parsed note.
        
    Raises:
        ValueError: If the note string is invalid.
    """
    try:
        match = re.match(r'^([A-Ga-g])([#b]?)(\d+)$', note_str)
        if not match:
            raise ValueError(f"Invalid note format: {note_str}")
        pitch = match.group(1).upper()
        accidental = match.group(2)
        octave = int(match.group(3))
        if pitch not in 'ABCDEFG':
            raise ValueError(f"Invalid pitch: {pitch}")
        if accidental not in ['', '#', 'b']:
            raise ValueError(f"Invalid accidental: {accidental}")
        return Note(pitch=pitch, accidental=accidental, octave=octave)
    except Exception as e:
        logging.error(f"Error parsing note {note_str}: {e}")
        raise

def format_notes(notes: List[Note]) -> str:
    """
    Format a list of Note objects into a space-separated string representation.
    
    Args:
        notes (List[Note]): List of Note objects to format.
        
    Returns:
        str: Formatted string of notes.
        
    Raises:
        ValueError: If input is invalid.
    """
    try:
        formatted = []
        for note in notes:
            pitch = note.pitch
            accidental = note.accidental or ''
            octave = note.octave
            acc_str = '#' if accidental == '#' else 'b' if accidental == 'b' else ''
            formatted.append(f"{pitch}{acc_str}{octave}")
        return ' '.join(formatted)
    except Exception as e:
        logging.error(f"Error formatting notes: {e}")
        raise

class Scale:
    """Represents a musical scale with a root note and scale type."""
    
    def __init__(self, root: str, scale_type: str):
        """
        Initialize a Scale object.
        
        Args:
            root (str): The root note of the scale (e.g., 'C4').
            scale_type (str): The type of scale (e.g., 'major', 'minor').
        """
        self.root = root
        self.scale_type = scale_type
        self.notes = self._generate_scale()
    
    def _generate_scale(self) -> List[Note]:
        """Generate the scale notes based on root and scale type."""
        try:
            root_note = parse_note(self.root)
            if self.scale_type.lower() == 'major':
                return [
                    root_note,
                    Note(pitch='D', octave=root_note.octave),
                    Note(pitch='E', octave=root_note.octave),
                    Note(pitch='F', octave=root_note.octave),
                    Note(pitch='G', octave=root_note.octave),
                    Note(pitch='A', octave=root_note.octave),
                    Note(pitch='B', octave=root_note.octave)
                ]
            elif self.scale_type.lower() == 'minor':
                return [
                    root_note,
                    Note(pitch='D', octave=root_note.octave),
                    Note(pitch='F', octave=root_note.octave),
                    Note(pitch='G', octave=root_note.octave),
                    Note(pitch='A', octave=root_note.octave),
                    Note(pitch='B', octave=root_note.octave),
                    Note(pitch='C', octave=root_note.octave + 1)
                ]
            else:
                raise ValueError(f"Unsupported scale type: {self.scale_type}")
        except Exception as e:
            logging.error(f"Error generating scale: {e}")
            raise
    
    def get_notes(self) -> List[Note]:
        """Get the list of notes in the scale."""
        return self.notes