# Makefile for kpopdb

build:
	docker-compose build

requirements:
	docker-compose run kpopdb pip3 freeze > requirements.txt

shell:
	docker-compose run kpopdb bash

validate:
	docker-compose up
