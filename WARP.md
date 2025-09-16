# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Project overview
- This repo is a hybrid of legacy AutoCAD LISP scripts and a modern Python/Streamlit application that generates structural/road/bridge drawings as DXF via ezdxf.
- The Streamlit app (app.py) is the main entry point for interactive use. It routes to feature pages implemented under modules/.
- The Tested_Bridge_GAD/ folder contains a standalone, parameter-driven bridge drawing generator (bridge_gad_app.py) that reads variables from an Excel sheet and emits a comprehensive DXF of a bridge General Arrangement Drawing (GAD).

Prerequisites
- Python 3.10+ on Windows (pwsh).
- Recommended: create and use a virtual environment.
- Core libraries:
  - streamlit (UI)
  - ezdxf (DXF generation)
  - pandas + openpyxl (Excel I/O; needed for bridge GAD and any Excel-driven modules)
  - reportlab (PDF output for tender report in bridge GAD; optional)

Setup and install
- Create venv and install dependencies:
  - py -m venv venv
  - .\venv\Scripts\Activate.ps1
  - pip install -r requirements.txt
  - If working on the bridge features or Excel/PDF outputs, also install:
    - pip install pandas openpyxl reportlab

Common commands
- Run the main Streamlit app (Structural Design Suite):
  - streamlit run app.py
- Run the beam module demo UI (tabs for Inverted T/L beams):
  - streamlit run test_beam_modules.py
- Run the standalone Bridge GAD generator (DXF + optional tender PDF):
  - python .\Tested_Bridge_GAD\bridge_gad_app.py
  Notes:
  - The script currently references hard-coded Windows paths (e.g., F:\\LISP 2005\\P1\\input.xlsx). Prefer placing an input.xlsx in Tested_Bridge_GAD/ and updating paths before use, or ensure the referenced drive/path exists.
  - Ensure pandas, openpyxl, and reportlab are installed if you intend to read Excel and generate the tender PDF.
- Export a DXF from individual page modules (pattern):
  - Most modules expose a page_* function used by Streamlit to collect inputs and invoke an ezdxf writer that returns/saves a DXF. For programmatic usage, import the module under modules/ and call its DXF generator (e.g., generate_inverted_t_beam_dxf). Example:
    - python -c "from modules.inverted_t_beam import generate_inverted_t_beam_dxf; open('out.dxf','wb').write(generate_inverted_t_beam_dxf(bf=1500, tf=150, bw=300, D=600, d=550, main_bars_dia=20, num_bars=5, stirrup_dia=10, stirrup_spacing=150))"

Single-feature runs and quick checks
- Beam DXF generator quick check:
  - python - << 'PY'
    from modules.inverted_l_beam import generate_inverted_l_beam_dxf
    dxf = generate_inverted_l_beam_dxf(bf=900, tf=150, bw=250, D=550, d=500, main_bars_dia=16, num_bars=4, stirrup_dia=8, stirrup_spacing=150, flange_position='Bottom Left')
    open('inverted_l_beam_sample.dxf','wb').write(dxf)
    print('Wrote inverted_l_beam_sample.dxf')
    PY

Linting and formatting
- No linter or formatter configuration is present in the repo. Do not assume flake8/ruff/black are configured. If you add one, document the commands here.

Tests
- There is no pytest suite configured. test_beam_modules.py is a Streamlit script to interactively exercise two beam generators.
- To try those interactively:
  - streamlit run test_beam_modules.py

Big-picture architecture
- Streamlit app (app.py):
  - Provides a left sidebar for navigation across modules: Columns (circular/rectangular/with footing), Beams (T/L), Other structures (Lintel, Sunshade, Staircase), Road design (L-Section, Plan, Cross Section, PMGSY), and Bridge.
  - Each menu item routes to a page_* function imported from modules/. Those page functions render forms, gather parameters, and call an ezdxf writer to build a DXF. Some pages also offer a download button for the DXF bytes.
  - app.py currently imports modules.* names that may not all exist. The README calls out missing modules still to be created (see below).
- Modules (modules/*.py):
  - Encapsulate one feature per file (e.g., inverted_t_beam.py, circular_column.py, road_plan.py). Typical structure: Streamlit page function (page_*), and a DXF generator function (e.g., generate_*_dxf) that returns DXF as bytes via ezdxf.
  - Keep UI (Streamlit) logic thin; concentrate DXF construction in pure functions to enable programmatic reuse and testing.
- Bridge GAD (Tested_Bridge_GAD/bridge_gad_app.py):
  - A standalone, procedural script that:
    - Reads variable definitions from Excel (Value, Variable, Description columns) into a pandas DataFrame.
    - Computes scaling and coordinate transforms (hpos/vpos, h2pos/v2pos) from datum/left and scale factors.
    - Draws the base axes and annotations (X/Y axes, chainage ticks, level ticks, labels) in modelspace.
    - Plots river cross-section and chainages from a Sheet2 (Chainage (x), RL (y)).
    - Builds superstructure in elevation: spans arrayed by span length, approach slabs with expansion joints, continuous wearing course.
    - Generates pier caps across spans, pier elevation outlines with dimensions, pier footings, and plan views using arcs/lines composed per span.
    - Draws left and right abutments (elevation and plan) derived from batter/cap/offset variables with skew adjustments.
    - Adds block boundaries for elevation and plan sheets, centers headings, and places mtext/title blocks.
    - Saves DXF(s) to disk; optionally composes a tender analysis PDF (generate_tender_report) when reportlab is available.
  - Caveats observed in code:
    - Multiple __main__ blocks and mixed UI approaches (console/Streamlit/Tkinter) coexist; only one should be used at a time in practice.
    - Several hard-coded file paths point to F:\\LISP 2005\\P1. Prefer making paths relative to Tested_Bridge_GAD/ and passing them as arguments.
    - requirements.txt does not list pandas, openpyxl, or reportlab though the bridge script uses them.

Important notes from repo docs
- README.md (key items):
  - Remaining modules to implement and include in navigation: Rectangle Column with Footing, Road L-Section, Road Plan, Road Cross Section, PMGSY Road, Lintel Sunshade, T-Beam, L-Beam, Staircase, Bridge (from Tested_Bridge_GAD folder).
  - Update the main app to include all pages and enhance UI consistency, validations, and DXF detail.
- what_warp_has_done_till_now_and_what_is_due.md:
  - Confirms gaps between LISP functionality and Python modules.
  - Prioritized missing modules: road_lsection.py, lintel.py, staircase.py, bridge.py (port from Tested_Bridge_GAD).
  - Notes that modules.circular_column_footing.py has been created and that the app structure is Streamlit + ezdxf.

Windows-specific tips
- Use PowerShell-friendly paths and quotes in commands.
- When using file pickers in Tkinter code paths, ensure you are in a desktop session (not headless). Prefer Streamlit-based flows for consistency within this repo.

When editing or extending
- If you add a new module under modules/, provide:
  - A page_* function for Streamlit routing.
  - A pure DXF builder function returning bytes for programmatic use and easier testing.
- If you port the bridge GAD into modules/bridge.py:
  - Replace hard-coded file system references with parameters and relative paths within the repo (e.g., Tested_Bridge_GAD/input.xlsx).
  - Isolate IO (Excel read/write) from geometry/DXF generation so the page and CLI flows can share a single core generator.

