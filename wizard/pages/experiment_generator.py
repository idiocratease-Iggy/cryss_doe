from dataclasses import dataclass
from typing import Optional


@dataclass
class Experiment:
    id: str                      # EXP001, EXP002, ...
    origin_id: str               # permanent ID of base experiment
    origin_plate_ref: Optional[str]  # e.g. "Plate1.A1" or "Plate1.001"
    starting_mix: int
    solvent: str
    volume: float
    salt_former: Optional[str]   # None for salt-free
    replicate_status: str        # "Base", "Replicate", "Extra replicate"
    plate: Optional[str] = None  # "Plate1", "Plate2", ...
    well: Optional[str] = None   # "A1" or "001"
    notes: str = ""

import math
import random


def generate_experiments(design) -> list[Experiment]:
    """
    design: your DesignModel instance, already filled by the wizard.
    Returns: list of Experiment objects.
    """

    experiments: list[Experiment] = []

    # -----------------------------
    # STEP 1: BASE COMBINATIONS (X)
    # -----------------------------
    starting_mixtures = range(1, design.number_of_starting_mixtures + 1)
    solvents = design.selected_solvents              # list of names
    volumes = design.volume_levels                   # e.g. [0.5, 1.0, 2.0]
    salt_formers = design.selected_salt_formers      # list of names (may be empty)

    include_salt_free = design.include_salt_free_set

    if not salt_formers:
        # Your logic: treat as 1 "salt former" and force salt-free set
        salt_formers = []
        include_salt_free = True

    base_id_counter = 1

    for mix in starting_mixtures:
        for solvent in solvents:
            for vol in volumes:
                # salt-free set
                if include_salt_free:
                    exp = Experiment(
                        id=f"EXP{base_id_counter:03d}",
                        origin_id=f"EXP{base_id_counter:03d}",
                        origin_plate_ref=None,
                        starting_mix=mix,
                        solvent=solvent,
                        volume=vol,
                        salt_former=None,
                        replicate_status="Base",
                    )
                    experiments.append(exp)
                    base_id_counter += 1

                # salt-former sets
                for salt in salt_formers:
                    exp = Experiment(
                        id=f"EXP{base_id_counter:03d}",
                        origin_id=f"EXP{base_id_counter:03d}",
                        origin_plate_ref=None,
                        starting_mix=mix,
                        solvent=solvent,
                        volume=vol,
                        salt_former=salt,
                        replicate_status="Base",
                    )
                    experiments.append(exp)
                    base_id_counter += 1

    # At this point, experiments = BaseExperiments (X + X*NoSaltFormers)

    # -----------------------------
    # STEP 2: REPLICATE PERCENTAGE
    # -----------------------------
    replicate_pct = design.replicate_percentage  # e.g. 0.33 for 33%

    if replicate_pct > 0:
        base_exps = experiments.copy()
        extra_reps: list[Experiment] = []

        # total extra replicates (approx)
        total_extra = round(len(base_exps) * replicate_pct)

        # simple strategy: sample with replacement
        for i in range(total_extra):
            parent = random.choice(base_exps)
            rep = Experiment(
                id=f"{parent.id}R{i+1}",
                origin_id=parent.origin_id,
                origin_plate_ref=parent.origin_plate_ref,
                starting_mix=parent.starting_mix,
                solvent=parent.solvent,
                volume=parent.volume,
                salt_former=parent.salt_former,
                replicate_status="Replicate",
                notes=parent.notes,
            )
            extra_reps.append(rep)

        experiments.extend(extra_reps)

    # -----------------------------
    # STEP 3: PLATE FILLING
    # -----------------------------
    plate_rows = design.plate_rows
    plate_cols = design.plate_cols
    fill_to_full = design.fill_to_full_plates

    no_react = plate_rows * plate_cols
    no_expts_base_case = len(experiments)

    no_plates = math.ceil(no_expts_base_case / no_react)
    total_wells = no_plates * no_react
    no_uur = total_wells - no_expts_base_case

    if fill_to_full and no_uur > 0:
        extra_fill_reps: list[Experiment] = []
        for i in range(no_uur):
            parent = random.choice(experiments)  # any existing experiment
            rep = Experiment(
                id=f"{parent.id}F{i+1}",
                origin_id=parent.origin_id,
                origin_plate_ref=parent.origin_plate_ref,
                starting_mix=parent.starting_mix,
                solvent=parent.solvent,
                volume=parent.volume,
                salt_former=parent.salt_former,
                replicate_status="Extra replicate (plate filling)",
                notes=parent.notes,
            )
            extra_fill_reps.append(rep)

        experiments.extend(extra_fill_reps)

    # -----------------------------
    # STEP 4: RANDOMIZATION
    # -----------------------------
    if design.randomize_design:
        random.shuffle(experiments)

    # -----------------------------
    # STEP 5: PLATE + WELL ASSIGNMENT
    # -----------------------------
    use_free_format = design.free_format  # True if user chose free format

    def generate_fixed_wells(rows, cols):
        wells = []
        import string
        for r in range(rows):
            row_label = string.ascii_uppercase[r]
            for c in range(cols):
                col_label = c + 1
                wells.append(f"{row_label}{col_label}")
        return wells

    def generate_free_wells(rows, cols):
        wells = []
        total = rows * cols
        for i in range(1, total + 1):
            wells.append(f"{i:03d}")  # 001, 002, ...
        return wells

    all_wells = generate_free_wells(plate_rows, plate_cols) if use_free_format \
                else generate_fixed_wells(plate_rows, plate_cols)
    
   

    exp_index = 0
    for plate_idx in range(1, no_plates + 1):
        plate_name = f"Plate{plate_idx}"
        for well in all_wells:
            if exp_index >= len(experiments):
                break
            exp = experiments[exp_index]
            exp.plate = plate_name
            exp.well = well

            # set origin_plate_ref for base experiments if not yet set
            if exp.replicate_status == "Base" and exp.origin_plate_ref is None:
                exp.origin_plate_ref = f"{plate_name}.{well}"

            exp_index += 1

    return experiments
