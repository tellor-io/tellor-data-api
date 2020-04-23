FROM tiangolo/uwsgi-nginx-flask:python3.7

# STATIC paths for file.
# Don't use flask static. Nginx is your friend
ENV STATIC_URL /static
ENV STATIC_PATH /app/static

# Place your flask application on the server
COPY ./app/ /app
WORKDIR /app


# Install requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt


ENV PYTHONPATH=/app


# Start Server
CMD ["/start.sh"]

EXPOSE 80 443
