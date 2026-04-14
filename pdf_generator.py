from reportlab.platypus import SimpleDocTemplate, Table, Spacer
from reportlab.lib.pagesizes import A4


def generate_section_pdf(section_tables):

    elements = []

    for sec, df in section_tables.items():

        data = [df.columns.tolist()] + df.values.tolist()

        table = Table(data)

        elements.append(table)
        elements.append(Spacer(1,20))

    doc = SimpleDocTemplate("Sections_timetable.pdf", pagesize=A4)

    doc.build(elements)


def generate_faculty_pdf(faculty_tables):

    elements = []

    for fac, df in faculty_tables.items():

        data = [df.columns.tolist()] + df.values.tolist()

        table = Table(data)

        elements.append(table)
        elements.append(Spacer(1,20))

    doc = SimpleDocTemplate("faculty_timetables.pdf", pagesize=A4)

    doc.build(elements)