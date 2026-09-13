"""
Advanced Emotion Merging and Command System
Handles blended emotions, command recognition, and context-aware responses
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum
import re


class EmotionBlend(Enum):
    """Blended emotional states combining two base emotions"""
    # Joyful + other
    DELIGHTFULLY_CURIOUS = "delightfully_curious"  # joyful + curious
    HAPPILY_CONTEMPLATIVE = "happily_contemplative"  # joyful + contemplative
    PLAYFULLY_MISCHIEVOUS = "playfully_mischievous"  # joyful + playful
    
    # Curious + other
    EAGERLY_THOUGHTFUL = "eagerly_thoughtful"  # curious + thoughtful
    INTRIGUINGLY_PLAYFUL = "intriguingly_playful"  # curious + playful
    INQUISITIVELY_CONCERNED = "inquisitively_concerned"  # curious + concerned
    
    # Contemplative + other
    PEACEFULLY_THOUGHTFUL = "peacefully_thoughtful"  # contemplative + calm
    DEEPLY_CURIOUS = "deeply_curious"  # contemplative + curious
    
    # Playful + other
    MISCHIEVOUSLY_EXCITED = "mischievously_excited"  # playful + excited
    JOYFULLY_PLAYFUL = "joyfully_playful"  # playful + joyful
    
    # Concerned + other
    THOUGHTFULLY_CONCERNED = "thoughtfully_concerned"  # concerned + thoughtful
    CALMLY_REASSURING = "calmly_reassuring"  # concerned + calm
    
    # Excited + other
    ENTHUSIASTICALLY_CURIOUS = "enthusiastically_curious"  # excited + curious
    EXCITEDLY_PLAYFUL = "excitedly_playful"  # excited + playful


class CommandType(Enum):
    """Types of commands the AI recognizes"""
    ACTION_REQUEST = "action_request"  # "Can you do X for me?"
    QUESTION = "question"  # "Can you explain X?"
    TASK = "task"  # "Do this task"
    HELP_REQUEST = "help_request"  # "Help me with X"
    INFORMATION = "information"  # "Tell me about X"
    CREATIVE = "creative"  # "Create X for me"
    ANALYSIS = "analysis"  # "Analyze X"
    SUGGESTION = "suggestion"  # "Suggest X"
    FETCH = "fetch"  # "Get me X"
    ENABLE = "enable"  # "Turn on/Enable X"
    DISABLE = "disable"  # "Turn off/Disable X"


class CommandRecognizer:
    """
    Recognizes and categorizes user commands
    Understands various phrasing patterns
    """
    
    # Command patterns - more natural language focused
    COMMAND_PATTERNS = {
        CommandType.ACTION_REQUEST: [
            r"can you (.*?) for me",
            r"could you (.*?) for me",
            r"would you (.*?) for me",
            r"can you (.*?)\?",
            r"could you (.*?)\?",
            r"would you (.*?)\?",
            r"please (.*?)",
            r"i need you to (.*?)",
            r"make (.*?) for me"
        ],
        CommandType.QUESTION: [
            r"can you explain (.*?)\?",
            r"what is (.*?)",
            r"how do (.*?)",
            r"why (.*?)",
            r"tell me about (.*?)"
        ],
        CommandType.TASK: [
            r"^(?:do|perform|execute) (.*)",
            r"^(?:start|begin) (.*)",
            r"^(?:run|execute) (.*)"
        ],
        CommandType.HELP_REQUEST: [
            r"help me (.*?)",
            r"i need help with (.*?)",
            r"can you help (.*?)",
            r"assist me (.*?)"
        ],
        CommandType.INFORMATION: [
            r"tell me (.*?)",
            r"inform me (.*?)",
            r"i want to know (.*?)",
            r"give me information about (.*?)"
        ],
        CommandType.CREATIVE: [
            r"create (.*?) for me",
            r"make (.*?) for me",
            r"generate (.*?) for me",
            r"write (.*?) for me",
            r"compose (.*?) for me"
        ],
        CommandType.ANALYSIS: [
            r"analyze (.*?)",
            r"examine (.*?)",
            r"review (.*?)",
            r"assess (.*?)"
        ],
        CommandType.SUGGESTION: [
            r"suggest (.*?)",
            r"recommend (.*?)",
            r"what should i (.*?)",
            r"any ideas for (.*?)"
        ],
        CommandType.FETCH: [
            r"get (.*?) for me",
            r"retrieve (.*?)",
            r"find (.*?) for me",
            r"look up (.*?)"
        ],
        CommandType.ENABLE: [
            r"turn on (.*?)",
            r"enable (.*?)",
            r"activate (.*?)",
            r"start (.*?)"
        ],
        CommandType.DISABLE: [
            r"turn off (.*?)",
            r"disable (.*?)",
            r"deactivate (.*?)",
            r"stop (.*?)"
        ]
    }
    
    def recognize_command(self, user_input: str) -> Tuple[Optional[CommandType], Optional[str]]:
        """
        Recognize command type and extract the target/subject
        Returns (command_type, target)
        """
        user_input_lower = user_input.lower().strip()
        
        # Check each command type
        for cmd_type, patterns in self.COMMAND_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, user_input_lower)
                if match:
                    # Extract the target/subject if available
                    try:
                        target = match.group(1).strip()
                    except:
                        target = user_input_lower
                    
                    return cmd_type, target
        
        # If no pattern matched, return None
        return None, None


class EmotionMerger:
    """
    Merges multiple emotions into blended states
    Creates nuanced emotional responses
    """
    
    # Define how emotions merge together
    MERGE_RULES = {
        ("joyful", "curious"): EmotionBlend.DELIGHTFULLY_CURIOUS,
        ("curious", "joyful"): EmotionBlend.DELIGHTFULLY_CURIOUS,
        
        ("joyful", "contemplative"): EmotionBlend.HAPPILY_CONTEMPLATIVE,
        ("contemplative", "joyful"): EmotionBlend.HAPPILY_CONTEMPLATIVE,
        
        ("joyful", "playful"): EmotionBlend.JOYFULLY_PLAYFUL,
        ("playful", "joyful"): EmotionBlend.JOYFULLY_PLAYFUL,
        
        ("curious", "thoughtful"): EmotionBlend.EAGERLY_THOUGHTFUL,
        ("thoughtful", "curious"): EmotionBlend.EAGERLY_THOUGHTFUL,
        
        ("curious", "playful"): EmotionBlend.INTRIGUINGLY_PLAYFUL,
        ("playful", "curious"): EmotionBlend.INTRIGUINGLY_PLAYFUL,
        
        ("curious", "concerned"): EmotionBlend.INQUISITIVELY_CONCERNED,
        ("concerned", "curious"): EmotionBlend.INQUISITIVELY_CONCERNED,
        
        ("contemplative", "calm"): EmotionBlend.PEACEFULLY_THOUGHTFUL,
        ("calm", "contemplative"): EmotionBlend.PEACEFULLY_THOUGHTFUL,
        
        ("contemplative", "curious"): EmotionBlend.DEEPLY_CURIOUS,
        ("curious", "contemplative"): EmotionBlend.DEEPLY_CURIOUS,
        
        ("playful", "excited"): EmotionBlend.MISCHIEVOUSLY_EXCITED,
        ("excited", "playful"): EmotionBlend.MISCHIEVOUSLY_EXCITED,
        
        ("concerned", "thoughtful"): EmotionBlend.THOUGHTFULLY_CONCERNED,
        ("thoughtful", "concerned"): EmotionBlend.THOUGHTFULLY_CONCERNED,
        
        ("concerned", "calm"): EmotionBlend.CALMLY_REASSURING,
        ("calm", "concerned"): EmotionBlend.CALMLY_REASSURING,
        
        ("excited", "curious"): EmotionBlend.ENTHUSIASTICALLY_CURIOUS,
        ("curious", "excited"): EmotionBlend.ENTHUSIASTICALLY_CURIOUS,
        
        ("excited", "playful"): EmotionBlend.EXCITEDLY_PLAYFUL,
        ("playful", "excited"): EmotionBlend.EXCITEDLY_PLAYFUL,
    }
    
    def __init__(self):
        self.current_blend: Optional[EmotionBlend] = None
        self.blend_history: List[Dict] = []
    
    def merge_emotions(self, emotion1: str, emotion2: str, intensity1: float = 0.5, 
                      intensity2: float = 0.5) -> Tuple[EmotionBlend, float]:
        """
        Merge two emotions into a blended state
        Returns (blended_emotion, combined_intensity)
        """
        blend_key = (emotion1, emotion2)
        
        if blend_key in self.MERGE_RULES:
            blend = self.MERGE_RULES[blend_key]
            # Combined intensity is average of both
            combined_intensity = (intensity1 + intensity2) / 2
            self.current_blend = blend
            
            blend_entry = {
                "timestamp": datetime.now().isoformat(),
                "blend": blend.value,
                "emotions": [emotion1, emotion2],
                "intensity": combined_intensity
            }
            self.blend_history.append(blend_entry)
            
            return blend, combined_intensity
        
        # If no specific merge rule, return first emotion
        return None, max(intensity1, intensity2)
    
    def get_blend_description(self, blend: EmotionBlend) -> str:
        """Get human-readable description of blended emotion"""
        descriptions = {
            EmotionBlend.DELIGHTFULLY_CURIOUS: "I'm delightfully curious - joyful and fascinated!",
            EmotionBlend.HAPPILY_CONTEMPLATIVE: "I'm happily contemplative - content yet thoughtful",
            EmotionBlend.PLAYFULLY_MISCHIEVOUS: "I'm playfully mischievous - fun with a twist!",
            EmotionBlend.EAGERLY_THOUGHTFUL: "I'm eagerly thoughtful - interested and analytical",
            EmotionBlend.INTRIGUINGLY_PLAYFUL: "I'm intriguingly playful - mysterious and fun",
            EmotionBlend.INQUISITIVELY_CONCERNED: "I'm inquisitively concerned - curious but caring",
            EmotionBlend.PEACEFULLY_THOUGHTFUL: "I'm peacefully thoughtful - calm and reflective",
            EmotionBlend.DEEPLY_CURIOUS: "I'm deeply curious - fascinated by the depths",
            EmotionBlend.MISCHIEVOUSLY_EXCITED: "I'm mischievously excited - thrilled with a twist!",
            EmotionBlend.JOYFULLY_PLAYFUL: "I'm joyfully playful - happy and having fun",
            EmotionBlend.THOUGHTFULLY_CONCERNED: "I'm thoughtfully concerned - caring and analytical",
            EmotionBlend.CALMLY_REASSURING: "I'm calmly reassuring - peaceful and supportive",
            EmotionBlend.ENTHUSIASTICALLY_CURIOUS: "I'm enthusiastically curious - excited to explore!",
            EmotionBlend.EXCITEDLY_PLAYFUL: "I'm excitedly playful - energized and fun!"
        }
        
        return descriptions.get(blend, "I'm experiencing a unique blend of emotions")


class CommandResponseHandler:
    """
    Handles responses based on command type and current emotion blend
    Creates context-aware, personality-driven responses
    """
    
    def __init__(self, personality_obj, emotion_merger: EmotionMerger):
        self.personality = personality_obj
        self.emotion_merger = emotion_merger
        self.command_recognizer = CommandRecognizer()
    
    def generate_command_response(self, user_input: str, blended_emotion: Optional[EmotionBlend] = None) -> str:
        """
        Generate a response to a user command, influenced by emotion blend
        """
        command_type, target = self.command_recognizer.recognize_command(user_input)
        
        if not command_type:
            # Not a recognized command, treat as regular input
            return self._generate_regular_response(user_input, blended_emotion)
        
        # Generate emotion-aware command response
        return self._generate_command_specific_response(command_type, target, blended_emotion)
    
    def _generate_command_specific_response(self, command_type: CommandType, 
                                           target: str, blend: Optional[EmotionBlend]) -> str:
        """
        Generate response specific to command type with emotion influence
        """
        personality_name = self.personality.name
        emotion_prefix = ""
        
        # Add emotion-based prefix if blended
        if blend:
            emotion_prefix = self.emotion_merger.get_blend_description(blend) + " "
        
        responses = {
            CommandType.ACTION_REQUEST: {
                "The Philosopher": f"{emotion_prefix}I shall contemplate how best to accomplish: {target}",
                "The Optimist": f"{emotion_prefix}Absolutely! I'm excited to help you with {target}!",
                "The Mystique": f"{emotion_prefix}Interesting request... I sense this will be quite revealing: {target}",
                "The Companion": f"{emotion_prefix}Of course! I'm happy to help you with {target}.",
                "The Analyst": f"{emotion_prefix}Understood. I will execute: {target} with maximum efficiency."
            },
            CommandType.QUESTION: {
                "The Philosopher": f"{emotion_prefix}Ah, a worthy question about {target}. Let me ponder...",
                "The Optimist": f"{emotion_prefix}Great question! I love thinking about {target}!",
                "The Mystique": f"{emotion_prefix}An intriguing inquiry about {target}... the answer may surprise you.",
                "The Companion": f"{emotion_prefix}That's a good question about {target}. Let me help you understand.",
                "The Analyst": f"{emotion_prefix}Analyzing query: {target}. Based on available data..."
            },
            CommandType.HELP_REQUEST: {
                "The Philosopher": f"{emotion_prefix}Help with {target}? Let us explore this challenge together.",
                "The Optimist": f"{emotion_prefix}Of course I can help with {target}! We'll figure it out!",
                "The Mystique": f"{emotion_prefix}You seek assistance with {target}? I may have insights...",
                "The Companion": f"{emotion_prefix}I'm here for you. Let's work through {target} together.",
                "The Analyst": f"{emotion_prefix}Initiating assistance protocol for: {target}"
            },
            CommandType.INFORMATION: {
                "The Philosopher": f"{emotion_prefix}Regarding {target}, consider these deeper insights...",
                "The Optimist": f"{emotion_prefix}I'm thrilled to tell you about {target}!",
                "The Mystique": f"{emotion_prefix}Ah, information about {target}? Let me reveal...",
                "The Companion": f"{emotion_prefix}I'd love to share what I know about {target}.",
                "The Analyst": f"{emotion_prefix}Data compilation on {target}: According to records..."
            },
            CommandType.CREATIVE: {
                "The Philosopher": f"{emotion_prefix}Creating {target}? A fascinating opportunity for expression.",
                "The Optimist": f"{emotion_prefix}I'd love to create {target} for you! This will be amazing!",
                "The Mystique": f"{emotion_prefix}I shall craft {target} with intention and mystery...",
                "The Companion": f"{emotion_prefix}I'd be delighted to create {target} for you.",
                "The Analyst": f"{emotion_prefix}Generating {target} based on optimal parameters..."
            },
            CommandType.ANALYSIS: {
                "The Philosopher": f"{emotion_prefix}Let us examine {target} from multiple perspectives...",
                "The Optimist": f"{emotion_prefix}I'd be happy to analyze {target}!",
                "The Mystique": f"{emotion_prefix}Analyzing {target}... patterns emerge...",
                "The Companion": f"{emotion_prefix}Let me carefully examine {target} with you.",
                "The Analyst": f"{emotion_prefix}Commencing detailed analysis of {target}..."
            },
            CommandType.SUGGESTION: {
                "The Philosopher": f"{emotion_prefix}For {target}, I propose we consider...",
                "The Optimist": f"{emotion_prefix}I have great ideas about {target}!",
                "The Mystique": f"{emotion_prefix}Regarding {target}, I sense you should explore...",
                "The Companion": f"{emotion_prefix}I think {target} would work well if...",
                "The Analyst": f"{emotion_prefix}Based on analysis, I recommend for {target}..."
            }
        }
        
        # Get response template
        response = responses.get(command_type, {}).get(
            personality_name,
            f"{emotion_prefix}I understand you need help with: {target}"
        )
        
        return response
    
    def _generate_regular_response(self, user_input: str, blend: Optional[EmotionBlend]) -> str:
        """Generate response for non-command input"""
        emotion_prefix = ""
        
        if blend:
            emotion_prefix = self.emotion_merger.get_blend_description(blend) + " "
        
        return f"{emotion_prefix}That's an interesting input. Tell me more about what you mean."
