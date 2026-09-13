"""
Advanced Animated Male Face System with Merging and Lip-Sync
Creates realistic male faces with blended emotions and speech synchronization
"""

from typing import Dict, Tuple, Optional, List
from enum import Enum
from datetime import datetime, timedelta
import math
import re


class FacialExpression(Enum):
    """Different facial expressions based on emotions"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    CURIOUS = "curious"
    CONFUSED = "confused"
    THINKING = "thinking"
    EXCITED = "excited"
    CONCERNED = "concerned"
    PLAYFUL = "playful"
    CONTEMPLATIVE = "contemplative"
    LISTENING = "listening"
    SPEAKING = "speaking"


class EyeState(Enum):
    """Eye animation states"""
    OPEN = "open"
    HALF_OPEN = "half_open"
    CLOSED = "closed"
    BLINKING = "blinking"
    LOOKING_LEFT = "looking_left"
    LOOKING_RIGHT = "looking_right"
    LOOKING_UP = "looking_up"
    LOOKING_DOWN = "looking_down"
    WIDE_OPEN = "wide_open"


class MouthState(Enum):
    """Mouth animation states for speech"""
    CLOSED = "closed"
    SLIGHT_SMILE = "slight_smile"
    SMILE = "smile"
    WIDE_SMILE = "wide_smile"
    # Phoneme states for lip-sync
    A_SHAPE = "a_shape"      # like "ay", "ah" - wide open
    E_SHAPE = "e_shape"      # like "ee" - spread smile
    I_SHAPE = "i_shape"      # like "ih" - narrow
    O_SHAPE = "o_shape"      # like "oh", "aw" - round
    U_SHAPE = "u_shape"      # like "oo" - rounded pout
    M_SHAPE = "m_shape"      # like "m", "b", "p" - closed lips
    THINKING = "thinking"
    CONCERNED = "concerned"
    NEUTRAL_OPEN = "neutral_open"


class MaleAnimatedFace:
    """
    Generates realistic animated male face with merging capabilities and lip-sync
    Supports face blending when emotions merge
    """
    
    # Base face dimensions (SVG-like coordinates)
    FACE_WIDTH = 200
    FACE_HEIGHT = 280  # Taller for male features
    
    def __init__(self, personality_name: str = "The Optimist"):
        self.personality_name = personality_name
        self.current_expression = FacialExpression.NEUTRAL
        self.left_eye_state = EyeState.OPEN
        self.right_eye_state = EyeState.OPEN
        self.mouth_state = MouthState.CLOSED
        
        # Blended face system
        self.primary_expression = FacialExpression.NEUTRAL
        self.secondary_expression: Optional[FacialExpression] = None
        self.blend_intensity = 0.0  # 0.0 = primary only, 1.0 = secondary only
        
        # Animation state
        self.blink_timer = 0
        self.blink_interval = 4000  # ms between blinks
        self.is_blinking = False
        
        # Speaking state with lip-sync
        self.is_speaking = False
        self.speech_timer = 0
        self.current_phoneme = "closed"
        self.speech_queue: List[Dict] = []  # Queue of phonemes to animate
        
        # Look direction (for interaction)
        self.look_direction = (0, 0)  # x, y offset
        self.look_intensity = 0.5
        
        # Jaw animation for speaking
        self.jaw_open = 0.0  # 0.0 = closed, 1.0 = fully open
        
        # Personality-specific colors (male-focused)
        self.personality_colors = self._get_male_personality_colors()
        
        # Animation state
        self.last_update = datetime.now()
    
    def _get_male_personality_colors(self) -> Dict:
        """Get personality-specific color scheme for male face"""
        colors = {
            "The Philosopher": {
                "primary": "#6B4423",      # Dark brown (scholarly)
                "secondary": "#8B6F47",    # Tan brown
                "accent": "#9D7E47",       # Warm tan
                "skin": "#C19A6B",         # Male skin tone
                "eyes": "#1C0F06",         # Very dark brown
                "eyebrows": "#4A2511",     # Dark brown eyebrows
                "stubble": "#8B7355",      # 5 o'clock shadow
                "glow": "#D4AF37"          # Gold glow
            },
            "The Optimist": {
                "primary": "#FFB300",      # Vibrant gold (energetic)
                "secondary": "#FFA500",    # Orange
                "accent": "#FF8C00",       # Dark orange
                "skin": "#E8B88B",         # Warm tan male skin
                "eyes": "#000000",         # Black
                "eyebrows": "#3D2817",     # Dark eyebrows
                "stubble": "#A68577",      # Light stubble
                "glow": "#FFEB3B"          # Bright yellow glow
            },
            "The Mystique": {
                "primary": "#6A0572",      # Deep purple (mysterious)
                "secondary": "#8B3A8B",    # Medium purple
                "accent": "#2D0047",       # Very dark purple
                "skin": "#D4A574",         # Pale cool-toned male skin
                "eyes": "#00FF00",         # Neon green
                "eyebrows": "#1A0033",     # Very dark purple-black
                "stubble": "#8B5A8B",      # Purple-tinted stubble
                "glow": "#FF00FF"          # Magenta glow
            },
            "The Companion": {
                "primary": "#E91E63",      # Hot pink (warm)
                "secondary": "#C2185B",    # Deeper pink
                "accent": "#880E4F",       # Dark pink
                "skin": "#D4A5A5",         # Warm peachy male skin
                "eyes": "#663344",         # Deep brown
                "eyebrows": "#4A1A2D",     # Dark reddish-brown
                "stubble": "#9D7080",      # Reddish stubble
                "glow": "#FF1493"          # Deep pink glow
            },
            "The Analyst": {
                "primary": "#0D47A1",      # Deep blue (logical)
                "secondary": "#1565C0",    # Royal blue
                "accent": "#00BCD4",       # Cyan accent
                "skin": "#C9B3A8",         # Cool-toned male skin
                "eyes": "#00FF00",         # Lime green
                "eyebrows": "#0A1F4A",     # Very dark blue
                "stubble": "#6B7B8E",      # Blue-tinted stubble
                "glow": "#00FFFF"          # Cyan glow
            }
        }
        
        return colors.get(self.personality_name, colors["The Optimist"])
    
    def set_blended_expression(self, primary_emotion: str, secondary_emotion: str, 
                              blend_amount: float = 0.5):
        """
        Set face to blend between two emotions
        blend_amount: 0.0 = 100% primary, 1.0 = 100% secondary
        """
        emotion_to_expression = {
            "joyful": FacialExpression.HAPPY,
            "curious": FacialExpression.CURIOUS,
            "contemplative": FacialExpression.CONTEMPLATIVE,
            "concerned": FacialExpression.CONCERNED,
            "playful": FacialExpression.PLAYFUL,
            "calm": FacialExpression.NEUTRAL,
            "excited": FacialExpression.EXCITED,
            "confused": FacialExpression.CONFUSED,
            "thoughtful": FacialExpression.THINKING,
            "mischievous": FacialExpression.PLAYFUL
        }
        
        self.primary_expression = emotion_to_expression.get(primary_emotion, FacialExpression.NEUTRAL)
        self.secondary_expression = emotion_to_expression.get(secondary_emotion, FacialExpression.NEUTRAL)
        self.blend_intensity = min(1.0, max(0.0, blend_amount))
        
        # Update facial features for blended expression
        self._update_blended_facial_features()
    
    def update_expression(self, emotion: str, intensity: float = 0.5):
        """Update facial expression based on emotion (non-blended)"""
        emotion_to_expression = {
            "joyful": FacialExpression.HAPPY,
            "curious": FacialExpression.CURIOUS,
            "contemplative": FacialExpression.CONTEMPLATIVE,
            "concerned": FacialExpression.CONCERNED,
            "playful": FacialExpression.PLAYFUL,
            "calm": FacialExpression.NEUTRAL,
            "excited": FacialExpression.EXCITED,
            "confused": FacialExpression.CONFUSED,
            "thoughtful": FacialExpression.THINKING,
            "mischievous": FacialExpression.PLAYFUL
        }
        
        self.current_expression = emotion_to_expression.get(emotion, FacialExpression.NEUTRAL)
        self.primary_expression = self.current_expression
        self.secondary_expression = None
        self.blend_intensity = 0.0
        self._update_facial_features(self.current_expression, intensity)
    
    def _update_blended_facial_features(self):
        """Update facial features for blended emotions"""
        # Get eye states for both expressions
        primary_eyes = self._get_expression_eye_state(self.primary_expression)
        secondary_eyes = self._get_expression_eye_state(self.secondary_expression)
        
        # Blend eye states
        if self.blend_intensity < 0.5:
            self.left_eye_state = primary_eyes[0]
            self.right_eye_state = primary_eyes[1]
        else:
            self.left_eye_state = secondary_eyes[0]
            self.right_eye_state = secondary_eyes[1]
        
        # Get mouth states for both expressions
        primary_mouth = self._get_expression_mouth_state(self.primary_expression)
        secondary_mouth = self._get_expression_mouth_state(self.secondary_expression)
        
        # Blend mouth states (favor more expressive state)
        if self.blend_intensity < 0.5:
            self.mouth_state = primary_mouth
        else:
            self.mouth_state = secondary_mouth
    
    def _get_expression_eye_state(self, expression: FacialExpression) -> Tuple:
        """Get default eye state for expression"""
        eye_states = {
            FacialExpression.HAPPY: (EyeState.OPEN, EyeState.OPEN),
            FacialExpression.CURIOUS: (EyeState.WIDE_OPEN, EyeState.WIDE_OPEN),
            FacialExpression.CONFUSED: (EyeState.HALF_OPEN, EyeState.HALF_OPEN),
            FacialExpression.THINKING: (EyeState.OPEN, EyeState.LOOKING_UP),
            FacialExpression.EXCITED: (EyeState.WIDE_OPEN, EyeState.WIDE_OPEN),
            FacialExpression.CONCERNED: (EyeState.HALF_OPEN, EyeState.HALF_OPEN),
            FacialExpression.PLAYFUL: (EyeState.OPEN, EyeState.OPEN),
            FacialExpression.CONTEMPLATIVE: (EyeState.HALF_OPEN, EyeState.HALF_OPEN),
            FacialExpression.LISTENING: (EyeState.OPEN, EyeState.OPEN),
            FacialExpression.NEUTRAL: (EyeState.OPEN, EyeState.OPEN),
        }
        return eye_states.get(expression, (EyeState.OPEN, EyeState.OPEN))
    
    def _get_expression_mouth_state(self, expression: FacialExpression) -> MouthState:
        """Get default mouth state for expression"""
        mouth_states = {
            FacialExpression.HAPPY: MouthState.WIDE_SMILE,
            FacialExpression.CURIOUS: MouthState.SLIGHT_SMILE,
            FacialExpression.CONFUSED: MouthState.THINKING,
            FacialExpression.THINKING: MouthState.THINKING,
            FacialExpression.EXCITED: MouthState.WIDE_SMILE,
            FacialExpression.CONCERNED: MouthState.CONCERNED,
            FacialExpression.PLAYFUL: MouthState.SMILE,
            FacialExpression.CONTEMPLATIVE: MouthState.SLIGHT_SMILE,
            FacialExpression.LISTENING: MouthState.NEUTRAL_OPEN,
            FacialExpression.NEUTRAL: MouthState.CLOSED,
        }
        return mouth_states.get(expression, MouthState.CLOSED)
    
    def _update_facial_features(self, expression: FacialExpression, intensity: float):
        """Update eye and mouth states based on expression"""
        if expression == FacialExpression.HAPPY:
            self.left_eye_state = EyeState.OPEN
            self.right_eye_state = EyeState.OPEN
            self.mouth_state = MouthState.WIDE_SMILE if intensity > 0.7 else MouthState.SMILE
        elif expression == FacialExpression.CURIOUS:
            self.left_eye_state = EyeState.WIDE_OPEN
            self.right_eye_state = EyeState.WIDE_OPEN
            self.mouth_state = MouthState.SLIGHT_SMILE
        elif expression == FacialExpression.CONFUSED:
            self.left_eye_state = EyeState.HALF_OPEN
            self.right_eye_state = EyeState.HALF_OPEN
            self.mouth_state = MouthState.THINKING
        elif expression == FacialExpression.THINKING:
            self.left_eye_state = EyeState.OPEN
            self.right_eye_state = EyeState.LOOKING_UP
            self.mouth_state = MouthState.THINKING
        elif expression == FacialExpression.EXCITED:
            self.left_eye_state = EyeState.WIDE_OPEN
            self.right_eye_state = EyeState.WIDE_OPEN
            self.mouth_state = MouthState.WIDE_SMILE
        elif expression == FacialExpression.CONCERNED:
            self.left_eye_state = EyeState.HALF_OPEN
            self.right_eye_state = EyeState.HALF_OPEN
            self.mouth_state = MouthState.CONCERNED
        elif expression == FacialExpression.PLAYFUL:
            self.left_eye_state = EyeState.OPEN
            self.right_eye_state = EyeState.OPEN
            self.mouth_state = MouthState.WIDE_SMILE
        elif expression == FacialExpression.CONTEMPLATIVE:
            self.left_eye_state = EyeState.HALF_OPEN
            self.right_eye_state = EyeState.HALF_OPEN
            self.mouth_state = MouthState.SLIGHT_SMILE
        elif expression == FacialExpression.LISTENING:
            self.left_eye_state = EyeState.OPEN
            self.right_eye_state = EyeState.OPEN
            self.mouth_state = MouthState.NEUTRAL_OPEN
    
    def analyze_speech_for_phonemes(self, text: str) -> List[Dict]:
        """
        Analyze speech text and generate phoneme sequence for lip-sync
        Returns list of {phoneme, duration_ms}
        """
        # Phoneme mapping for common English sounds
        phoneme_map = {
            r'[aeiou]': 'vowel',
            r'[b|p|m]': 'm_shape',
            r'[f|v]': 'e_shape',
            r'[t|d|n|l|s|z|r]': 'i_shape',
            r'[k|g|ng|j|ch|sh|th|w|y]': 'o_shape',
        }
        
        text_lower = text.lower()
        phonemes = []
        current_pos = 0
        
        for match in re.finditer(r'\w', text_lower):
            char = match.group()
            duration = 80  # ms per phoneme
            
            if char in 'aeiou':
                if char in 'ae':
                    phonemes.append({'phoneme': MouthState.A_SHAPE, 'duration': duration})
                elif char in 'iu':
                    phonemes.append({'phoneme': MouthState.I_SHAPE, 'duration': duration})
                else:  # o
                    phonemes.append({'phoneme': MouthState.O_SHAPE, 'duration': duration})
            elif char in 'bpm':
                phonemes.append({'phoneme': MouthState.M_SHAPE, 'duration': duration})
            elif char in 'fv':
                phonemes.append({'phoneme': MouthState.E_SHAPE, 'duration': duration})
            elif char in 'tdnlsz':
                phonemes.append({'phoneme': MouthState.I_SHAPE, 'duration': duration})
            elif char in 'kgwj':
                phonemes.append({'phoneme': MouthState.O_SHAPE, 'duration': duration})
        
        return phonemes
    
    def start_speaking_with_text(self, text: str):
        """
        Start speaking animation with text for lip-sync
        """
        self.is_speaking = True
        self.speech_timer = 0
        self.current_expression = FacialExpression.SPEAKING
        self.left_eye_state = EyeState.OPEN
        self.right_eye_state = EyeState.OPEN
        
        # Generate phoneme sequence
        self.speech_queue = self.analyze_speech_for_phonemes(text)
    
    def stop_speaking(self):
        """Stop speaking animation"""
        self.is_speaking = False
        self.speech_timer = 0
        self.jaw_open = 0.0
        self.mouth_state = MouthState.CLOSED
        self.speech_queue = []
    
    def update_speech_animation(self, delta_time_ms: float = 16):
        """
        Update speech animation with lip-sync
        Call every frame during speaking
        """
        if not self.is_speaking or not self.speech_queue:
            return
        
        self.speech_timer += delta_time_ms
        
        # Update mouth based on speech queue
        elapsed = 0
        for phoneme_data in self.speech_queue:
            phoneme = phoneme_data['phoneme']
            duration = phoneme_data['duration']
            
            if elapsed <= self.speech_timer < elapsed + duration:
                self.mouth_state = phoneme
                # Update jaw based on phoneme openness
                if phoneme in [MouthState.A_SHAPE, MouthState.O_SHAPE]:
                    self.jaw_open = 0.8
                elif phoneme in [MouthState.E_SHAPE, MouthState.I_SHAPE]:
                    self.jaw_open = 0.4
                else:
                    self.jaw_open = 0.2
                return
            
            elapsed += duration
        
        # Speech complete
        self.stop_speaking()
    
    def update_blink(self, delta_time_ms: float = 16):
        """Update blink animation (call every frame)"""
        self.blink_timer += delta_time_ms
        
        if self.blink_timer >= self.blink_interval:
            self.is_blinking = True
            self.blink_timer = 0
        
        if self.is_blinking:
            # Blink animation duration: 150ms
            if self.speech_timer < 150:
                # Closing phase
                progress = self.speech_timer / 75
                if progress < 1.0:
                    self.left_eye_state = EyeState.HALF_OPEN
                    self.right_eye_state = EyeState.HALF_OPEN
                else:
                    self.left_eye_state = EyeState.CLOSED
                    self.right_eye_state = EyeState.CLOSED
            else:
                # Opening phase
                progress = (self.speech_timer - 150) / 75
                if progress < 1.0:
                    self.left_eye_state = EyeState.HALF_OPEN
                    self.right_eye_state = EyeState.HALF_OPEN
                else:
                    self.left_eye_state = EyeState.OPEN
                    self.right_eye_state = EyeState.OPEN
                    self.is_blinking = False
            
            self.speech_timer += delta_time_ms
    
    def look_at_direction(self, x_offset: float, y_offset: float, intensity: float = 0.5):
        """Make the face look in a direction"""
        self.look_direction = (x_offset, y_offset)
        self.look_intensity = min(1.0, max(0.0, intensity))
        
        # Update eye state based on direction
        if intensity > 0.3:
            if x_offset < -0.3:
                self.left_eye_state = EyeState.LOOKING_LEFT
                self.right_eye_state = EyeState.LOOKING_LEFT
            elif x_offset > 0.3:
                self.left_eye_state = EyeState.LOOKING_RIGHT
                self.right_eye_state = EyeState.LOOKING_RIGHT
            elif y_offset < -0.3:
                self.left_eye_state = EyeState.LOOKING_UP
                self.right_eye_state = EyeState.LOOKING_UP
            elif y_offset > 0.3:
                self.left_eye_state = EyeState.LOOKING_DOWN
                self.right_eye_state = EyeState.LOOKING_DOWN
    
    def get_svg_male_face(self, size: int = 200) -> str:
        """
        Generate SVG representation of the animated male face
        Returns SVG string for rendering
        """
        scale = size / self.FACE_WIDTH
        colors = self.personality_colors
        
        # Build SVG with male features
        svg_parts = [
            f'<svg width="{size}" height="{int(self.FACE_HEIGHT * scale)}" viewBox="0 0 {self.FACE_WIDTH} {self.FACE_HEIGHT}" xmlns="http://www.w3.org/2000/svg">',
            
            # Defs for gradients and filters
            f'<defs>',
            f'  <radialGradient id="skin-gradient" cx="40%" cy="40%">',
            f'    <stop offset="0%" style="stop-color:{colors["skin"]};stop-opacity:1" />',
            f'    <stop offset="100%" style="stop-color:{self._darken_color(colors["skin"], 0.8)};stop-opacity:1" />',
            f'  </radialGradient>',
            f'  <radialGradient id="glow" cx="50%" cy="50%" r="50%">',
            f'    <stop offset="0%" style="stop-color:{colors["glow"]};stop-opacity:0.4" />',
            f'    <stop offset="100%" style="stop-color:{colors["glow"]};stop-opacity:0" />',
            f'  </radialGradient>',
            f'  <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">',
            f'    <feDropShadow dx="0" dy="3" stdDeviation="4" flood-opacity="0.4"/>',
            f'  </filter>',
            f'</defs>',
            
            # Glow circle
            f'<circle cx="100" cy="140" r="115" fill="url(#glow)" filter="url(#shadow)"/>',
            
            # Male face shape (more angular/squared)
            f'<path d="M 60 80 L 40 140 Q 35 180 60 220 L 140 220 Q 165 180 160 140 L 140 80 Z" fill="url(#skin-gradient)" stroke="{colors["secondary"]}" stroke-width="1.5"/>',
            
            # Stubble/shadow (5 o'clock shadow effect)
            f'<ellipse cx="100" cy="160" rx="35" ry="30" fill="{colors["stubble"]}" opacity="0.15"/>',
            
            # Left eyebrow (thicker, more masculine)
            f'<path d="M 65 70 Q 80 60 90 65" stroke="{colors["eyebrows"]}" stroke-width="4" fill="none" stroke-linecap="round"/>',
            
            # Right eyebrow
            f'<path d="M 110 65 Q 120 60 135 70" stroke="{colors["eyebrows"]}" stroke-width="4" fill="none" stroke-linecap="round"/>',
            
            # Eyes container
            self._get_left_eye_svg_male(colors),
            self._get_right_eye_svg_male(colors),
            
            # Mouth with jaw animation
            self._get_mouth_svg_male(colors),
            
            '</svg>'
        ]
        
        return '\n'.join(svg_parts)
    
    def _get_left_eye_svg_male(self, colors: Dict) -> str:
        """Generate left eye SVG with male features"""
        eye_x = 70
        eye_y = 100
        
        eye_svg = f'<g id="left-eye">'
        
        # Eye white (slightly smaller/more angular for male)
        eye_svg += f'<ellipse cx="{eye_x}" cy="{eye_y}" rx="16" ry="20" fill="white" stroke="{colors["secondary"]}" stroke-width="1.5"/>'
        
        # Pupil with look direction
        pupil_offset_x = self.look_direction[0] * self.look_intensity * 8
        pupil_offset_y = self.look_direction[1] * self.look_intensity * 8
        eye_svg += f'<circle cx="{eye_x + pupil_offset_x}" cy="{eye_y + pupil_offset_y}" r="9" fill="{colors["eyes"]}"/>'
        
        # Pupil shine
        eye_svg += f'<circle cx="{eye_x + pupil_offset_x - 3}" cy="{eye_y + pupil_offset_y - 3}" r="3" fill="white" opacity="0.7"/>'
        
        # Eyelids based on state
        if self.left_eye_state == EyeState.CLOSED:
            eye_svg += f'<ellipse cx="{eye_x}" cy="{eye_y}" rx="16" ry="20" fill="{colors["skin"]}"/>'
        elif self.left_eye_state == EyeState.HALF_OPEN:
            eye_svg += f'<path d="M {eye_x-16} {eye_y-8} Q {eye_x} {eye_y-10} {eye_x+16} {eye_y-8}" fill="{colors["skin"]}" opacity="0.6"/>'
        
        eye_svg += '</g>'
        return eye_svg
    
    def _get_right_eye_svg_male(self, colors: Dict) -> str:
        """Generate right eye SVG with male features"""
        eye_x = 130
        eye_y = 100
        
        eye_svg = f'<g id="right-eye">'
        
        # Eye white
        eye_svg += f'<ellipse cx="{eye_x}" cy="{eye_y}" rx="16" ry="20" fill="white" stroke="{colors["secondary"]}" stroke-width="1.5"/>'
        
        # Pupil with look direction
        pupil_offset_x = self.look_direction[0] * self.look_intensity * 8
        pupil_offset_y = self.look_direction[1] * self.look_intensity * 8
        eye_svg += f'<circle cx="{eye_x + pupil_offset_x}" cy="{eye_y + pupil_offset_y}" r="9" fill="{colors["eyes"]}"/>'
        
        # Pupil shine
        eye_svg += f'<circle cx="{eye_x + pupil_offset_x - 3}" cy="{eye_y + pupil_offset_y - 3}" r="3" fill="white" opacity="0.7"/>'
        
        # Eyelids based on state
        if self.right_eye_state == EyeState.CLOSED:
            eye_svg += f'<ellipse cx="{eye_x}" cy="{eye_y}" rx="16" ry="20" fill="{colors["skin"]}"/>'
        elif self.right_eye_state == EyeState.HALF_OPEN:
            eye_svg += f'<path d="M {eye_x-16} {eye_y-8} Q {eye_x} {eye_y-10} {eye_x+16} {eye_y-8}" fill="{colors["skin"]}" opacity="0.6"/>'
        
        eye_svg += '</g>'
        return eye_svg
    
    def _get_mouth_svg_male(self, colors: Dict) -> str:
        """Generate mouth SVG with jaw animation and lip-sync"""
        mouth_svg = '<g id="mouth">'
        
        # Jaw movement for speech
        jaw_offset = self.jaw_open * 8
        
        # Lips
        if self.mouth_state == MouthState.CLOSED:
            mouth_svg += f'<line x1="80" y1="180" x2="120" y2="180" stroke="{colors["secondary"]}" stroke-width="2.5" stroke-linecap="round"/>'
        
        elif self.mouth_state == MouthState.SLIGHT_SMILE:
            mouth_svg += f'<path d="M 80 180 Q 100 185 120 180" stroke="{colors["secondary"]}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
        
        elif self.mouth_state == MouthState.SMILE:
            mouth_svg += f'<path d="M 75 182 Q 100 190 125 182" stroke="{colors["secondary"]}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
        
        elif self.mouth_state == MouthState.WIDE_SMILE:
            mouth_svg += f'<path d="M 70 185 Q 100 198 130 185" stroke="{colors["secondary"]}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
            mouth_svg += f'<path d="M 75 185 Q 100 193 125 185" fill="{colors["accent"]}" opacity="0.2"/>'
        
        # Phoneme shapes for lip-sync
        elif self.mouth_state == MouthState.A_SHAPE:  # Wide open "ah"
            mouth_svg += f'<ellipse cx="100" cy="{180 + jaw_offset}" rx="14" ry="16" fill="{colors["secondary"]}"/>'
            mouth_svg += f'<line x1="100" y1="{180 + jaw_offset}" x2="100" y2="{196 + jaw_offset}" stroke="#333" stroke-width="0.5"/>'
        
        elif self.mouth_state == MouthState.E_SHAPE:  # Spread smile "ee"
            mouth_svg += f'<path d="M 80 {180 + jaw_offset*0.5} Q 100 {182 + jaw_offset} 120 {180 + jaw_offset*0.5}" stroke="{colors["secondary"]}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
        
        elif self.mouth_state == MouthState.I_SHAPE:  # Narrow "ih"
            mouth_svg += f'<ellipse cx="100" cy="{180 + jaw_offset*0.5}" rx="8" ry="10" fill="{colors["secondary"]}"/>'
        
        elif self.mouth_state == MouthState.O_SHAPE:  # Round "oh"
            mouth_svg += f'<ellipse cx="100" cy="{180 + jaw_offset}" rx="12" ry="15" fill="{colors["secondary"]}"/>'
        
        elif self.mouth_state == MouthState.U_SHAPE:  # Rounded pout "oo"
            mouth_svg += f'<ellipse cx="100" cy="{182 + jaw_offset}" rx="10" ry="14" fill="{colors["secondary"]}"/>'
        
        elif self.mouth_state == MouthState.M_SHAPE:  # Closed lips "m"
            mouth_svg += f'<path d="M 80 180 Q 90 {180 + jaw_offset*0.3} 100 180 Q 110 {180 + jaw_offset*0.3} 120 180" stroke="{colors["secondary"]}" stroke-width="3" fill="none" stroke-linecap="round"/>'
        
        elif self.mouth_state == MouthState.THINKING:
            mouth_svg += f'<path d="M 85 182 Q 100 176 115 182" stroke="{colors["secondary"]}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
        
        elif self.mouth_state == MouthState.CONCERNED:
            mouth_svg += f'<path d="M 75 185 Q 100 176 125 185" stroke="{colors["secondary"]}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
        
        elif self.mouth_state == MouthState.NEUTRAL_OPEN:
            mouth_svg += f'<ellipse cx="100" cy="{180 + jaw_offset*0.5}" rx="10" ry="12" fill="{colors["secondary"]}"/>'
        
        mouth_svg += '</g>'
        return mouth_svg
    
    def _darken_color(self, hex_color: str, factor: float) -> str:
        """Darken a hex color"""
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r, g, b = int(r * factor), int(g * factor), int(b * factor)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def get_animation_data(self) -> Dict:
        """Get current animation state as dictionary"""
        return {
            "expression": self.current_expression.value,
            "primary_expression": self.primary_expression.value,
            "secondary_expression": self.secondary_expression.value if self.secondary_expression else None,
            "blend_intensity": self.blend_intensity,
            "left_eye": self.left_eye_state.value,
            "right_eye": self.right_eye_state.value,
            "mouth": self.mouth_state.value,
            "jaw_open": self.jaw_open,
            "is_speaking": self.is_speaking,
            "is_blinking": self.is_blinking,
            "look_direction": self.look_direction,
            "personality_colors": self.personality_colors
        }


class MaleAnimatedFaceWidget:
    """
    Persistent widget displaying the male animated face
    Can be positioned in bottom-right corner or within chat UI
    Syncs with voice output and emotion changes
    """
    
    def __init__(self, face: MaleAnimatedFace, width: int = 150):
        self.face = face
        self.width = width
        self.is_visible = True
        self.position = "bottom-right"  # Can be "bottom-right", "bottom-left", "chat-header"
        self.opacity = 1.0
        self.scale = 1.0
    
    def render(self) -> Dict:
        """Return render data for the face widget"""
        return {
            "type": "male_face_widget",
            "position": self.position,
            "width": self.width,
            "height": int(self.width * 1.4),
            "opacity": self.opacity,
            "scale": self.scale,
            "is_visible": self.is_visible,
            "svg": self.face.get_svg_male_face(self.width),
            "animation_data": self.face.get_animation_data()
        }
    
    def show(self):
        """Show the face widget"""
        self.is_visible = True
    
    def hide(self):
        """Hide the face widget"""
        self.is_visible = False
    
    def set_position(self, position: str):
        """Set widget position"""
        if position in ["bottom-right", "bottom-left", "chat-header"]:
            self.position = position
    
    def set_opacity(self, opacity: float):
        """Set widget opacity (0.0 to 1.0)"""
        self.opacity = min(1.0, max(0.0, opacity))
    
    def animate_focus(self):
        """Animate face to draw attention (bounce effect)"""
        return {"animation": "bounce", "duration": 500}
