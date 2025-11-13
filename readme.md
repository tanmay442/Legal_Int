# Legal_Int (Legal Integration)

## Project Overview

Modern judicial ecosystems are overwhelmed by an ever-expanding corpus of legal documents—case files, precedents, statutory updates, and procedural records. Courts and legal practitioners often operate with fragmented information, resulting in prolonged case cycles, inconsistent interpretations, and systemic inefficiencies. The inability to synthesize voluminous, heterogenous legal data in a timely manner exacerbates backlogs and undermines access to justice.

Legal_Int aims to address these challenges by providing a secure, role-based digital evidence locker and case management system. It allows legal and investigative professionals to collaborate on cases by uploading, viewing, and managing documents according to a strict set of permissions, thereby streamlining legal processes and improving access to justice.

## Setup and Running the Application

### Backend Setup

1.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Backend Server:**
    ```bash
    python backend/app/app.py
    ```
    The backend server will run on `http://127.0.0.1:5001`.

### Frontend Setup

1.  **Navigate to the Frontend Directory:**
    ```bash
    cd frontend
    ```
2.  **Install Node.js Dependencies:**
    ```bash
    npm install
    ```
3.  **Run the Frontend Development Server:**
    ```bash
    npm run dev
    ```
    The frontend development server will typically run on `http://localhost:5173`.

Once both servers are running, open your web browser and navigate to the frontend URL to access the Legal_Int application.
