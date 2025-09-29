---

# 🏷️ Bid Marketplace – CS50 Web Project 2

An online **auction platform** built as part of **CS50 Web Programming with Python and JavaScript**.
The app allows users to create listings, place bids, leave comments, add items to their watchlist, and manage active/closed auctions.

This project demonstrates key concepts of **Django**, **database models**, **forms handling**, and **full-stack development** with backend–frontend integration.

---

## 📽️ Project Demo

Watch the demo video on YouTube:
👉 [Project Video Walkthrough](https://youtu.be/NTE4Jmpay0A)

---

## ⚙️ Features

* User authentication (register, login, logout)
* Create and manage auction listings
* Place bids on active listings
* Add comments to listings
* Add/remove listings from your personal watchlist
* Close auctions (listing creator only)
* Dedicated pages for:

  * Active listings
  * Categories
  * Watchlist
  * Listing detail with bidding history and comments
* Responsive UI with Django templates

---

## 🛠️ Tech Stack

* **Backend**: Django (Python)
* **Frontend**: HTML, CSS (vanilla, with Django templates)
* **Database**: SQLite (development)
* **Containerization**: Docker + Docker Compose
* **Testing**: Pytest + pytest-django + Coverage
* **CI/CD**: GitHub Actions + SonarCloud

---

## 🧪 Tests

Unit and integration tests are written using **pytest**.

Main coverage:

* Authentication (login, register, logout)
* Creating listings (validation, errors, success)
* Bidding system (valid/invalid bids)
* Comments
* Watchlist (add/remove listings)
* Closing auctions
* Edge cases (unauthorized access, invalid form inputs, etc.)

Run tests locally and generate coverage inside Docker:

```bash
make test
```

---

## 🔄 Continuous Integration

The project uses **GitHub Actions** with:

* Linting (flake8) and formatting (black) checks
* Security checks (bandit, safety)
* Automated tests with `pytest`
* Coverage report uploaded to **SonarCloud** for code quality analysis

---

## 🐳 Docker Setup

The application is fully containerized with **Docker Compose**.

### Build and run:

```bash
make start
```

---

## 📂 Project Structure

```
app/
|── auctions/         # Core app (models, views, forms, urls)
|── commerce/         # Django project settings
|── tests/            # Unit and integration tests
.github/workflows/    # CI pipelines
docker/               # Docker configuration
requirements/         # Python dependencies
```

---

## 🚀 Future Improvements

* Add image upload for listings
* Real-time bidding with WebSockets
* Deploy to a production server with HTTPS (Heroku / Render / Fly.io)

---
