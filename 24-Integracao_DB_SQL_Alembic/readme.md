Rodar main.py:
* uvicorn main:app --reload

Comando do Alembic
* Init aliembic:
    * alembic init -t async migrations

* After change the model, this command add new change:
    * alembic revision --autogenerate -m "Adding User and Article Table"

* To apply the change:
    * alembic upgrade head

* to check
    * alembic check