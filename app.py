import streamlit as st
import pandas as pd

from solver import generate_timetable
from validator import validate_inputs
from pdf_generator import generate_section_pdf, generate_faculty_pdf

st.set_page_config(
    page_title="AI Academic Timetable Generator",
    layout="wide"
)

st.title("🎓 AI Academic Timetable Generator")

st.markdown("---")

# ---------------- SIDEBAR ---------------- #

st.sidebar.header("Upload Input Files")

subjects_file = st.sidebar.file_uploader(
    "Upload subjects.csv", type=["csv"]
)

faculty_file = st.sidebar.file_uploader(
    "Upload faculty.csv", type=["csv"]
)

sections = st.sidebar.number_input(
    "Number of Sections",
    min_value=1,
    max_value=10,
    value=4
)

generate_button = st.sidebar.button("Generate Timetable")

# ---------------- SESSION STATE ---------------- #

if "generated" not in st.session_state:
    st.session_state.generated = False

# ---------------- GENERATE TIMETABLE ---------------- #

if generate_button:

    if subjects_file and faculty_file:

        subjects_df = pd.read_csv(subjects_file)
        faculty_df = pd.read_csv(faculty_file)

        valid, message = validate_inputs(subjects_df)

        if not valid:

            st.error(message)

        else:

            status, solver, X, subjects, DAYS, SLOTS, LUNCH_SLOT, SECTIONS = generate_timetable(
                subjects_df,
                faculty_df,
                sections
            )

            if status:

                st.success("✅ Timetable Generated Successfully")

                DAY_NAMES = ["Mon","Tue","Wed","Thu","Fri"]
                COLUMN_NAMES = ["S1","S2","S3","S4","LUNCH","S6","S7","S8"]

                section_tables = {}

                for sec in SECTIONS:

                    table_data = []

                    for d in DAYS:

                        row = []

                        for s in SLOTS:

                            if s == LUNCH_SLOT:

                                row.append("LUNCH")

                            else:

                                value = "FREE"

                                for sub in subjects:

                                    if solver.Value(X[(sec,d,s,sub)]) == 1:
                                        value = sub
                                        break

                                row.append(value)

                        table_data.append(row)

                    df = pd.DataFrame(
                        table_data,
                        index=DAY_NAMES,
                        columns=COLUMN_NAMES
                    )

                    section_tables[sec] = df

                generate_section_pdf(section_tables)

                # ---------- FACULTY TABLES ---------- #

                faculty_of = {}

                for _, row in faculty_df.iterrows():

                    for sub in row["subjects"].split(","):

                        faculty_of[sub.strip()] = row["faculty_id"]

                faculties = set(faculty_of.values())

                faculty_tables = {}

                for fac in faculties:

                    table = []

                    for d in DAYS:

                        row = []

                        for s in SLOTS:

                            if s == LUNCH_SLOT:

                                row.append("LUNCH")

                            else:

                                value = "--"

                                for sec in SECTIONS:

                                    for sub in subjects:

                                        if faculty_of[sub] == fac and solver.Value(X[(sec,d,s,sub)]) == 1:

                                            value = f"SEC-{sec+1}"

                                row.append(value)

                        table.append(row)

                    df = pd.DataFrame(
                        table,
                        index=DAY_NAMES,
                        columns=COLUMN_NAMES
                    )

                    faculty_tables[fac] = df

                generate_faculty_pdf(faculty_tables)

                st.session_state.generated = True
                st.session_state.section_tables = section_tables
                st.session_state.faculty_tables = faculty_tables

            else:

                st.error("❌ No feasible solution found. Reduce number of sections.")

    else:

        st.warning("Please upload both CSV files.")

# ---------------- DISPLAY DASHBOARD ---------------- #

if st.session_state.generated:

    tab1, tab2 = st.tabs(["📚 Section Timetables", "👩‍🏫 Faculty Timetables"])

    # ---------- SECTION TAB ---------- #

    with tab1:

        for sec, df in st.session_state.section_tables.items():

            st.subheader(f"Section {sec+1}")

            def color_cells(val):

                if val == "LUNCH":
                    return "background-color:#FFA726;color:white"

                if val == "FREE":
                    return "background-color:#ECEFF1"

                return "background-color:#64B5F6;color:white"

            st.dataframe(
                df.style.map(color_cells),
                use_container_width=True
            )

    # ---------- FACULTY TAB ---------- #

    with tab2:

        for fac, df in st.session_state.faculty_tables.items():

            st.subheader(f"Faculty {fac}")

            def color_cells(val):

                if val == "LUNCH":
                    return "background-color:#FFA726;color:white"

                if val == "--":
                    return "background-color:#ECEFF1"

                return "background-color:#81C784;color:black"

            st.dataframe(
                df.style.map(color_cells),
                use_container_width=True
            )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        with open("Sections_timetable.pdf", "rb") as file:

            st.download_button(
                "Download Section Timetable PDF",
                file,
                file_name="Sections_timetable.pdf"
            )

    with col2:

        with open("faculty_timetables.pdf", "rb") as file:

            st.download_button(
                "Download Faculty Timetable PDF",
                file,
                file_name="faculty_timetables.pdf"
            )