"""
Animated Character Face System
Creates an expressive animated face inspired by Caine from The Amazing Digital Circus
Displays in chat UI and persistent corner widget with voice synchronization
"""

from typing import Dict, Tuple, Optional
from enum import Enum
from datetime import datetime, timedelta
import math


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
    """Mouth animation states"""
    CLOSED = "closed"
    SLIGHT_SMILE = "slight_smile"
    SMILE = "smile"
    WIDE_SMILE = "wide_smile"
    O_SHAPE = "o_shape"
    THINKING = "thinking"
    CONCERNED = "concerned"
    NEUTRAL_OPEN = "neutral_open"


class AnimatedFace:
    """
    Generates animated face data for rendering
    Inspired by Caine's expressive digital design
    """
    
    # Base face dimensions (SVG-like coordinates)
    FACE_WIDTH = 200
    FACE_HEIGHT = 240
    
    def __init__(self, personality_name: str = "The Optimist"):
        self.personality_name = personality_name
        self.current_expression = FacialExpression.NEUTRAL
        self.left_eye_state = EyeState.OPEN
        self.right_eye_state = EyeState.OPEN
        self.mouth_state = MouthState.CLOSED
        
        # Animation state
        self.blink_timer = 0
        self.blink_interval = 4000  # ms between blinks
        self.is_blinking = False
        
        # Speaking state
        self.is_speaking = False
        self.speech_timer = 0
        
        # Look direction (for interaction)
        self.look_direction = (0, 0)  # x, y offset
        self.look_intensity = 0.5
        
        # Personality-specific colors
        self.personality_colors = self._get_personality_colors()
        
        # Animation state
        self.last_update = datetime.now()
        self.animation_queue = []
    
    def _get_personality_colors(self) -> Dict:
        """Get personality-specific color scheme"""
        colors = {
            "The Philosopher": {
                "primary": "#8B5A3C",  # Brown
                "secondary": "#D4A574",  # Tan
                "accent": "#A0522D",  # Sienna
                "eyes": "#2C1810",  # Dark brown
                "glow": "#FFD700"  # Gold glow
            },
            "The Optimist": {
                "primary": "#FFD700",  # Gold
                "secondary": "#FFA500",  # Orange
                "accent": "#FF69B4",  # Hot pink
                "eyes": "#000000",  # Black
                "glow": "#FFEB3B"  # Bright yellow glow
            },
            "The Mystique": {
                "primary": "#4B0082",  # Indigo
                "secondary": "#9370DB",  # Medium purple
                "accent": "#1A1A2E",  # Dark blue
                "eyes": "#00FF00",  # Neon green
                "glow": "#FF00FF"  # Magenta glow
            },
            "The Companion": {
                "primary": "#FF6B9D",  # Pink
                "secondary": "#C44569",  # Warm red
                "accent": "#FF9A9E",  # Light pink
                "eyes": "#FFFFFF",  # White
                "glow": "#FF1493"  # Deep pink glow
            },
            "The Analyst": {
                "primary": "#1E90FF",  # Dodger blue
                "secondary": "#00CED1",  # Dark turquoise
                "accent": "#0F4C75",  # Dark blue
                "eyes": "#00FF00",  # Lime
                "glow": "#00FFFF"  # Cyan glow
            }
        }
        
        return colors.get(self.personality_name, colors["The Optimist"])
    
    def update_expression(self, emotion: str, intensity: float = 0.5):
        """Update facial expression based on emotion"""
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
        
        self.current_expression = emotion_to_expression.get(
            emotion, FacialExpression.NEUTRAL
        )
        self._update_facial_features(self.current_expression, intensity)
    
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
        
        elif expression == FacialExpression.SPEAKING:
            self.left_eye_state = EyeState.OPEN
            self.right_eye_state = EyeState.OPEN
            self.mouth_state = MouthState.O_SHAPE
    
    def start_speaking(self):
        """Start speaking animation"""
        self.is_speaking = True
        self.speech_timer = 0
        self.current_expression = FacialExpression.SPEAKING
        self._update_facial_features(FacialExpression.SPEAKING, 1.0)
    
    def stop_speaking(self):
        """Stop speaking animation"""
        self.is_speaking = False
        self.speech_timer = 0
    
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
    
    def get_svg_face(self, size: int = 200) -> str:
        """
        Generate SVG representation of the animated face
        Returns SVG string for rendering
        """
        scale = size / self.FACE_WIDTH
        colors = self.personality_colors
        
        # Build SVG
        svg_parts = [
            f'<svg width="{size}" height="{int(self.FACE_HEIGHT * scale)}" viewBox="0 0 {self.FACE_WIDTH} {self.FACE_HEIGHT}" xmlns="http://www.w3.org/2000/svg">',
            
            # Background glow effect
            f'<defs>',
            f'  <radialGradient id="glow" cx="50%" cy="50%" r="50%">',
            f'    <stop offset="0%" style="stop-color:{colors["glow"]};stop-opacity:0.3" />',
            f'    <stop offset="100%" style="stop-color:{colors["glow"]};stop-opacity:0" />',
            f'  </radialGradient>',
            f'  <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">',
            f'    <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.3"/>',
            f'  </filter>',
            f'</defs>',
            
            # Glow circle
            f'<circle cx="100" cy="120" r="110" fill="url(#glow)" filter="url(#shadow)"/>',
            
            # Face shape
            f'<ellipse cx="100" cy="120" rx="85" ry="100" fill="{colors["primary"]}" stroke="{colors["secondary"]}" stroke-width="2"/>',
            
            # Eyes container
            self._get_left_eye_svg(colors),
            self._get_right_eye_svg(colors),
            
            # Mouth
            self._get_mouth_svg(colors),
            
            '</svg>'
        ]
        
        return '\n'.join(svg_parts)
    
    def _get_left_eye_svg(self, colors: Dict) -> str:
        """Generate left eye SVG"""
        eye_x = 70
        eye_y = 100
        
        eye_svg = f'<g id="left-eye">'
        
        # Eye white
        eye_svg += f'<ellipse cx="{eye_x}" cy="{eye_y}" rx="18" ry="22" fill="white" stroke="{colors["secondary"]}" stroke-width="1"/>'
        
        # Pupil with look direction
        pupil_offset_x = self.look_direction[0] * self.look_intensity * 8
        pupil_offset_y = self.look_direction[1] * self.look_intensity * 8
        eye_svg += f'<circle cx="{eye_x + pupil_offset_x}" cy="{eye_y + pupil_offset_y}" r="10" fill="{colors["eyes"]}"/>'
        
        # Pupil shine
        eye_svg += f'<circle cx="{eye_x + pupil_offset_x - 3}" cy="{eye_y + pupil_offset_y - 3}" r="3" fill="white" opacity="0.6"/>'
        
        # Eyelids based on state
        if self.left_eye_state == EyeState.CLOSED:
            eye_svg += f'<ellipse cx="{eye_x}" cy="{eye_y}" rx="18" ry="22" fill="{colors["primary"]}"/>'
        elif self.left_eye_state == EyeState.HALF_OPEN:
            eye_svg += f'<path d="M {eye_x-18} {eye_y-10} Q {eye_x} {eye_y-12} {eye_x+18} {eye_y-10}" fill="{colors["primary"]}" opacity="0.5"/>'
        
        eye_svg += '</g>'
        return eye_svg
    
    def _get_right_eye_svg(self, colors: Dict) -> str:
        """Generate right eye SVG"""
        eye_x = 130
        eye_y = 100
        
        eye_svg = f'<g id="right-eye">'
        
        # Eye white
        eye_svg += f'<ellipse cx="{eye_x}" cy="{eye_y}" rx="18" ry="22" fill="white" stroke="{colors["secondary"]}" stroke-width="1"/>'
        
        # Pupil with look direction
        pupil_offset_x = self.look_direction[0] * self.look_intensity * 8
        pupil_offset_y = self.look_direction[1] * self.look_intensity * 8
        eye_svg += f'<circle cx="{eye_x + pupil_offset_x}" cy="{eye_y + pupil_offset_y}" r="10" fill="{colors["eyes"]}"/>'
        
        # Pupil shine
        eye_svg += f'<circle cx="{eye_x + pupil_offset_x - 3}" cy="{eye_y + pupil_offset_y - 3}" r="3" fill="white" opacity="0.6"/>'
        
        # Eyelids based on state
        if self.right_eye_state == EyeState.CLOSED:
            eye_svg += f'<ellipse cx="{eye_x}" cy="{eye_y}" rx="18" ry="22" fill="{colors["primary"]}"/>'
        elif self.right_eye_state == EyeState.HALF_OPEN:
            eye_svg += f'<path d="M {eye_x-18} {eye_y-10} Q {eye_x} {eye_y-12} {eye_x+18} {eye_y-10}" fill="{colors["primary"]}" opacity="0.5"/>'
        
        eye_svg += '</g>'
        return eye_svg
    
    def _get_mouth_svg(self, colors: Dict) -> str:
        """Generate mouth SVG based on mouth state"""
        mouth_svg = '<g id="mouth">'
        
        if self.mouth_state == MouthState.CLOSED:
            mouth_svg += f'<line x1="85" y1="170" x2="115" y2="170" stroke="{colors["secondary"]}" stroke-width="2" stroke-linecap="round"/>'
        
        elif self.mouth_state == MouthState.SLIGHT_SMILE:
            mouth_svg += f'<path d="M 85 170 Q 100 175 115 170" stroke="{colors["secondary"]}" stroke-width="2" fill="none" stroke-linecap="round"/>'
        
        elif self.mouth_state == MouthState.SMILE:
            mouth_svg += f'<path d="M 80 172 Q 100 182 120 172" stroke="{colors["secondary"]}" stroke-width="2" fill="none" stroke-linecap="round"/>'
        
        elif self.mouth_state == MouthState.WIDE_SMILE:
            mouth_svg += f'<path d="M 75 175 Q 100 188 125 175" stroke="{colors["secondary"]}" stroke-width="2" fill="none" stroke-linecap="round"/>'
            mouth_svg += f'<path d="M 80 175 Q 100 185 120 175" fill="{colors["accent"]}" opacity="0.3"/>'
        
        elif self.mouth_state == MouthState.O_SHAPE:
            mouth_svg += f'<ellipse cx="100" cy="173" rx="10" ry="13" fill="{colors["secondary"]}"/>'
        
        elif self.mouth_state == MouthState.THINKING:
            mouth_svg += f'<path d="M 85 170 Q 100 168 115 170" stroke="{colors["secondary"]}" stroke-width="2" fill="none" stroke-linecap="round"/>'
        
        elif self.mouth_state == MouthState.CONCERNED:
            mouth_svg += f'<path d="M 80 175 Q 100 168 120 175" stroke="{colors["secondary"]}" stroke-width="2" fill="none" stroke-linecap="round"/>'
        
        elif self.mouth_state == MouthState.NEUTRAL_OPEN:
            mouth_svg += f'<ellipse cx="100" cy="174" rx="8" ry="10" fill="{colors["secondary"]}"/>'
        
        mouth_svg += '</g>'
        return mouth_svg
    
    def get_animation_data(self) -> Dict:
        """Get current animation state as dictionary"""
        return {
            "expression": self.current_expression.value,
            "left_eye": self.left_eye_state.value,
            "right_eye": self.right_eye_state.value,
            "mouth": self.mouth_state.value,
            "is_speaking": self.is_speaking,
            "is_blinking": self.is_blinking,
            "look_direction": self.look_direction,
            "personality_colors": self.personality_colors
        }


class FaceWidget:
    """
    Persistent widget that displays the animated face
    Can be placed in bottom-right corner or within chat UI
    """
    
    def __init__(self, face: AnimatedFace, width: int = 150):
        self.face = face
        self.width = width
        self.is_visible = True
        self.position = "bottom-right"  # Can be "bottom-right", "bottom-left", "chat-header"
        self.opacity = 1.0
        self.scale = 1.0
    
    def render(self) -> Dict:
        """Return render data for the face widget"""
        return {
            "type": "face_widget",
            "position": self.position,
            "width": self.width,
            "height": int(self.width * 1.2),
            "opacity": self.opacity,
            "scale": self.scale,
            "is_visible": self.is_visible,
            "svg": self.face.get_svg_face(self.width),
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
        # This would trigger a bounce animation on the frontend
        return {"animation": "bounce", "duration": 500}
