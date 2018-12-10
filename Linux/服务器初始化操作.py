1.更换国内的yum源
yum -y install wget
1)备份原来自带的yum源
略

2)下载国内yum源和epel
wget -O /etc/yum.repos.d/epel.repo //mirrors.aliyun.com/repo/epel-7.repo
wget -O /etc/yum.repos.d/CentOS-Base.repo //mirrors.aliyun.com/repo/Centos-7.repo

3)更新缓存
yum clean all 
yum makecache

2.安装常用工具
yum install ntpdate lsof net-tools gcc gcc-c++ make sysstat mtr iftop lrzsz vim openssh* -y

3.系统时间同步
ntpdate cn.pool.ntp.org
echo '*/30 * * * * ntpdate cn.pool.ntp.org && hwclock -w && hwclock --systohc >/dev/null 2>&1' >> /var/spool/cron/root
systemctl restart crond

3. 调整文件描述符大小
echo -e "* soft nofile 65535 \n* hard nofile 65535 \n* soft nproc 65535 \n* hard nproc 65535" >> /etc/security/limits.conf
ulimit -SHn 65535 && ulimit -s 65535

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
HISTSIZE=1000
HISTTIMEFORMAT="[%F %T][`whoami`][${USER_IP}] ";export HISTTIMEFORMAT
export HISTORY_FILE=/var/log/audit.log   ##注意日志
export PROMPT_COMMAND='{ thisHistID=`history 1|awk "{print \\$1}"`;lastCommand=`history 1| awk "{\\$1=\"\" ;print}"`;user=`id -un`;whoStr=(`who -u am i`);realUser=${whoStr[0]};logMonth=${whoStr[2]};logDay=${whoStr[3]};logTime=${whoStr[4]};pid=${whoStr[6]};ip=${whoStr[7]};if [ ${thisHistID}x != ${lastHistID}x ];then echo -E `date "+%Y/%m/%d %H:%M:%S"` $user\($realUser\)@$ip[PID:$pid][LOGIN:$logMonth $logDay $logTime] --- $lastCommand ;lastHistID=$thisHistID;fi; } >> $HISTORY_FILE'

source /etc/profile


6.如果出差配置服务器而且有配置外网一定要启用防火墙并且创建普通用户；否则有可能等你回公司发现服务器已经登陆不上去了


6.内核参数调整
cp /etc/sysctl.conf /etc/sysctl.conf.default
略
至少如下4个：
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_fin_timeout = 30


