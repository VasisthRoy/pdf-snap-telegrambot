"""
Analytics utilities for PDF Telegram Bot.
Tracks user activity and generates statistics.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from telegram import User


class Analytics:
    """Handles user activity tracking and statistics."""
    
    def __init__(self):
        """Initialize analytics with data file."""
        self.data_file = Path("/tmp/pdf_bot_analytics.json")
        self.data = self._load_data()
    
    def _load_data(self) -> dict:
        """Load analytics data from file."""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading analytics data: {e}")
        
        return {
            'users': {},  # user_id -> user data
            'daily_stats': {},  # date -> stats
            'operations': []  # list of operations
        }
    
    def _save_data(self) -> None:
        """Save analytics data to file."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Error saving analytics data: {e}")
    
    def track_user(self, user: User, operation: str) -> None:
        """
        Track user activity.
        
        Args:
            user: Telegram User object
            operation: Operation performed (merge, split, compress, etc.)
        """
        user_id = str(user.id)
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Update user data
        if user_id not in self.data['users']:
            self.data['users'][user_id] = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'first_seen': today,
                'last_seen': today,
                'total_operations': 0,
                'operations_by_type': {}
            }
        
        user_data = self.data['users'][user_id]
        user_data['last_seen'] = today
        user_data['total_operations'] += 1
        
        # Update username in case it changed
        user_data['username'] = user.username
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        
        # Track operation type
        if operation not in user_data['operations_by_type']:
            user_data['operations_by_type'][operation] = 0
        user_data['operations_by_type'][operation] += 1
        
        # Update daily stats
        if today not in self.data['daily_stats']:
            self.data['daily_stats'][today] = {
                'unique_users': set(),
                'total_operations': 0,
                'operations_by_type': {}
            }
        
        daily_stats = self.data['daily_stats'][today]
        
        # Convert set to list for JSON serialization, then back to set
        if isinstance(daily_stats['unique_users'], list):
            daily_stats['unique_users'] = set(daily_stats['unique_users'])
        
        daily_stats['unique_users'].add(user_id)
        daily_stats['total_operations'] += 1
        
        if operation not in daily_stats['operations_by_type']:
            daily_stats['operations_by_type'][operation] = 0
        daily_stats['operations_by_type'][operation] += 1
        
        # Convert set back to list for JSON serialization
        daily_stats['unique_users'] = list(daily_stats['unique_users'])
        
        # Save data
        self._save_data()
    
    def get_statistics(self) -> dict:
        """
        Get comprehensive statistics.
        
        Returns:
            dict: Statistics including today's users, all-time stats, etc.
        """
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Get today's stats
        today_stats = self.data['daily_stats'].get(today, {
            'unique_users': [],
            'total_operations': 0,
            'operations_by_type': {}
        })
        
        # Get today's users with details
        today_users = []
        for user_id in today_stats.get('unique_users', []):
            if user_id in self.data['users']:
                user_data = self.data['users'][user_id]
                today_users.append({
                    'id': user_data['id'],
                    'name': f"{user_data['first_name']} {user_data.get('last_name', '')}".strip(),
                    'username': user_data.get('username'),
                    'operations': user_data['total_operations']
                })
        
        # Sort today's users by operations
        today_users.sort(key=lambda x: x['operations'], reverse=True)
        
        # Get top users all-time
        top_users = []
        for user_id, user_data in self.data['users'].items():
            top_users.append({
                'id': user_data['id'],
                'name': f"{user_data['first_name']} {user_data.get('last_name', '')}".strip(),
                'username': user_data.get('username'),
                'operations': user_data['total_operations']
            })
        
        # Sort by total operations
        top_users.sort(key=lambda x: x['operations'], reverse=True)
        
        # Calculate total operations by type
        operations_by_type = {}
        for user_data in self.data['users'].values():
            for op_type, count in user_data.get('operations_by_type', {}).items():
                if op_type not in operations_by_type:
                    operations_by_type[op_type] = 0
                operations_by_type[op_type] += count
        
        return {
            'today_unique_users': len(today_stats.get('unique_users', [])),
            'today_operations': today_stats.get('total_operations', 0),
            'today_users': today_users,
            'total_unique_users': len(self.data['users']),
            'total_operations': sum(u['total_operations'] for u in self.data['users'].values()),
            'top_users': top_users,
            'operations_by_type': operations_by_type,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_user_info(self, user_id: int) -> Optional[dict]:
        """
        Get information about a specific user.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            dict: User information or None if not found
        """
        return self.data['users'].get(str(user_id))
    
    def cleanup_old_data(self, days: int = 30) -> None:
        """
        Clean up daily stats older than specified days.
        
        Args:
            days: Number of days to keep
        """
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Remove old daily stats
        dates_to_remove = [
            date for date in self.data['daily_stats'].keys()
            if date < cutoff_date
        ]
        
        for date in dates_to_remove:
            del self.data['daily_stats'][date]
        
        self._save_data()
        print(f"Cleaned up {len(dates_to_remove)} days of old analytics data")


# Global analytics instance
analytics = Analytics()