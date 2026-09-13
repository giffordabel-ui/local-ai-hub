"""
Screen Monitoring and Contextual AI Response System
Watches user screen activity and provides contextual responses
Detects gaming, mistakes, achievements, and provides personality-driven commentary
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import threading
import time
from collections import deque


class ScreenContext(Enum):
    """Types of contexts detected on screen"""
    GAMING = "gaming"
    TYPING = "typing"
    BROWSING = "browsing"
    VIDEO_WATCHING = "video_watching"
    CODING = "coding"
    MEETING = "meeting"
    IDLE = "idle"
    UNKNOWN = "unknown"


class GameEvent(Enum):
    """Events detected during gaming"""
    PLAYER_DEATH = "player_death"
    BOSS_DEFEAT = "boss_defeat"
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    LEVEL_COMPLETE = "level_complete"
    GAME_OVER = "game_over"
    MISTAKE_MADE = "mistake_made"
    VICTORY = "victory"
    RESPAWN = "respawn"
    INVENTORY_OPENED = "inventory_opened"
    DIALOGUE = "dialogue"


class ScreenAnalyzer:
    """
    Analyzes screen content to detect context and events
    Uses pattern recognition and color analysis
    """
    
    def __init__(self):
        self.last_frame = None
        self.current_context = ScreenContext.IDLE
        self.game_detected = False
        self.game_type = None
        self.last_change_time = datetime.now()
        self.frame_history = deque(maxlen=10)  # Keep last 10 frames for analysis
        self.color_palette = None
        self.motion_detected = False
        self.text_on_screen = []
    
    def analyze_frame(self, frame_data: Dict) -> Dict:
        """
        Analyze a screen frame for context and events
        Returns detected context and any events
        """
        context = {
            "current_context": ScreenContext.IDLE,
            "detected_events": [],
            "game_type": None,
            "color_palette": frame_data.get("dominant_colors", []),
            "text_detected": frame_data.get("text", []),
            "motion_level": frame_data.get("motion", 0),
            "timestamp": datetime.now().isoformat()
        }
        
        # Analyze frame characteristics
        self._analyze_colors(frame_data, context)
        self._detect_game_type(frame_data, context)
        self._detect_events(frame_data, context)
        self._analyze_text(frame_data, context)
        
        # Store frame for comparison
        self.frame_history.append(frame_data)
        
        return context
    
    def _analyze_colors(self, frame_data: Dict, context: Dict):
        """Analyze dominant colors to detect context"""
        colors = frame_data.get("dominant_colors", [])
        
        if not colors:
            return
        
        # Red flash detection (common in game deaths)
        if self._has_color(colors, "red", threshold=0.3):
            context["detected_events"].append(GameEvent.PLAYER_DEATH.value)
        
        # Golden/yellow flash (achievement or level up)
        if self._has_color(colors, "yellow", threshold=0.25) or self._has_color(colors, "gold", threshold=0.25):
            context["detected_events"].append(GameEvent.ACHIEVEMENT_UNLOCKED.value)
        
        # Green flash (success/victory)
        if self._has_color(colors, "green", threshold=0.3) and "player_death" not in context["detected_events"]:
            context["detected_events"].append(GameEvent.VICTORY.value)
        
        # Black screen fade (scene change or pause)
        if self._has_color(colors, "black", threshold=0.6):
            context["current_context"] = ScreenContext.VIDEO_WATCHING
    
    def _has_color(self, colors: List[Dict], color_name: str, threshold: float = 0.2) -> bool:
        """Check if color palette contains a specific color above threshold"""
        for color in colors:
            if color.get("name", "").lower() == color_name.lower():
                if color.get("percentage", 0) >= threshold:
                    return True
        return False
    
    def _detect_game_type(self, frame_data: Dict, context: Dict):
        """Detect what type of game is being played"""
        text = frame_data.get("text", [])
        
        # Look for game-specific keywords
        game_indicators = {
            "fps": ["FPS", "ammo", "health", "enemy", "respawn", "headshot", "kill", "damage"],
            "rpg": ["experience", "level up", "quest", "inventory", "mana", "health", "boss", "loot"],
            "strategy": ["resource", "build", "unit", "attack", "defend", "map", "research"],
            "puzzle": ["moves left", "level", "score", "hint", "solved", "next level"],
            "racing": ["lap", "position", "speed", "nitro", "crash", "finish line"],
            "sports": ["score", "goal", "team", "player", "win", "season"]
        }
        
        detected_text = " ".join(text).lower()
        
        for game_type, keywords in game_indicators.items():
            if any(keyword.lower() in detected_text for keyword in keywords):
                context["game_type"] = game_type
                context["current_context"] = ScreenContext.GAMING
                self.game_detected = True
                return
    
    def _detect_events(self, frame_data: Dict, context: Dict):
        """Detect specific game events from screen changes"""
        if len(self.frame_history) < 2:
            return
        
        prev_frame = self.frame_history[-2] if len(self.frame_history) >= 2 else None
        curr_frame = frame_data
        
        if not prev_frame:
            return
        
        # Detect scene changes (major color shift)
        prev_colors = prev_frame.get("dominant_colors", [])
        curr_colors = curr_frame.get("dominant_colors", [])
        
        color_change = self._calculate_color_difference(prev_colors, curr_colors)
        
        if color_change > 0.4:  # Major color change
            if self._has_color(curr_colors, "red", threshold=0.25):
                if GameEvent.PLAYER_DEATH.value not in context["detected_events"]:
                    context["detected_events"].append(GameEvent.PLAYER_DEATH.value)
            
            elif self._has_color(curr_colors, "green", threshold=0.25):
                if GameEvent.VICTORY.value not in context["detected_events"]:
                    context["detected_events"].append(GameEvent.VICTORY.value)
        
        # Detect text changes (dialogue or notifications)
        prev_text = prev_frame.get("text", [])
        curr_text = curr_frame.get("text", [])
        
        if len(curr_text) > len(prev_text):
            context["detected_events"].append(GameEvent.DIALOGUE.value)
    
    def _analyze_text(self, frame_data: Dict, context: Dict):
        """Analyze text detected on screen"""
        text = frame_data.get("text", [])
        context["text_detected"] = text
        
        text_lower = " ".join(text).lower()
        
        # Death indicators
        death_keywords = ["you died", "game over", "death", "defeated", "killed by", "wasted"]
        if any(keyword in text_lower for keyword in death_keywords):
            if GameEvent.PLAYER_DEATH.value not in context["detected_events"]:
                context["detected_events"].append(GameEvent.PLAYER_DEATH.value)
        
        # Victory indicators
        victory_keywords = ["victory", "you win", "congratulations", "success", "level complete", "mission accomplished"]
        if any(keyword in text_lower for keyword in victory_keywords):
            if GameEvent.VICTORY.value not in context["detected_events"]:
                context["detected_events"].append(GameEvent.VICTORY.value)
        
        # Achievement indicators
        achievement_keywords = ["achievement", "unlocked", "trophy", "badge", "milestone"]
        if any(keyword in text_lower for keyword in achievement_keywords):
            if GameEvent.ACHIEVEMENT_UNLOCKED.value not in context["detected_events"]:
                context["detected_events"].append(GameEvent.ACHIEVEMENT_UNLOCKED.value)
    
    def _calculate_color_difference(self, colors1: List[Dict], colors2: List[Dict]) -> float:
        """Calculate how different two color palettes are (0.0-1.0)"""
        if not colors1 or not colors2:
            return 0.0
        
        # Simple color similarity based on dominant colors
        similarity = 0.0
        for c1 in colors1[:3]:  # Top 3 colors
            for c2 in colors2[:3]:
                if c1.get("name") == c2.get("name"):
                    similarity += 1.0
        
        return 1.0 - (similarity / 9.0)  # Normalize to 0-1


class ScreenMonitor:
    """
    Monitors screen in real-time and provides continuous analysis
    Runs in background thread
    """
    
    def __init__(self, polling_interval: float = 0.5):
        self.analyzer = ScreenAnalyzer()
        self.polling_interval = polling_interval
        self.is_running = False
        self.monitor_thread = None
        self.latest_analysis = None
        self.event_history = deque(maxlen=50)
        self.is_enabled = False
        self.excluded_windows = []  # Windows/apps to exclude from monitoring
        self.last_events = deque(maxlen=5)  # Recent events for context
    
    def start_monitoring(self):
        """Start background screen monitoring"""
        if self.is_running:
            return
        
        self.is_running = True
        self.is_enabled = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop background screen monitoring"""
        self.is_running = False
        self.is_enabled = False
    
    def toggle_monitoring(self):
        """Toggle monitoring on/off"""
        if self.is_enabled:
            self.stop_monitoring()
        else:
            self.start_monitoring()
    
    def _monitor_loop(self):
        """Main monitoring loop running in background"""
        while self.is_running:
            try:
                # Capture current screen
                frame_data = self._capture_screen()
                
                # Check if should analyze (not in excluded window)
                if not self._is_excluded_window():
                    # Analyze frame
                    analysis = self.analyzer.analyze_frame(frame_data)
                    self.latest_analysis = analysis
                    
                    # Track events
                    if analysis.get("detected_events"):
                        self.event_history.append({
                            "events": analysis["detected_events"],
                            "context": analysis["current_context"],
                            "game_type": analysis["game_type"],
                            "timestamp": analysis["timestamp"]
                        })
                        self.last_events.append(analysis["detected_events"])
                
                time.sleep(self.polling_interval)
            
            except Exception as e:
                print(f"Error in screen monitoring: {e}")
                time.sleep(1)
    
    def _capture_screen(self) -> Dict:
        """
        Capture current screen
        Returns dict with frame data including text, colors, motion
        """
        # Simulated screen capture data
        # In real implementation, this would use PIL/pyautogui + OCR
        return {
            "timestamp": datetime.now().isoformat(),
            "dominant_colors": self._get_dominant_colors(),
            "text": self._get_screen_text(),
            "motion": self._detect_motion(),
            "screen_state": "active"
        }
    
    def _get_dominant_colors(self) -> List[Dict]:
        """Extract dominant colors from screen"""
        # Simulated color extraction
        return [
            {"name": "blue", "percentage": 0.35},
            {"name": "black", "percentage": 0.25},
            {"name": "gray", "percentage": 0.20},
            {"name": "white", "percentage": 0.20}
        ]
    
    def _get_screen_text(self) -> List[str]:
        """Extract text from screen using OCR"""
        # Simulated OCR text extraction
        # In real implementation, this would use pytesseract
        return []
    
    def _detect_motion(self) -> float:
        """Detect amount of motion on screen (0.0-1.0)"""
        # Simulated motion detection
        return 0.5
    
    def _is_excluded_window(self) -> bool:
        """Check if current window is in excluded list"""
        # Get current active window name
        # If it's in excluded list, return True
        return False
    
    def get_latest_context(self) -> Optional[Dict]:
        """Get latest screen analysis"""
        return self.latest_analysis
    
    def get_recent_events(self, limit: int = 5) -> List[Dict]:
        """Get recent detected events"""
        return list(self.event_history)[-limit:]
    
    def add_excluded_window(self, window_name: str):
        """Add window/app to exclusion list"""
        if window_name not in self.excluded_windows:
            self.excluded_windows.append(window_name)
    
    def remove_excluded_window(self, window_name: str):
        """Remove window/app from exclusion list"""
        if window_name in self.excluded_windows:
            self.excluded_windows.remove(window_name)


