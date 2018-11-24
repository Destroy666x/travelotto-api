### Installation:

1. Enter `docker` directory and copy `.env.dist` to `.env`,
modify it to suit your needs
2. Run `docker-compose up -d --build`
3. Get inside the container `docker exec -ti <containerId> bash`
4. Run migrations `python manage.py migrate api`
5. Load fixtures `python manage.py loaddata initial_data`
