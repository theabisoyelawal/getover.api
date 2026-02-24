GetOver API 
A robust Task Management API built with Django REST Framework (DRF). This project implements specific business rules to handle task lifecycles, user authentication, and data integrity.

* Key Features & Business Logic
1. Task Locking Mechanism: To ensure data integrity, any task marked with status="Completed" becomes read-only. Users cannot update or delete completed tasks.

2. Date Integrity: Custom validation prevents the creation of tasks with a due_date in the past.

3. Multi-Level Filtering: Users can filter tasks by status (Pending/Completed) and priority (Low/Medium/High).

4. Dynamic Sorting: Supports ordering by due_date to highlight upcoming deadlines.

5. Security: All endpoints are protected by Token Authentication. Users can only access tasks they created.

*  API Endpoints & Usage
1. Authentication
2. Task Management (Requires Token Header)
Authorization: Token <your token>

*  Local Installation
1. Clone the Repo
git clone 
cd getover

2. Setup Environment
python -m venv venv
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Initialize Database
python manage.py migrate

5. Run Project
python manage.py runserver

* Main Dependencies
Django

djangorestframework

django-filter (for the search/sort functionality)