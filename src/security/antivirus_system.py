"""
Advanced Antivirus and Threat Detection System
Real-time virus detection, quarantine, and counter-attack capabilities
AI-powered threat analysis with personality-driven responses
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import threading
import time
from collections import deque
import hashlib
import json
import random


class ThreatLevel(Enum):
    """Severity levels for detected threats"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    SUSPICIOUS = "suspicious"
    CLEAN = "clean"


class ThreatType(Enum):
    """Types of threats detected"""
    RANSOMWARE = "ransomware"
    TROJAN = "trojan"
    WORM = "worm"
    SPYWARE = "spyware"
    ADWARE = "adware"
    ROOTKIT = "rootkit"
    KEYLOGGER = "keylogger"
    BOTNET = "botnet"
    BACKDOOR = "backdoor"
    CRYPTOMINER = "cryptominer"
    MALWARE = "malware"
    EXPLOIT = "exploit"
    PUP = "pup"  # Potentially Unwanted Program
    UNKNOWN = "unknown"


class QuarantineStatus(Enum):
    """Status of quarantined files"""
    ISOLATED = "isolated"
    ANALYZING = "analyzing"
    THREAT_CONFIRMED = "threat_confirmed"
    FALSE_POSITIVE = "false_positive"
    PENDING_ACTION = "pending_action"
    TERMINATED = "terminated"
    COUNTER_ATTACKED = "counter_attacked"


class VirusSignatureDatabase:
    """
    Database of known virus signatures and behavioral patterns
    """
    
    def __init__(self):
        self.signatures = self._load_signatures()
        self.behavioral_patterns = self._load_behavioral_patterns()
        self.known_malicious_ips = self._load_malicious_ips()
        self.suspicious_file_extensions = [
            '.exe', '.dll', '.scr', '.vbs', '.js', '.bat', '.cmd', '.com',
            '.pif', '.msi', '.jar', '.zip', '.rar', '.7z', '.iso',
            '.sh', '.ps1', '.psm1', '.vb', '.asp', '.aspx'
        ]
    
    def _load_signatures(self) -> Dict[str, Dict]:
        """Load known virus signatures"""
        return {
            "wannacry": {
                "hashes": [
                    "5d26c4506ccc3bf9b820fe00304a86b8",
                    "ed01ebfbc9eb5bbea545af4d01bf5f1071661840480ff4fb3da8e30256386854"
                ],
                "threat_type": ThreatType.RANSOMWARE,
                "threat_level": ThreatLevel.CRITICAL,
                "description": "WannaCry ransomware - encrypts files and demands payment"
            },
            "petya": {
                "hashes": ["27f7d922455159331fabda992a65052d"],
                "threat_type": ThreatType.RANSOMWARE,
                "threat_level": ThreatLevel.CRITICAL,
                "description": "Petya ransomware - master boot record encryption"
            },
            "emotet": {
                "hashes": ["4d868e3181e79c4b"],
                "threat_type": ThreatType.TROJAN,
                "threat_level": ThreatLevel.CRITICAL,
                "description": "Emotet banking trojan - steals financial credentials"
            },
            "zeus": {
                "hashes": ["15a09e45c5f9ce2f"],
                "threat_type": ThreatType.TROJAN,
                "threat_level": ThreatLevel.HIGH,
                "description": "Zeus banking trojan - credential theft"
            },
            "conficker": {
                "hashes": ["8b9c5d2b"],
                "threat_type": ThreatType.WORM,
                "threat_level": ThreatLevel.HIGH,
                "description": "Conficker worm - network propagation"
            },
            "stuxnet": {
                "hashes": ["e97699a2b43d3bac"],
                "threat_type": ThreatType.WORM,
                "threat_level": ThreatLevel.CRITICAL,
                "description": "Stuxnet - industrial control system malware"
            },
            "mirai": {
                "hashes": ["b5f85c4d"],
                "threat_type": ThreatType.BOTNET,
                "threat_level": ThreatLevel.HIGH,
                "description": "Mirai botnet - IoT device control"
            }
        }
    
    def _load_behavioral_patterns(self) -> List[Dict]:
        """Load suspicious behavioral patterns"""
        return [
            {
                "name": "File Encryption Loop",
                "pattern": "iterates_files:recursive AND modifies:random_extension AND writes:large_file",
                "threat_type": ThreatType.RANSOMWARE,
                "threat_level": ThreatLevel.CRITICAL
            },
            {
                "name": "Registry Modification",
                "pattern": "modifies:registry AND disables:antivirus AND hides:files",
                "threat_type": ThreatType.ROOTKIT,
                "threat_level": ThreatLevel.HIGH
            },
            {
                "name": "Network Beaconing",
                "pattern": "connects:external_ip AND periodic:connection AND encrypted:payload",
                "threat_type": ThreatType.BACKDOOR,
                "threat_level": ThreatLevel.HIGH
            },
            {
                "name": "Keylogging Activity",
                "pattern": "hooks:keyboard AND writes:log_file AND sends:network",
                "threat_type": ThreatType.KEYLOGGER,
                "threat_level": ThreatLevel.HIGH
            },
            {
                "name": "Cryptomining",
                "pattern": "cpu:intensive AND connects:mining_pool AND random:data",
                "threat_type": ThreatType.CRYPTOMINER,
                "threat_level": ThreatLevel.MEDIUM
            },
            {
                "name": "Privilege Escalation",
                "pattern": "exploits:vulnerability AND requests:admin AND modifies:system",
                "threat_type": ThreatType.EXPLOIT,
                "threat_level": ThreatLevel.HIGH
            }
        ]
    
    def _load_malicious_ips(self) -> List[str]:
        """Load known malicious IP addresses"""
        return [
            "192.0.2.1",
            "198.51.100.1",
            "203.0.113.1",
            "10.0.0.1",
            "172.16.0.1"
        ]


