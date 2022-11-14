FROM php:8.1

RUN apt-get update -y && apt-get install -y \
    openssl \
    zip \
    unzip \
    git \
    libonig-dev \
    libpq-dev
    
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

RUN docker-php-ext-install -j$(nproc) pgsql \
    && docker-php-ext-install -j$(nproc) pdo_pgsql

WORKDIR /app/backend
COPY . .
RUN composer install

EXPOSE 8000
# ENTRYPOINT ['waiting.sh']
CMD php artisan serve  --host=0.0.0.0