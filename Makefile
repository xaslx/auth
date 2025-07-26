.PHONY: app app-down app-logs


app:
	docker-compose up -d --build

app-down:
	docker-compose down

app-logs:
	docker-compose logs -f app

