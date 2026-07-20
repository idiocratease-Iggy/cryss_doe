import openpyxl

def write_experiment_excel(experiments, filename):
    """
    Minimal Excel writer so your wizard can run.
    Writes a simple sheet with experiment fields.
    """

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Experiments"

    # Header row
    ws.append([
        "ID", "Origin ID", "Origin Plate Ref",
        "Starting Mix", "Solvent", "Volume", "Salt Former",
        "Replicate Status", "Plate", "Well", "Notes"
    ])

    # Data rows
    for exp in experiments:
        ws.append([
            exp.id,
            exp.origin_id,
            exp.origin_plate_ref,
            exp.starting_mix,
            exp.solvent,
            exp.volume,
            exp.salt_former,
            exp.replicate_status,
            exp.plate,
            exp.well,
            exp.notes,
        ])

    wb.save(filename)
