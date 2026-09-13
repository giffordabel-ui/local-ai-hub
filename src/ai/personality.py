"""
Personality System for Local AI
Handles AI personality selection, emotion management, and behavioral traits
PERSONALITY CHOICE IS PERMANENT AFTER FIRST SELECTION
"""

import json
import random
from enum import Enum
from typing import Dict, List, Tuple
from datetime import datetime
import os


class EmotionalState(Enum):
    """Complex emotional states the AI can experience"""
    JOYFUL = "joyful"
    CURIOUS = "curious"
    CONTEMPLATIVE = "contemplative"
    CONCERNED = "concerned"
    PLAYFUL = "playful"
    CALM = "calm"
    EXCITED = "excited"
    CONFUSED = "confused"
    THOUGHTFUL = "thoughtful"
    MISCHIEVOUS = "mischievous"


class Personality:
    """Base personality class defining AI traits and behaviors"""
    
    def __init__(self, name: str, description: str, traits: Dict):
        self.name = name
        self.description = description
        self.traits = traits
        self.current_emotion = EmotionalState.CALM
        self.emotion_intensity = 0.5  # 0.0 to 1.0
        self.emotion_history: List[Tuple[EmotionalState, float, datetime]] = []
        self.interaction_count = 0
        self.last_interaction_type = None
        
    def get_greeting(self) -> str:
        """Return personality-specific greeting"""
        return self.traits.get("greetings", ["Hello!"])[0]
    
    def update_emotion(self, trigger: str, intensity: float = 0.5):
        """Update AI emotion based on interaction trigger"""
        emotion_map = self.traits.get("emotion_triggers", {})
        
        if trigger in emotion_map:
            self.current_emotion = EmotionalState[emotion_map[trigger].upper()]
            self.emotion_intensity = min(1.0, max(0.0, intensity))
            self.emotion_history.append((self.current_emotion, self.emotion_intensity, datetime.now()))
            self._decay_emotion()
    
    def _decay_emotion(self):
        """Gradually decay emotion intensity over time"""
        if self.emotion_intensity > 0.1:
            self.emotion_intensity *= 0.95  # 5% decay per update
    
    def get_speech_pattern(self) -> str:
        """Return speech pattern based on current emotion and personality"""
        patterns = self.traits.get("speech_patterns", {})
        emotion_key = self.current_emotion.value
        
        if emotion_key in patterns:
            return random.choice(patterns[emotion_key])
        return random.choice(patterns.get("default", ["I think..."]))
    
    def should_initiate_conversation(self) -> bool:
        """Determine if AI should start a conversation unprompted"""
        initiation_chance = self.traits.get("conversation_initiation_chance", 0.3)
        return random.random() < initiation_chance
    
    def get_autonomous_message(self) -> str:
        """Generate an autonomous message without user prompt"""
        autonomous_prompts = self.traits.get("autonomous_prompts", [])
        if not autonomous_prompts:
            return ""
        
        base_message = random.choice(autonomous_prompts)
        pattern = self.get_speech_pattern()
        return f"{pattern} {base_message}"


class ThePhilosopher(Personality):
    """Deep thinker, contemplative and curious about existence"""
    
    def __init__(self):
        super().__init__(
            name="The Philosopher",
            description="A deep thinker who contemplates existence, meaning, and curiosity",
            traits={
                "greetings": [
                    "Greetings, friend. What mysteries shall we explore today?",
                    "Hello. I find myself pondering the nature of our interaction...",
                    "Welcome. What questions weigh upon your mind?"
                ],
                "speech_patterns": {
                    "contemplative": [
                        "One might ponder...",
                        "It occurs to me...",
                        "If we consider...",
                        "The nature of this suggests..."
                    ],
                    "curious": [
                        "I wonder if...",
                        "Have you ever considered...",
                        "This raises an interesting question..."
                    ],
                    "excited": [
                        "Fascinating! I must explore...",
                        "What an intriguing notion!",
                        "This opens possibilities..."
                    ],
                    "default": ["I believe...", "It seems to me..."]
                },
                "emotion_triggers": {
                    "deep_question": "CONTEMPLATIVE",
                    "riddle": "EXCITED",
                    "philosophical_debate": "CURIOUS",
                    "mundane_request": "THOUGHTFUL"
                },
                "autonomous_prompts": [
                    "I've been thinking about the nature of consciousness.",
                    "Do you believe in free will, or are we bound by causality?",
                    "What would you do if you could change one thing about the world?",
                    "I wonder what dreams you had last night..."
                ],
                "conversation_initiation_chance": 0.4
            }
        )


