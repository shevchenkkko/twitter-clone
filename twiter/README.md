# Twitter Clone Project

This project is a clone of the popular social network Twitter, built with Django. It enables users to register, create posts, interact with others through likes and comments, follow other users, and edit profiles.

## Features

- **User Authentication**: Registration, login, and logout.
- **User Profile**: View profiles, edit profiles, add avatars, and update descriptions.
- **Posts**: Create, edit, and delete posts.
- **Interactions**: Like posts, add comments.
- **Follow System**: Follow other users and see their posts in the feed.
- **Admin Panel**: Manage content and users.

## Tech Stack

- **Back-end**: Django
- **Front-end**: HTML, CSS, Bootstrap
- **Database**: SQLite or PostgreSQL for production

## Installation

### Requirements

- Python 3.8+
- Django 4.0+
- Other dependencies are listed in `requirements.txt`

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/shevchenkkko/twitter-clone.git
    cd twiter
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the root directory with the following content:
    ```env
    SECRET_KEY=your-secret-key
    DEBUG=True
    ```

5. **Run migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser** (for admin panel access):
    ```bash
    python manage.py createsuperuser
    ```

7. **Start the server**:
    ```bash
    python manage.py runserver
    ```

8. **Access the application**:
    - Open your browser and go to `http://127.0.0.1:8000`
    - Admin panel: `http://127.0.0.1:8000/admin`


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss the proposed changes.

## License

This project is licensed under the MIT License.
