#run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    if "--seed" in __import__("sys").argv:
        from app.seed.seed_data import seed_data

        with app.app_context():
            seed_data()
    app.run(host="0.0.0.0", port=5000, debug=True)