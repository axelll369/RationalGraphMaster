import json
import os
from datetime import datetime
from typing import List, Dict

class Database:
    def __init__(self, filename="leaderboard.json"):
        self.filename = filename
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create the JSON file if it doesn't exist"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)
    
    def save_score(self, player_name: str, score: int) -> None:
        """Save a player's score to the database"""
        try:
            # Load existing scores
            scores = self._load_scores()
            
            # Create new score entry
            new_score = {
                'player_name': player_name,
                'score': score,
                'date_played': datetime.now().isoformat()
            }
            
            # Add to scores
            scores.append(new_score)
            
            # Save back to file
            self._save_scores(scores)
            
        except Exception as e:
            print(f"Error saving score: {e}")
    
    def get_leaderboard(self, limit: int = 50) -> List[Dict]:
        """Get the leaderboard sorted by score (highest first)"""
        try:
            scores = self._load_scores()
            
            # Sort by score (descending) then by date (most recent first)
            sorted_scores = sorted(
                scores, 
                key=lambda x: (-x['score'], x['date_played']), 
                reverse=False
            )
            
            return sorted_scores[:limit]
            
        except Exception as e:
            print(f"Error loading leaderboard: {e}")
            return []
    
    def get_player_best_score(self, player_name: str) -> int:
        """Get a player's best score"""
        try:
            scores = self._load_scores()
            player_scores = [s['score'] for s in scores if s['player_name'] == player_name]
            return max(player_scores) if player_scores else 0
            
        except Exception as e:
            print(f"Error getting player best score: {e}")
            return 0
    
    def get_player_stats(self, player_name: str) -> Dict:
        """Get comprehensive stats for a player"""
        try:
            scores = self._load_scores()
            player_scores = [s for s in scores if s['player_name'] == player_name]
            
            if not player_scores:
                return {
                    'games_played': 0,
                    'best_score': 0,
                    'average_score': 0,
                    'total_score': 0
                }
            
            score_values = [s['score'] for s in player_scores]
            
            return {
                'games_played': len(player_scores),
                'best_score': max(score_values),
                'average_score': round(sum(score_values) / len(score_values), 1),
                'total_score': sum(score_values),
                'last_played': max(s['date_played'] for s in player_scores)
            }
            
        except Exception as e:
            print(f"Error getting player stats: {e}")
            return {}
    
    def _load_scores(self) -> List[Dict]:
        """Load scores from JSON file"""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading scores: {e}")
            return []
    
    def _save_scores(self, scores: List[Dict]) -> None:
        """Save scores to JSON file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(scores, f, indent=2)
        except Exception as e:
            print(f"Error saving scores: {e}")
    
    def clear_leaderboard(self) -> None:
        """Clear all scores (admin function)"""
        try:
            with open(self.filename, 'w') as f:
                json.dump([], f)
        except Exception as e:
            print(f"Error clearing leaderboard: {e}")
    
    def export_data(self, export_filename: str = None) -> str:
        """Export data to a new file for backup"""
        if export_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_filename = f"leaderboard_backup_{timestamp}.json"
        
        try:
            scores = self._load_scores()
            with open(export_filename, 'w') as f:
                json.dump(scores, f, indent=2)
            return export_filename
        except Exception as e:
            print(f"Error exporting data: {e}")
            return ""
