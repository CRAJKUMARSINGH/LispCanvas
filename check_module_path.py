"""
Script to check the module path and content
"""

import sys
import os

def check_module_path():
    """Check the module path and content"""
    print("Checking module path...")
    
    # Add the modules directory to the path
    modules_dir = os.path.join(os.path.dirname(__file__), 'modules')
    if modules_dir not in sys.path:
        sys.path.insert(0, modules_dir)
        print(f"Added {modules_dir} to sys.path")
    
    try:
        import modules.circular_column_footing
        print(f"Module file path: {modules.circular_column_footing.__file__}")
        
        # Read the file and check specific lines
        with open(circular_column_footing.__file__, 'r') as f:
            lines = f.readlines()
            
        print(f"Total lines in file: {len(lines)}")
        
        # Check the lines around 157
        start_line = max(0, 157-5)
        end_line = min(len(lines), 157+5)
        
        print(f"\nLines around 157:")
        for i in range(start_line, end_line):
            print(f"{i+1:3d}: {lines[i].rstrip()}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_module_path()