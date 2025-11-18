"""
Test script to reproduce and fix the NumPy error in sunshade module
"""

import sys
import os

def test_sunshade_numpy_operations():
    """Test the specific NumPy operations used in the sunshade module"""
    print("Testing sunshade-specific NumPy operations...")
    try:
        import numpy as np
        
        # Test the specific operations used in sunshade module
        print("Testing reinforcement calculations...")
        
        # Test 1: Main steel area calculation
        main_bar_dia = 10
        main_steel_area = np.pi * (main_bar_dia/2)**2
        print(f"✅ Main steel area calculation: {main_steel_area:.1f} mm²/bar")
        
        # Test 2: Distribution steel calculation
        dist_bar_dia = 8
        dist_bar_spacing = 150
        dist_bars_per_meter = 1000 / dist_bar_spacing
        dist_steel_per_meter = dist_bars_per_meter * np.pi * (dist_bar_dia/2)**2
        print(f"✅ Distribution steel calculation: {dist_steel_per_meter:.0f} mm²/m")
        
        # Test 3: Bottom steel area calculation
        num_bottom_bars = 4
        bottom_bar_dia = 16
        bottom_steel_area = num_bottom_bars * np.pi * (bottom_bar_dia/2)**2
        print(f"✅ Bottom steel area calculation: {bottom_steel_area:.0f} mm²")
        
        # Test 4: Top steel area calculation
        num_top_bars = 2
        top_bar_dia = 12
        top_steel_area = num_top_bars * np.pi * (top_bar_dia/2)**2
        print(f"✅ Top steel area calculation: {top_steel_area:.0f} mm²")
        
        # Test 5: Steel percentage calculation
        web_width = 300
        total_depth = 450
        beam_gross_area = web_width * total_depth
        steel_percentage = ((bottom_steel_area + top_steel_area) / beam_gross_area) * 100
        print(f"✅ Steel percentage calculation: {steel_percentage:.2f}%")
        
        print("✅ All sunshade NumPy operations work correctly")
        return True
        
    except Exception as e:
        print(f"❌ Sunshade NumPy operations failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sunshade_module_directly():
    """Test the sunshade module directly"""
    print("\nTesting sunshade module directly...")
    try:
        from modules.sunshade import page_sunshade
        print("✅ Sunshade module imported successfully")
        return True
    except Exception as e:
        print(f"❌ Sunshade module import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("SUNSHADE NUMPY ERROR REPRODUCTION AND VERIFICATION")
    print("=" * 60)
    
    # Test NumPy operations used in sunshade
    numpy_test = test_sunshade_numpy_operations()
    
    # Test sunshade module import
    module_test = test_sunshade_module_directly()
    
    print("\n" + "=" * 60)
    if numpy_test and module_test:
        print("✅ ALL TESTS PASSED")
        print("The NumPy error may be related to specific input conditions")
        print("or runtime environment rather than the NumPy installation itself.")
    else:
        print("❌ SOME TESTS FAILED")
        print("There may be issues with NumPy or the sunshade module.")
    print("=" * 60)

if __name__ == "__main__":
    main()