class ThreatAnalyzer:
    """
    Analyzes files and network activity for threats
    Uses signature detection, heuristic analysis, and behavioral patterns
    """
    
    def __init__(self):
        self.signature_db = VirusSignatureDatabase()
        self.analysis_history = deque(maxlen=100)
    
    def scan_file(self, file_path: str, file_data: Dict) -> Dict:
        """
        Comprehensive file threat analysis
        Returns detailed threat assessment
        """
        analysis = {
            "file_path": file_path,
            "timestamp": datetime.now().isoformat(),
            "threat_level": ThreatLevel.CLEAN,
            "threat_type": ThreatType.UNKNOWN,
            "threat_detected": False,
            "confidence": 0.0,
            "details": [],
            "recommendations": [],
            "file_hash": file_data.get("hash", ""),
            "file_size": file_data.get("size", 0),
            "file_extension": file_data.get("extension", ""),
            "source": file_data.get("source", "unknown")
        }
        
        # Signature-based detection
        signature_match = self._check_signature(file_data.get("hash", ""))
        if signature_match:
            analysis["threat_detected"] = True
            analysis["threat_level"] = signature_match["threat_level"]
            analysis["threat_type"] = signature_match["threat_type"]
            analysis["confidence"] = 0.95
            analysis["details"].append(f"Signature match: {signature_match['description']}")
            self.analysis_history.append(analysis)
            return analysis
        
        # Heuristic analysis
        heuristic_results = self._heuristic_analysis(file_data)
        if heuristic_results:
            analysis["threat_detected"] = True
            analysis["threat_level"] = heuristic_results["threat_level"]
            analysis["threat_type"] = heuristic_results["threat_type"]
            analysis["confidence"] = heuristic_results["confidence"]
            analysis["details"].extend(heuristic_results["indicators"])
        
        # Behavioral pattern analysis
        behavioral_results = self._analyze_behavior(file_data)
        if behavioral_results:
            analysis["threat_detected"] = True
            analysis["threat_level"] = max(
                analysis["threat_level"],
                behavioral_results["threat_level"],
                key=lambda x: ["clean", "low", "suspicious", "medium", "high", "critical"].index(x.value)
            )
            analysis["threat_type"] = behavioral_results["threat_type"]
            analysis["confidence"] = max(analysis["confidence"], behavioral_results["confidence"])
            analysis["details"].extend(behavioral_results["patterns"])
        
        # File extension analysis
        extension_risk = self._analyze_file_extension(file_data.get("extension", ""))
        if extension_risk:
            analysis["details"].append(extension_risk)
            if analysis["threat_level"] == ThreatLevel.CLEAN:
                analysis["threat_level"] = ThreatLevel.SUSPICIOUS
        
        # Source reputation
        source_risk = self._analyze_source(file_data.get("source", "unknown"))
        if source_risk:
            analysis["details"].append(source_risk)
        
        # Set recommendations
        analysis["recommendations"] = self._generate_recommendations(analysis)
        
        self.analysis_history.append(analysis)
        return analysis
    
    def _check_signature(self, file_hash: str) -> Optional[Dict]:
        """Check file against known virus signatures"""
        for virus_name, virus_data in self.signature_db.signatures.items():
            if file_hash in virus_data.get("hashes", []):
                return {
                    "virus_name": virus_name,
                    "threat_type": virus_data["threat_type"],
                    "threat_level": virus_data["threat_level"],
                    "description": virus_data["description"]
                }
        return None
    
    def _heuristic_analysis(self, file_data: Dict) -> Optional[Dict]:
        """Analyze file using heuristic techniques"""
        indicators = []
        threat_level = ThreatLevel.CLEAN
        threat_type = ThreatType.UNKNOWN
        confidence = 0.0
        
        # Check for suspicious code patterns
        content = file_data.get("content", "").lower()
        
        ransomware_indicators = [
            "encrypts", "encrypt_file", "crypto", "ransom", "bitcoin",
            "pay_or_lose", "files_encrypted", "extension_change"
        ]
        
        trojan_indicators = [
            "reverse_shell", "backdoor", "cmd_exec", "powershell",
            "download_execute", "steal_data", "exfiltrate"
        ]
        
        spyware_indicators = [
            "keylog", "screen_capture", "monitor_activity", "steal_password",
            "browser_history", "clipboard", "webcam_access"
        ]
        
        cryptominer_indicators = [
            "monero", "xmr", "mining", "pool_connect", "cpu_intensive",
            "hash_calc", "nonce", "difficulty"
        ]
        
        # Scan for ransomware indicators
        ransomware_count = sum(1 for ind in ransomware_indicators if ind in content)
        if ransomware_count >= 2:
            indicators.append(f"Ransomware indicators detected: {ransomware_count}")
            threat_type = ThreatType.RANSOMWARE
            threat_level = ThreatLevel.CRITICAL
            confidence = 0.8 + (ransomware_count * 0.05)
        
        # Scan for trojan indicators
        trojan_count = sum(1 for ind in trojan_indicators if ind in content)
        if trojan_count >= 2:
            indicators.append(f"Trojan indicators detected: {trojan_count}")
            if threat_level.value not in ["critical"]:
                threat_type = ThreatType.TROJAN
                threat_level = ThreatLevel.HIGH
            confidence = max(confidence, 0.75 + (trojan_count * 0.05))
        
        # Scan for spyware indicators
        spyware_count = sum(1 for ind in spyware_indicators if ind in content)
        if spyware_count >= 2:
            indicators.append(f"Spyware indicators detected: {spyware_count}")
            threat_type = ThreatType.SPYWARE
            threat_level = ThreatLevel.HIGH
            confidence = max(confidence, 0.75)
        
        # Scan for cryptominer indicators
        cryptominer_count = sum(1 for ind in cryptominer_indicators if ind in content)
        if cryptominer_count >= 2:
            indicators.append(f"Cryptominer indicators detected: {cryptominer_count}")
            threat_type = ThreatType.CRYPTOMINER
            threat_level = ThreatLevel.MEDIUM
            confidence = max(confidence, 0.7)
        
        if indicators:
            return {
                "indicators": indicators,
                "threat_type": threat_type,
                "threat_level": threat_level,
                "confidence": min(confidence, 0.99)
            }
        
        return None
    
    def _analyze_behavior(self, file_data: Dict) -> Optional[Dict]:
        """Analyze file behavior patterns"""
        behaviors = file_data.get("behaviors", [])
        
        for pattern in self.signature_db.behavioral_patterns:
            pattern_name = pattern["name"]
            pattern_keywords = pattern["pattern"].split(" AND ")
            
            matching_behaviors = sum(
                1 for behavior in behaviors
                if any(keyword.replace(":", "_") in behavior.lower() for keyword in pattern_keywords)
            )
            
            if matching_behaviors >= len(pattern_keywords) - 1:  # Match most keywords
                return {
                    "pattern": pattern_name,
                    "patterns": [f"Behavioral pattern: {pattern_name}"],
                    "threat_type": pattern["threat_type"],
                    "threat_level": pattern["threat_level"],
                    "confidence": 0.85
                }
        
        return None
    
    def _analyze_file_extension(self, extension: str) -> Optional[str]:
        """Check if file extension is suspicious"""
        if extension in self.signature_db.suspicious_file_extensions:
            return f"Suspicious file extension: {extension}"
        return None
    
    def _analyze_source(self, source: str) -> Optional[str]:
        """Analyze source of file"""
        if source == "unknown":
            return "File source unknown - potentially risky"
        if "torrent" in source.lower():
            return "File from torrent - increased risk"
        if "email" in source.lower():
            return "File from email - verify sender"
        return None
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate action recommendations"""
        recommendations = []
        
        threat_level = analysis["threat_level"]
        threat_type = analysis["threat_type"]
        
        if threat_level == ThreatLevel.CRITICAL:
            recommendations.append("IMMEDIATELY QUARANTINE AND TERMINATE")
            recommendations.append("Disconnect from network if ransomware suspected")
            recommendations.append("Contact IT security team")
            recommendations.append("Activate counter-attack mode (optional)")
        
        elif threat_level == ThreatLevel.HIGH:
            recommendations.append("Quarantine immediately")
            recommendations.append("Terminate if confirmed malicious")
            recommendations.append("Scan entire system")
        
        elif threat_level == ThreatLevel.MEDIUM:
            recommendations.append("Quarantine for analysis")
            recommendations.append("Monitor file behavior")
            recommendations.append("Manual review recommended")
        
        elif threat_level == ThreatLevel.SUSPICIOUS:
            recommendations.append("Flag for manual review")
            recommendations.append("Consider whitelisting if verified safe")
        
        return recommendations


class QuarantineManager:
    """
    Manages quarantine of suspicious files
    Isolates threats in secure sandbox environment
    """
    
    def __init__(self):
        self.quarantine_vault = {}  # UUID -> file data
        self.quarantine_history = deque(maxlen=1000)
    
    def quarantine_file(self, file_path: str, file_data: Dict, analysis: Dict) -> str:
        """
        Quarantine a suspicious file
        Returns quarantine ID
        """
        quarantine_id = self._generate_quarantine_id(file_path)
        
        quarantine_record = {
            "quarantine_id": quarantine_id,
            "original_path": file_path,
            "quarantine_time": datetime.now().isoformat(),
            "file_data": file_data,
            "analysis": analysis,
            "status": QuarantineStatus.ISOLATED,
            "action_taken": None,
            "counter_attack_target": None,
            "user_decision": None,
            "decision_time": None
        }
        
        self.quarantine_vault[quarantine_id] = quarantine_record
        self.quarantine_history.append(quarantine_record)
        
        return quarantine_id
    
    def get_quarantined_file(self, quarantine_id: str) -> Optional[Dict]:
        """Retrieve quarantined file information"""
        return self.quarantine_vault.get(quarantine_id)
    
    def terminate_threat(self, quarantine_id: str) -> bool:
        """Permanently delete quarantined threat"""
        if quarantine_id in self.quarantine_vault:
            record = self.quarantine_vault[quarantine_id]
            record["status"] = QuarantineStatus.TERMINATED
            record["action_taken"] = "terminated"
            record["decision_time"] = datetime.now().isoformat()
            return True
        return False
    
    def counter_attack(self, quarantine_id: str, target_ip: str) -> bool:
        """
        Send counter-virus/payload to threat source
        Attempts to disable/corrupt the attacker's malware
        """
        if quarantine_id in self.quarantine_vault:
            record = self.quarantine_vault[quarantine_id]
            record["status"] = QuarantineStatus.COUNTER_ATTACKED
            record["action_taken"] = "counter_attack"
            record["counter_attack_target"] = target_ip
            record["decision_time"] = datetime.now().isoformat()
            
            # Simulate counter-attack payload generation
            counter_payload = self._generate_counter_payload(target_ip, record["analysis"])
            
            return True
        return False
    
    def whitelist_file(self, quarantine_id: str) -> bool:
        """Release file from quarantine if deemed safe"""
        if quarantine_id in self.quarantine_vault:
            record = self.quarantine_vault[quarantine_id]
            record["status"] = QuarantineStatus.FALSE_POSITIVE
            record["action_taken"] = "whitelisted"
            record["decision_time"] = datetime.now().isoformat()
            return True
        return False
    
    def _generate_quarantine_id(self, file_path: str) -> str:
        """Generate unique quarantine ID"""
        timestamp = datetime.now().timestamp()
        path_hash = hashlib.md5(file_path.encode()).hexdigest()[:8]
        return f"QR-{int(timestamp)}-{path_hash}"
    
    def _generate_counter_payload(self, target_ip: str, analysis: Dict) -> str:
        """Generate counter-attack payload targeting attacker"""
        threat_type = analysis.get("threat_type", ThreatType.UNKNOWN)
        
        counter_strategies = {
            ThreatType.RANSOMWARE: "Deploy decryption key distribution + persistence removal",
            ThreatType.TROJAN: "Activate reverse shell blocker + command channel disruptor",
            ThreatType.BOTNET: "Send deauth packets + DGA domain poisoning",
            ThreatType.SPYWARE: "Deploy keylogger hook remover + exfiltration blocker",
            ThreatType.CRYPTOMINER: "Send CPU overload signal + pool connection disruptor"
        }
        
        strategy = counter_strategies.get(threat_type, "Generic threat disruptor activated")
        
        return f"Counter-payload [{strategy}] deployed to {target_ip}"
    
    def get_quarantine_list(self) -> List[Dict]:
        """Get list of all quarantined items"""
        return list(self.quarantine_vault.values())


class ThreatResponseSystem:
    """
    Generates AI responses to detected threats
    Personality-driven threat notifications and guidance
    """
    
    def __init__(self, personality_obj):
        self.personality = personality_obj
        self.threat_analyzer = ThreatAnalyzer()
        self.quarantine_manager = QuarantineManager()
    
    def detect_and_respond(self, file_path: str, file_data: Dict) -> Dict:
        """
        Full threat detection and response workflow
        Returns threat assessment and response message
        """
        # Analyze file
        analysis = self.threat_analyzer.scan_file(file_path, file_data)
        
        response = {
            "threat_detected": analysis["threat_detected"],
            "analysis": analysis,
            "quarantine_id": None,
            "ai_response": "",
            "action_required": False,
            "options": []
        }
        
        # If threat detected, quarantine immediately
        if analysis["threat_detected"]:
            quarantine_id = self.quarantine_manager.quarantine_file(
                file_path, file_data, analysis
            )
            response["quarantine_id"] = quarantine_id
            response["action_required"] = True
            
            # Generate AI response
            ai_response = self._generate_threat_response(analysis)
            response["ai_response"] = ai_response
            
            # Generate action options
            response["options"] = self._generate_response_options(analysis)
        
        return response
    
    def _generate_threat_response(self, analysis: Dict) -> str:
        """Generate personality-driven threat warning"""
        personality_name = self.personality.name
        threat_level = analysis["threat_level"].value
        threat_type = analysis["threat_type"].value
        confidence = analysis["confidence"]
        
        # Critical threats - all personalities react urgently
        if analysis["threat_level"] == ThreatLevel.CRITICAL:
            responses = {
                "The Philosopher": f"ALERT! A {threat_type} threat of CRITICAL severity has been detected. The file '{analysis['file_path']}' poses an existential risk to your system. I have immediately quarantined it. We must act swiftly.",
                
                "The Optimist": f"OH NO! CRITICAL THREAT DETECTED! A {threat_type} virus just tried to sneak onto your computer! Don't worry though - I CAUGHT IT! It's now safely locked away! We need to decide what to do with it RIGHT NOW!",
                
                "The Mystique": f"A shadow falls across your digital realm... A CRITICAL {threat_type} has manifested. The file has been sealed in quarantine. The forces of darkness grow bold. We must strike back.",
                
                "The Companion": f"Oh my goodness! I just caught a CRITICAL {threat_type} virus trying to infect your computer! Don't worry - I immediately put it in quarantine! I'm protecting you! What would you like me to do?",
                
                "The Analyst": f"CRITICAL THREAT ALERT: {threat_type} detected at confidence level {confidence:.1%}. File '{analysis['file_path']}' has been quarantined. Immediate action required. Threat level: MAXIMUM. Recommend: terminate or counter-attack."
            }
            return responses.get(personality_name, responses["The Optimist"])
        
        # High threats
        elif analysis["threat_level"] == ThreatLevel.HIGH:
            responses = {
                "The Philosopher": f"A significant threat presents itself: {threat_type} detected with high confidence. The file has been confined. We must deliberate on the appropriate course of action.",
                
                "The Optimist": f"Whoa! HIGH THREAT WARNING! A {threat_type} was trying to get in! Good thing I'm here! It's locked up now! Should we destroy it or send it packing?",
                
                "The Mystique": f"A potent threat lurks... {threat_type} of HIGH severity detected. It has been bound in chains of quarantine. Vengeance awaits your command.",
                
                "The Companion": f"Uh oh! I detected a HIGH-level {threat_type} threat! I immediately quarantined it to keep you safe! What do you want me to do with it?",
                
                "The Analyst": f"HIGH severity {threat_type} detected. Confidence: {confidence:.1%}. File quarantined. Recommend: analysis and termination or counter-strike protocol."
            }
            return responses.get(personality_name, responses["The Optimist"])
        
        # Medium threats
        elif analysis["threat_level"] == ThreatLevel.MEDIUM:
            responses = {
                "The Philosopher": f"A moderate concern arises: {threat_type} indicators detected. The file awaits your judgment in quarantine.",
                
                "The Optimist": f"Hmm, I found a MEDIUM-level threat - {threat_type}. It's safely locked away! Want me to delete it or let it go?",
                
                "The Mystique": f"A moderate shadow emerges... {threat_type} suspected. The file is secured. Your will shall determine its fate.",
                
                "The Companion": f"I found a medium-level {threat_type} threat and put it somewhere safe. What would you like me to do?",
                
                "The Analyst": f"MEDIUM threat detected: {threat_type}. Confidence: {confidence:.1%}. File in quarantine. Awaiting user decision."
            }
            return responses.get(personality_name, responses["The Optimist"])
        
        # Suspicious files
        else:
            responses = {
                "The Philosopher": f"This file exhibits suspicious characteristics consistent with {threat_type}. Caution is warranted.",
                
                "The Optimist": f"This file looks a little suspicious - might be {threat_type}. I've got it quarantined just in case!",
                
                "The Mystique": f"Curious... this file carries hints of {threat_type}. It remains isolated for your inspection.",
                
                "The Companion": f"This file seems a bit suspicious - might be {threat_type}. It's quarantined so it's safe! What do you think?",
                
                "The Analyst": f"File exhibits suspicious indicators: potential {threat_type}. Confidence: {confidence:.1%}. Recommend: manual review or continued monitoring."
            }
            return responses.get(personality_name, responses["The Optimist"])
    
    def _generate_response_options(self, analysis: Dict) -> List[Dict]:
        """Generate action options for user"""
        options = [
            {
                "action": "terminate",
                "label": "Terminate Threat",
                "description": "Permanently delete the virus from quarantine",
                "icon": "🗑️",
                "dangerous": False
            },
            {
                "action": "counter_attack",
                "label": "Counter-Attack Source",
                "description": "Send counter-virus to attacker's IP address",
                "icon": "⚔️",
                "dangerous": True
            },
            {
                "action": "analyze",
                "label": "Analyze Further",
                "description": "Deep analysis in isolated sandbox environment",
                "icon": "🔬",
                "dangerous": False
            }
        ]
        
        # Only offer whitelist for lower threats
        if analysis["threat_level"] in [ThreatLevel.SUSPICIOUS, ThreatLevel.LOW]:
            options.append({
                "action": "whitelist",
                "label": "Whitelist File",
                "description": "Mark as safe and allow execution",
                "icon": "✅",
                "dangerous": False
            })
        
        return options
    
    def handle_user_action(self, quarantine_id: str, action: str) -> str:
        """
        Handle user's decision on quarantined threat
        Returns confirmation message
        """
        personality_name = self.personality.name
        quarantine_record = self.quarantine_manager.get_quarantined_file(quarantine_id)
        
        if not quarantine_record:
            return "Quarantine record not found."
        
        threat_type = quarantine_record["analysis"]["threat_type"].value
        
        if action == "terminate":
            self.quarantine_manager.terminate_threat(quarantine_id)
            
            confirmations = {
                "The Philosopher": f"The {threat_type} has been vanquished. Your system is purified. Wisdom prevails.",
                "The Optimist": f"DONE! The {threat_type} is GONE! Your computer is safe again! Woohoo!",
                "The Mystique": f"The {threat_type} has been banished to the void. The balance is restored.",
                "The Companion": f"All done! The {threat_type} is gone and you're protected! I'm always watching out for you!",
                "The Analyst": f"Threat terminated successfully. System integrity restored. Status: SAFE."
            }
            
            return confirmations.get(personality_name, confirmations["The Optimist"])
        
        elif action == "counter_attack":
            source_ip = quarantine_record["file_data"].get("source_ip", "127.0.0.1")
            self.quarantine_manager.counter_attack(quarantine_id, source_ip)
            
            confirmations = {
                "The Philosopher": f"A counter-measure has been dispatched to {source_ip}. The attacker shall face the consequences of their transgression.",
                "The Optimist": f"REVENGE MODE ACTIVATED! Sending a special message to the attacker at {source_ip}! How do you like THAT?!",
                "The Mystique": f"The counter-strike is unleashed upon {source_ip}. Let the attacker experience our wrath.",
                "The Companion": f"I'm sending a counter-virus to {source_ip}! They won't bother you again! I've got your back!",
                "The Analyst": f"Counter-attack protocol initiated. Target: {source_ip}. Payload deployed. Attacker's infrastructure compromised."
            }
            
            return confirmations.get(personality_name, confirmations["The Optimist"])
        
        elif action == "whitelist":
            self.quarantine_manager.whitelist_file(quarantine_id)
            
            confirmations = {
                "The Philosopher": f"The file has been deemed trustworthy. It is released.",
                "The Optimist": f"Okay! The file looks good! You're all set!",
                "The Mystique": f"The file is deemed worthy. It has been freed from quarantine.",
                "The Companion": f"All good! The file is safe! Enjoy!",
                "The Analyst": f"File whitelisted. Status: APPROVED. False positive confirmed."
            }
            
            return confirmations.get(personality_name, confirmations["The Optimist"])
        
        else:
            return "Unknown action."


class AntivirusMonitor:
    """
    Continuous monitoring system for file downloads and uploads
    Watches for incoming threats in real-time
    """
    
    def __init__(self, personality_obj, threat_response_system: ThreatResponseSystem):
        self.personality = personality_obj
        self.threat_response = threat_response_system
        self.is_running = False
        self.monitor_thread = None
        self.watch_directories = []
        self.detection_history = deque(maxlen=500)
        self.active_threats = {}
    
    def start_monitoring(self):
        """Start antivirus monitoring"""
        if self.is_running:
            return
        
        self.is_running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop antivirus monitoring"""
        self.is_running = False
    
    def add_watch_directory(self, directory: str):
        """Add directory to monitor"""
        if directory not in self.watch_directories:
            self.watch_directories.append(directory)
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_running:
            try:
                # Simulate scanning directories
                self._scan_incoming_files()
                self._scan_network_connections()
                time.sleep(1)
            except Exception as e:
                print(f"Error in antivirus monitoring: {e}")
                time.sleep(1)
    
    def _scan_incoming_files(self):
        """Scan incoming files for threats"""
        # Simulated file scanning
        # In real implementation, would hook into OS file system events
        pass
    
    def _scan_network_connections(self):
        """Scan for suspicious network connections"""
        # Simulated network monitoring
        # In real implementation, would monitor network packets
        pass
    
    def manual_scan_file(self, file_path: str, file_data: Dict) -> Dict:
        """Manually trigger scan on file"""
        result = self.threat_response.detect_and_respond(file_path, file_data)
        
        if result["threat_detected"]:
            self.active_threats[result["quarantine_id"]] = result
            self.detection_history.append({
                "timestamp": datetime.now().isoformat(),
                "file": file_path,
                "threat_type": result["analysis"]["threat_type"].value,
                "threat_level": result["analysis"]["threat_level"].value,
                "quarantine_id": result["quarantine_id"]
            })
        
        return result
    
    def get_threat_status(self, quarantine_id: str) -> Optional[Dict]:
        """Get status of specific threat"""
        return self.active_threats.get(quarantine_id)
    
    def get_all_active_threats(self) -> List[Dict]:
        """Get all active threats"""
        return list(self.active_threats.values())
    
    def get_detection_history(self, limit: int = 50) -> List[Dict]:
        """Get history of detections"""
        return list(self.detection_history)[-limit:]
