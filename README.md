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

then All requests are proxied(proxy_pass) to the server group "web_cluster", 

and nginx applies HTTP load balancing to distribute the requests.

When the load balancing method is not specifically configured, it defaults to round-robin.

### Different kinds of load balacner
1. Default load balancing configuration

平均分配，每個instance車輪接request
```
upstream web_cluster{
    server webapp:8000;
    server webapp2:8001;
}
```

2. Least connected load balancing

根據負載(連線時間)來分發request
```
upstream web_cluster{
    least_conn;
    server webapp:8000;
    server webapp2:8001;
}
```

3. Session persistence

利用 hash ip 的方式，來確保同ip 會請求在一樣的 instance 以達到 session persistence
```
upstream web_cluster{
    ip_hash;
    server webapp:8000;
    server webapp2:8001;
}
```

4. Weighted load balancing

利用權重來分發requests
```
upstream web_cluster{
    server webapp:8000 weight=3;
    server webapp2:8001 weight=7;
}
```

You can change default load balancing configuration,

and re-bulid nginx image to test different load balancer way!

## django setting /webapp

Using Gunicorn be a WSGI server,

and return environment variable "APP" on endpoint('/')

In the upper folder "docker-compose.yml" file,

setting run two webapp instance(webapp, webapp2),

and give this two instance different environment var "APP".

## test load balancer

just run load_balance_test.py script

```python
import requests


if __name__ == '__main__':
    url = 'http://0.0.0.0:8000'
    res_count = {}
    for _ in range(10):
        re = requests.get(url).text
        if re in res_count.keys():
            res_count[re] += 1
        else:
            res_count[re] = 1
    print(res_count)
```
