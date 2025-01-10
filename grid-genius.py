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
            "Grid Genius: Column Grid with Margins and Gutters",
            "Creates evenly distributed vertical guides with optional gutters between columns and applies margins.",
            name
        )
        procedure.set_attribution("Your Name", "Your License", "2025")
        return procedure

    def create_dialog(self):
        """Creates and returns the dialog layout with user input fields."""
        dialog = GimpUi.Dialog(title="Grid Genius: Column Grid with Margins and Gutters", role="grid-genius")
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_OK", Gtk.ResponseType.OK)

        # Main vertical box for layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        dialog.get_content_area().add(main_box)

        # --- Unified Grid for Inputs ---
        input_grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        main_box.pack_start(input_grid, False, False, 0)

        # --- Section: Column Grid ---
        column_grid_label = Gtk.Label(label="Column Grid")
        column_grid_label.set_markup("<b>Column Grid</b>")
        column_grid_label.set_halign(Gtk.Align.START)
        column_grid_label.set_margin_bottom(5)
        input_grid.attach(column_grid_label, 0, 0, 2, 1)

        # Number of Columns Row
        column_label = Gtk.Label(label="Number of Columns:")
        column_label.set_halign(Gtk.Align.END)
        column_label.set_size_request(150, -1)
        column_spinner = Gtk.SpinButton()
        column_spinner.set_adjustment(Gtk.Adjustment(1, 1, 100, 1))
        column_spinner.set_value(3)  # Default value
        input_grid.attach(column_label, 0, 1, 1, 1)
        input_grid.attach(column_spinner, 1, 1, 1, 1)

        # --- Section: Margins ---
        margin_section_label = Gtk.Label(label="Margins")
        margin_section_label.set_markup("<b>Margins</b>")
        margin_section_label.set_halign(Gtk.Align.START)
        margin_section_label.set_margin_top(20)
        input_grid.attach(margin_section_label, 0, 2, 2, 1)

        margin_label = Gtk.Label(label="Margin Size:")
        margin_label.set_halign(Gtk.Align.END)
        margin_spinner = Gtk.SpinButton()
        margin_spinner.set_adjustment(Gtk.Adjustment(0.0, 0.0, 1000.0, 1.0))
        margin_spinner.set_value(0)  # Default value
        margin_unit_combo = Gtk.ComboBoxText()
        for unit in ["px", "inches", "mm"]:
            margin_unit_combo.append_text(unit)
        margin_unit_combo.set_active(0)  # Default to "px"
        input_grid.attach(margin_label, 0, 3, 1, 1)
        input_grid.attach(margin_spinner, 1, 3, 1, 1)
        input_grid.attach(margin_unit_combo, 2, 3, 1, 1)

        # --- Section: Gutters ---
        gutter_section_label = Gtk.Label(label="Gutters")
        gutter_section_label.set_markup("<b>Gutters</b>")
        gutter_section_label.set_halign(Gtk.Align.START)
        gutter_section_label.set_margin_top(20)
        input_grid.attach(gutter_section_label, 0, 4, 2, 1)

        gutter_label = Gtk.Label(label="Gutter Width:")
        gutter_label.set_halign(Gtk.Align.END)
        gutter_spinner = Gtk.SpinButton()
        gutter_spinner.set_adjustment(Gtk.Adjustment(0.0, 0.0, 1000.0, 0.1))
        gutter_spinner.set_value(0)  # Default value
        gutter_unit_combo = Gtk.ComboBoxText()
        for unit in ["px", "inches", "mm"]:
            gutter_unit_combo.append_text(unit)
        gutter_unit_combo.set_active(0)  # Default to "px"
        input_grid.attach(gutter_label, 0, 5, 1, 1)
        input_grid.attach(gutter_spinner, 1, 5, 1, 1)
        input_grid.attach(gutter_unit_combo, 2, 5, 1, 1)

        # --- Checkbox for Deleting Existing Guides ---
        delete_guides_check = Gtk.CheckButton(label="Delete Existing Guides")
        delete_guides_check.set_active(False)  # Default to unchecked
        input_grid.attach(delete_guides_check, 0, 6, 2, 1)

        dialog.get_content_area().show_all()

        return dialog, column_spinner, margin_spinner, margin_unit_combo, gutter_spinner, gutter_unit_combo, delete_guides_check

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        Gimp.message("Starting Grid Genius plugin...")

        # Create the dialog and get widgets
        dialog, column_spinner, margin_spinner, margin_unit_combo, gutter_spinner, gutter_unit_combo, delete_guides_check = self.create_dialog()

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            # Get user inputs
            num_columns = column_spinner.get_value_as_int()
            margin_size = margin_spinner.get_value()
            margin_unit = margin_unit_combo.get_active_text()
            gutter_width = gutter_spinner.get_value()
            gutter_unit = gutter_unit_combo.get_active_text()
            delete_guides = delete_guides_check.get_active()

            Gimp.message(f"Number of Columns: {num_columns}, Margin: {margin_size} {margin_unit}, Gutter: {gutter_width} {gutter_unit}, Delete Guides: {delete_guides}")

            # Get image dimensions
            image_width = image.get_width()
            image_height = image.get_height()
            Gimp.message(f"Image Dimensions - Width: {image_width}, Height: {image_height}")

            success, dpi_x, dpi_y = image.get_resolution()
            if not success:
                dpi_x = dpi_y = 72.0
                Gimp.message("Warning: Resolution not found. Defaulting to 72 DPI.")
            else:
                Gimp.message(f"DPI - X: {dpi_x}, Y: {dpi_y}")

            # Conversion function
            def convert_to_pixels(value, unit, dpi):
                if unit == "inches":
                    return int(value * dpi)
                elif unit == "mm":
                    return int(value * dpi / 25.4)
                else:
                    return int(value)

            # Convert margin and gutter to pixels
            margin_px = convert_to_pixels(margin_size, margin_unit, dpi_x)
            gutter_px = convert_to_pixels(gutter_width, gutter_unit, dpi_x)
            Gimp.message(f"Margin in pixels: {margin_px}px, Gutter in pixels: {gutter_px}px")

            # Adjust usable width and height
            total_gutter_space = (num_columns - 1) * gutter_px
            usable_width = image_width - 2 * margin_px - total_gutter_space
            usable_height = image_height - 2 * margin_px

            if usable_width <= 0 or usable_height <= 0:
                Gimp.message("Invalid margin or gutter size! It leaves no usable space.")
                dialog.destroy()
                return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

            # Delete existing guides if checkbox is selected
            if delete_guides:
                Gimp.message("Deleting existing guides...")
                guide = image.find_next_guide(0)
                while guide != 0:
                    image.delete_guide(guide)
                    guide = image.find_next_guide(0)

            # Draw horizontal guides for margins (top and bottom)
            image.add_hguide(margin_px)  # Top margin
            image.add_hguide(image_height - margin_px)  # Bottom margin
            Gimp.message("Added top and bottom margin guides.")

            # Draw vertical guides for margins (left and right)
            image.add_vguide(margin_px)  # Left margin
            image.add_vguide(image_width - margin_px)  # Right margin
            Gimp.message("Added left and right margin guides.")

            # Draw vertical guides for columns and gutters
            column_width = usable_width / num_columns
            for i in range(num_columns):
                start_x = int(margin_px + i * (column_width + gutter_px))
                image.add_vguide(start_x)  # Left side of the column
                if i < num_columns - 1:
                    gutter_start = int(start_x + column_width)
                    image.add_vguide(gutter_start)  # Start of the gutter
                    Gimp.message(f"Added gutter guide at {gutter_start}px")

            Gimp.message(f"Grid Genius: {num_columns} columns with margins and gutters applied!")
        else:
            Gimp.message("Grid Genius: User cancelled.")
        dialog.destroy()

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

# Register the plugin
Gimp.main(GridGenius.__gtype__, sys.argv)
