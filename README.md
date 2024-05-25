# Identity Reconciliation

## Project Overview
This project is a Flask-based web application that serves as APIs for identifying and keeping track of a customer's identity across multiple purchases. 
The application uses SQLAlchemy for database interactions and Flask-RESTful for creating RESTful APIs. 
It also leverages Jinja2 for templating and Flask-CORS for handling Cross-Origin Resource Sharing.

## Hosted Endpoint
- The API is hosted and can be accessed at the following endpoint (please check the assumptions below):
[https://identityreconciliation-qf86.onrender.com]
- Use /identity to access the identity endpoint.
[https://identityreconciliation-qf86.onrender.com/identity]

## Features
- **RESTful API Endpoints:** Provides API endpoints to manage contact data.
- **Database Integration:** Uses PostgreSQL for storing contact information.
- **Data Processing:** Implements BFS algorithm to search for contacts with matching emails or phone numbers.
- **Environment Configuration:** Utilizes environment variables for database configuration.
- **Cross-Origin Resource Sharing:** Supports CORS to allow requests from different origins.
- **ORM:** Uses Object Relational Mapping for easy DB access and avoid using SQL scripts in code.

## Environment Variables
Created a `.env` file in the root directory and include the following variables:

- DB_SERVER=pg_datacenter
- DB_NAME=db_distributed
- DB_USERNAME=postgres
- DB_PASSWORD=yourpassword
- DB_PORT=5432
- DB_HOST=localhost
- DB_CONN_STRING
- CONTACT_TABLE=contact_table_name
- SCHEMA=schema_name
- PRIMARY=primary (name for primary contacts)
- SECONDARY=secondary (name for secondary contacts)

## Application Structure
- **app.py:** Main application file which starts the flask server.
- **model:** Data transfer models.
- **entity:** Map objects to DB tables. Used for setting up ORM
- **api:** API layer. Defines API endpoints.
- **service:** Service layer. Interacts with DAO layer and implements business logic.
- **DAO:** DAO (Data Access Object Layer). Interacts with database.
- **templates/**: Directory containing Jinja2 templates.

## API Endpoints
### `/`
- **Description:** Home route to confirm the application is running.
- **Method:** GET
- **Response:** Welcome message indicating the server and database in use.

### `/contacts`
- **Description:** Endpoint to manage contacts.
- **Method:** POST
- **Request Body:** JSON with `email` and `phoneNumber`.
- **Response:** JSON with the processed contact information.

## Business Logic
Implemented a three layer approach (maybe over-engineered a little) to keep API, Business and Data Access seperate.

### BFS Contact Search
The solution implements a BFS algorithm to search for records with matching emails or phone numbers and return all related records.

### Contact Linking
- **Primary Contact:** The first contact in a linked group.
- **Secondary Contact:** Contacts linked to the primary contact based on email or phone number matches.
- **Link Precedence:** Determines the primary and secondary contacts in a linked group.

### Assumptions
The problem statement was a bit open-ended so used the following assumptions to build the solution:
- Assumption 1: When primary contact turns into secondary contact, all other contacts which had that contact as primary now points to the oldest contact which is primary.
- Assumption 2: When request comes, all contacts are linked by common email or number. But contacts are also linked if they have linkedId as the oldest id (same as primary).

## How to Run
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   
2. **Run the Application:**
   ```bash
    python app.py

## Contact
For any issues or inquiries, please contact:
- Name: Yash Pathak
- Email: yashpathak115@gmail.com