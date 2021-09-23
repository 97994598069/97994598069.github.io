1.更换国内的yum源
yum -y install wget
1)备份原来自带的yum源
mkdir -pv /etc/yum.repos.d/backup  &&  mv /etc/yum.repos.d/*.repo /etc/yum.repos.d/backup

2)下载国内yum源和epel
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.163.com/.help/CentOS7-Base-163.repo
mv /etc/yum.repos.d/CentOS7-Base-163.repo /etc/yum.repos.d/CentOS-Base.repo

3)更新缓存
yum clean all 
yum makecache

4)更新系统
yum update ##说明：升级所有包同时也升级软件和系统内核     ##yum upgrade：只升级所有包，不升级软件和系统内核





2.安装常用工具
yum install ntpdate lsof net-tools gcc gcc-c++ make mtr nethogs iftop lrzsz vim openssh* psmisc openssl* ncurses ncurses-devel -y


安装最新版的sysstat
cd /usr/local/src
wget http://pagesperso-orange.fr/sebastien.godard/sysstat-12.3.3.tar.gz
tar xf sysstat-12.3.3.tar.gz
cd sysstat-12.3.3 
./configure 
make && make install 

测试使用：
pidstat -d 1  ##老版本没有io的延迟iodelay，新版本有
pidstat -u 1 ##也多了iowait%
sar -n DEV 1 ##多了 %ifutil


3.系统时间同步
EDT：指美国东部夏令时间
EST：英国时间
CST：北京时间
##如果时间为EST；需要先将时区改为CST
[root@localhost ~]# mv /etc/localtime /etc/localtime.bak
[root@localhost ~]# ln -s /usr/share/zoneinfo/Asia/Shanghai  /etc/localtime
[root@localhost ~]# date

ntpdate cn.pool.ntp.org
echo '*/30 * * * * /usr/sbin/ntpdate cn.pool.ntp.org && hwclock -w && hwclock --systohc >/dev/null 2>&1' >> /var/spool/cron/root
systemctl restart crond

3. 调整文件描述符大小
echo -e "* soft nofile 65536 \n* hard nofile 65536 \n* soft nproc 65536 \n* hard nproc 65536" >> /etc/security/limits.conf
ulimit -SHn 65536 && ulimit -s 65536

4.锁定文件关键系统
chattr +i /etc/passwd 
chattr +i /etc/inittab 
chattr +i /etc/group 
chattr +i /etc/shadow 
chattr +i /etc/gshadow

5.配置history命令显示
在/etc/profile文件最后加两行：
USER_IP=`who -u -m | awk '{print $NF}'| sed 's/[()]//g'`
export HISTTIMEFORMAT="[%F %T][`whoami`][${USER_IP}] "
或者开启审计功能
采用以下步骤配置用户命令日志审计功能：
1.创建用户审计文件存放目录和审计日志文件 ； 
mkdir -p /var/log/usermonitor/
2.创建用户审计日志文件；
echo usermonitor >/var/log/usermonitor/usermonitor.log
3.将日志文件所有者赋予一个最低权限的用户；
chown nobody:nobody /var/log/usermonitor/usermonitor.log
4.给该日志文件赋予所有人的写权限； 
chmod 002 /var/log/usermonitor/usermonitor.log
5.设置文件权限,使所有用户对该文件只有追加权限 ；
chattr +a /var/log/usermonitor/usermonitor.log
6.编辑vim /etc/profile文件，添加如下脚本命令；
export HISTORY_FILE=/var/log/usermonitor/usermonitor.log
export PROMPT_COMMAND='{ date "+%y-%m-%d %T ##### $(who am i |awk "{print \$1\" \"\$2\" \"\$5}") #### $(whoami) #### $(history 1 | { read x cmd; echo "$cmd"; })"; } >>$HISTORY_FILE'
7.使配置生效
source /etc/profile
审计时查看/var/log/usermonitor/usermonitor.log文件即可，它会记录登上服务器所有用户使用的命令。为了更安全，还可以将改文件打包压缩，ftp至其它本地。
source /etc/profile


新建用户并配置sudo权限:
 useradd admin  
 passwd admin
  
 root	ALL=(ALL) 	ALL
 admin	ALL=(ALL) 	NOPASSWD:ALL  ##新增；此时admin用户可以直接使用sudo kill命令，不需要输入root密码。若需要输入root密码则格式为:admin	ALL=(ALL) 	ALL



