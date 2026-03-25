# just-invoice

A self-hosted Flask web application for creating, managing, and printing invoices. Supports a customer and product registry, PDF invoice generation, and a bilingual Greek / English interface.

---

## Installation

### Option 1 — Docker Compose

**Prerequisites:** [Docker](https://docs.docker.com/get-docker/) with the Compose plugin.

```bash
git clone https://github.com/tseste/just-invoice.git
cd just-invoice
docker compose up --build
```

The app will be available at `http://localhost:5000`. MySQL is initialised automatically from `InvoiceDB_schema.sql` on first start and data is persisted in the `mysql_data` Docker volume.

To stop:

```bash
docker compose down
docker compose down -v # delete volume
```

### Option 2 — Run locally

**Prerequisites:** Python ≥ 3.10, [uv](https://github.com/astral-sh/uv), a running MySQL instance, and `wkhtmltopdf`.

**1. Install wkhtmltopdf:**

```bash
# Debian / Ubuntu
sudo apt-get install wkhtmltopdf

# macOS
brew install wkhtmltopdf

# Windows — download from https://wkhtmltopdf.org/downloads.html
```

**2. Install Python dependencies:**

```bash
uv sync
```

**3. Create a `.env` file** in the project root (Flask loads it automatically):

```dotenv
SECRET_KEY=dev-secret-change-me
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=InvoiceDB
DB_USER=invoice_user
DB_PASSWORD=invoice_password
PDF_OUTPUT_DIR=assets/invoices
```

**4. Start the development server:**

```bash
uv run flask --app flask_app run --debug
```

---

## Usage

| Page | URL | Description |
|---|---|---|
| Home | `/` | Landing page |
| New Invoice | `/invoice` | Fill in and generate a PDF invoice |
| Customer | `/customer` | Add or update a customer record |
| Product | `/product` | Add or update a product record |
| Unit Type | `/unittype` | Add a new product unit of measure |
| Search | `/search` | Search customers, products, and invoices |

Switch the UI language with the **EL / EN** toggle in the navigation bar.

---

## Configuration

All settings are read from environment variables. Set them in `.env` (local) or in the `environment` block of `docker-compose.yml`.

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `dev-secret-change-me` | Flask session signing key — **change in production** |
| `DB_HOST` | `127.0.0.1` | MySQL host |
| `DB_PORT` | `3306` | MySQL port |
| `DB_NAME` | _(empty)_ | Database name |
| `DB_USER` | _(empty)_ | Database user |
| `DB_PASSWORD` | _(empty)_ | Database password |
| `PDF_OUTPUT_DIR` | `assets/invoices` | Directory where generated PDFs are saved |
| `BABEL_DEFAULT_LOCALE` | `el` | Default UI language (`el` or `en`) |
| `FLASK_DEBUG` | `0` | Set to `1` to enable debug mode |

---

## Testing

Run the test suite without a database:

```bash
uv run pytest
```

---

## Internationalization (i18n)

This project uses Flask-Babel and stores English translations under `translations/en/LC_MESSAGES/`.

**1. Extract translatable strings to a POT template:**

```bash
uv run pybabel extract -F babel.cfg -o messages.pot .
```

**2. Update the English PO file from the template:**

```bash
uv run pybabel update -i messages.pot -d translations -l en
```

**3. Compile PO files to MO files used at runtime:**

```bash
uv run pybabel compile -d translations -l en
```

---

## Remaining work

- [ ] Search for customers, products, and invoices
- [ ] Track invoice status
- [ ] Basic landing page dashboard with invoice, customer and products monthly analytics
---
