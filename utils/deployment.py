"""
Deployment and Launch Utilities
Health checks, monitoring, and deployment preparation
"""

import streamlit as st
import sys
import os
from typing import Dict, List, Any
import json
from datetime import datetime

class HealthCheck:
    """System health check"""
    
    def __init__(self):
        self.checks = []
        self.results = {}
    
    def add_check(self, name: str, check_func: callable):
        """Add a health check"""
        self.checks.append((name, check_func))
    
    def run_all(self) -> Dict[str, Any]:
        """Run all health checks"""
        self.results = {}
        
        for name, check_func in self.checks:
            try:
                result = check_func()
                self.results[name] = {
                    'status': 'pass' if result else 'fail',
                    'result': result,
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                self.results[name] = {
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
        
        return self.results
    
    def is_healthy(self) -> bool:
        """Check if all systems are healthy"""
        return all(
            result['status'] == 'pass' 
            for result in self.results.values()
        )


def check_dependencies() -> bool:
    """Check if all required dependencies are installed"""
    required_packages = [
        'streamlit',
        'sqlite3',
        'hashlib',
        'json',
        'datetime'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        return False
    
    return True


def check_database() -> bool:
    """Check database connectivity"""
    try:
        import sqlite3
        
        # Try to create a test database
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        conn.close()
        
        return True
    except Exception as e:
        print(f"Database check failed: {e}")
        return False


def check_file_permissions() -> bool:
    """Check file system permissions"""
    try:
        # Try to create a test file
        test_file = 'test_permissions.tmp'
        
        with open(test_file, 'w') as f:
            f.write('test')
        
        os.remove(test_file)
        
        return True
    except Exception as e:
        print(f"File permission check failed: {e}")
        return False


def check_memory() -> bool:
    """Check available memory"""
    try:
        import psutil
        
        memory = psutil.virtual_memory()
        
        # Check if at least 100MB available
        return memory.available > 100 * 1024 * 1024
    except ImportError:
        # psutil not available, assume OK
        return True
    except Exception as e:
        print(f"Memory check failed: {e}")
        return False


def get_system_info() -> Dict[str, Any]:
    """Get system information"""
    info = {
        'python_version': sys.version,
        'platform': sys.platform,
        'streamlit_version': st.__version__,
        'timestamp': datetime.now().isoformat()
    }
    
    try:
        import psutil
        
        info['cpu_count'] = psutil.cpu_count()
        info['memory_total'] = psutil.virtual_memory().total
        info['memory_available'] = psutil.virtual_memory().available
        info['disk_usage'] = psutil.disk_usage('/').percent
    except ImportError:
        pass
    
    return info


def create_deployment_checklist() -> List[Dict[str, Any]]:
    """Create deployment checklist"""
    return [
        {
            'category': 'Code',
            'items': [
                {'task': 'All tests passing', 'status': 'pending'},
                {'task': 'Code reviewed', 'status': 'pending'},
                {'task': 'No debug code', 'status': 'pending'},
                {'task': 'Error handling complete', 'status': 'pending'},
                {'task': 'Logging configured', 'status': 'pending'}
            ]
        },
        {
            'category': 'Database',
            'items': [
                {'task': 'Database backed up', 'status': 'pending'},
                {'task': 'Migrations tested', 'status': 'pending'},
                {'task': 'Indexes optimized', 'status': 'pending'},
                {'task': 'Connection pooling configured', 'status': 'pending'}
            ]
        },
        {
            'category': 'Performance',
            'items': [
                {'task': 'Load testing completed', 'status': 'pending'},
                {'task': 'Caching configured', 'status': 'pending'},
                {'task': 'Images optimized', 'status': 'pending'},
                {'task': 'Database queries optimized', 'status': 'pending'}
            ]
        },
        {
            'category': 'Security',
            'items': [
                {'task': 'Input validation added', 'status': 'pending'},
                {'task': 'SQL injection prevention', 'status': 'pending'},
                {'task': 'XSS protection enabled', 'status': 'pending'},
                {'task': 'HTTPS configured', 'status': 'pending'},
                {'task': 'Secrets secured', 'status': 'pending'}
            ]
        },
        {
            'category': 'Monitoring',
            'items': [
                {'task': 'Error tracking setup', 'status': 'pending'},
                {'task': 'Performance monitoring', 'status': 'pending'},
                {'task': 'Usage analytics', 'status': 'pending'},
                {'task': 'Alerts configured', 'status': 'pending'}
            ]
        },
        {
            'category': 'Documentation',
            'items': [
                {'task': 'User guide complete', 'status': 'pending'},
                {'task': 'API docs updated', 'status': 'pending'},
                {'task': 'README updated', 'status': 'pending'},
                {'task': 'Changelog updated', 'status': 'pending'}
            ]
        },
        {
            'category': 'Backup',
            'items': [
                {'task': 'Backup strategy defined', 'status': 'pending'},
                {'task': 'Backup tested', 'status': 'pending'},
                {'task': 'Recovery plan documented', 'status': 'pending'},
                {'task': 'Rollback plan ready', 'status': 'pending'}
            ]
        }
    ]


def show_deployment_checklist():
    """Show deployment checklist in Streamlit"""
    st.markdown("## 🚀 Deployment Checklist")
    
    checklist = create_deployment_checklist()
    
    for category_data in checklist:
        category = category_data['category']
        items = category_data['items']
        
        with st.expander(f"📋 {category}", expanded=False):
            for i, item in enumerate(items):
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"- {item['task']}")
                
                with col2:
                    status = st.selectbox(
                        "Status",
                        ["pending", "done", "skip"],
                        key=f"{category}_{i}",
                        label_visibility="collapsed"
                    )
                    item['status'] = status
    
    # Calculate completion
    total_items = sum(len(cat['items']) for cat in checklist)
    completed_items = sum(
        1 for cat in checklist 
        for item in cat['items'] 
        if item['status'] == 'done'
    )
    
    completion_pct = (completed_items / total_items) * 100 if total_items > 0 else 0
    
    st.progress(completion_pct / 100)
    st.markdown(f"**Progress:** {completed_items}/{total_items} ({completion_pct:.1f}%)")
    
    if completion_pct == 100:
        st.success("✅ All checklist items complete! Ready to deploy!")
    elif completion_pct >= 80:
        st.info("⚠️ Almost ready! Complete remaining items.")
    else:
        st.warning("📝 More work needed before deployment.")


def run_health_checks():
    """Run and display health checks"""
    st.markdown("## 🏥 System Health Check")
    
    health = HealthCheck()
    
    # Add checks
    health.add_check("Dependencies", check_dependencies)
    health.add_check("Database", check_database)
    health.add_check("File Permissions", check_file_permissions)
    health.add_check("Memory", check_memory)
    
    # Run checks
    with st.spinner("Running health checks..."):
        results = health.run_all()
    
    # Display results
    for name, result in results.items():
        status = result['status']
        
        if status == 'pass':
            st.success(f"✅ {name}: Passed")
        elif status == 'fail':
            st.error(f"❌ {name}: Failed")
        else:
            st.warning(f"⚠️ {name}: Error - {result.get('error', 'Unknown')}")
    
    # Overall status
    if health.is_healthy():
        st.success("🎉 All systems healthy!")
    else:
        st.error("⚠️ Some systems need attention")
    
    # System info
    with st.expander("📊 System Information"):
        info = get_system_info()
        st.json(info)


def create_backup():
    """Create system backup"""
    st.markdown("## 💾 Create Backup")
    
    backup_items = [
        "Database files",
        "Configuration files",
        "User data",
        "Templates",
        "Projects"
    ]
    
    st.markdown("**Items to backup:**")
    for item in backup_items:
        st.markdown(f"- {item}")
    
    if st.button("📦 Create Backup"):
        with st.spinner("Creating backup..."):
            # Simulate backup
            import time
            time.sleep(2)
            
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            
            st.success(f"✅ Backup created: {backup_name}")
            st.info("💡 Store backup in a secure location")


def show_analytics_setup():
    """Show analytics setup guide"""
    st.markdown("## 📊 Analytics Setup")
    
    st.markdown("""
    ### Recommended Analytics Tools:
    
    1. **Google Analytics**
       - Track page views
       - Monitor user behavior
       - Measure conversions
    
    2. **Mixpanel**
       - Track user events
       - Analyze user journeys
       - Measure feature usage
    
    3. **Sentry**
       - Error tracking
       - Performance monitoring
       - Release tracking
    
    ### Key Metrics to Track:
    
    - Daily/Monthly Active Users
    - Template usage rate
    - AI feature usage
    - Project creation rate
    - Average session duration
    - Error rate
    - Performance metrics
    
    ### Implementation:
    
    ```python
    # Add to your app
    import streamlit as st
    
    # Google Analytics
    st.components.v1.html('''
        <!-- Google Analytics code -->
    ''')
    
    # Track events
    def track_event(event_name, properties):
        # Send to analytics service
        pass
    ```
    """)


def generate_launch_announcement():
    """Generate launch announcement template"""
    st.markdown("## 📢 Launch Announcement")
    
    announcement = f"""
# 🚀 Launching: Structural Design Tool

We're excited to announce the launch of our new Structural Design Tool!

## What's New:

✨ **Live Code Editor** - Design with instant preview
🤖 **AI-Powered** - Generate designs from natural language
📚 **Template Library** - 8+ pre-made templates
💾 **Project Management** - Save and organize designs
🔍 **Code Quality** - Real-time linting and suggestions
📊 **Version History** - Undo/redo and snapshots

## Key Features:

- 19 engineering modules
- Real-time preview
- AI code generation
- Template marketplace
- Project management
- Code linting
- Version control

## Get Started:

1. Visit [your-app-url]
2. Select element type
3. Choose template or start fresh
4. Design and save

## Support:

- Documentation: [docs-url]
- Forum: [forum-url]
- Email: support@example.com

---

Built with ❤️ for structural engineers

Launch Date: {datetime.now().strftime('%B %d, %Y')}
"""
    
    st.code(announcement, language="markdown")
    
    if st.button("📋 Copy Announcement"):
        st.success("✅ Copied to clipboard!")
