FROM python:3.11.4

ENV USERS_CSV_PATH=/app/data/users.csv
ENV EXPERIMENTS_CSV_PATH=/app/data/user_experiments.csv
ENV COMPOUNDS_CSV_PATH=/app/data/compounds.csv

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD [ "python", "./app/main.py" ]