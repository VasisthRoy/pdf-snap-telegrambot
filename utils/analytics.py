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
import calendar


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
    
    def get_daily_statistics(self) -> dict:
        """
        Get daily statistics including unique users, operations, top 3 users, and recent 10 users.
        
        Returns:
            dict: Daily statistics
        """
        if not self.enabled:
            return self._empty_daily_stats()
        
        try:
            conn = self._get_connection()
            if not conn:
                return self._empty_daily_stats()
            
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            today = datetime.now().date()
            
            # Today's unique users
            cursor.execute("""
                SELECT COUNT(DISTINCT user_id) as count
                FROM operations
                WHERE DATE(timestamp) = %s
            """, (today,))
            unique_users = cursor.fetchone()['count']
            
            # Today's total operations
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM operations
                WHERE DATE(timestamp) = %s
            """, (today,))
            total_operations = cursor.fetchone()['count']
            
            # Operations by type today
            cursor.execute("""
                SELECT operation_type, COUNT(*) as count
                FROM operations
                WHERE DATE(timestamp) = %s
                GROUP BY operation_type
            """, (today,))
            operations_by_type = {row['operation_type']: row['count'] for row in cursor.fetchall()}
            
            # Top 3 users today (by operation count)
            cursor.execute("""
                SELECT u.user_id, u.username, u.first_name, u.last_name, COUNT(o.id) as operations
                FROM users u
                JOIN operations o ON u.user_id = o.user_id
                WHERE DATE(o.timestamp) = %s
                GROUP BY u.user_id, u.username, u.first_name, u.last_name
                ORDER BY operations DESC
                LIMIT 3
            """, (today,))
            top_3_users = []
            for row in cursor.fetchall():
                top_3_users.append({
                    'id': row['user_id'],
                    'name': f"{row['first_name']} {row['last_name'] or ''}".strip(),
                    'username': row['username'],
                    'operations': row['operations']
                })
            
            # Recent 10 users (by last activity time today)
            cursor.execute("""
                SELECT DISTINCT ON (u.user_id) 
                    u.user_id, 
                    u.username, 
                    u.first_name, 
                    u.last_name, 
                    COUNT(o.id) as operations,
                    MAX(o.timestamp) as last_activity
                FROM users u
                JOIN operations o ON u.user_id = o.user_id
                WHERE DATE(o.timestamp) = %s
                GROUP BY u.user_id, u.username, u.first_name, u.last_name
                ORDER BY last_activity DESC
                LIMIT 10
            """, (today,))
            recent_10_users = []
            for row in cursor.fetchall():
                recent_10_users.append({
                    'id': row['user_id'],
                    'name': f"{row['first_name']} {row['last_name'] or ''}".strip(),
                    'username': row['username'],
                    'operations': row['operations'],
                    'last_active': row['last_activity'].strftime('%H:%M:%S')
                })
            
            cursor.close()
            conn.close()
            
            return {
                'date': today.strftime('%Y-%m-%d'),
                'unique_users': unique_users,
                'total_operations': total_operations,
                'operations_by_type': operations_by_type,
                'top_3_users': top_3_users,
                'recent_10_users': recent_10_users,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        
        except Exception as e:
            print(f"Error getting daily statistics: {e}")
            return self._empty_daily_stats()
    
    def get_weekly_statistics(self) -> dict:
        """
        Get weekly statistics for the current month, including week-by-week breakdown.
        
        Returns:
            dict: Weekly statistics
        """
        if not self.enabled:
            return self._empty_weekly_stats()
        
        try:
            conn = self._get_connection()
            if not conn:
                return self._empty_weekly_stats()
            
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            now = datetime.now()
            
            # Get first and last day of current month
            first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            last_day = now.replace(day=calendar.monthrange(now.year, now.month)[1], hour=23, minute=59, second=59)
            
            # Calculate weeks in the month
            weeks = []
            current_week_start = first_day
            week_number = 1
            
            while current_week_start <= last_day:
                # Calculate end of week (Sunday)
                days_until_sunday = (6 - current_week_start.weekday()) % 7
                current_week_end = current_week_start + timedelta(days=days_until_sunday, hours=23, minutes=59, seconds=59)
                
                # Don't go past end of month
                if current_week_end > last_day:
                    current_week_end = last_day
                
                # Get stats for this week
                cursor.execute("""
                    SELECT COUNT(DISTINCT user_id) as unique_users
                    FROM operations
                    WHERE timestamp >= %s AND timestamp <= %s
                """, (current_week_start, current_week_end))
                week_unique_users = cursor.fetchone()['unique_users']
                
                cursor.execute("""
                    SELECT COUNT(*) as total_operations
                    FROM operations
                    WHERE timestamp >= %s AND timestamp <= %s
                """, (current_week_start, current_week_end))
                week_total_operations = cursor.fetchone()['total_operations']
                
                # Operations by type for this week
                cursor.execute("""
                    SELECT operation_type, COUNT(*) as count
                    FROM operations
                    WHERE timestamp >= %s AND timestamp <= %s
                    GROUP BY operation_type
                    ORDER BY count DESC
                """, (current_week_start, current_week_end))
                week_operations_by_type = {row['operation_type']: row['count'] for row in cursor.fetchall()}
                
                # Top 3 users for this week
                cursor.execute("""
                    SELECT u.user_id, u.username, u.first_name, u.last_name, COUNT(o.id) as operations
                    FROM users u
                    JOIN operations o ON u.user_id = o.user_id
                    WHERE o.timestamp >= %s AND o.timestamp <= %s
                    GROUP BY u.user_id, u.username, u.first_name, u.last_name
                    ORDER BY operations DESC
                    LIMIT 3
                """, (current_week_start, current_week_end))
                week_top_3_users = []
                for row in cursor.fetchall():
                    week_top_3_users.append({
                        'id': row['user_id'],
                        'name': f"{row['first_name']} {row['last_name'] or ''}".strip(),
                        'username': row['username'],
                        'operations': row['operations']
                    })
                
                weeks.append({
                    'week_number': week_number,
                    'date_range': f"{current_week_start.strftime('%b %d')} - {current_week_end.strftime('%b %d')}",
                    'unique_users': week_unique_users,
                    'total_operations': week_total_operations,
                    'operations_by_type': week_operations_by_type,
                    'top_3_users': week_top_3_users
                })
                
                # Move to next week (start on Monday)
                current_week_start = current_week_end + timedelta(seconds=1)
                current_week_start = current_week_start.replace(hour=0, minute=0, second=0, microsecond=0)
                # Adjust to Monday
                days_since_monday = current_week_start.weekday()
                if days_since_monday != 0:
                    current_week_start += timedelta(days=(7 - days_since_monday))
                
                week_number += 1
            
            # Overall month statistics
            cursor.execute("""
                SELECT COUNT(DISTINCT user_id) as count
                FROM operations
                WHERE timestamp >= %s AND timestamp <= %s
            """, (first_day, last_day))
            total_unique_users = cursor.fetchone()['count']
            
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM operations
                WHERE timestamp >= %s AND timestamp <= %s
            """, (first_day, last_day))
            total_operations = cursor.fetchone()['count']
            
            # Overall top 3 users this month
            cursor.execute("""
                SELECT u.user_id, u.username, u.first_name, u.last_name, COUNT(o.id) as operations
                FROM users u
                JOIN operations o ON u.user_id = o.user_id
                WHERE o.timestamp >= %s AND o.timestamp <= %s
                GROUP BY u.user_id, u.username, u.first_name, u.last_name
                ORDER BY operations DESC
                LIMIT 3
            """, (first_day, last_day))
            overall_top_3 = []
            for row in cursor.fetchall():
                overall_top_3.append({
                    'id': row['user_id'],
                    'name': f"{row['first_name']} {row['last_name'] or ''}".strip(),
                    'username': row['username'],
                    'operations': row['operations']
                })
            
            # Total operations by type this month
            cursor.execute("""
                SELECT operation_type, COUNT(*) as count
                FROM operations
                WHERE timestamp >= %s AND timestamp <= %s
                GROUP BY operation_type
                ORDER BY count DESC
            """, (first_day, last_day))
            total_operations_by_type = {row['operation_type']: row['count'] for row in cursor.fetchall()}
            
            cursor.close()
            conn.close()
            
            return {
                'month_name': now.strftime('%B'),
                'year': now.year,
                'total_unique_users': total_unique_users,
                'total_operations': total_operations,
                'weeks': weeks,
                'overall_top_3': overall_top_3,
                'total_operations_by_type': total_operations_by_type,
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        
        except Exception as e:
            print(f"Error getting weekly statistics: {e}")
            return self._empty_weekly_stats()
    
    def _empty_daily_stats(self) -> dict:
        """Return empty daily statistics structure."""
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'unique_users': 0,
            'total_operations': 0,
            'operations_by_type': {},
            'top_3_users': [],
            'recent_10_users': [],
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _empty_weekly_stats(self) -> dict:
        """Return empty weekly statistics structure."""
        now = datetime.now()
        return {
            'month_name': now.strftime('%B'),
            'year': now.year,
            'total_unique_users': 0,
            'total_operations': 0,
            'weeks': [],
            'overall_top_3': [],
            'total_operations_by_type': {},
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