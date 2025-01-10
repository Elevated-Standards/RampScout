import os
from openpyxl import load_workbook
import pandas as pd
from datetime import datetime

def write_to_excel(template_path, data_frames, column_mapping, output_dir):
    """
    Write processed data to an Excel template and save the file.

    :param template_path: Path to the Excel template.
    :param data_frames: List of DataFrames to consolidate and write.
    :param column_mapping: Mapping of DataFrame columns to Excel columns.
    :param output_dir: Directory to save the output file.
    """
    # Load the Excel template
    wb = load_workbook(template_path)
    sheet = wb["Inventory"]

    # Combine all DataFrames
    final_df = pd.concat(data_frames, ignore_index=True)
    final_df = final_df.rename(columns={v: k for k, v in column_mapping.items()})

    # Write data to the sheet
    for index, row in final_df.iterrows():
        for col, value in row.items():
            col_idx = list(column_mapping.keys()).index(col) + 1  # Excel is 1-indexed
            sheet.cell(row=index + 6, column=col_idx).value = value

    # Save the workbook
    save_workbook(wb, output_dir)

def save_workbook(wb, output_dir):
    """
    Save the workbook to the output directory with a timestamped filename.

    :param wb: The openpyxl workbook object.
    :param output_dir: Directory to save the file.
    """
    # Generate a dynamic save path
    current_date = datetime.now()
    save_path = os.path.join(output_dir, f"{current_date.year}/{current_date.month:02}-{current_date.day:02}-Inventory.xlsx")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Save the file
    wb.save(save_path)
    print(f"Excel file saved to: {save_path}")
