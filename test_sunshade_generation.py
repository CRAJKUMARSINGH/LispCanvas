"""
Test script to test actual sunshade generation and reproduce the NumPy error
"""

import sys
import os

def test_sunshade_generation():
    """Test actual sunshade DXF generation"""
    print("Testing sunshade DXF generation...")
    try:
        from modules.sunshade import create_sunshade_dxf
        
        # Test with typical values
        doc = create_sunshade_dxf(
            web_width=300, 
            total_depth=450, 
            projection=1000, 
            support_thickness=150, 
            edge_thickness=100,
            bottom_bar_dia=16, 
            num_bottom_bars=4, 
            top_bar_dia=12, 
            num_top_bars=2,
            stirrup_dia=8, 
            stirrup_spacing=150, 
            main_bar_dia=10, 
            dist_bar_dia=8,
            dist_bar_spacing=150, 
            scale=25, 
            sunshade_num="01"
        )
        
        print("✅ Sunshade DXF generation successful")
        print(f"✅ Generated DXF document: {type(doc)}")
        return True
        
    except Exception as e:
        print(f"❌ Sunshade DXF generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sunshade_with_edge_cases():
    """Test sunshade generation with edge cases that might trigger NumPy errors"""
    print("\nTesting sunshade generation with edge cases...")
    
    test_cases = [
        # Case 1: Very small values
        {
            "name": "Small values",
            "web_width": 200, 
            "total_depth": 200, 
            "projection": 500, 
            "support_thickness": 50, 
            "edge_thickness": 30,
            "bottom_bar_dia": 8, 
            "num_bottom_bars": 2, 
            "top_bar_dia": 8, 
            "num_top_bars": 2,
            "stirrup_dia": 6, 
            "stirrup_spacing": 100, 
            "main_bar_dia": 6, 
            "dist_bar_dia": 6,
            "dist_bar_spacing": 100, 
            "scale": 10, 
            "sunshade_num": "S1"
        },
        # Case 2: Very large values
        {
            "name": "Large values",
            "web_width": 1000, 
            "total_depth": 1000, 
            "projection": 3000, 
            "support_thickness": 300, 
            "edge_thickness": 200,
            "bottom_bar_dia": 32, 
            "num_bottom_bars": 10, 
            "top_bar_dia": 25, 
            "num_top_bars": 8,
            "stirrup_dia": 12, 
            "stirrup_spacing": 300, 
            "main_bar_dia": 16, 
            "dist_bar_dia": 12,
            "dist_bar_spacing": 300, 
            "scale": 50, 
            "sunshade_num": "S2"
        },
        # Case 3: Zero or near-zero values that might cause division issues
        {
            "name": "Near-zero spacing",
            "web_width": 300, 
            "total_depth": 450, 
            "projection": 1000, 
            "support_thickness": 150, 
            "edge_thickness": 100,
            "bottom_bar_dia": 16, 
            "num_bottom_bars": 4, 
            "top_bar_dia": 12, 
            "num_top_bars": 2,
            "stirrup_dia": 8, 
            "stirrup_spacing": 50,  # Very small spacing
            "main_bar_dia": 10, 
            "dist_bar_dia": 8,
            "dist_bar_spacing": 100, 
            "scale": 25, 
            "sunshade_num": "S3"
        }
    ]
    
    results = []
    for case in test_cases:
        print(f"\nTesting {case['name']}...")
        try:
            from modules.sunshade import create_sunshade_dxf
            
            doc = create_sunshade_dxf(**{k: v for k, v in case.items() if k != "name"})
            print(f"✅ {case['name']} generation successful")
            results.append(True)
        except Exception as e:
            print(f"❌ {case['name']} generation failed: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    return all(results)

def main():
    """Run all tests"""
    print("=" * 60)
    print("SUNSHADE GENERATION TEST WITH NUMPY ERROR REPRODUCTION")
    print("=" * 60)
    
    # Test normal sunshade generation
    normal_test = test_sunshade_generation()
    
    # Test edge cases
    edge_case_test = test_sunshade_with_edge_cases()
    
    print("\n" + "=" * 60)
    if normal_test and edge_case_test:
        print("✅ ALL SUNSHADE GENERATION TESTS PASSED")
        print("No NumPy errors detected in sunshade generation.")
        print("The error might be happening in a different context.")
    else:
        print("❌ SOME SUNSHADE GENERATION TESTS FAILED")
        print("NumPy errors were detected during sunshade generation.")
    print("=" * 60)

if __name__ == "__main__":
    main()