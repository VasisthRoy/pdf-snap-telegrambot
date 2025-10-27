"""
Analytics utilities for PDF Telegram Bot.
Tracks user activity and generates statistics using PostgreSQL.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from telegram import User


class Analytics:
    """Handles user activity tracking and statistics with PostgreSQL."""
    
    def __init__(self):
        """Initialize analytics with PostgreSQL connection."""
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            print("⚠️  WARNING: DATABASE_URL not found. Analytics will be disabled.")
            self.enabled = False
        else:
            self.enabled = True
            self._init_database()
    
    def _get_connection(self):
        """Get database connection."""
        if not self.enabled:
            return None
        try:
            return psycopg2.connect(self.database_url)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None
    
    def _init_database(self) -> None:
        """Initialize database tables if they don't exist."""
        if not self.enabled:
            return
        
        try:
            conn = self._get_connection()
            if not conn:
                return
            
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username VARCHAR(255),
                    first_name VARCHAR(255),
                    last_name VARCHAR(255),
                    first_seen DATE NOT NULL,
                    last_seen DATE NOT NULL,
                    total_operations INTEGER DEFAULT 0
                )
            """)
            
            # Create operations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS operations (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    operation_type VARCHAR(50) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """)
            
            # Create index for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_operations_timestamp 
                ON operations(timestamp)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_operations_user_id 
                ON operations(user_id)
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print("✅ Database tables initialized successfully")
        
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def track_user(self, user: User, operation: str) -> None:
        """
        Track user activity.
        
        Args:
            user: Telegram User object
            operation: Operation performed (merge, split, compress, etc.)
        """
        if not self.enabled:
            return
        
        try:
            conn = self._get_connection()
            if not conn:
                return
            
            cursor = conn.cursor()
            today = datetime.now().date()
            
            # Insert or update user
            cursor.execute("""
                INSERT INTO users (user_id, username, first_name, last_name, first_seen, last_seen, total_operations)
                VALUES (%s, %s, %s, %s, %s, %s, 1)
                ON CONFLICT (user_id) 
                DO UPDATE SET
                    username = EXCLUDED.username,
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    last_seen = EXCLUDED.last_seen,
                    total_operations = users.total_operations + 1
            """, (user.id, user.username, user.first_name, user.last_name, today, today))
            
            # Insert operation record
            cursor.execute("""
                INSERT INTO operations (user_id, operation_type)
                VALUES (%s, %s)
            """, (user.id, operation))
            
            conn.commit()
            cursor.close()
            conn.close()
        
        except Exception as e:
            print(f"Error tracking user: {e}")
    
    def get_statistics(self) -> dict:
        """
        Get comprehensive statistics.
        
        Returns:
            dict: Statistics including today's users, all-time stats, etc.
        """
        if not self.enabled:
            return self._empty_stats()
        
        try:
            conn = self._get_connection()
            if not conn:
                return self._empty_stats()
            
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            today = datetime.now().date()
            
            # Today's unique users
            cursor.execute("""
                SELECT COUNT(DISTINCT user_id) as count
                FROM operations
                WHERE DATE(timestamp) = %s
            """, (today,))
            today_unique_users = cursor.fetchone()['count']
            
            # Today's total operations
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM operations
                WHERE DATE(timestamp) = %s
            """, (today,))
            today_operations = cursor.fetchone()['count']
            
            # Today's users with details
            cursor.execute("""
                SELECT u.user_id, u.username, u.first_name, u.last_name, u.total_operations
                FROM users u
                WHERE u.last_seen = %s
                ORDER BY u.total_operations DESC
            """, (today,))
            today_users = []
            for row in cursor.fetchall():
                today_users.append({
                    'id': row['user_id'],
                    'name': f"{row['first_name']} {row['last_name'] or ''}".strip(),
                    'username': row['username'],
                    'operations': row['total_operations']
                })
            
            # Total unique users
            cursor.execute("SELECT COUNT(*) as count FROM users")
            total_unique_users = cursor.fetchone()['count']
            
            # Total operations
            cursor.execute("SELECT COUNT(*) as count FROM operations")
            total_operations = cursor.fetchone()['count']
            
            # Top users all-time
            cursor.execute("""
                SELECT user_id, username, first_name, last_name, total_operations
                FROM users
                ORDER BY total_operations DESC
                LIMIT 10
            """)
            top_users = []
            for row in cursor.fetchall():
                top_users.append({
                    'id': row['user_id'],
                    'name': f"{row['first_name']} {row['last_name'] or ''}".strip(),
                    'username': row['username'],
                    'operations': row['total_operations']
                })
            
            # Operations by type
            cursor.execute("""
                SELECT operation_type, COUNT(*) as count
                FROM operations
                GROUP BY operation_type
            """)
            operations_by_type = {row['operation_type']: row['count'] for row in cursor.fetchall()}
            
            cursor.close()
            conn.close()
            
            return {
                'today_unique_users': today_unique_users,
                'today_operations': today_operations,
                'today_users': today_users,
                'total_unique_users': total_unique_users,
                'total_operations': total_operations,
                'top_users': top_users,
                'operations_by_type': operations_by_type,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return self._empty_stats()
    
    def _empty_stats(self) -> dict:
        """Return empty statistics structure."""
        return {
            'today_unique_users': 0,
            'today_operations': 0,
            'today_users': [],
            'total_unique_users': 0,
            'total_operations': 0,
            'top_users': [],
            'operations_by_type': {},
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
        if not self.enabled:
            return None
        
        try:
            conn = self._get_connection()
            if not conn:
                return None
            
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT * FROM users WHERE user_id = %s
            """, (user_id,))
            
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return dict(result) if result else None
        
        except Exception as e:
            print(f"Error getting user info: {e}")
            return None
    
    def cleanup_old_data(self, days: int = 90) -> None:
        """
        Clean up operations older than specified days.
        
        Args:
            days: Number of days to keep
        """
        if not self.enabled:
            return
        
        try:
            conn = self._get_connection()
            if not conn:
                return
            
            cursor = conn.cursor()
            cutoff_date = datetime.now() - timedelta(days=days)
            
            cursor.execute("""
                DELETE FROM operations
                WHERE timestamp < %s
            """, (cutoff_date,))
            
            deleted_count = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"Cleaned up {deleted_count} old operation records")
        
        except Exception as e:
            print(f"Error cleaning up old data: {e}")


# Global analytics instance
analytics = Analytics()