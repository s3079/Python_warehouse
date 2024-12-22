# Warehouse Management System

A Python-based warehouse management system built using the Model-View-Controller (MVC) architectural pattern and Object-Oriented Programming principles.

## Project Structure

```
warehouse/
├── app/
│   ├── config/
│   │   ├── config.py         # Application configuration
│   │   └── schema.sql        # Database schema
│   ├── controllers/
│   │   ├── base_controller.py
│   │   └── category_controller.py
│   ├── models/
│   │   ├── base_model.py
│   │   └── category_model.py
│   ├── utils/
│   │   ├── database.py       # Database connection handler
│   │   └── languages.py      # Internationalization support
│   ├── views/
│   │   ├── base_view.py
│   │   └── category_view.py
│   └── main.py              # Application entry point
└── requirements.txt         # Project dependencies
```

## Features

- MVC Architecture for better code organization and maintainability
- Object-Oriented design with inheritance and encapsulation
- Multi-language support
- MySQL database integration
- Category management (more modules coming soon)

## Prerequisites

- Python 3.8 or higher
- MySQL Server
- Tkinter (usually comes with Python)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd warehouse
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:
   - Create a MySQL database named 'warehouse'
   - Update database credentials in `app/config/config.py`
   - Import the schema:
     ```bash
     mysql -u root -p warehouse < app/config/schema.sql
     ```

## Running the Application

```bash
python app/main.py
```

## Project Structure Details

### Models
- `BaseModel`: Abstract base class for all models
- `CategoryModel`: Handles category data operations

### Views
- `BaseView`: Abstract base class for all views
- `CategoryView`: Handles category UI components

### Controllers
- `BaseController`: Abstract base class for all controllers
- `CategoryController`: Handles category business logic

### Configuration
- Database settings
- Application settings
- Language settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
