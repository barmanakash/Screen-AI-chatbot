from typing import Dict, Any

class SafetyController:
    def __init__(self):
        self.is_paused = False
        # Sensitive action keys that demand dynamic validation loops
        self.sensitive_actions = ["click_submit", "delete", "post_content", "save_sensitive"]

    def requires_confirmation(self, action_type: str, metadata: Dict[str, Any]) -> bool:
        if action_type in self.sensitive_actions:
            return True
        # Look for explicit "submit" identifiers inside interaction logs
        if action_type == "click" and "submit" in str(metadata.get("target", "")).lower():
            return True
        return False