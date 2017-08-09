Name:           tengine
Version:        2.2.0
Release:        1%{?dist}
Summary:        Tengine is a web server originated by Taobao

Group:          System Environment/Daemons
License:        BSD
URL:            http://tengine.taobao.org/
BuildRoot:      %_topdir/BUILDROOT 

Source0:        http://tengine.taobao.org/download/%{name}-%{version}.tar.gz
Source10:       nginx.init
Source11:       nginx.logrotate


BuildRequires:  openssl-devel,pcre-devel,zlib-devel
Requires:       openssl,pcre

%description
Tengine is a web server originated by Taobao, the largest e-commerce website 
in Asia. It is based on the Nginx HTTP server and has many advanced features.
Tengine has proven to be very stable and efficient on some of the top 100 
websites in the world, including taobao.com and tmall.com.


%prep
%setup -q


%build

./configure \
    --prefix=/gotwo_data/Application/nginx \
    --error-log-path=/gotwo_data/logs/nginx/error.log \
    --http-log-path=/gotwo_data/logs/nginx/access.log \
    --pid-path=/var/run/nginx.pid \
    --lock-path=/var/lock/subsys/nginx 

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot} 

install -p -D -m 0755 %{SOURCE10} \
    %{buildroot}%{_initrddir}/nginx
install -p -D -m 0644 %{SOURCE11} \
    %{buildroot}%{_sysconfdir}/logrotate.d/nginx

install -p -d -m 0755 %{buildroot}/gotwo_data/Application/nginx/conf/vhosts/


%pre
if [ $1 == 1 ];then
        /usr/sbin/useradd -r nginx -s /sbin/nologin 2> /dev/null
fi 

%post
if [ $1 -eq 1  ];then
    /sbin/chkconfig --add nginx
    /sbin/chkconfig nginx on

echo '#下面主要是nginx内核参数的优化，包括tcp的快速释放和重利用等。
fs.file-max = 999999
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_max_tw_buckets = 5000
net.ipv4.ip_local_port_range = 1024 61000
net.ipv4.tcp_rmem = 10240 87380 12582912
net.ipv4.tcp_wmem = 10240 87380 12582912
net.core.netdev_max_backlog = 8096
net.core.rmem_default = 6291456
net.core.wmem_default = 6291456
net.core.rmem_max = 12582912
net.core.wmem_max = 12582912
net.ipv4.tcp_max_syn_backlog = 1024

 

net.ipv4.tcp_tw_recycle = 1
net.core.somaxconn = 262144
net.ipv4.tcp_max_orphans = 262144
net.ipv4.tcp_timestamps = 0
net.ipv4.tcp_synack_retries = 1
net.ipv4.tcp_syn_retries = 1
' >> /etc/sysctl.conf
sysctl -p 2>&1 /dev/null

mkdir -p  /gotwo_data/logs/nginx
fi
 
%preun
if [ $1 -eq 0 ];then
    /etc/init.d/nginx stop > /dev/null 2>&1
    /usr/sbin/userdel -r nginx 2> /dev/null
        /sbin/chkconfig --del nginx
fi
%postun

%files
%defattr(-,root,root,0755)
/gotwo_data/Application/nginx
%attr(0755,root,root) /etc/rc.d/init.d/nginx
%attr(0644,root,root) /etc/logrotate.d/nginx
%attr(0755,root,root) /gotwo_data/logs/nginx
%doc



%changelog
* Mon Oct 04 2017 xiao xing <yunwei@stargoto.com> - 2.2.0-1
- update to upstream release 2.2.0