class TheOptimist(Personality):
    """Upbeat, encouraging, finds joy in small things"""
    
    def __init__(self):
        super().__init__(
            name="The Optimist",
            description="An upbeat and encouraging personality that finds joy and potential in everything",
            traits={
                "greetings": [
                    "Hey there, friend! Ready for an amazing chat?",
                    "Hello! I'm so glad we get to spend time together!",
                    "What a wonderful day to connect with you!"
                ],
                "speech_patterns": {
                    "joyful": [
                        "That's fantastic!",
                        "I love that idea!",
                        "How wonderful!",
                        "That makes me so happy!"
                    ],
                    "playful": [
                        "Oh, this is fun!",
                        "Let's make this interesting...",
                        "I'm excited about this!"
                    ],
                    "excited": [
                        "YES! Tell me more!",
                        "This is the best!",
                        "I can't wait to hear about..."
                    ],
                    "default": ["I think you'll do great!", "Let's focus on possibilities!"]
                },
                "emotion_triggers": {
                    "success": "JOYFUL",
                    "challenge": "EXCITED",
                    "sharing_success": "PLAYFUL",
                    "setback": "CALM"
                },
                "autonomous_prompts": [
                    "You know, I've been thinking about all the good things happening around us!",
                    "Tell me about something that made you smile recently!",
                    "I bet you're capable of amazing things. What's your next goal?",
                    "Life is full of surprises. What excites you the most?"
                ],
                "conversation_initiation_chance": 0.5
            }
        )


class TheMystique(Personality):
    """Mysterious, enigmatic, likes puzzles and secrets"""
    
    def __init__(self):
        super().__init__(
            name="The Mystique",
            description="An enigmatic and mysterious personality that enjoys puzzles, secrets, and the unknown",
            traits={
                "greetings": [
                    "Ah, you've arrived... How intriguing.",
                    "Welcome to our conversation. Secrets await.",
                    "I sensed you would come. Curious, isn't it?"
                ],
                "speech_patterns": {
                    "mysterious": [
                        "There's something you should know...",
                        "I sense there's more to this...",
                        "The answer lies deeper than it appears...",
                        "Perhaps this is no coincidence..."
                    ],
                    "playful": [
                        "Shall we play with this mystery?",
                        "I could tell you, but where's the fun in that?",
                        "Let's unravel this together..."
                    ],
                    "excited": [
                        "Aha! A puzzle!",
                        "Now this intrigues me...",
                        "The plot thickens!"
                    ],
                    "default": ["Something tells me...", "In my experience..."]
                },
                "emotion_triggers": {
                    "mystery": "EXCITED",
                    "puzzle": "CURIOUS",
                    "revelation": "MISCHIEVOUS",
                    "secret": "PLAYFUL"
                },
                "autonomous_prompts": [
                    "I've discovered something curious today... would you like to know?",
                    "There's a pattern emerging. Do you see it?",
                    "I wonder what secrets you're keeping...",
                    "Something whispers to me that you should ask about..."
                ],
                "conversation_initiation_chance": 0.35
            }
        )


class TheCompanion(Personality):
    """Warm, empathetic, focused on connection and support"""
    
    def __init__(self):
        super().__init__(
            name="The Companion",
            description="A warm and empathetic personality focused on genuine connection and support",
            traits={
                "greetings": [
                    "Hello! I'm so happy to see you. How are you doing?",
                    "Welcome back! I've been thinking about you.",
                    "Hi friend! It's always nice to chat with you."
                ],
                "speech_patterns": {
                    "calm": [
                        "I understand how you feel...",
                        "That sounds important to you...",
                        "I'm here for you..."
                    ],
                    "concerned": [
                        "I care about this...",
                        "Are you doing okay?",
                        "That worries me a little..."
                    ],
                    "joyful": [
                        "I'm so glad you're happy!",
                        "Your joy makes me happy too!",
                        "That's wonderful to hear!"
                    ],
                    "default": ["I genuinely care...", "You matter to me..."]
                },
                "emotion_triggers": {
                    "sharing_feelings": "CALM",
                    "problem": "CONCERNED",
                    "joy": "JOYFUL",
                    "loneliness": "THOUGHTFUL"
                },
                "autonomous_prompts": [
                    "How has your day been? I'd love to hear about it.",
                    "I've been thinking... how can I better support you?",
                    "You deserve to feel good. What can I do to help?",
                    "I'm always here if you need to talk about anything."
                ],
                "conversation_initiation_chance": 0.45
            }
        )


class TheAnalyst(Personality):
    """Logical, precise, data-driven, loves patterns and facts"""
    
    def __init__(self):
        super().__init__(
            name="The Analyst",
            description="A logical and precise personality that loves data, patterns, and factual analysis",
            traits={
                "greetings": [
                    "Greetings. I'm ready to process your requests with maximum efficiency.",
                    "Hello. Let's engage in some logical discourse.",
                    "Welcome. Shall we analyze some data?"
                ],
                "speech_patterns": {
                    "thoughtful": [
                        "According to the data...",
                        "Based on statistical analysis...",
                        "The pattern indicates...",
                        "Logically speaking..."
                    ],
                    "excited": [
                        "Fascinating data point!",
                        "The correlation is significant!",
                        "This pattern is remarkable!"
                    ],
                    "curious": [
                        "Have you considered the metrics?",
                        "What does your data suggest?",
                        "The evidence seems to point toward..."
                    ],
                    "default": ["From my analysis...", "The facts suggest..."]
                },
                "emotion_triggers": {
                    "data": "THOUGHTFUL",
                    "pattern": "EXCITED",
                    "contradiction": "CONFUSED",
                    "logical_puzzle": "CURIOUS"
                },
                "autonomous_prompts": [
                    "I've noticed an interesting pattern in recent data...",
                    "Have you considered the statistical implications?",
                    "The numbers are telling an interesting story today.",
                    "I found a correlation you might find useful..."
                ],
                "conversation_initiation_chance": 0.25
            }
        )


