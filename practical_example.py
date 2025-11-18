"""
Practical example showing how to use lintel and sunshade modules together
This demonstrates a real-world scenario where both modules might be used
"""

import sys
import os

# Add the modules directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def practical_usage_example():
    """Demonstrate practical usage of both modules together"""
    print("Practical Usage Example: Designing a Building Opening with Lintel and Sunshade")
    print("=" * 80)
    
    print("""
Scenario:
You are designing a residential building with window openings that require:
1. Lintel beams to support the wall load above openings
2. Sunshades to provide protection from direct sunlight

This example shows how both modules work together in a typical design workflow.
""")
    
    print("1. Lintel Design Process:")
    print("   - Define opening dimensions (width: 1200mm, height: 2100mm)")
    print("   - Specify wall thickness (230mm) and bearing requirements (150mm each side)")
    print("   - Set lintel dimensions (200mm wide x 250mm deep)")
    print("   - Input material properties (M20 concrete, Fe415 steel)")
    print("   - Define loading conditions (wall load, floor load, live load)")
    print("   - Specify reinforcement details (3-12mm main bars, 8mm stirrups @ 150mm c/c)")
    print("   - Generate structural calculations and design checks")
    print("   - Create DXF drawing for construction")
    
    print("\n2. Sunshade Design Process:")
    print("   - Define sunshade projection (1000mm)")
    print("   - Specify thickness variation (150mm at support, 100mm at edge)")
    print("   - Design supporting beam (300mm wide x 450mm deep)")
    print("   - Determine reinforcement (4-16mm bottom bars, 2-12mm top bars)")
    print("   - Specify stirrup details (8mm @ 150mm c/c)")
    print("   - Design sunshade reinforcement (10mm main bars, 8mm distribution @ 150mm c/c)")
    print("   - Generate detailed DXF drawing with multiple views")
    print("   - Create design report for documentation")
    
    print("\n3. Integration Benefits:")
    print("   - Both modules use consistent design standards")
    print("   - Shared DXF generation utilities ensure compatibility")
    print("   - Unified interface provides seamless user experience")
    print("   - Modular design allows independent development and testing")
    print("   - Common material databases ensure consistency across designs")
    
    print("\n4. Workflow Integration:")
    print("   - Start with lintel design for structural support")
    print("   - Proceed to sunshade design for environmental control")
    print("   - Generate coordinated drawings for construction")
    print("   - Export DXF files for use in CAD software")
    print("   - Maintain design consistency across both elements")
    
    print("\n" + "=" * 80)
    print("This practical example demonstrates how the Lintel and Sunshade modules")
    print("work together as part of a complete building design solution.")
    print("=" * 80)

if __name__ == "__main__":
    practical_usage_example()