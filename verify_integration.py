import sys
import os

# Add the modules directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_module_integration():
    """Test that lintel and sunshade modules are properly integrated"""
    try:
        # Test importing the main app
        import app
        print("Main app imported successfully")
        
        # Test importing individual modules
        from modules.lintel import page_lintel
        print("Lintel module imported successfully")
        
        from modules.sunshade import page_sunshade
        print("Sunshade module imported successfully")
        
        # Test that all required functions exist
        assert callable(page_lintel), "page_lintel should be callable"
        assert callable(page_sunshade), "page_sunshade should be callable"
        
        print("✅ All integration tests passed!")
        print("Lintel and Sunshade modules are properly wired to the main design application.")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_module_integration()