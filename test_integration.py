"""
Integration Test Script
Tests all modules and functionality
"""

import sys
import os
import importlib
from datetime import datetime

# Add modules to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class IntegrationTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        
    def test_module_import(self, module_name, function_name):
        """Test if a module can be imported"""
        try:
            module = importlib.import_module(f'modules.{module_name}')
            if hasattr(module, function_name):
                self.passed += 1
                self.results.append(f"✅ {module_name}: Import successful")
                return True
            else:
                self.failed += 1
                self.results.append(f"❌ {module_name}: Function {function_name} not found")
                return False
        except Exception as e:
            self.failed += 1
            self.results.append(f"❌ {module_name}: Import failed - {str(e)}")
            return False
    
    def test_all_modules(self):
        """Test all 17 modules"""
        modules = [
            ('lintel', 'page_lintel'),
            ('sunshade', 'page_sunshade'),
            ('circular_column', 'page_circular_column'),
            ('rectangular_column', 'page_rectangular_column'),
            ('rect_column_footing', 'page_rect_column_footing'),
            ('circular_column_footing', 'page_circular_column_footing'),
            ('road_plan', 'page_road_plan'),
            ('road_lsection', 'page_road_lsection'),
            ('road_cross_section', 'page_road_cross_section'),
            ('pmgsy_road', 'page_pmgsy_road'),
            ('t_beam', 'page_t_beam'),
            ('l_beam', 'page_l_beam'),
            ('rectangular_beam', 'page_rectangular_beam'),
            ('inverted_t_beam', 'page_inverted_t_beam'),
            ('inverted_l_beam', 'page_inverted_l_beam'),
            ('staircase', 'page_staircase'),
            ('bridge', 'page_bridge'),
        ]
        
        print("\n" + "="*60)
        print("🧪 INTEGRATION TEST - MODULE IMPORTS")
        print("="*60 + "\n")
        
        for module_name, function_name in modules:
            self.test_module_import(module_name, function_name)
        
        self.print_results()
    
    def test_dependencies(self):
        """Test required dependencies"""
        print("\n" + "="*60)
        print("📦 DEPENDENCY CHECK")
        print("="*60 + "\n")
        
        dependencies = [
            'streamlit',
            'ezdxf',
            'numpy',
            'pandas',
        ]
        
        for dep in dependencies:
            try:
                importlib.import_module(dep)
                self.passed += 1
                self.results.append(f"✅ {dep}: Installed")
            except ImportError:
                self.failed += 1
                self.results.append(f"❌ {dep}: Not installed")
        
        # Test matplotlib separately (optional)
        try:
            importlib.import_module('matplotlib')
            self.passed += 1
            self.results.append(f"✅ matplotlib: Installed (optional for road modules)")
        except ImportError:
            self.passed += 1  # Don't fail if matplotlib missing
            self.results.append(f"⚠️ matplotlib: Not installed (optional - road modules will work without charts)")
        
        self.print_results()
    
    def test_export_dependencies(self):
        """Test export dependencies"""
        print("\n" + "="*60)
        print("📊 EXPORT DEPENDENCIES CHECK")
        print("="*60 + "\n")
        
        export_deps = [
            ('openpyxl', 'Excel export'),
            ('reportlab', 'PDF export'),
        ]
        
        for dep, purpose in export_deps:
            try:
                importlib.import_module(dep)
                self.passed += 1
                self.results.append(f"✅ {dep}: Installed ({purpose})")
            except ImportError:
                self.failed += 1
                self.results.append(f"⚠️ {dep}: Not installed ({purpose}) - Optional")
        
        self.print_results()
    
    def print_results(self):
        """Print test results"""
        for result in self.results:
            print(result)
        self.results = []
    
    def print_summary(self):
        """Print final summary"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"\n✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📊 Total: {self.passed + self.failed}")
        print(f"📈 Success Rate: {(self.passed/(self.passed+self.failed)*100):.1f}%")
        
        if self.failed == 0:
            print("\n🎉 ALL TESTS PASSED! Ready for launch!")
        else:
            print(f"\n⚠️ {self.failed} test(s) failed. Please fix before launch.")
        
        print("\n" + "="*60)

def main():
    """Run all integration tests"""
    print("\n" + "="*60)
    print("🚀 STRUCTURAL DESIGN SUITE - INTEGRATION TEST")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    tester = IntegrationTester()
    
    # Run tests
    tester.test_dependencies()
    tester.test_export_dependencies()
    tester.test_all_modules()
    
    # Print summary
    tester.print_summary()

if __name__ == "__main__":
    main()
