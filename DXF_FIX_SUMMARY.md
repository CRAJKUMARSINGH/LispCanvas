# DXF Generation Fix Summary

## Issue Description
The error `OSError: [Errno 22] Invalid argument: '<_io.BytesIO object at 0x000001A97FDA7240>'` was occurring when trying to generate DXF files in several modules. This was caused by incorrectly using `doc.saveas()` with a BytesIO object instead of a file path.

## Root Cause
The `ezdxf` library's `saveas()` method expects a file path string, not a BytesIO object. When a BytesIO object was passed, it caused the OSError.

## Modules Affected and Fixed

### 1. Circular Column Module (`circular_column.py`)
- **Issue**: Line 74 used `doc.saveas(dxf_bytes)` where `dxf_bytes` was a BytesIO object
- **Fix**: Replaced with proper temporary file approach using `doc.saveas(temp_filename)` with a temporary file

### 2. Rectangular Column Module (`rectangular_column.py`)
- **Issue**: Line 104 used `doc.saveas(dxf_bytes)` where `dxf_bytes` was a BytesIO object
- **Fix**: Replaced with proper temporary file approach using `doc.saveas(temp_filename)` with a temporary file

### 3. Rectangular Column with Footing Module (`rect_column_footing.py`)
- **Issue**: Line 160 used `doc.saveas(dxf_bytes)` where `dxf_bytes` was a BytesIO object
- **Fix**: Replaced with proper temporary file approach using `doc.saveas(temp_filename)` with a temporary file

### 4. Circular Column with Footing Module (`circular_column_footing.py`)
- **Issue**: Line 155 used `doc.write(buffer)` which also had compatibility issues
- **Fix**: Replaced with proper temporary file approach using `doc.saveas(temp_filename)` with a temporary file

## Solution Implemented
All affected modules now use the following pattern for DXF generation:

```python
# Save DXF to bytes using temporary file approach
import tempfile
import os
with tempfile.NamedTemporaryFile(suffix='.dxf', delete=False) as fp:
    temp_filename = fp.name
doc.saveas(temp_filename)
with open(temp_filename, 'rb') as f:
    dxf_content = f.read()
os.unlink(temp_filename)
```

## Verification
All fixes have been verified through testing:
- ✅ Circular Column module DXF generation works
- ✅ Rectangular Column module DXF generation works
- ✅ Rectangular Column with Footing module DXF generation works
- ✅ Circular Column with Footing module DXF generation works

## Benefits of the Fix
1. **Resolves the OSError**: The original error no longer occurs
2. **Maintains functionality**: All DXF generation features work as expected
3. **Cross-platform compatibility**: The solution works on Windows, macOS, and Linux
4. **Memory efficient**: Temporary files are properly cleaned up after use

## Testing
The fix has been thoroughly tested with a verification script that confirms:
- All modules can be imported without errors
- DXF generation functions work correctly
- Generated DXF content is valid
- Temporary files are properly managed

The application should now run without the BytesIO-related OSError when generating DXF files.