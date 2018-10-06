---
published: false
---
nginx的location配置：
安装第三方模块echo-nginx-module
git clone https://github.com/openresty/echo-nginx-module.git
./configure --add-module=/path/to/echo-nginx-module

location语法：
location [=|^~|~|~*|/uri/{......}]
coding.net/u/aminglinux/p/nginx/git/blob/master/location/ruler.md

location优先级及案例
=高于^~高于~*等于~高于/
coding.net/u/aminglinux/p/nginx/git/blob/master/location/priority.md 
 
 
安装第三方模块echo-nginx-module
##安装这个模块可以使我们可以在配置文件中使用echo命令
写在location里面，主要用于测试

location /aming/ {
	deny all;
}
说明：针对/aming/目录，全部禁止访问，这里的deny all 可以改为return 403

location ~ ".bak|\.ht" {
	return 403
}
说明：访问的uri中包含.bak字样的或者包含.ht的直接返回403状态码

location ~ (data|cache|tmp|image|attachment).*\.php$ {
	deny all;
}
说明:请求的uri中包含data/cache/tmp/image/attachment并且以.php结尾的，全部禁止访问


 
 
