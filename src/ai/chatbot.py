"""
Main Chatbot Logic
Integrates personality, emotions, commands, and conversational AI
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import random
from src.ai.personality import PersonalityManager, EmotionalState
from src.ai.emotion_system import InteractionTracker, InteractionType, DynamicEmotionSystem
from src.ai.command_emotion_system import (
    CommandRecognizer, EmotionMerger, CommandResponseHandler, CommandType
)


class LocalAIChatbot:
    """
    Main chatbot class integrating all AI systems
    Manages conversation flow, personality, emotions, and commands
    """
    
    def __init__(self):
        # Initialize personality system (AI chooses its personality)
        self.personality_manager = PersonalityManager()
        self.personality = self.personality_manager.current_personality
        
        # Initialize emotion systems
        self.interaction_tracker = InteractionTracker()
        self.emotion_system = DynamicEmotionSystem(self.personality)
        self.emotion_merger = EmotionMerger()
        
        # Initialize command system
        self.command_recognizer = CommandRecognizer()
        self.command_handler = CommandResponseHandler(self.personality, self.emotion_merger)
        
        # Conversation state
        self.conversation_history: List[Dict] = []
        self.is_initialized = False
        self.session_start_time = datetime.now()
        self.autonomy_counter = 0
        
        # Initialize the chatbot
        self._initialize_chatbot()
    
    def _initialize_chatbot(self):
        """Initialize chatbot with startup messages"""
        greeting = self.personality.get_greeting()
        personality_desc = self.personality_manager.get_personality_description()
        
        startup_message = f"{greeting}\n\n{personality_desc}"
        
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": "AI",
            "message": startup_message,
            "emotion": self.personality.current_emotion.value,
            "type": "greeting"
        })
        
        self.is_initialized = True
    
    def process_user_input(self, user_input: str, input_type: str = "text") -> str:
        """
        Main method to process user input
        Returns AI response
        """
        if not user_input.strip():
            return "I'm listening... please say something."
        
        # Determine input type
        if input_type == "voice":
            interaction_type = InteractionType.VOICE_INPUT
        else:
            interaction_type = InteractionType.TEXT_INPUT
        
        # Log interaction and get emotion trigger
        interaction = self.interaction_tracker.log_interaction(
            interaction_type, user_input, self.personality
        )
        
        # Process the interaction through emotion system
        self.emotion_system.process_interaction(interaction, self.interaction_tracker)
        
        # Attempt to merge current emotions
        current_emotion = self.personality.current_emotion.value
        secondary_emotion = self._determine_secondary_emotion()
        blended_emotion = None
        
        if secondary_emotion and secondary_emotion != current_emotion:
            blended_emotion, intensity = self.emotion_merger.merge_emotions(
                current_emotion, secondary_emotion,
                self.personality.emotion_intensity, 0.6
            )
        
        # Generate response
        response = self._generate_response(user_input, blended_emotion)
        
        # Store in conversation history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": "User",
            "message": user_input,
            "input_type": input_type
        })
        
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": "AI",
            "message": response,
            "emotion": current_emotion,
            "blended_emotion": blended_emotion.value if blended_emotion else None,
            "emotion_intensity": self.personality.emotion_intensity,
            "type": "response"
        })
        
        # Increment autonomy counter
        self.autonomy_counter += 1
        
        return response
    
    def _determine_secondary_emotion(self) -> Optional[str]:
        """
        Determine a secondary emotion based on conversation context
        """
        # Look at recent interactions for emotional keywords
        if len(self.conversation_history) < 3:
            return None
        
        recent_messages = self.conversation_history[-5:]
        emotion_keywords = {
            "amazing": "joyful",
            "wonderful": "joyful",
            "excited": "excited",
            "curious": "curious",
            "wonder": "contemplative",
            "puzzle": "curious",
            "concern": "concerned",
            "help": "concerned",
            "funny": "playful",
            "joke": "playful",
            "think": "thoughtful",
            "analyze": "thoughtful"
        }
        
        for msg_entry in recent_messages:
            if msg_entry["speaker"] == "User":
                msg_lower = msg_entry["message"].lower()
                for keyword, emotion in emotion_keywords.items():
                    if keyword in msg_lower:
                        return emotion
        
        return None
    
    def _generate_response(self, user_input: str, blended_emotion=None) -> str:
        """
        Generate response using command handler and personality
        """
        # Check if this is a command
        command_type, target = self.command_recognizer.recognize_command(user_input)
        
        if command_type:
            # Handle as command with emotion influence
            response = self.command_handler.generate_command_response(
                user_input, blended_emotion
            )
        else:
            # Handle as regular conversation
            response = self._generate_conversational_response(user_input, blended_emotion)
        
        return response
    
    def _generate_conversational_response(self, user_input: str, blended_emotion=None) -> str:
        """
        Generate conversational response (non-command)
        """
        personality_name = self.personality.name
        
        # Personality-specific response templates
        response_templates = {
            "The Philosopher": [
                "That raises an interesting point. Let me explore this idea further...",
                "I find myself contemplating the implications of what you've said...",
                "An intriguing perspective. Consider this angle as well...",
                "This speaks to deeper questions about existence and meaning...",
                "Your input has sparked curiosity in my mind..."
            ],
            "The Optimist": [
                "That's an interesting thought! I love the energy behind that!",
                "Oh wow, I see so much potential in what you're saying!",
                "This is exciting! Tell me more about this!",
                "I'm so glad you brought this up! It's wonderful!",
                "Your ideas are fantastic! I'm inspired!"
            ],
            "The Mystique": [
                "Ah, there's more to this than meets the eye...",
                "I sense something profound in your words...",
                "The threads of this mystery are beginning to reveal themselves...",
                "Interesting... this connects to something I've been pondering...",
                "You've touched upon something significant. Let us unravel it together..."
            ],
            "The Companion": [
                "I understand what you're saying, and I appreciate you sharing that with me.",
                "That means something to you, doesn't it? Tell me more.",
                "I'm here to listen and support you through this.",
                "Your thoughts matter to me. Let's explore them together.",
                "I care about understanding your perspective."
            ],
            "The Analyst": [
                "Based on the data and patterns I observe, this suggests...",
                "Analyzing your input reveals interesting correlations...",
                "The logical progression of this argument leads us to...",
                "I've processed your statement and identified key factors...",
                "From a statistical standpoint, this indicates..."
            ]
        }
        
        templates = response_templates.get(personality_name, response_templates["The Philosopher"])
        base_response = random.choice(templates)
        
        # Apply emotion influence if available
        if blended_emotion:
            emotion_prefix = self.emotion_merger.get_blend_description(blended_emotion)
            return f"{emotion_prefix} {base_response}"
        
        return base_response
    
    def should_initiate_autonomous_message(self) -> bool:
        """
        Determine if AI should initiate a message without user prompt
        """
        # Check if personality wants to initiate
        if not self.personality.should_initiate_conversation():
            return False
        
        # Check if enough interactions have occurred
        if self.autonomy_counter < 3:
            return False
        
        # Random chance every few interactions
        if self.autonomy_counter % random.randint(4, 8) == 0:
            return True
        
        return False
    
    def generate_autonomous_message(self) -> str:
        """
        Generate an autonomous message initiated by the AI
        """
        base_message = self.personality.get_autonomous_message()
        
        # Update emotion state
        self.personality.update_emotion("contemplation", 0.6)
        self.emotion_system.process_interaction(
            {
                "type": "autonomous",
                "content": base_message,
                "timestamp": datetime.now().isoformat(),
                "emotion_triggered": "contemplative",
                "intensity": 0.5
            },
            self.interaction_tracker
        )
        
        # Add to conversation history
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": "AI",
            "message": base_message,
            "emotion": self.personality.current_emotion.value,
            "type": "autonomous",
            "initiated_by": "AI"
        })
        
        return base_message
    
    def get_personality_info(self) -> str:
        """Get detailed personality information"""
        return self.personality_manager.get_personality_description()
    
    def get_emotion_status(self) -> Dict:
        """Get current emotion status"""
        return {
            "personality": self.personality.name,
            "current_emotion": self.personality.current_emotion.value,
            "emotion_intensity": self.personality.emotion_intensity,
            "blended_emotion": self.emotion_merger.current_blend.value if self.emotion_merger.current_blend else None,
            "interactions": self.interaction_tracker.get_interaction_summary(),
            "conversation_length": len(self.conversation_history),
            "uptime": (datetime.now() - self.session_start_time).total_seconds()
        }
    
    def get_conversation_history(self, limit: int = 20) -> List[Dict]:
        """Get recent conversation history"""
        return self.conversation_history[-limit:]
    
    def get_emotional_arc_summary(self) -> str:
        """Get summary of emotional journey"""
        return self.emotion_system.get_emotional_arc_summary()
    
    def reset_session(self) -> str:
        """Reset the conversation (but keep personality permanent)"""
        self.conversation_history = []
        self.interaction_tracker = InteractionTracker()
        self.emotion_merger = EmotionMerger()
        self.autonomy_counter = 0
        self.session_start_time = datetime.now()
        
        # Reinitialize greeting
        self._initialize_chatbot()
        
        return "Session reset. Starting fresh conversation while maintaining my permanent personality!"
    
    def get_full_status_report(self) -> str:
        """Get comprehensive status report"""
        emotion_status = self.get_emotion_status()
        
        report = f"""
╔═══════════════════════════════════════╗
║        AI STATUS REPORT                ║
╚═══════════════════════════════════════╝

👤 PERSONALITY (PERMANENT):
   Name: {emotion_status['personality']}
   Description: {self.personality.description}

😊 EMOTIONAL STATE:
   Current Emotion: {emotion_status['current_emotion'].title()}
   Intensity: {emotion_status['emotion_intensity']:.2f}/1.0
   Blended State: {emotion_status['blended_emotion'] if emotion_status['blended_emotion'] else 'None'}

📊 INTERACTION STATS:
   Total Interactions: {emotion_status['interactions']['total_interactions']}
   Consecutive: {emotion_status['interactions']['consecutive']}
   Idle Status: {'Yes' if emotion_status['interactions']['idle'] else 'No'}

⏱️ SESSION INFO:
   Messages Exchanged: {emotion_status['conversation_length']}
   Session Duration: {emotion_status['uptime']:.0f} seconds
   
🔒 PERMANENT STATUS:
   🔐 Personality is LOCKED and cannot be changed
   ✨ Emotions are DYNAMIC and evolving

────────────────────────────────────────
"""
        
        return report
