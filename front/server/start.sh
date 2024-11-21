#!/bin/sh

set -e

cd /app/nuxt/temp/;
echo "
VITE_API_URL='${VITE_API_URL}'
" > .env;

nuxt generate;
rm .env;
mv .output/public/* ../;
cd /app/nuxt/;
chown nginx:nginx /app/nuxt/ -R;
rm -Rf temp/;

nginx -g "daemon off;"