#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gimp", "3.0")
gi.require_version("GimpUi", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gimp, GimpUi, Gtk, GLib
import sys

class GridGenius(Gimp.PlugIn):
    def do_query_procedures(self):
        return ["python-fu-grid-genius"]

    def do_create_procedure(self, name):
        GimpUi.init("grid-genius")
        procedure = Gimp.ImageProcedure.new(
            self, name, Gimp.PDBProcType.PLUGIN, self.run, None
        )
        procedure.set_image_types("*")
        procedure.set_menu_label("Grid Genius")
        procedure.add_menu_path("<Image>/Image/Guides/")
        procedure.set_documentation(
            "Grid Genius with customizable guide grid",
            "Generates guides based on user-defined cell width and height in px, inches, mm, or percentage.",
            name
        )
        procedure.set_attribution("Your Name", "Your License", "2025")
        return procedure

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        # Dialog for user input
        dialog = GimpUi.Dialog(title="Grid Genius", role="grid-genius")
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_OK", Gtk.ResponseType.OK)

        # Main vertical box layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        dialog.get_content_area().add(main_box)
        main_box.show()

        # Create a "Cell Sizing" frame
        cell_sizing_frame = Gtk.Frame()
        main_box.pack_start(cell_sizing_frame, False, False, 0)
        cell_sizing_frame.show()

        # Bold section label
        section_label = Gtk.Label()
        section_label.set_markup("<b>Cell Sizing</b>")
        section_label.set_halign(Gtk.Align.START)
        section_label.set_margin_bottom(10)
        section_label.show()

        # Grid layout for inputs
        grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        cell_sizing_frame.add(grid)
        grid.show()

        # Add section label at the top
        grid.attach(section_label, 0, 0, 3, 1)

        # Width input row
        width_label = Gtk.Label(label="Width:")
        width_label.set_halign(Gtk.Align.END)
        width_label.set_hexpand(False)
        width_spinner = Gtk.SpinButton()
        width_spinner.set_adjustment(Gtk.Adjustment(1.0, 0.1, 10000.0, 0.1))  # Allow floats
        width_spinner.set_value(100)
        width_spinner.set_width_chars(10)  # Fixed width for alignment

        width_label.show()
        width_spinner.show()

        grid.attach(width_label, 0, 1, 1, 1)
        grid.attach(width_spinner, 1, 1, 1, 1)

        # Height input row
        height_label = Gtk.Label(label="Height:")
        height_label.set_halign(Gtk.Align.END)
        height_label.set_hexpand(False)
        height_spinner = Gtk.SpinButton()
        height_spinner.set_adjustment(Gtk.Adjustment(1.0, 0.1, 10000.0, 0.1))  # Allow floats
        height_spinner.set_value(100)
        height_spinner.set_width_chars(10)  # Fixed width for alignment
        unit_combo = Gtk.ComboBoxText()
        unit_combo.append_text("px")
        unit_combo.append_text("inches")
        unit_combo.append_text("mm")
        unit_combo.append_text("%")
        unit_combo.set_active(0)  # Default to "px"

        height_label.show()
        height_spinner.show()
        unit_combo.show()

        grid.attach(height_label, 0, 2, 1, 1)
        grid.attach(height_spinner, 1, 2, 1, 1)
        grid.attach(unit_combo, 2, 2, 1, 1)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            # Get user inputs
            cell_width = width_spinner.get_value()
            cell_height = height_spinner.get_value()
            unit = unit_combo.get_active_text()

            # Get image dimensions
            image_width = image.get_width()
            image_height = image.get_height()

            # Try to get the resolution
            success, dpi_x, dpi_y = image.get_resolution()
            if success:
                Gimp.message(f"Resolution retrieved - DPI X: {dpi_x}, DPI Y: {dpi_y}")
            else:
                Gimp.message("Resolution retrieval failed. Defaulting to 72 DPI.")
                dpi_x = 72.0
                dpi_y = 72.0

            # Conversion function
            def convert_to_pixels(value, unit, dpi, image_dimension):
                if unit == "inches":
                    return int(value * dpi)
                elif unit == "mm":
                    return int(value * dpi / 25.4)  # Convert mm to inches, then to pixels
                elif unit == "%":
                    return int(value / 100.0 * image_dimension)  # Percentage of image dimension
                else:  # px
                    return int(value)

            # Convert inputs to pixels
            cell_width_px = convert_to_pixels(cell_width, unit, dpi_x, image_width)
            cell_height_px = convert_to_pixels(cell_height, unit, dpi_y, image_height)

            if cell_width_px <= 0 or cell_height_px <= 0:
                Gimp.message("Invalid cell size! Please enter positive values.")
                dialog.destroy()
                return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

            # Draw horizontal guides
            for y in range(cell_height_px, image_height, cell_height_px):
                image.add_hguide(y)

            # Draw vertical guides
            for x in range(cell_width_px, image_width, cell_width_px):
                image.add_vguide(x)

            Gimp.message("Grid Genius: Guide grid created successfully!")
        else:
            Gimp.message("Grid Genius: User cancelled.")
        dialog.destroy()

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

# Register the plugin
Gimp.main(GridGenius.__gtype__, sys.argv)
