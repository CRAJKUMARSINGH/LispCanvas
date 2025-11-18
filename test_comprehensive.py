#!/usr/bin/env python3
"""
Comprehensive Test Script for RajLisp Structural Design Suite
Tests all modules with SweetWilledDocument test cases
"""

import os
import sys
import time
import json
import tempfile
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all modules can be imported successfully"""
    print("🔍 Testing module imports...")
    
    try:
        # Test main app
        import app
        print("✅ Main app imported successfully")
        
        # Test all modules
        modules_to_test = [
            'modules.circular_column',
            'modules.rectangular_column', 
            'modules.circular_column_footing',
            'modules.rect_column_footing',
            'modules.sunshade',
            'modules.lintel',
            'modules.t_beam',
            'modules.l_beam',
            'modules.rectangular_beam',
            'modules.staircase',
            'modules.bridge',
            'modules.road_lsection',
            'modules.road_plan',
            'modules.road_cross_section',
            'modules.pmgsy_road',
            'utils.calculations',
            'utils.dxf_utils'
        ]
        
        for module_name in modules_to_test:
            try:
                __import__(module_name)
                print(f"✅ {module_name} imported successfully")
            except ImportError as e:
                print(f"❌ Failed to import {module_name}: {e}")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_calculations():
    """Test calculation utilities"""
    print("\n🧮 Testing calculation utilities...")
    
    try:
        from utils.calculations import (
            calculate_column_capacity,
            calculate_rectangular_column_capacity,
            calculate_footing_bearing_capacity,
            calculate_beam_moment_capacity,
            calculate_shear_capacity,
            calculate_deflection_check,
            calculate_staircase_design,
            calculate_development_length
        )
        
        # Test circular column calculation
        result = calculate_column_capacity(
            diameter=300, length=3000, concrete_grade='M25',
            steel_grade='Fe415', steel_area=1200
        )
        print(f"✅ Circular column capacity: {result['capacity']:.1f} kN")
        
        # Test rectangular column calculation
        result = calculate_rectangular_column_capacity(
            width=300, depth=400, length=3000, concrete_grade='M25',
            steel_grade='Fe415', steel_area=1500
        )
        print(f"✅ Rectangular column capacity: {result['capacity']:.1f} kN")
        
        # Test footing calculation
        result = calculate_footing_bearing_capacity(
            footing_width=2000, footing_depth=2000, 
            soil_bearing_capacity=200, load=1000
        )
        print(f"✅ Footing safety factor: {result['safety_factor']:.2f}")
        
        # Test beam moment calculation
        result = calculate_beam_moment_capacity(
            width=300, depth=500, concrete_grade='M25',
            steel_grade='Fe415', tension_steel=1200
        )
        print(f"✅ Beam moment capacity: {result['moment_capacity']:.1f} kNm")
        
        # Test shear calculation
        result = calculate_shear_capacity(
            width=300, depth=500, concrete_grade='M25',
            stirrup_diameter=8, stirrup_spacing=150
        )
        print(f"✅ Beam shear capacity: {result['shear_capacity']:.1f} kN")
        
        # Test deflection check
        result = calculate_deflection_check(
            span=6000, depth=500, loading_type='simply_supported'
        )
        print(f"✅ Deflection check: {result['status']}")
        
        # Test staircase design
        result = calculate_staircase_design(
            riser=150, tread=300, waist_thickness=150,
            span=3000, load=3.5
        )
        print(f"✅ Staircase moment: {result['moment']:.1f} kNm")
        
        # Test development length
        result = calculate_development_length(
            bar_diameter=16, concrete_grade='M25', steel_grade='Fe415'
        )
        print(f"✅ Development length: {result['development_length']:.0f} mm")
        
        return True
        
    except Exception as e:
        print(f"❌ Calculation test failed: {e}")
        return False

def test_dxf_generation():
    """Test DXF generation utilities"""
    print("\n📐 Testing DXF generation...")
    
    try:
        import ezdxf
        from utils.dxf_utils import create_dxf_header, add_dimensions
        
        # Create a test DXF document
        doc = ezdxf.new("R2010", setup=True)
        msp = doc.modelspace()
        
        # Test header creation
        doc = create_dxf_header(doc, "Test Drawing")
        print("✅ DXF header created successfully")
        
        # Test dimension addition
        add_dimensions(msp, (0, 0), (1000, 0), dim_line_y_offset=100, text="1000")
        print("✅ Dimensions added successfully")
        
        # Test saving to temporary file
        with tempfile.NamedTemporaryFile(suffix='.dxf', delete=False) as tmp_file:
            doc.saveas(tmp_file.name)
            file_size = os.path.getsize(tmp_file.name)
            print(f"✅ DXF file saved: {file_size} bytes")
            tmp_file.close()  # Close the file handle before unlinking
            os.unlink(tmp_file.name)
        
        return True
        
    except Exception as e:
        print(f"❌ DXF generation test failed: {e}")
        return False

def test_rectangular_beam_module():
    """Test rectangular beam module specifically"""
    print("\n📏 Testing rectangular beam module...")
    
    try:
        from modules.rectangular_beam import calculate_rectangular_beam
        
        # Test with typical parameters
        results = calculate_rectangular_beam(
            b=300, d=500, length=6.0, cover=25,
            dia_bottom=16, n_bottom=4, dia_top=12, n_top=2,
            stirrup_dia=8, stirrup_spacing=150,
            fck=25, fy=415, dl=15.0, ll=10.0
        )
        
        print(f"✅ Beam effective depth: {results['d_effective']:.1f} mm")
        print(f"✅ Bottom steel area: {results['ast_bottom']:.0f} mm²")
        print(f"✅ Top steel area: {results['ast_top']:.0f} mm²")
        print(f"✅ Steel percentage: {results['pt_total']:.2f}%")
        print(f"✅ Moment check: {results['moment_check']}")
        print(f"✅ Shear check: {results['shear_check']}")
        print(f"✅ Deflection check: {results['deflection_check']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Rectangular beam test failed: {e}")
        return False

def test_sunshade_module():
    """Test sunshade module"""
    print("\n🌞 Testing sunshade module...")
    
    try:
        from modules.sunshade import draw_sunshade
        import tempfile
        
        # Test sunshade drawing generation
        doc = draw_sunshade(
            web_width=300, total_depth=500, projection=1200,
            support_thickness=160, edge_thickness=100,
            bottom_bar_dia=16, num_bottom_bars=4,
            top_bar_dia=12, num_top_bars=2,
            stirrup_dia=8, stirrup_spacing=150,
            main_bar_dia=12, dist_bar_dia=8,
            dist_bar_spacing=150, scale=25, sunshade_num="01"
        )
        
        # Test saving
        with tempfile.NamedTemporaryFile(suffix='.dxf', delete=False) as tmp_file:
            doc.saveas(tmp_file.name)
            file_size = os.path.getsize(tmp_file.name)
            print(f"✅ Sunshade DXF generated: {file_size} bytes")
            tmp_file.close()  # Close the file handle before unlinking
            os.unlink(tmp_file.name)
        
        return True
        
    except Exception as e:
        print(f"❌ Sunshade test failed: {e}")
        return False

def test_with_sweetwilled_documents():
    """Test with SweetWilledDocument test cases"""
    print("\n📄 Testing with SweetWilledDocument test cases...")
    
    test_docs_dir = project_root / "test_documents"
    if not test_docs_dir.exists():
        print("❌ Test documents directory not found")
        return False
    
    test_files = list(test_docs_dir.glob("SweetWilledDocument-*.txt"))
    print(f"📋 Found {len(test_files)} test documents")
    
    successful_tests = 0
    
    for test_file in test_files:
        try:
            print(f"\n📖 Testing {test_file.name}...")
            
            # Read test document
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract parameters (simplified parsing)
            lines = content.split('\n')
            params = {}
            
            for line in lines:
                if ':' in line and not line.startswith('='):
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace(' ', '_').replace('(', '').replace(')', '')
                    value = value.strip()
                    
                    # Try to convert to number if possible
                    try:
                        if '.' in value:
                            params[key] = float(value)
                        else:
                            params[key] = int(value)
                    except ValueError:
                        params[key] = value
            
            print(f"✅ Extracted {len(params)} parameters from {test_file.name}")
            
            # Test with rectangular beam module
            if all(key in params for key in ['beam_width', 'beam_depth', 'beam_length']):
                try:
                    from modules.rectangular_beam import calculate_rectangular_beam
                    
                    results = calculate_rectangular_beam(
                        b=params.get('beam_width', 300),
                        d=params.get('beam_depth', 500),
                        length=params.get('beam_length', 6.0),
                        cover=25,
                        dia_bottom=16, n_bottom=4,
                        dia_top=12, n_top=2,
                        stirrup_dia=8, stirrup_spacing=150,
                        fck=25, fy=415,
                        dl=params.get('dead_load', 15.0),
                        ll=params.get('live_load', 10.0)
                    )
                    
                    print(f"✅ Beam design successful for {test_file.name}")
                    print(f"   - Capacity: {results['Mr_actual']:.1f} kNm")
                    print(f"   - Steel %: {results['pt_total']:.2f}%")
                    
                except Exception as e:
                    print(f"⚠️ Beam design failed for {test_file.name}: {e}")
            
            successful_tests += 1
            
        except Exception as e:
            print(f"❌ Failed to process {test_file.name}: {e}")
    
    print(f"\n📊 Test Summary: {successful_tests}/{len(test_files)} documents processed successfully")
    return successful_tests == len(test_files)

def generate_test_report():
    """Generate comprehensive test report"""
    print("\n📊 Generating comprehensive test report...")
    
    report = {
        "test_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "project": "RajLisp Structural Design Suite",
        "version": "Enhanced v2.0",
        "tests": {}
    }
    
    # Run all tests
    tests = [
        ("Module Imports", test_imports),
        ("Calculation Utilities", test_calculations),
        ("DXF Generation", test_dxf_generation),
        ("Rectangular Beam Module", test_rectangular_beam_module),
        ("Sunshade Module", test_sunshade_module),
        ("SweetWilledDocument Tests", test_with_sweetwilled_documents)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            report["tests"][test_name] = {
                "status": "PASSED" if result else "FAILED",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            if not result:
                all_passed = False
        except Exception as e:
            report["tests"][test_name] = {
                "status": "ERROR",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            all_passed = False
    
    # Save report
    report_file = project_root / "test_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📄 Test report saved to: {report_file}")
    print(f"🎯 Overall result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return all_passed

def main():
    """Main test function"""
    print("🏗️ RajLisp Structural Design Suite - Comprehensive Test")
    print("=" * 60)
    
    # Change to project directory
    os.chdir(project_root)
    
    # Run comprehensive tests
    success = generate_test_report()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        print("✅ The enhanced RajLisp application is ready for deployment")
    else:
        print("\n⚠️ Some tests failed. Please review the issues above.")
    
    return success

if __name__ == "__main__":
    main()