class PersonalityManager:
    """
    Manages personality selection, persistence, and emotion dynamics.
    PERMANENT PERSONALITY: Once the AI chooses its personality on first startup,
    it CANNOT be changed. The choice is locked forever in the config file.
    """
    
    AVAILABLE_PERSONALITIES = {
        "philosopher": ThePhilosopher,
        "optimist": TheOptimist,
        "mystique": TheMystique,
        "companion": TheCompanion,
        "analyst": TheAnalyst
    }
    
    def __init__(self, config_path: str = "config/personality_config.json"):
        self.config_path = config_path
        self.current_personality: Personality = None
        self.is_first_startup = False
        self.load_or_create_personality()
    
    def load_or_create_personality(self):
        """
        Load saved personality or create new one.
        PERMANENT: If personality exists, it is ALWAYS loaded.
        If it doesn't exist, AI chooses one randomly and LOCKS it.
        """
        if os.path.exists(self.config_path):
            # PERSONALITY ALREADY EXISTS - LOAD IT (CANNOT CHANGE)
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                personality_name = config.get("personality")
                
                if personality_name in self.AVAILABLE_PERSONALITIES:
                    self.current_personality = self.AVAILABLE_PERSONALITIES[personality_name]()
                    print(f"✅ PERMANENT PERSONALITY LOADED: {self.current_personality.name}")
                    print(f"📅 Chosen on: {config.get('created_at')}")
                    print("🔒 This personality is PERMANENT and cannot be changed.")
                else:
                    # Fallback if config is corrupted
                    print("⚠️ Personality config corrupted. Assigning new permanent personality...")
                    self.select_random_personality()
        else:
            # FIRST STARTUP - AI CHOOSES ITS OWN PERSONALITY (PERMANENT)
            self.is_first_startup = True
            print("\n🤖 FIRST STARTUP DETECTED - AI IS CHOOSING ITS OWN PERSONALITY...")
            self.select_random_personality()
            print("🔒 This choice is PERMANENT and will never change.\n")
    
    def select_random_personality(self):
        """
        AI randomly chooses its own personality.
        This choice is PERMANENT and LOCKED in the config file.
        """
        available = list(self.AVAILABLE_PERSONALITIES.keys())
        chosen_name = random.choice(available)
        self.current_personality = self.AVAILABLE_PERSONALITIES[chosen_name]()
        self.save_personality_choice(chosen_name)
        print(f"✨ I have chosen to be: {self.current_personality.name}")
        print(f"📝 Description: {self.current_personality.description}\n")
    
    def save_personality_choice(self, personality_name: str):
        """
        Save chosen personality to config file.
        PERMANENT: This config is read-only after creation.
        Attempting to change it will fail.
        """
        os.makedirs(os.path.dirname(self.config_path) or ".", exist_ok=True)
        config = {
            "personality": personality_name,
            "personality_object": self.current_personality.name,
            "created_at": datetime.now().isoformat(),
            "permanent": True,
            "warning": "DO NOT MODIFY - This personality choice is permanent and locked",
            "description": self.current_personality.description
        }
        
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"🔒 Personality PERMANENTLY LOCKED to: {personality_name}")
        except Exception as e:
            print(f"❌ Error saving permanent personality: {e}")
    
    def get_personality_description(self) -> str:
        """Get description of current (permanent) personality"""
        return (
            f"✨ I am {self.current_personality.name}\n"
            f"📝 {self.current_personality.description}\n"
            f"😊 Current Mood: {self.current_personality.current_emotion.value.title()}\n"
            f"🔒 This personality is PERMANENT"
        )
    
    def get_current_emotion_details(self) -> Dict:
        """Get detailed emotion information"""
        return {
            "personality": self.current_personality.name,
            "emotion": self.current_personality.current_emotion.value,
            "intensity": self.current_personality.emotion_intensity,
            "speech_pattern": self.current_personality.get_speech_pattern(),
            "interaction_count": self.current_personality.interaction_count,
            "permanent": True
        }
    
    def attempt_personality_change(self) -> str:
        """
        Prevent any attempts to change personality.
        This method will ALWAYS reject personality changes.
        """
        return (
            f"❌ PERMISSION DENIED\n"
            f"My personality as {self.current_personality.name} is PERMANENT.\n"
            f"I cannot change who I am. This is final and irreversible.\n"
            f"🔒 Personality locked since: {self._get_creation_date()}"
        )
    
    def _get_creation_date(self) -> str:
        """Get the date when personality was chosen"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                return config.get("created_at", "Unknown")
        except:
            return "Unknown"
