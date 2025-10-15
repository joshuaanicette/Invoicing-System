ED Invoicing System
Overview
The ED Invoicing System is a web-based application designed to simplify invoicing for businesses and freelancers. It offers a user-friendly interface for creating, managing, and tracking invoices.
Features

Invoice Creation: Generate professional invoices with customizable fields.
Client Management: Store and organize client information.
Payment Tracking: Monitor invoice statuses (e.g., paid, pending, overdue).
Responsive Design: Accessible on desktop and mobile devices.
Secure Hosting: Deployed on Vercel for reliable performance.

Technologies Used

Frontend: React.js, Tailwind CSS
Backend: Python with Flask
Database: SQLite
Deployment: Vercel
Other: (Add any additional libraries, e.g., Requests for API calls, Flask-RESTful for API endpoints)

Getting Started
Prerequisites

Node.js (v16 or higher) for frontend
Python (v3.8 or higher) for backend
npm or yarn
A Vercel account for deployment (optional)

Installation

Clone the Repository:
``bash
git clone https://github.com/your-username/ed-invoicing-system.git
cd ed-invoicing-system
``

Install Frontend Dependencies:


``bash
npm install
``

or

``bash
yarn install
``

Install Backend Dependencies: Assuming a requirements.txt file for Flask and SQLite:
``bash
pip install -r requirements.txt
``

Configure Environment Variables: Create a .env file in the root directory and add necessary variables (e.g., database path, API keys). Example:
``bash
DATABASE_URL=sqlite:///invoices.db
API_KEY=your_api_key
FLASK_ENV=development
``

Initialize the Database:Ensure the SQLite database (invoices.db) is set up. If your Flask app includes an initialization script:

``bash 
python init_db.py
``
Or manually create the database tables as per your Flask app's setup.

Run the Backend:

``bash
python app.py
``

The Flask backend will typically run on http://localhost:5000.

Run the Frontend:In a separate terminal:

``bash
npm run dev
``

or

``bash
yarn dev
``

The frontend will be available at http://localhost:3000.


Deployment
To deploy on Vercel:

Push your code to a GitHub repository.
For the frontend, connect the repository to Vercel via the Vercel dashboard.

For the Flask backend with SQLite, deploy to a platform supporting Python and persistent storage (e.g., Heroku, Render, or a Vercel serverless setup with adjustments for SQLite).

Configure environment variables in Vercel or your backend hosting platform (e.g., DATABASE_URL=sqlite:///invoices.db).

Deploy the app, and access it at a URL like https://ed-s-invoicing-system-2.vercel.app/ 

Note: SQLite may require special consideration for deployment (e.g., persistent storage or switching to a cloud database like PostgreSQL for production).

Usage

Create an Invoice:

Navigate to the "New Invoice" section.
Fill in client details, items, and payment terms.
Save or send the invoice directly to the client.


Manage Clients:

Add new clients in the "Clients" section.
View and edit client details as needed.


Track Payments:

Check the "Dashboard" for an overview of invoice statuses.
Filter invoices by status (e.g., paid, pending).



Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes and commit (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or support, contact your-email@example.com or open an issue on GitHub.
