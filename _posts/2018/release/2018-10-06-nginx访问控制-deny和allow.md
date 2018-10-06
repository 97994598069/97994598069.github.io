---
published: false
---
语法：allow/deny address | CIDR |unix： |all 
它表示，允许/拒绝某个ip或者一个IP段访问.如果指定unix:,那将允许socket的访问。
备注：unix在1.5.1中新加入的功能

在nginx中，allow和deny的规则是按顺序执行的

示例：
location / {
	allow 192.168.0.0/24;
	allow 127.0.0.1;
	deny all;
}
说明：这段配置将允许192.168.0.0/24网段和127.0.0.1的请求，其他来源ip全部拒绝

location ~ "admin" {
	allow 110.21.33.121；
	deny all;
}
说明：访问的uri中包含admin的请求，只允许110.21.33.121这个IP的请求
