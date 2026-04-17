🎓 CSE_35 Smart Classroom & Timetable Scheduler

🚀 A Python-based system to automatically generate conflict-free academic timetables using constraint satisfaction logic.

✨ Features
🧠 Automated Scheduling
Generates optimized, conflict-free timetables.
⚠️ Conflict Management
Prevents faculty double-booking and ensures required hours.
🌐 Web Interface
Built with Flask (app.py) for easy interaction.
📊 Data Driven
Uses CSV files (faculty.csv, subjects.csv).
📄 PDF Generation
Export schedules into clean PDF format.
📓 Notebook Support
Includes Jupyter Notebook for testing and analysis.
🛠️ Tech Stack
Category	Technology
Language	Python
Framework	Flask
Data	Pandas / CSV
Environment	Jupyter Notebook
📂 Project Structure
CSE_35_SmartClassRoomAndTimeTableScheduler/
│── app.py
│── solver.py
│── pdf_generator.py
│── TimetableScheduler.ipynb
│── faculty.csv
│── subjects.csv
│── CSE_35_IEEE1.docx
│── CSE_35_Review5.pptx
⚙️ Installation & Usage
🧩 Step 1: Clone Repository
git clone https://github.com/Bhargavi872004/CSE_35_SmartClassRoomAndTimeTableScheduler.git
cd CSE_35_SmartClassRoomAndTimeTableScheduler
📦 Step 2: Install Dependencies
pip install flask pandas reportlab
▶️ Step 3: Run Application
python app.py

🔗 Open in browser:
http://127.0.0.1:5000

🔍 How It Works
Input: Reads subject + faculty data from CSV
Processing: Applies scheduling constraints
Output: Displays timetable + PDF export
👩‍💻 Authors
Bhargavi K
Bhargavi N
Rahul K M
