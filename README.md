# using docker services to implement nginx load balancer

## usage
```bash
git clone https://github.com/htkuan/nginx-load-balancer.git
cd nginx-load-balancer
docker-compose up -d
```

## nginx setting /webserver

nginx.conf is nginx setting file
```
...
    upstream web_cluster{
        server webapp:8000;
        server webapp2:8001;
    }

    #include /etc/nginx/conf.d/*.conf;

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://web_cluster;
            proxy_set_header Host $host:$proxy_port;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
...
```
upstream is load balancing configuration!

When nginx get request, and mapping location,

there are 2 instances of the same application running on webapp,webapp2. 

then All requests are proxied to the server group "web_cluster", 

and nginx applies HTTP load balancing to distribute the requests.

When the load balancing method is not specifically configured, it defaults to round-robin.
## django setting /webapp

Using Gunicorn be a WSGI server,

and return environment variable "APP" on endpoint('/')

In the upper folder "docker-compose.yml" file,

setting run two webapp instance(webapp, webapp2),

and give this two instance different environment var "APP".
