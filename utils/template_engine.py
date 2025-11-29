"""
Template Engine for Structural Design
Manages templates, variables, and code generation
"""

import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path
import hashlib
import re

class Template:
    """Represents a design template"""
    
    def __init__(self, template_id: str, name: str, code: str, 
                 element_type: str, category: str = "general",
                 description: str = "", tags: List[str] = None,
                 variables: Dict[str, Any] = None, author: str = "system",
                 is_public: bool = True, rating: float = 0.0):
        """
        Initialize template
        
        Args:
            template_id: Unique template identifier
            name: Template name
            code: Lisp code template
            element_type: Type of element (lintel, sunshade, etc.)
            category: Template category
            description: Template description
            tags: List of tags for searching
            variables: Template variables with defaults
            author: Template author
            is_public: Whether template is public
            rating: User rating (0-5)
        """
        self.id = template_id
        self.name = name
        self.code = code
        self.element_type = element_type
        self.category = category
        self.description = description
        self.tags = tags or []
        self.variables = variables or {}
        self.author = author
        self.is_public = is_public
        self.rating = rating
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.use_count = 0
    
    def to_dict(self) -> Dict:
        """Convert template to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'element_type': self.element_type,
            'category': self.category,
            'description': self.description,
            'tags': self.tags,
            'variables': self.variables,
            'author': self.author,
            'is_public': self.is_public,
            'rating': self.rating,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'use_count': self.use_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Template':
        """Create template from dictionary"""
        template = cls(
            template_id=data['id'],
            name=data['name'],
            code=data['code'],
            element_type=data['element_type'],
            category=data.get('category', 'general'),
            description=data.get('description', ''),
            tags=data.get('tags', []),
            variables=data.get('variables', {}),
            author=data.get('author', 'system'),
            is_public=data.get('is_public', True),
            rating=data.get('rating', 0.0)
        )
        template.created_at = data.get('created_at', template.created_at)
        template.updated_at = data.get('updated_at', template.updated_at)
        template.use_count = data.get('use_count', 0)
        return template
    
    def apply_variables(self, values: Dict[str, Any]) -> str:
        """
        Apply variable values to template code
        
        Args:
            values: Dictionary of variable values
            
        Returns:
            Code with variables substituted
        """
        code = self.code
        
        # Merge with defaults
        all_values = {**self.variables, **values}
        
        # Replace variables in code
        for var_name, var_value in all_values.items():
            # Replace {{variable}} patterns
            pattern = r'\{\{' + re.escape(var_name) + r'\}\}'
            code = re.sub(pattern, str(var_value), code)
        
        return code
    
    def get_variables(self) -> List[Dict]:
        """
        Get list of template variables with metadata
        
        Returns:
            List of variable definitions
        """
        variables = []
        
        for var_name, var_value in self.variables.items():
            var_type = type(var_value).__name__
            
            variables.append({
                'name': var_name,
                'default': var_value,
                'type': var_type,
                'required': True
            })
        
        return variables


class TemplateEngine:
    """Manages template storage, retrieval, and application"""
    
    def __init__(self, db_path: str = "templates.db"):
        """
        Initialize template engine
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Templates table
        c.execute('''
            CREATE TABLE IF NOT EXISTS templates (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                code TEXT NOT NULL,
                element_type TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                tags TEXT,
                variables TEXT,
                author TEXT,
                is_public BOOLEAN,
                rating REAL,
                created_at TEXT,
                updated_at TEXT,
                use_count INTEGER DEFAULT 0
            )
        ''')
        
        # Create indexes
        c.execute('''
            CREATE INDEX IF NOT EXISTS idx_element_type ON templates(element_type)
        ''')
        
        c.execute('''
            CREATE INDEX IF NOT EXISTS idx_category ON templates(category)
        ''')
        
        c.execute('''
            CREATE INDEX IF NOT EXISTS idx_author ON templates(author)
        ''')
        
        # User favorites table
        c.execute('''
            CREATE TABLE IF NOT EXISTS favorites (
                user_id TEXT NOT NULL,
                template_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (user_id, template_id),
                FOREIGN KEY (template_id) REFERENCES templates(id)
            )
        ''')
        
        # Template ratings table
        c.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                user_id TEXT NOT NULL,
                template_id TEXT NOT NULL,
                rating INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (user_id, template_id),
                FOREIGN KEY (template_id) REFERENCES templates(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_template(self, template: Template) -> str:
        """
        Save template to database
        
        Args:
            template: Template to save
            
        Returns:
            Template ID
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        template.updated_at = datetime.now().isoformat()
        
        c.execute('''
            INSERT OR REPLACE INTO templates 
            (id, name, code, element_type, category, description, tags, 
             variables, author, is_public, rating, created_at, updated_at, use_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            template.id,
            template.name,
            template.code,
            template.element_type,
            template.category,
            template.description,
            json.dumps(template.tags),
            json.dumps(template.variables),
            template.author,
            template.is_public,
            template.rating,
            template.created_at,
            template.updated_at,
            template.use_count
        ))
        
        conn.commit()
        conn.close()
        
        return template.id
    
    def get_template(self, template_id: str) -> Optional[Template]:
        """
        Get template by ID
        
        Args:
            template_id: Template identifier
            
        Returns:
            Template or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT id, name, code, element_type, category, description, tags,
                   variables, author, is_public, rating, created_at, updated_at, use_count
            FROM templates
            WHERE id = ?
        ''', (template_id,))
        
        row = c.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return self._row_to_template(row)
    
    def list_templates(self, element_type: Optional[str] = None,
                      category: Optional[str] = None,
                      author: Optional[str] = None,
                      tags: Optional[List[str]] = None,
                      public_only: bool = True,
                      limit: int = 50) -> List[Template]:
        """
        List templates with filters
        
        Args:
            element_type: Filter by element type
            category: Filter by category
            author: Filter by author
            tags: Filter by tags
            public_only: Only show public templates
            limit: Maximum number of templates
            
        Returns:
            List of templates
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        query = '''
            SELECT id, name, code, element_type, category, description, tags,
                   variables, author, is_public, rating, created_at, updated_at, use_count
            FROM templates
            WHERE 1=1
        '''
        params = []
        
        if element_type:
            query += ' AND element_type = ?'
            params.append(element_type)
        
        if category:
            query += ' AND category = ?'
            params.append(category)
        
        if author:
            query += ' AND author = ?'
            params.append(author)
        
        if public_only:
            query += ' AND is_public = 1'
        
        query += ' ORDER BY rating DESC, use_count DESC, created_at DESC LIMIT ?'
        params.append(limit)
        
        c.execute(query, params)
        rows = c.fetchall()
        conn.close()
        
        templates = [self._row_to_template(row) for row in rows]
        
        # Filter by tags if specified
        if tags:
            templates = [t for t in templates if any(tag in t.tags for tag in tags)]
        
        return templates
    
    def search_templates(self, query: str, element_type: Optional[str] = None,
                        limit: int = 20) -> List[Template]:
        """
        Search templates by name, description, or tags
        
        Args:
            query: Search query
            element_type: Filter by element type
            limit: Maximum number of results
            
        Returns:
            List of matching templates
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        search_query = '''
            SELECT id, name, code, element_type, category, description, tags,
                   variables, author, is_public, rating, created_at, updated_at, use_count
            FROM templates
            WHERE is_public = 1
            AND (name LIKE ? OR description LIKE ? OR tags LIKE ?)
        '''
        params = [f'%{query}%', f'%{query}%', f'%{query}%']
        
        if element_type:
            search_query += ' AND element_type = ?'
            params.append(element_type)
        
        search_query += ' ORDER BY rating DESC, use_count DESC LIMIT ?'
        params.append(limit)
        
        c.execute(search_query, params)
        rows = c.fetchall()
        conn.close()
        
        return [self._row_to_template(row) for row in rows]
    
    def delete_template(self, template_id: str) -> bool:
        """
        Delete template
        
        Args:
            template_id: Template identifier
            
        Returns:
            True if deleted successfully
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('DELETE FROM templates WHERE id = ?', (template_id,))
        c.execute('DELETE FROM favorites WHERE template_id = ?', (template_id,))
        c.execute('DELETE FROM ratings WHERE template_id = ?', (template_id,))
        
        deleted = c.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted
    
    def increment_use_count(self, template_id: str):
        """
        Increment template use count
        
        Args:
            template_id: Template identifier
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            UPDATE templates
            SET use_count = use_count + 1
            WHERE id = ?
        ''', (template_id,))
        
        conn.commit()
        conn.close()
    
    def add_favorite(self, user_id: str, template_id: str):
        """
        Add template to user favorites
        
        Args:
            user_id: User identifier
            template_id: Template identifier
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            INSERT OR IGNORE INTO favorites (user_id, template_id, created_at)
            VALUES (?, ?, ?)
        ''', (user_id, template_id, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def remove_favorite(self, user_id: str, template_id: str):
        """
        Remove template from user favorites
        
        Args:
            user_id: User identifier
            template_id: Template identifier
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            DELETE FROM favorites
            WHERE user_id = ? AND template_id = ?
        ''', (user_id, template_id))
        
        conn.commit()
        conn.close()
    
    def get_favorites(self, user_id: str) -> List[Template]:
        """
        Get user's favorite templates
        
        Args:
            user_id: User identifier
            
        Returns:
            List of favorite templates
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT t.id, t.name, t.code, t.element_type, t.category, t.description,
                   t.tags, t.variables, t.author, t.is_public, t.rating,
                   t.created_at, t.updated_at, t.use_count
            FROM templates t
            JOIN favorites f ON t.id = f.template_id
            WHERE f.user_id = ?
            ORDER BY f.created_at DESC
        ''', (user_id,))
        
        rows = c.fetchall()
        conn.close()
        
        return [self._row_to_template(row) for row in rows]
    
    def rate_template(self, user_id: str, template_id: str, rating: int):
        """
        Rate a template
        
        Args:
            user_id: User identifier
            template_id: Template identifier
            rating: Rating (1-5)
        """
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Save user rating
        c.execute('''
            INSERT OR REPLACE INTO ratings (user_id, template_id, rating, created_at)
            VALUES (?, ?, ?, ?)
        ''', (user_id, template_id, rating, datetime.now().isoformat()))
        
        # Update template average rating
        c.execute('''
            SELECT AVG(rating) FROM ratings WHERE template_id = ?
        ''', (template_id,))
        
        avg_rating = c.fetchone()[0]
        
        c.execute('''
            UPDATE templates SET rating = ? WHERE id = ?
        ''', (avg_rating, template_id))
        
        conn.commit()
        conn.close()
    
    def get_categories(self, element_type: Optional[str] = None) -> List[Dict]:
        """
        Get list of template categories
        
        Args:
            element_type: Filter by element type
            
        Returns:
            List of categories with counts
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        query = '''
            SELECT category, COUNT(*) as count
            FROM templates
            WHERE is_public = 1
        '''
        params = []
        
        if element_type:
            query += ' AND element_type = ?'
            params.append(element_type)
        
        query += ' GROUP BY category ORDER BY count DESC'
        
        c.execute(query, params)
        rows = c.fetchall()
        conn.close()
        
        return [{'category': row[0], 'count': row[1]} for row in rows]
    
    def get_popular_templates(self, element_type: Optional[str] = None,
                             limit: int = 10) -> List[Template]:
        """
        Get most popular templates
        
        Args:
            element_type: Filter by element type
            limit: Maximum number of templates
            
        Returns:
            List of popular templates
        """
        return self.list_templates(
            element_type=element_type,
            public_only=True,
            limit=limit
        )
    
    def create_template_from_code(self, name: str, code: str, element_type: str,
                                 category: str = "custom", description: str = "",
                                 author: str = "user") -> Template:
        """
        Create template from existing code
        
        Args:
            name: Template name
            code: Lisp code
            element_type: Element type
            category: Template category
            description: Template description
            author: Template author
            
        Returns:
            Created template
        """
        # Generate template ID
        template_id = self._generate_template_id(name, element_type)
        
        # Extract variables from code
        variables = self._extract_variables(code)
        
        # Create template
        template = Template(
            template_id=template_id,
            name=name,
            code=code,
            element_type=element_type,
            category=category,
            description=description,
            variables=variables,
            author=author,
            is_public=False  # User templates are private by default
        )
        
        # Save template
        self.save_template(template)
        
        return template
    
    def _row_to_template(self, row) -> Template:
        """Convert database row to Template object"""
        return Template.from_dict({
            'id': row[0],
            'name': row[1],
            'code': row[2],
            'element_type': row[3],
            'category': row[4],
            'description': row[5],
            'tags': json.loads(row[6]) if row[6] else [],
            'variables': json.loads(row[7]) if row[7] else {},
            'author': row[8],
            'is_public': bool(row[9]),
            'rating': row[10],
            'created_at': row[11],
            'updated_at': row[12],
            'use_count': row[13]
        })
    
    def _generate_template_id(self, name: str, element_type: str) -> str:
        """Generate unique template ID"""
        content = f"{name}_{element_type}_{datetime.now().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _extract_variables(self, code: str) -> Dict[str, Any]:
        """Extract variables from code"""
        variables = {}
        
        # Find (def variable value) patterns
        pattern = r'\(def\s+(\w+)\s+([^\)]+)\)'
        matches = re.findall(pattern, code)
        
        for var_name, var_value in matches:
            try:
                # Try to parse as number
                if '.' in var_value:
                    variables[var_name] = float(var_value)
                else:
                    variables[var_name] = int(var_value)
            except ValueError:
                # Keep as string
                variables[var_name] = var_value.strip('"\'')
        
        return variables


# Convenience functions
def get_template_engine() -> TemplateEngine:
    """Get singleton template engine"""
    if not hasattr(get_template_engine, '_instance'):
        get_template_engine._instance = TemplateEngine()
    return get_template_engine._instance
