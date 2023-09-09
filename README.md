# Store-of-boxes

## Description

This API service provides functionality for managing a store's inventory of cuboid boxes. Each box has dimensions (length, breadth, height) and is associated with a store employee who is the creator of the box. The API allows for adding, updating, listing, and deleting boxes, along with various permissions and filters.

## Getting Started

### Prerequisites

- Python
- Django
- Django REST framework


### Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   
Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt
Run the Django development server:
python manage.py runserver
Access the API at http://localhost:8000/api/ (or as configured).


API Endpoints
Add API - POST /api/boxes/add/
Update API - PUT /api/boxes/update/{box_id}/
List All API - GET /api/boxes/
List My Boxes API - GET /api/boxes/mine/
Delete API - DELETE /api/boxes/delete/{box_id}/
Permissions
To add a box, the user must be logged in and have staff privileges.
To update a box, any staff user can do so, but the creator and creation date cannot be changed.
Any user can list all boxes in the store.
Only staff users can see the "Created By" and "Last Updated" fields in the list.
Various filters are available for listing boxes.
Configuration
Average area of all added boxes should not exceed A1 (default: 100).
Average volume of all boxes added by a user should not exceed V1 (default: 1000).
Total boxes added in a week should not exceed L1 (default: 100).
Total boxes added in a week by a user should not exceed L2 (default: 50).


Contact
prabhrati17@gmail.com