6.tcp快速回收
cp /etc/sysctl.conf /etc/sysctl.conf.default
fs.file-max = 99999   #提高整个系统的文件限制
net.ipv4.tcp_syncookies = 1  #表示开启SYN Cookies。当出现SYN等待队列溢出时，启用cookies来处理，可防范少量SYN攻击，默认为0，表示关闭；
net.ipv4.tcp_tw_reuse = 1  #表示开启重用。允许将TIME-WAIT sockets重新用于新的TCP连接，默认为0，表示关闭；
net.ipv4.tcp_tw_recycle = 0 ##表示开启TCP连接中TIME-WAIT sockets的快速回收，默认为0，表示关闭；为了对NAT设备更友好，建议设置为0
net.ipv4.tcp_fin_timeout = 30 #修改系統默认的 TIMEOUT 时间。
net.ipv4.tcp_keepalive_time = 1200  #表示当keepalive起用的时候，TCP发送keepalive消息的频度。缺省是2小时，改为20分钟。
net.ipv4.ip_local_port_range = 10000 65000 #表示用于向外连接的端口范围。缺省情况下很小：32768到61000;若出现Cannot assign requested address这个报错，则需要增加这个值来缓解，例如1024 65535
net.ipv4.tcp_max_syn_backlog = 8192 #表示SYN队列的长度，默认为1024，加大队列长度为8192，可以容纳更多等待连接的网络连接数。
net.ipv4.tcp_max_tw_buckets = 5000 #表示系统同时保持TIME_WAIT的最大数量，如果超过这个数字，TIME_WAIT将立刻被清除并打印警告信息。


netstat -ant |grep '^tcp' |awk '{print $NF}' |sort |uniq -c |sort -rn


服务器初始化系统参数：

常用：
sysctl -n net.core.netdev_max_backlog  ##查看系统该参数的值  ##或者直接sysctl net.core.netdev_max_backlog
sysctl -w net.core.netdev_max_backlog=8192  ##临时写入，重启无效


fs.file-max = 999999：这个参数表示进程（比如一个worker进程）可以同时打开的最大句柄数，这个参数直线限制最大并发连接数，需根据实际情况配置。 默认为1000

net.ipv4.tcp_max_tw_buckets = 6000 #这个参数表示操作系统允许TIME_WAIT套接字数量的最大值，如果超过这个数字，TIME_WAIT套接字将立刻被清除并打印警告信息。该参数默认为180000，过多的TIME_WAIT套接字会使Web服务器变慢。
注：主动关闭连接的服务端会产生TIME_WAIT状态的连接


net.ipv4.ip_local_port_range = 1024 65000 #允许系统打开的端口范围。默认值为32768到60999，也就是说共有28231个端口，如果做为客户端2ML（4分钟）超时的话，系统默认的秒并发即是28231/（4*60）=117个

net.ipv4.tcp_tw_recycle = 0 #启用timewait快速回收。  ##对于nat网络有可能会访问不了，不建议开启， 1表示开启，0表示关闭

net.ipv4.tcp_tw_reuse = 1 #开启重用。允许将TIME-WAIT sockets重新用于新的TCP连接。这对于服务器来说很有意义，因为服务器上总会有大量TIME-WAIT状态的连接。

net.ipv4.tcp_keepalive_time = 30：这个参数表示当keepalive启用时，TCP发送keepalive消息的频度。默认是2小时，若将其设置的小一些，可以更快地清理无效的连接。
##使用场景: https://www.cnblogs.com/bugutian/p/12939473.html

net.ipv4.tcp_syncookies = 1 #开启SYN Cookies，当出现SYN等待队列溢出时，启用cookies来处理。


net.core.somaxconn = 40960 #web 应用中 listen 函数的 backlog 默认会给我们内核参数的 net.core.somaxconn 限制到128，而nginx定义的NGX_LISTEN_BACKLOG 默认为511，所以有必要调整这个值。
注：对于一个TCP连接，Server与Client需要通过三次握手来建立网络连接.当三次握手成功后,我们可以看到端口的状态由LISTEN转变为ESTABLISHED,接着这条链路上就可以开始传送数据了.每一个处于监听(Listen)状态的端口,都有自己的监听队列.监听队列的长度与如somaxconn参数和使用该端口的程序中listen()函数有关
somaxconn参数:定义了系统中每一个端口最大的监听队列的长度,这是个全局的参数,默认值为128，对于一个经常处理新连接的高负载 web服务环境来说，默认的 128 太小了。大多数环境这个值建议增加到 1024 或者更多。大的侦听队列对防止拒绝服务 DoS 攻击也会有所帮助。


net.core.netdev_max_backlog = 262144 #每个网络接口接收数据包的速率比内核处理这些包的速率快时，允许送到队列的数据包的最大数目。

net.ipv4.tcp_max_syn_backlog = 262144#这个参数标示TCP三次握手建立阶段接受SYN请求队列的最大长度，默认为1024，将其设置得大一些可以使出现Nginx繁忙来不及accept新连接的情况时，Linux不至于丢失客户端发起的连接请求。

net.ipv4.tcp_rmem = 10240  87380  12582912#这个参数定义了TCP接受缓存（用于TCP接受滑动窗口）的最小值、默认值、最大值。
net.ipv4.tcp_wmem = 10240 87380 12582912：这个参数定义了TCP发送缓存（用于TCP发送滑动窗口）的最小值、默认值、最大值。
net.core.rmem_default = 6291456：这个参数表示内核套接字接受缓存区默认的大小。
net.core.wmem_default = 6291456：这个参数表示内核套接字发送缓存区默认的大小。
net.core.rmem_max = 12582912：这个参数表示内核套接字接受缓存区的最大大小。
net.core.wmem_max = 12582912：这个参数表示内核套接字发送缓存区的最大大小。





