# 🌍 Country Info Web Application

This is a Django-based web application that displays information about countries using a simple interface. It includes API endpoints, user authentication, and template-rendered views styled with Bootstrap.

---

## ✅ Features

- 🔐 User authentication (Login, Signup, Logout)
- 🌐 List of all countries (paginated)
- 🔍 Search countries by name (partial match)
- 📍 View details of a country
  - Countries in the same region
  - Countries that speak the same language
- 🎨 Clean UI using Bootstrap 5
- 🧩 JSON-based API endpoints (Django function-based views)

---

## 🛠 Tech Stack

- **Backend:** Python Django
- **Frontend:** HTML, Bootstrap
- **Database:** PostgreSQL (My Choice)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/MuntasirMac/cf_assigned.git
cd cf_assigned
```

### 2. Create Virtual Environment and Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup The Database
- Create a file named `.env`
- Copy and paste the text from the file `env_example` to `.env`
- Now, following the instructions, enter your db name, db pass, db host an db port

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run The Development Server
```bash
python manage.py runserver
```

Visit: http://localhost:8000/countries/list

---

## 🔐 Authentication
* /signup – Register new user

* /login – Log in

* /logout – Log out

* Authenticated users can access the country list and details.

---

## 🧩 API Endpoints
| Endpoint                                | Description                            |
| --------------------------------------- | -------------------------------------- |
| `/countries/list`                           | List all countries                     |
| `/countries/detail/<id>`                      | View details of a country              |
| `/countries/search-country-by-name?name=nepal`         | Search country by name (partial match) |
| `/countries/same-region-countries/<id>`               | Same-region countries                  |
| `/countries/countries-by-language?language=english` | Countries that speak given language    |
