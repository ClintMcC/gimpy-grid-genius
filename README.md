# GIMP Advanced Guide Grid Generator

A **GIMP 3.x** plugin for creating advanced, customizable grids and guide layouts. This plugin allows you to specify cell sizes in **pixels, inches, millimeters, or percentages**, with additional features such as **margins, gutters, and center guides**. It’s designed to enhance your workflow for precise layouts in GIMP.

---

## Features
- Flexible cell sizing: Choose between **px, inches, mm, or percentages**.
- Optional **margins** and **gutters**.
- Add **center guides** to mark the middle of your image.
- Fully customizable guide layout with precise control.

---

## Installation

1. **Download the Plugin:**
   - Clone the repository:
     ```bash
     git clone https://github.com/yourusername/gimp-guide-grid-enhancer.git
     ```
   - Or [download the zip file](https://github.com/yourusername/gimp-guide-grid-enhancer/archive/main.zip).

2. **Install the Plugin:**
   - Copy the Python files (`guide_grid.py`, `guide_grid_ui.py`, etc.) to your GIMP plug-ins folder:
     - **Linux:** `~/.config/GIMP/3.0/plug-ins/`
     - **Windows:** `C:\Users\<YourUsername>\AppData\Roaming\GIMP\3.0\plug-ins\`
     - **macOS:** `~/Library/Application Support/GIMP/3.0/plug-ins/`

3. **Make the Script Executable (Linux/macOS):**
   ```bash
   chmod +x guide_grid.py
