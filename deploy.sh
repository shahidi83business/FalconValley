#!/bin/bash

PROJECT_PATH="/mnt/c/Users/AmirReza/Desktop/Ecokirom"             # مسیر پروژه
SERVER_USER="root"                      # نام کاربری
SERVER_IP="45.139.10.9"                         # آی‌پی
SERVER_PATH="/var/www/html/eco-kirom"        # مسیر مقصد
SERVER_PASS="amirreza"                 # پسورد سرور

rsync -avz --progress  "$PROJECT_PATH/" "$SERVER_USER@$SERVER_IP:$SERVER_PATH"

echo "انتقال با موفقیت انجام شد."
