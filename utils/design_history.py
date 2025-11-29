"""
Design History Manager
Tracks changes, enables undo/redo, version comparison
"""

import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import hashlib

class DesignHistory:
    """Manages design history with undo/redo and version tracking"""
    
    def __init__(self, db_path: str = "design_history.db"):
        """
        Initialize design history manager
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self.init_db()
        
        # In-memory undo/redo stacks for current session
        self.undo_stack = []
        self.redo_stack = []
        self.max_undo_levels = 50
    
    def init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # History table
        c.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                code TEXT NOT NULL,
                description TEXT,
                code_hash TEXT,
                variables TEXT,
                commands_count INTEGER
            )
        ''')
        
        # Create indexes for history table
        c.execute('''
            CREATE INDEX IF NOT EXISTS idx_project_id ON history(project_id)
        ''')
        
        c.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON history(timestamp)
        ''')
        
        # Projects table
        c.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                element_type TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                current_code TEXT,
                thumbnail TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_snapshot(self, project_id: str, code: str, 
                     description: str = "", metadata: Optional[Dict] = None) -> int:
        """
        Save design snapshot to history
        
        Args:
            project_id: Project identifier
            code: Current code
            description: Optional description of changes
            metadata: Optional metadata (variables, commands, etc.)
            
        Returns:
            Snapshot ID
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Calculate code hash for deduplication
        code_hash = hashlib.md5(code.encode()).hexdigest()
        
        # Extract metadata
        variables_json = json.dumps(metadata.get('variables', {})) if metadata else '{}'
        commands_count = metadata.get('commands_count', 0) if metadata else 0
        
        # Insert snapshot
        c.execute('''
            INSERT INTO history (project_id, timestamp, code, description, 
                               code_hash, variables, commands_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_id,
            datetime.now().isoformat(),
            code,
            description,
            code_hash,
            variables_json,
            commands_count
        ))
        
        snapshot_id = c.lastrowid
        
        # Update project
        c.execute('''
            INSERT OR REPLACE INTO projects (id, name, element_type, created_at, updated_at, current_code)
            VALUES (
                ?,
                COALESCE((SELECT name FROM projects WHERE id = ?), ?),
                COALESCE((SELECT element_type FROM projects WHERE id = ?), 'lintel'),
                COALESCE((SELECT created_at FROM projects WHERE id = ?), ?),
                ?,
                ?
            )
        ''', (
            project_id, project_id, f"Project {project_id}", 
            project_id, project_id, datetime.now().isoformat(),
            datetime.now().isoformat(), code
        ))
        
        conn.commit()
        conn.close()
        
        # Add to undo stack
        self.undo_stack.append({
            'snapshot_id': snapshot_id,
            'code': code,
            'description': description
        })
        
        # Limit undo stack size
        if len(self.undo_stack) > self.max_undo_levels:
            self.undo_stack.pop(0)
        
        # Clear redo stack on new change
        self.redo_stack.clear()
        
        return snapshot_id
    
    def get_history(self, project_id: str, limit: int = 20) -> List[Dict]:
        """
        Get design history for project
        
        Args:
            project_id: Project identifier
            limit: Maximum number of snapshots to return
            
        Returns:
            List of snapshots
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT id, timestamp, code, description, code_hash, 
                   variables, commands_count
            FROM history
            WHERE project_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (project_id, limit))
        
        history = []
        for row in c.fetchall():
            history.append({
                'id': row[0],
                'timestamp': row[1],
                'code': row[2],
                'description': row[3],
                'code_hash': row[4],
                'variables': json.loads(row[5]) if row[5] else {},
                'commands_count': row[6]
            })
        
        conn.close()
        return history
    
    def restore_snapshot(self, snapshot_id: int) -> Optional[str]:
        """
        Restore design from snapshot
        
        Args:
            snapshot_id: Snapshot ID to restore
            
        Returns:
            Code from snapshot, or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('SELECT code FROM history WHERE id = ?', (snapshot_id,))
        row = c.fetchone()
        conn.close()
        
        return row[0] if row else None
    
    def undo(self) -> Optional[Tuple[str, str]]:
        """
        Undo last change
        
        Returns:
            Tuple of (code, description) or None
        """
        if len(self.undo_stack) < 2:
            return None
        
        # Move current state to redo stack
        current = self.undo_stack.pop()
        self.redo_stack.append(current)
        
        # Get previous state
        previous = self.undo_stack[-1]
        
        return previous['code'], previous.get('description', 'Undo')
    
    def redo(self) -> Optional[Tuple[str, str]]:
        """
        Redo last undone change
        
        Returns:
            Tuple of (code, description) or None
        """
        if not self.redo_stack:
            return None
        
        # Move state back to undo stack
        state = self.redo_stack.pop()
        self.undo_stack.append(state)
        
        return state['code'], state.get('description', 'Redo')
    
    def can_undo(self) -> bool:
        """Check if undo is available"""
        return len(self.undo_stack) > 1
    
    def can_redo(self) -> bool:
        """Check if redo is available"""
        return len(self.redo_stack) > 0
    
    def compare_versions(self, snapshot_id1: int, snapshot_id2: int) -> Dict:
        """
        Compare two snapshots
        
        Args:
            snapshot_id1: First snapshot ID
            snapshot_id2: Second snapshot ID
            
        Returns:
            Comparison results
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('SELECT code, timestamp FROM history WHERE id IN (?, ?)', 
                 (snapshot_id1, snapshot_id2))
        rows = c.fetchall()
        conn.close()
        
        if len(rows) != 2:
            return {'error': 'Snapshots not found'}
        
        code1, time1 = rows[0]
        code2, time2 = rows[1]
        
        # Simple line-by-line comparison
        lines1 = code1.split('\n')
        lines2 = code2.split('\n')
        
        diff = {
            'snapshot1': {'id': snapshot_id1, 'timestamp': time1, 'lines': len(lines1)},
            'snapshot2': {'id': snapshot_id2, 'timestamp': time2, 'lines': len(lines2)},
            'added_lines': len(lines2) - len(lines1),
            'changed': code1 != code2
        }
        
        return diff
    
    def get_project_stats(self, project_id: str) -> Dict:
        """
        Get statistics for project
        
        Args:
            project_id: Project identifier
            
        Returns:
            Project statistics
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Get snapshot count
        c.execute('SELECT COUNT(*) FROM history WHERE project_id = ?', (project_id,))
        snapshot_count = c.fetchone()[0]
        
        # Get first and last timestamps
        c.execute('''
            SELECT MIN(timestamp), MAX(timestamp)
            FROM history
            WHERE project_id = ?
        ''', (project_id,))
        first_time, last_time = c.fetchone()
        
        # Get project info
        c.execute('SELECT name, element_type FROM projects WHERE id = ?', (project_id,))
        row = c.fetchone()
        
        conn.close()
        
        return {
            'project_id': project_id,
            'name': row[0] if row else 'Unknown',
            'element_type': row[1] if row else 'Unknown',
            'snapshot_count': snapshot_count,
            'first_edit': first_time,
            'last_edit': last_time,
            'can_undo': self.can_undo(),
            'can_redo': self.can_redo()
        }
    
    def list_projects(self) -> List[Dict]:
        """
        List all projects
        
        Returns:
            List of projects
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT id, name, element_type, created_at, updated_at
            FROM projects
            ORDER BY updated_at DESC
        ''')
        
        projects = []
        for row in c.fetchall():
            projects.append({
                'id': row[0],
                'name': row[1],
                'element_type': row[2],
                'created_at': row[3],
                'updated_at': row[4]
            })
        
        conn.close()
        return projects
    
    def delete_project(self, project_id: str) -> bool:
        """
        Delete project and its history
        
        Args:
            project_id: Project identifier
            
        Returns:
            True if deleted successfully
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('DELETE FROM history WHERE project_id = ?', (project_id,))
        c.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        
        conn.commit()
        deleted = c.rowcount > 0
        conn.close()
        
        return deleted
    
    def cleanup_old_snapshots(self, days: int = 30, keep_count: int = 10):
        """
        Clean up old snapshots, keeping recent ones
        
        Args:
            days: Delete snapshots older than this many days
            keep_count: Always keep at least this many snapshots per project
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        cutoff_iso = datetime.fromtimestamp(cutoff_date).isoformat()
        
        # Delete old snapshots, but keep recent ones
        c.execute('''
            DELETE FROM history
            WHERE id NOT IN (
                SELECT id FROM history h1
                WHERE (
                    SELECT COUNT(*)
                    FROM history h2
                    WHERE h2.project_id = h1.project_id
                    AND h2.timestamp >= h1.timestamp
                ) <= ?
            )
            AND timestamp < ?
        ''', (keep_count, cutoff_iso))
        
        deleted = c.rowcount
        conn.commit()
        conn.close()
        
        return deleted


# Convenience functions
def create_history_manager(db_path: str = "design_history.db") -> DesignHistory:
    """Create and return a history manager instance"""
    return DesignHistory(db_path)
