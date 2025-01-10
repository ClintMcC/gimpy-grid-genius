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
            "Grid Genius: Modular Grid with Margins",
            "Creates evenly distributed vertical columns and horizontal rows with optional gutters and margins.",
            name
        )
        procedure.set_attribution("Your Name", "Your License", "2025")
        return procedure

    def create_dialog(self):
        """Creates and returns the dialog layout with user input fields."""
        dialog = GimpUi.Dialog(title="Grid Genius: Modular Grid with Margins", role="grid-genius")
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_OK", Gtk.ResponseType.OK)

        # Main vertical box for layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        dialog.get_content_area().add(main_box)

        # --- Unified Grid for Inputs ---
        input_grid = Gtk.Grid(column_spacing=10, row_spacing=10)
        main_box.pack_start(input_grid, False, False, 0)

        # --- Section: Margins ---
        margin_section_label = Gtk.Label(label="Margins")
        margin_section_label.set_markup("<b>Margins</b>")
        margin_section_label.set_halign(Gtk.Align.START)
        input_grid.attach(margin_section_label, 0, 0, 2, 1)

        # Margin Inputs
        margin_labels = ["Top/Bottom Margin:", "Left/Right Margin:"]
        margin_spinners = []
        for i, label_text in enumerate(margin_labels):
            margin_label = Gtk.Label(label=label_text)
            margin_label.set_halign(Gtk.Align.END)
            margin_spinner = Gtk.SpinButton()
            margin_spinner.set_adjustment(Gtk.Adjustment(0.0, 0.0, 1000.0, 1.0))
            margin_spinner.set_value(0)
            margin_unit_combo = Gtk.ComboBoxText()
            for unit in ["px", "inches", "mm"]:
                margin_unit_combo.append_text(unit)
            margin_unit_combo.set_active(0)
            input_grid.attach(margin_label, 0, i + 1, 1, 1)
            input_grid.attach(margin_spinner, 1, i + 1, 1, 1)
            input_grid.attach(margin_unit_combo, 2, i + 1, 1, 1)
            margin_spinners.append((margin_spinner, margin_unit_combo))

        # --- Section: Column Grid ---
        column_grid_label = Gtk.Label(label="Column Grid")
        column_grid_label.set_markup("<b>Column Grid</b>")
        column_grid_label.set_halign(Gtk.Align.START)
        input_grid.attach(column_grid_label, 0, 3, 2, 1)

        # Number of Columns
        column_label = Gtk.Label(label="Number of Columns:")
        column_label.set_halign(Gtk.Align.END)
        column_spinner = Gtk.SpinButton()
        column_spinner.set_adjustment(Gtk.Adjustment(1, 1, 100, 1))
        column_spinner.set_value(3)
        input_grid.attach(column_label, 0, 4, 1, 1)
        input_grid.attach(column_spinner, 1, 4, 1, 1)

        # Gutter Width (Columns)
        gutter_label = Gtk.Label(label="Vertical Gutter Width:")
        gutter_label.set_halign(Gtk.Align.END)
        gutter_spinner = Gtk.SpinButton()
        gutter_spinner.set_adjustment(Gtk.Adjustment(0.0, 0.0, 1000.0, 0.1))
        gutter_spinner.set_value(0)
        gutter_unit_combo = Gtk.ComboBoxText()
        for unit in ["px", "inches", "mm"]:
            gutter_unit_combo.append_text(unit)
        gutter_unit_combo.set_active(0)
        input_grid.attach(gutter_label, 0, 5, 1, 1)
        input_grid.attach(gutter_spinner, 1, 5, 1, 1)
        input_grid.attach(gutter_unit_combo, 2, 5, 1, 1)

        # --- Section: Row Grid ---
        row_grid_label = Gtk.Label(label="Row Grid")
        row_grid_label.set_markup("<b>Row Grid</b>")
        row_grid_label.set_halign(Gtk.Align.START)
        input_grid.attach(row_grid_label, 0, 6, 2, 1)

        # Number of Rows
        row_label = Gtk.Label(label="Number of Rows:")
        row_label.set_halign(Gtk.Align.END)
        row_spinner = Gtk.SpinButton()
        row_spinner.set_adjustment(Gtk.Adjustment(1, 1, 100, 1))
        row_spinner.set_value(3)
        input_grid.attach(row_label, 0, 7, 1, 1)
        input_grid.attach(row_spinner, 1, 7, 1, 1)

        # Gutter Height (Rows)
        flowline_label = Gtk.Label(label="Horizontal Gutter Height:")
        flowline_label.set_halign(Gtk.Align.END)
        flowline_spinner = Gtk.SpinButton()
        flowline_spinner.set_adjustment(Gtk.Adjustment(0.0, 0.0, 1000.0, 0.1))
        flowline_spinner.set_value(0)
        flowline_unit_combo = Gtk.ComboBoxText()
        for unit in ["px", "inches", "mm"]:
            flowline_unit_combo.append_text(unit)
        flowline_unit_combo.set_active(0)
        input_grid.attach(flowline_label, 0, 8, 1, 1)
        input_grid.attach(flowline_spinner, 1, 8, 1, 1)
        input_grid.attach(flowline_unit_combo, 2, 8, 1, 1)

        # --- Checkbox for Deleting Existing Guides ---
        delete_guides_check = Gtk.CheckButton(label="Delete Existing Guides")
        delete_guides_check.set_active(True)  # Default to checked
        input_grid.attach(delete_guides_check, 0, 9, 2, 1)

        dialog.get_content_area().show_all()

        return dialog, column_spinner, gutter_spinner, gutter_unit_combo, row_spinner, flowline_spinner, flowline_unit_combo, delete_guides_check, margin_spinners

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        Gimp.message("Starting Grid Genius plugin...")

        # Create the dialog and get widgets
        dialog, column_spinner, gutter_spinner, gutter_unit_combo, row_spinner, flowline_spinner, flowline_unit_combo, delete_guides_check, margin_spinners = self.create_dialog()

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            # Get user inputs
            num_columns = column_spinner.get_value_as_int()
            gutter_width = gutter_spinner.get_value()
            gutter_unit = gutter_unit_combo.get_active_text()
            num_rows = row_spinner.get_value_as_int()
            flowline_height = flowline_spinner.get_value()
            flowline_unit = flowline_unit_combo.get_active_text()
            delete_guides = delete_guides_check.get_active()

            # Margins
            top_bottom_margin = margin_spinners[0][0].get_value()
            top_bottom_unit = margin_spinners[0][1].get_active_text()
            left_right_margin = margin_spinners[1][0].get_value()
            left_right_unit = margin_spinners[1][1].get_active_text()

            Gimp.message(f"Columns: {num_columns}, Rows: {num_rows}, Vertical Gutter: {gutter_width} {gutter_unit}, Horizontal Gutter: {flowline_height} {flowline_unit}, Margins: {top_bottom_margin}px TB, {left_right_margin}px LR")

            # Get image dimensions
            image_width = image.get_width()
            image_height = image.get_height()
            success, dpi_x, dpi_y = image.get_resolution()
            if not success:
                dpi_x = dpi_y = 72.0

            def convert_to_pixels(value, unit, dpi):
                if unit == "inches":
                    return int(value * dpi)
                elif unit == "mm":
                    return int(value * dpi / 25.4)
                else:
                    return int(value)

            # Convert margins and gutters to pixels
            margin_tb_px = convert_to_pixels(top_bottom_margin, top_bottom_unit, dpi_y)
            margin_lr_px = convert_to_pixels(left_right_margin, left_right_unit, dpi_x)
            gutter_px = convert_to_pixels(gutter_width, gutter_unit, dpi_x)
            flowline_px = convert_to_pixels(flowline_height, flowline_unit, dpi_y)

            if delete_guides:
                Gimp.message("Deleting existing guides...")
                guide = image.find_next_guide(0)
                while guide != 0:
                    image.delete_guide(guide)
                    guide = image.find_next_guide(0)

            # Draw margins
            image.add_hguide(margin_tb_px)
            image.add_hguide(image_height - margin_tb_px)
            image.add_vguide(margin_lr_px)
            image.add_vguide(image_width - margin_lr_px)

            # Usable width and height
            usable_width = image_width - 2 * margin_lr_px - (num_columns - 1) * gutter_px
            usable_height = image_height - 2 * margin_tb_px - (num_rows - 1) * flowline_px

            if usable_width <= 0 or usable_height <= 0:
                Gimp.message("Invalid margin or gutter size! It leaves no usable space.")
                dialog.destroy()
                return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

            # Draw vertical guides for columns
            column_width = usable_width / num_columns
            for i in range(num_columns):
                start_x = int(margin_lr_px + i * (column_width + gutter_px))
                image.add_vguide(start_x)
                if i < num_columns - 1:
                    image.add_vguide(int(start_x + column_width))

            # Draw horizontal guides for rows
            row_height = usable_height / num_rows
            for j in range(num_rows):
                start_y = int(margin_tb_px + j * (row_height + flowline_px))
                image.add_hguide(start_y)
                if j < num_rows - 1:
                    image.add_hguide(int(start_y + row_height))

            Gimp.message(f"Grid Genius: {num_columns} columns and {num_rows} rows with margins applied.")
        else:
            Gimp.message("Grid Genius: User cancelled.")
        dialog.destroy()

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

# Register the plugin
Gimp.main(GridGenius.__gtype__, sys.argv)
