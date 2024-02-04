FROM nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=builder ./frontend/build .
EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]
