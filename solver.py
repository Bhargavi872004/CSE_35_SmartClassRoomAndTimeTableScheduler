from ortools.sat.python import cp_model
import pandas as pd


def generate_timetable(subjects_df, faculty_df, sections):

    # -----------------------------
    # PARAMETERS
    # -----------------------------
    DAYS = range(5)
    SLOTS = range(8)
    LUNCH_SLOT = 4
    SECTIONS = range(sections)

    # -----------------------------
    # SUBJECT DATA
    # -----------------------------
    subjects = list(subjects_df["subject_code"])

    subject_hours = dict(
        zip(subjects_df["subject_code"], subjects_df["Total_hours"])
    )

    # -----------------------------
    # DIFFICULTY CALCULATION
    # -----------------------------
    subjects_df["raw_difficulty"] = (
        subjects_df["credits"] * subjects_df["failure rate"]
    )

    max_diff = subjects_df["raw_difficulty"].max()
    min_diff = subjects_df["raw_difficulty"].min()

    subjects_df["difficulty"] = (
        (subjects_df["raw_difficulty"] - min_diff) /
        (max_diff - min_diff)
    )

    subjects_df = subjects_df.sort_values(
        by="difficulty", ascending=False
    )

    difficult_subjects = subjects_df.head(2)["subject_code"].tolist()

    # -----------------------------
    # FACULTY MAP
    # -----------------------------
    faculty_of = {}

    for _, row in faculty_df.iterrows():
        for s in row["subjects"].split(","):
            faculty_of[s.strip()] = row["faculty_id"]

    faculties = set(faculty_of.values())

    # -----------------------------
    # MODEL
    # -----------------------------
    model = cp_model.CpModel()

    # Decision variables
    X = {}

    for sec in SECTIONS:
        for d in DAYS:
            for s in SLOTS:
                for sub in subjects:

                    X[(sec, d, s, sub)] = model.NewBoolVar(
                        f"x_s{sec}_d{d}_t{s}_{sub}"
                    )

    # --------------------------------------------------
    # CONSTRAINT 1: One subject per slot
    # --------------------------------------------------
    for sec in SECTIONS:
        for d in DAYS:
            for s in SLOTS:

                if s == LUNCH_SLOT:

                    model.Add(
                        sum(X[(sec, d, s, sub)] for sub in subjects) == 0
                    )

                else:

                    model.Add(
                        sum(X[(sec, d, s, sub)] for sub in subjects) <= 1
                    )

    # --------------------------------------------------
    # CONSTRAINT 2: Subject at most once per day
    # --------------------------------------------------
    for sec in SECTIONS:
        for d in DAYS:
            for sub in subjects:

                model.Add(
                    sum(X[(sec, d, s, sub)] for s in SLOTS) <= 1
                )

    # --------------------------------------------------
    # CONSTRAINT 3: Weekly hours exact
    # --------------------------------------------------
    for sec in SECTIONS:
        for sub in subjects:

            model.Add(
                sum(
                    X[(sec, d, s, sub)]
                    for d in DAYS
                    for s in SLOTS
                ) == subject_hours[sub]
            )

    # --------------------------------------------------
    # CONSTRAINT 4: Faculty clash
    # --------------------------------------------------
    for d in DAYS:
        for s in SLOTS:

            if s == LUNCH_SLOT:
                continue

            for fac in faculties:

                model.Add(
                    sum(
                        X[(sec, d, s, sub)]
                        for sec in SECTIONS
                        for sub in subjects
                        if faculty_of[sub] == fac
                    ) <= 1
                )

    # --------------------------------------------------
    # CONSTRAINT 5: Difficult subjects morning only
    # --------------------------------------------------
    for sub in difficult_subjects:

        for sec in SECTIONS:
            for d in DAYS:

                for s in range(LUNCH_SLOT + 1, 8):

                    model.Add(
                        X[(sec, d, s, sub)] == 0
                    )

    # --------------------------------------------------
    # SOLVER
    # --------------------------------------------------
    solver = cp_model.CpSolver()

    solver.parameters.max_time_in_seconds = 30
    solver.parameters.num_search_workers = 8

    status = solver.Solve(model)

    return (
        status,
        solver,
        X,
        subjects,
        DAYS,
        SLOTS,
        LUNCH_SLOT,
        SECTIONS
    )