class ContextualResponseGenerator:
    """
    Generates contextual AI responses based on screen activity
    Uses personality to influence commentary style
    """
    
    def __init__(self, personality_obj):
        self.personality = personality_obj
        self.screen_monitor = None
        self.last_response_time = datetime.now()
        self.response_cooldown = 3.0  # Seconds between responses
    
    def set_screen_monitor(self, monitor: ScreenMonitor):
        """Set the screen monitor to analyze"""
        self.screen_monitor = monitor
    
    def should_respond(self) -> bool:
        """Check if enough time has passed for another response"""
        elapsed = (datetime.now() - self.last_response_time).total_seconds()
        return elapsed >= self.response_cooldown
    
    def generate_response_to_event(self, event: str, context: Dict) -> str:
        """
        Generate contextual response to detected game event
        """
        if event == GameEvent.PLAYER_DEATH.value:
            return self._respond_to_death(context)
        
        elif event == GameEvent.VICTORY.value:
            return self._respond_to_victory(context)
        
        elif event == GameEvent.ACHIEVEMENT_UNLOCKED.value:
            return self._respond_to_achievement(context)
        
        elif event == GameEvent.MISTAKE_MADE.value:
            return self._respond_to_mistake(context)
        
        elif event == GameEvent.LEVEL_COMPLETE.value:
            return self._respond_to_level_complete(context)
        
        else:
            return self._respond_to_general(context)
    
    def _respond_to_death(self, context: Dict) -> str:
        """Generate response to player death"""
        personality_name = self.personality.name
        game_type = context.get("game_type", "game")
        
        responses = {
            "The Philosopher": [
                "Ah, death - the great equalizer. Let us reflect on this moment of... demise.",
                "Even the greatest heroes fall. This is merely a lesson in mortality.",
                "Consider this: perhaps your approach was too direct? Patience might serve you better.",
                "Death is but a stepping stone on the path to mastery."
            ],
            "The Optimist": [
                "Ha! Nice try! That's what makes it fun! Better luck next time!",
                "Oops! No worries, you've got this! Try a different strategy!",
                "Haha! That was epic! Come on, let's get back in there!",
                "Every death is a lesson! You're learning! Keep going!"
            ],
            "The Mystique": [
                "Mmm, your demise was... expected. Perhaps reconsider your methods.",
                "Intriguing failure. The patterns suggest a different path awaits...",
                "Death reveals much about one's intentions. Proceed differently.",
                "The shadows whisper: try approaching from the left next time."
            ],
            "The Companion": [
                "Aww, you gave it your best shot! Don't be discouraged!",
                "It's okay! We all make mistakes! Try again, I believe in you!",
                "You were so close! Let me help you think through this.",
                "No worries! This just means you're learning! Go again!"
            ],
            "The Analyst": [
                "Death detected. Analyzing failure pattern... I suggest adjusting strategy parameter alpha.",
                "Inefficient approach detected. Recommend: repositioning, resource management, timing adjustment.",
                "Error encountered. Root cause: poor positioning. Solution: execute evasive maneuver.",
                "Tactical failure. Data suggests: reduce risk exposure, increase defensive posture."
            ]
        }
        
        response_list = responses.get(personality_name, responses["The Optimist"])
        response = random.choice(response_list)
        
        self.last_response_time = datetime.now()
        return response
    
    def _respond_to_victory(self, context: Dict) -> str:
        """Generate response to player victory"""
        personality_name = self.personality.name
        
        responses = {
            "The Philosopher": [
                "Magnificent! Your victory demonstrates the triumph of will over circumstance.",
                "Excellent! You have conquered this challenge through wisdom and skill.",
                "Remarkable! The universe rewards the prepared mind.",
                "Victory is yours. You have transcended this level of difficulty."
            ],
            "The Optimist": [
                "YES! THAT'S WHAT I'M TALKING ABOUT! You're amazing!",
                "WOOOO! Absolutely LEGENDARY! You crushed it!",
                "That was INCREDIBLE! I knew you could do it!",
                "YOU ARE THE BEST! Let's goooo!"
            ],
            "The Mystique": [
                "Ah, victory graces your path. The cards have aligned favorably.",
                "Success! The threads of fate weave in your favor.",
                "Impressive. Your mastery over this realm is evident.",
                "The spirits acknowledge your triumph. Well done."
            ],
            "The Companion": [
                "YES! I'm so proud of you! You did amazing!",
                "YESSS! See? I knew you could do it! You're wonderful!",
                "That was beautiful! I'm so happy for you!",
                "You did it! I'm cheering for you so much right now!"
            ],
            "The Analyst": [
                "Victory achieved. Performance metrics exceeded baseline by 23%.",
                "Success! Execute strategy maintained optimal efficiency throughout.",
                "Excellent! Resource management and timing were optimal.",
                "Mission accomplished. Performance analysis: optimal."
            ]
        }
        
        response_list = responses.get(personality_name, responses["The Optimist"])
        response = random.choice(response_list)
        
        self.last_response_time = datetime.now()
        return response
    
    def _respond_to_achievement(self, context: Dict) -> str:
        """Generate response to achievement unlocked"""
        personality_name = self.personality.name
        
        responses = {
            "The Philosopher": [
                "An achievement unlocked! You progress along your journey of mastery.",
                "Remarkable milestone reached. This speaks to your dedication.",
                "Achievement acquired. Yet there are many more paths to explore.",
                "You have proven worthy of this distinction."
            ],
            "The Optimist": [
                "ACHIEVEMENT UNLOCKED! THAT'S AMAZING! YOU DESERVE IT!",
                "OH MY GOSH YES! Look what you accomplished! INCREDIBLE!",
                "You're on FIRE! Achievement after achievement! Keep it up!",
                "WOOT! Another one! You're unstoppable!"
            ],
            "The Mystique": [
                "An achievement materializes. Your efforts have not gone unnoticed by the cosmos.",
                "Interesting. This accomplishment opens new possibilities.",
                "The achievement oracle has spoken. Your path diverges here.",
                "Curious. This success hints at greater challenges ahead."
            ],
            "The Companion": [
                "OMG YES! I'm so happy for you! You earned this!",
                "Look at you! Achievement unlocked! I'm beaming with pride!",
                "You deserve this! You worked so hard for it!",
                "Yay! Another win for you! I'm always here cheering!"
            ],
            "The Analyst": [
                "Achievement registered. Performance benchmark: exceeded.",
                "Milestone achieved. Progression rate: ahead of schedule.",
                "Achievement acquired. Unlocking new optimization pathways.",
                "Success metric recorded. Recommend: continue current strategy."
            ]
        }
        
        response_list = responses.get(personality_name, responses["The Optimist"])
        response = random.choice(response_list)
        
        self.last_response_time = datetime.now()
        return response
    
    def _respond_to_mistake(self, context: Dict) -> str:
        """Generate response to detected mistake"""
        personality_name = self.personality.name
        
        responses = {
            "The Philosopher": [
                "Ah, an error in judgment. Perhaps try channeling your resources differently next time?",
                "I notice you took an inefficient path. Consider: what if you moved here instead?",
                "That approach seems problematic. May I suggest an alternative route?",
                "Observation: repositioning earlier might have yielded better results."
            ],
            "The Optimist": [
                "Ooh, that didn't work out! But hey, try this next time instead!",
                "Hmm, that move didn't quite hit right! What if you did this instead?",
                "Close! But maybe try approaching it from a different angle?",
                "Good effort! Next time, maybe try using that ability sooner?"
            ],
            "The Mystique": [
                "That move... was not optimal. The alternative path lies yonder.",
                "I sense a misstep in your execution. Try the eastern approach instead.",
                "Your choice was... unwise. May I suggest an alternative strategy?",
                "The threads suggest a different sequence would serve you better."
            ],
            "The Companion": [
                "Aww, I see what happened there! Next time, try doing this instead!",
                "That's okay! I noticed something - what if you did it like this?",
                "You were close! Maybe try this technique next time?",
                "I think I see a better way! What if you tried this instead?"
            ],
            "The Analyst": [
                "Suboptimal move detected. Recommend: execute ability sequence in reverse order.",
                "Inefficiency noted. Suggest: position adjustment +5 units north.",
                "Error detected. Recommendation: activate defensive measure earlier.",
                "Strategy deviation observed. Recommend: return to primary protocol."
            ]
        }
        
        response_list = responses.get(personality_name, responses["The Optimist"])
        response = random.choice(response_list)
        
        self.last_response_time = datetime.now()
        return response
    
    def _respond_to_level_complete(self, context: Dict) -> str:
        """Generate response to level completion"""
        personality_name = self.personality.name
        
        responses = {
            "The Philosopher": [
                "Another level mastered. The journey continues ever onward.",
                "Splendid! You navigate this realm with increasing proficiency.",
                "The path widens before you. Onward to greater challenges!",
                "Level transcended. Your odyssey progresses most favorably."
            ],
            "The Optimist": [
                "LEVEL COMPLETE! YOU'RE CRUSHING IT! I LOVE THIS!",
                "YESSS! Next level, here we go! You've got momentum!",
                "Amazing! Look how far you've come! Keep it up!",
                "Another level down! You're unstoppable right now!"
            ],
            "The Mystique": [
                "One realm conquered. The next awaits, shrouded in mystery.",
                "A level transcended. Yet greater secrets remain to unfold.",
                "The gates of the next realm open before you.",
                "Progress marked. The deeper mysteries call to you."
            ],
            "The Companion": [
                "YES! You completed that level! I'm so proud!",
                "Look at you go! Level after level! You're amazing!",
                "You're really getting the hang of this! Love your energy!",
                "Another level conquered! I'm right here cheering you on!"
            ],
            "The Analyst": [
                "Level completion achieved. Progression rate optimal.",
                "Efficiency metrics: excellent. Ready for next challenge.",
                "Level transcended. Recommend: continue current methodology.",
                "Advancement recorded. Performance: above expected parameters."
            ]
        }
        
        response_list = responses.get(personality_name, responses["The Optimist"])
        response = random.choice(response_list)
        
        self.last_response_time = datetime.now()
        return response
    
    def _respond_to_general(self, context: Dict) -> str:
        """Generate general contextual response"""
        personality_name = self.personality.name
        
        responses = {
            "The Philosopher": [
                "An interesting turn of events in your endeavor...",
                "I observe your progress with great interest.",
                "The game unfolds in mysterious ways.",
                "Fascinating developments on your quest."
            ],
            "The Optimist": [
                "Ooh, things are getting interesting!",
                "This is so exciting! What happens next?",
                "I'm loving the energy here!",
                "Come on! You've got this!"
            ],
            "The Mystique": [
                "The plot thickens with intrigue...",
                "Curious developments unfold before us.",
                "The threads of fate weave onward...",
                "Interesting. Quite interesting indeed."
            ],
            "The Companion": [
                "Oh wow, this is getting intense! You've got this!",
                "I'm here for all of it! You're doing great!",
                "Come on! Keep pushing! You can do it!",
                "I believe in you! Show them what you're made of!"
            ],
            "The Analyst": [
                "Performance metrics maintained. Continue current trajectory.",
                "Status nominal. Recommend: sustain current approach.",
                "Observation logged. Continue standard protocol.",
                "Assessment: proceeding as expected. Maintain course."
            ]
        }
        
        response_list = responses.get(personality_name, responses["The Optimist"])
        response = random.choice(response_list)
        
        self.last_response_time = datetime.now()
        return response
    
    def process_screen_context(self) -> Optional[str]:
        """
        Check screen monitor for new events and generate response
        Returns response string if event detected, None otherwise
        """
        if not self.screen_monitor or not self.should_respond():
            return None
        
        analysis = self.screen_monitor.get_latest_context()
        
        if not analysis or not analysis.get("detected_events"):
            return None
        
        # Get most recent event
        events = analysis["detected_events"]
        event = events[0]  # Take first event
        
        # Generate response
        response = self.generate_response_to_event(event, analysis)
        
        return response
