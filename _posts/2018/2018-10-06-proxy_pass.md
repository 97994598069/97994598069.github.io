---
published: false
---
示例：
proxy_pass http://www.aminglinux.com/;
proxy_pass http://192.168.200.101:8080/uri;
proxy_pass unix:/tmp/www.sock;

proxy_pass的配置的注意事项：

location /aming/ {
	proxy_pass http://192.168.1.10;     ##直接转发至ip  并且proxy_pass的ip没有/
	......
}

location /aming/ {
	proxy_pass http://192.168.1.10/;    ##直接转发至ip 并且proxy_pass的ip后加了/
	......
}

location /aming/ {
	proxy_pass http://192.168.1.10/linux/;   ##转发至ip后的linux目录。并且和/aming/不是同一个目录，并加了/
	......
}

location /aming/ {
	proxy_pass http://192.168.1.10/linux;    ##转发至ip后的linux目录。并且和/aming/不是同一个目录，但是没有加/
	......
}


假设：server_name 为www.aminglinux.com 
当请求http://www.aminglinux.com/aming/a.html的时候 以上示例的访问结果依次是：
http://192.168.1.10/aming/a.html 
http://192.168.1.10/a.html 
http://192.168.1.10/linux/a.html
http://192.168.1.10/linuxa.html 

注意上述的区别




