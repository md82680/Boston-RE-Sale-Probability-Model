.PHONY: start-backend start-frontend start-all

start-backend:
	cd backend && uvicorn api.main:app --reload --port 8000

start-frontend:
	cd frontend && npm start

start-all:
	make -j 2 start-backend start-frontend
