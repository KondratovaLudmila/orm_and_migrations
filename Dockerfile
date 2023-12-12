FROM postgres:14-bullseye

ENV POSTGRES_PASSWORD qwerty

COPY dump-test.sql /docker-entrypoint-initdb.d/