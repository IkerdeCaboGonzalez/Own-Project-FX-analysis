FROM postgres:latest

# Definimos las credenciales que ya usas en tu código Python
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=IK008626
ENV POSTGRES_DB=postgres

# Exponemos el puerto estándar de PostgreSQL
EXPOSE 5432

CMD ["postgres"]