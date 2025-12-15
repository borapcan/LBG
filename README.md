# Django Glycan Database

## Overview
This Django application serves as a database for glycans, their monosaccharide compositions, associated species, and relevant scientific studies. It provides an intuitive admin interface for managing glycan-related data, allowing researchers and biologists to efficiently store, search, and analyze glycan structures and their biological significance.

### Features:
- **Comprehensive Glycan Database**: Store and manage glycans along with their structural resolution, mass, and associated species.
- **Monosaccharide Composition Tracking**: Keep track of individual glycan components like hexose, fucose, and sialic acid derivatives.
- **Species and Sublocations**: Categorize glycans based on species and anatomical sublocations.
- **Study Integration**: Link glycans to published research studies, including authors, journals, and DOIs.
- **Django Admin Panel**: A powerful web-based interface for managing the database.

## Prerequisites
Before running the project, ensure you have the following installed:

- Python (>= 3.8 recommended)
- Django (>= 4.0 recommended)
- **PostgreSQL** (>= 12 recommended) - Download and install from [PostgreSQL Official Site](https://www.postgresql.org/)
- Git (optional but useful for version control)

## Installation

### 1. Clone the Repository
```sh
git clone <your-repository-url>
cd <your-project-folder>
```

### 2. Create a Virtual Environment (Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure PostgreSQL Database

Ensure PostgreSQL is installed and running, then configure Django to connect to it.

#### 4.1 Install PostgreSQL
Download and install the **latest PostgreSQL version** from the official EnterpriseDB distribution:

https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

During installation:
- Ensure **pgAdmin 4** is selected (enabled by default)
- Remember the **postgres superuser password**, as it will be required later

After installation, start PostgreSQL and open **pgAdmin 4**.

---

#### 4.2 Create the database in pgAdmin 4

1. Open **pgAdmin 4**
2. Connect to your local PostgreSQL server (e.g. `PostgreSQL XX`)
3. Right-click **Databases** → **Create** → **Database**
4. Set:
   - **Database name:** `DB`
   - **Owner:** `postgres`
5. Click **Save**

The database `DB` should now appear in the list.

---

#### 4.3 Update Django database settings (based on your DB setup)

Update the `DATABASES` section in `settings.py` to match your local PostgreSQL setup:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "DB",
        "USER": "postgres",
        "PASSWORD": "admin",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


### 5. Apply Migrations
```sh
python manage.py migrate
```

### 6. Create a Superuser
This step is needed to access the Django Admin panel.
```sh
python manage.py createsuperuser
```
Follow the prompts to set up an admin username and password.

### 7. Run the Development Server
```sh
python manage.py runserver
```
The application should now be accessible at `http://127.0.0.1:8000/admin`.

## Using the Application
### Accessing the Admin Interface
1. Open `http://127.0.0.1:8000/admin/` in your web browser.
2. Log in with the superuser credentials you created earlier.
3. You can now manage species, glycan compositions, studies, and more.

### Importing Sample Glycan Data
To import initial 359 glycan dataset, you can run a custom import script. This script will process and load the data automatically into your database.

For Windows users, navigate to the script’s directory and run it as follows:
```sh
python import_all.py
```
This script will import all available glycan v0.9 data into your database. Ensure that the file path to the script is correct before running it. If needed, adjust the path based on where the script is stored on your system.

> **Note:** This repository does not include media files (images) related to glycans. Ensure external image files are added manually if required.

### Searching and Filtering
- **Filter by Species:** Quickly find glycans associated with specific species.
- **Search by Mass or Monosaccharide Composition:** Locate glycans based on their chemical composition.
- **Link to Scientific Studies:** View related research studies for each glycan.

## Summary
This project is designed for researchers, biologists, and database administrators working with glycans. It provides:
- A structured and searchable glycan database.
- Integration with research studies and species-specific data.
- A user-friendly Django Admin interface for managing the database.

For further customization, modify `models.py`, `admin.py`, or `views.py` as needed.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact
For support or contributions, contact [@borapcan](https://github.com/borapcan).
