# CSE_35_SmartClassRoomAndTimeTableScheduler

## Smart Classroom & Timetable Scheduler

A Python-based automated solution designed to solve the complex task of scheduling academic timetables. This project uses **constraint satisfaction logic** to assign faculty members to subjects and time slots while ensuring **no conflicts occur** and **resource utilization is optimized**.

---

## 🚀 Features

- **Automated Scheduling:**  
  Generates conflict-free timetables for multiple subjects and faculty members.

- **Conflict Management:**  
  Ensures faculty are not double-booked and subjects meet their weekly hour requirements.

- **Web Interface:**  
  A simple Flask web application (`app.py`) to interact with the scheduler.

- **Data Driven:**  
  Uses CSV files (`faculty.csv`, `subjects.csv`) to easily manage input data.

- **PDF Generation:**  
  Includes a utility to export the final schedules into a readable PDF format.

- **Notebook Integration:**  
  Includes a Jupyter Notebook for testing logic and data visualization.

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Web Framework:** Flask  
- **Data Handling:** Pandas / CSV  
- **Environment:** Jupyter Notebook (for development and analysis)  
- **Documentation:** IEEE Standard documentation and Project Review presentation  

---

## 📁 Repository Structure

| File Name | Description |
|----------|------------|
| `app.py` | The main entry point for the Flask web application |
| `solver.py` | Contains the core logic and algorithms for timetable generation |
| `pdf_generator.py` | Handles the conversion of generated schedules into PDF files |
| `TimetableScheduler.ipynb` | Interactive notebook for prototyping the scheduling algorithm |
| `faculty.csv` | Dataset containing faculty names, IDs, and specializations |
| `subjects.csv` | Dataset containing subject names, codes, and weekly credit hours |
| `CSE_35_IEEE1.docx` | Formal project documentation following IEEE standards |
| `CSE_35_Review5.pptx` | Presentation slides for project reviews |

---

## ⚙️ Installation & Usage

### 1. Setup and Run the Project

#### Clone the Repository
```bash
git clone https://github.com/Bhargavi872004/CSE_35_SmartClassRoomAndTimeTableScheduler.git
cd CSE_35_SmartClassRoomAndTimeTableScheduler
Install Dependencies

(Ensure Python is installed)

pip install flask pandas reportlab
Run the Application
python app.py

The app will typically be available at:
http://127.0.0.1:5000

📊 How It Works
Input:
The system reads the subject requirements and faculty availability from the CSV files.
Processing:
The solver.py script applies constraints (e.g., maximum hours per day, avoiding overlapping slots).
Output:
The result is displayed via the web UI and can be exported as a PDF for distribution.
👩‍💻 Authors
Bhargavi K
Bhargavi N
Rahul K M
