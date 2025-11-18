import sys
import os

# Add the modules directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Debugging module imports...")
print("=" * 40)

# Try importing individual modules to identify the problematic one
modules_to_test = [
    "lintel",
    "sunshade",
    "circular_column", 
    "rectangular_column",
    "rect_column_footing",
    "circular_column_footing",
    "road_lsection",
    "road_plan",
    "road_cross_section",
    "pmgsy_road",
    "t_beam",
    "l_beam",
    "staircase",
    "bridge"
]

failed_modules = []
successful_modules = []

for module_name in modules_to_test:
    try:
        module_path = f"modules.{module_name}"
        __import__(module_path)
        print(f"✅ {module_name}: SUCCESS")
        successful_modules.append(module_name)
    except Exception as e:
        print(f"❌ {module_name}: FAILED - {str(e)}")
        failed_modules.append((module_name, str(e)))

print("\n" + "=" * 40)
print("SUMMARY")
print("=" * 40)
print(f"Successful imports: {len(successful_modules)}")
for module in successful_modules:
    print(f"  - {module}")

print(f"\nFailed imports: {len(failed_modules)}")
for module, error in failed_modules:
    print(f"  - {module}: {error}")

# Specifically test the lintel and sunshade modules that the user is interested in
print("\n" + "=" * 40)
print("TARGET MODULES (Lintel & Sunshade)")
print("=" * 40)

target_modules = ["lintel", "sunshade"]

for module_name in target_modules:
    try:
        module_path = f"modules.{module_name}"
        module = __import__(module_path, fromlist=[module_name])
        print(f"✅ {module_name}: SUCCESSFULLY IMPORTED")
        
        # Try to access the main function
        page_function = getattr(module, f"page_{module_name}")
        print(f"✅ {module_name}: page_{module_name} function accessible")
        
    except Exception as e:
        print(f"❌ {module_name}: FAILED - {str(e)}")