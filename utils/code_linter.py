"""
Code Linter for Lisp Design Code
Real-time error detection and quality analysis
"""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class LintIssue:
    """Represents a linting issue"""
    line: int
    column: int
    severity: str  # 'error', 'warning', 'info'
    message: str
    suggestion: str = ""
    code: str = ""  # Error code like 'E001'

class CodeLinter:
    """Lints Lisp code for errors and best practices"""
    
    def __init__(self):
        """Initialize linter with rules"""
        self.rules = {
            'parentheses': True,
            'undefined_vars': True,
            'unused_vars': True,
            'performance': True,
            'style': True,
            'best_practices': True
        }
    
    def lint(self, code: str) -> Dict:
        """
        Lint code and return issues
        
        Args:
            code: Lisp code to lint
            
        Returns:
            Dictionary with issues, score, and summary
        """
        issues = []
        lines = code.split('\n')
        
        # Run all checks
        issues.extend(self._check_parentheses(lines))
        issues.extend(self._check_variables(code, lines))
        issues.extend(self._check_performance(lines))
        issues.extend(self._check_style(lines))
        issues.extend(self._check_best_practices(code, lines))
        
        # Calculate score
        score = self._calculate_score(issues)
        
        # Generate summary
        error_count = len([i for i in issues if i.severity == 'error'])
        warning_count = len([i for i in issues if i.severity == 'warning'])
        info_count = len([i for i in issues if i.severity == 'info'])
        
        summary = f"{error_count} errors, {warning_count} warnings, {info_count} info - Score: {score}/100"
        
        return {
            'issues': issues,
            'score': score,
            'summary': summary,
            'error_count': error_count,
            'warning_count': warning_count,
            'info_count': info_count
        }
    
    def _check_parentheses(self, lines: List[str]) -> List[LintIssue]:
        """Check for parentheses balance"""
        issues = []
        
        for line_num, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith(';'):
                continue
            
            # Count parentheses
            open_count = line.count('(')
            close_count = line.count(')')
            
            if open_count != close_count:
                issues.append(LintIssue(
                    line=line_num,
                    column=0,
                    severity='error',
                    message=f'Parentheses mismatch: {open_count} open, {close_count} close',
                    suggestion='Check that all parentheses are balanced',
                    code='E001'
                ))
        
        return issues
    
    def _check_variables(self, code: str, lines: List[str]) -> List[LintIssue]:
        """Check for undefined and unused variables"""
        issues = []
        
        # Find all variable definitions
        defined_vars = set()
        var_def_lines = {}
        
        for line_num, line in enumerate(lines, 1):
            if '(def ' in line:
                match = re.search(r'\(def\s+(\w+)', line)
                if match:
                    var_name = match.group(1)
                    defined_vars.add(var_name)
                    var_def_lines[var_name] = line_num
        
        # Find all variable usages
        used_vars = set()
        for line in lines:
            # Skip def lines
            if '(def ' in line:
                continue
            
            # Find variable references
            for var in defined_vars:
                if re.search(r'\b' + re.escape(var) + r'\b', line):
                    used_vars.add(var)
        
        # Check for unused variables
        unused = defined_vars - used_vars
        for var in unused:
            issues.append(LintIssue(
                line=var_def_lines[var],
                column=0,
                severity='warning',
                message=f'Variable "{var}" is defined but never used',
                suggestion='Remove unused variables or use them in your design',
                code='W001'
            ))
        
        # Check for undefined variables (simple heuristic)
        # This is tricky without full parsing, so we'll be conservative
        
        return issues
    
    def _check_performance(self, lines: List[str]) -> List[LintIssue]:
        """Check for performance issues"""
        issues = []
        
        for line_num, line in enumerate(lines, 1):
            # Check for excessive repeat counts
            if '(repeat' in line:
                match = re.search(r'\(repeat\s+(\d+)', line)
                if match:
                    count = int(match.group(1))
                    if count > 1000:
                        issues.append(LintIssue(
                            line=line_num,
                            column=0,
                            severity='warning',
                            message=f'High repeat count ({count}) may cause performance issues',
                            suggestion='Consider reducing repeat count or optimizing the loop',
                            code='W002'
                        ))
                    elif count > 10000:
                        issues.append(LintIssue(
                            line=line_num,
                            column=0,
                            severity='error',
                            message=f'Excessive repeat count ({count}) will cause severe performance issues',
                            suggestion='Reduce repeat count to under 1000',
                            code='E002'
                        ))
        
        return issues
    
    def _check_style(self, lines: List[str]) -> List[LintIssue]:
        """Check for style issues"""
        issues = []
        
        for line_num, line in enumerate(lines, 1):
            # Skip empty lines and comments
            if not line.strip() or line.strip().startswith(';'):
                continue
            
            # Check line length
            if len(line) > 100:
                issues.append(LintIssue(
                    line=line_num,
                    column=100,
                    severity='info',
                    message='Line is very long (hard to read)',
                    suggestion='Consider breaking into multiple lines',
                    code='I001'
                ))
            
            # Check for inconsistent spacing
            if '  (' in line or ')  ' in line:
                issues.append(LintIssue(
                    line=line_num,
                    column=0,
                    severity='info',
                    message='Inconsistent spacing detected',
                    suggestion='Use consistent spacing around parentheses',
                    code='I002'
                ))
        
        return issues
    
    def _check_best_practices(self, code: str, lines: List[str]) -> List[LintIssue]:
        """Check for best practice violations"""
        issues = []
        
        # Check for missing background
        if '(background' not in code:
            issues.append(LintIssue(
                line=1,
                column=0,
                severity='info',
                message='No background color defined',
                suggestion='Add (background #color) for better visualization',
                code='I003'
            ))
        
        # Check for magic numbers
        for line_num, line in enumerate(lines, 1):
            # Skip def lines and comments
            if '(def ' in line or line.strip().startswith(';'):
                continue
            
            # Find large numbers that should probably be variables
            numbers = re.findall(r'\b(\d{3,})\b', line)
            if numbers:
                issues.append(LintIssue(
                    line=line_num,
                    column=0,
                    severity='info',
                    message=f'Consider using variables instead of magic numbers: {", ".join(numbers)}',
                    suggestion='Define dimensions as variables with (def) for better maintainability',
                    code='I004'
                ))
        
        # Check for lack of comments
        comment_lines = len([l for l in lines if l.strip().startswith(';')])
        code_lines = len([l for l in lines if l.strip() and not l.strip().startswith(';')])
        
        if code_lines > 10 and comment_lines == 0:
            issues.append(LintIssue(
                line=1,
                column=0,
                severity='info',
                message='No comments found in code',
                suggestion='Add comments to explain your design logic',
                code='I005'
            ))
        
        return issues
    
    def _calculate_score(self, issues: List[LintIssue]) -> int:
        """Calculate code quality score"""
        score = 100
        
        for issue in issues:
            if issue.severity == 'error':
                score -= 10
            elif issue.severity == 'warning':
                score -= 3
            elif issue.severity == 'info':
                score -= 1
        
        return max(0, score)
    
    def get_suggestions(self, code: str) -> List[str]:
        """Get improvement suggestions"""
        suggestions = []
        
        # Check for common improvements
        if code.count('(def ') < 3:
            suggestions.append("💡 Add more variables for parametric design flexibility")
        
        if '(repeat' not in code:
            suggestions.append("💡 Use (repeat) for creating patterns and arrays")
        
        if '(text' not in code or code.count('(text') < 2:
            suggestions.append("💡 Add labels and dimensions for clarity")
        
        if '(fill' not in code or code.count('(fill') < 2:
            suggestions.append("💡 Use different colors to distinguish elements")
        
        if '(background' not in code:
            suggestions.append("💡 Add (background #color) for better visualization")
        
        # Check for reinforcement in structural elements
        if any(word in code.lower() for word in ['column', 'beam', 'lintel']) and 'circle' not in code:
            suggestions.append("💡 Add reinforcement bars with (circle) commands")
        
        # Check for dimensions
        if 'text' not in code.lower():
            suggestions.append("💡 Add dimension labels with (text) for professional drawings")
        
        return suggestions
    
    def format_issue(self, issue: LintIssue) -> str:
        """Format issue for display"""
        severity_icons = {
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        }
        
        icon = severity_icons.get(issue.severity, '•')
        return f"{icon} Line {issue.line}: {issue.message}"
    
    def get_quick_fixes(self, code: str, issue: LintIssue) -> List[str]:
        """Get quick fix suggestions for an issue"""
        fixes = []
        
        if issue.code == 'E001':  # Parentheses mismatch
            fixes.append("Add missing closing parenthesis")
            fixes.append("Remove extra opening parenthesis")
        
        elif issue.code == 'W001':  # Unused variable
            fixes.append(f"Remove variable definition")
            fixes.append(f"Use variable in your design")
        
        elif issue.code == 'W002':  # High repeat count
            fixes.append("Reduce repeat count")
            fixes.append("Optimize loop body")
        
        elif issue.code == 'I003':  # Missing background
            fixes.append("Add (background #fff) at the start")
        
        return fixes


# Convenience function
def lint_code(code: str) -> Dict:
    """Quick function to lint code"""
    linter = CodeLinter()
    return linter.lint(code)
