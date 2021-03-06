Name:           php
Version:        7.0.22
Release:        1%{?dist}
Summary:        PHP is a popular general-purpose scripting language that is especially suited to web development

Group:          Development/Languages
License:        PHP
URL:            http://www.php.net/
BuildRoot:      %_topdir/BUILDROOT 

Source0:        http://php.net/get/%{name}-%{version}.tar.bz2
Source10:       php-fpm.init
Source11:       php-fpm.logrotate
Source12:       php.ini
Source13:       php-fpm.conf
Source14:       www.conf
Source15:       redis.so


BuildRequires:  openssl-devel,pcre-devel,zlib-devel,bzip2-devel,libcurl-devel,libjpeg-turbo-devel,libpng-devel,freetype-devel,libmcrypt-devel,readline-devel
Requires:       openssl,pcre

%description
PHP is an HTML-embedded scripting language. Much of its syntax is
borrowed from C, Java and Perl with a couple of unique PHP-specific
features thrown in. The goal of the language is to allow web 
developers to write dynamically generated pages quickly.


%prep
%setup -q


%build
./configure \
    --prefix=/gotwo_data/Application/php \
    --with-config-file-path=/gotwo_data/Application/php/etc \
    --with-fpm-user=nobody \
    --with-fpm-group=nobody \
    --enable-inline-optimization \
    --disable-debug \
    --disable-rpath \
    --enable-shared \
    --enable-fpm \
    --enable-mysqlnd \
    --with-mysqli=mysqlnd \
    --with-pdo-mysql=mysqlnd \
    --with-gettext \
    --enable-mbstring \
    --with-iconv \
    --with-mcrypt \
    --with-mhash \
    --with-openssl \
    --enable-soap \
    --enable-xml \
    --with-libxml-dir \
    --enable-pcntl \
    --enable-shmop \
    --enable-sysvmsg \
    --enable-sysvsem \
    --enable-sysvshm \
    --enable-sockets \
    --with-curl \
    --with-zlib \
    --enable-zip \
    --with-bz2 \
    --with-readline \
    --enable-ftp \
    --enable-wddx \
    --with-gd \
    --with-jpeg-dir \
    --with-png-dir \
    --enable-gd-native-ttf \
    --enable-bcmath \
    --enable-exif \
    --with-pcre-regex \
    --enable-mbstring=all \
    --with-libmbfl \
    --with-freetype-dir=/usr/include/freetype2/ \
    --enable-opcache \
    --with-zlib-dir


make %{?_smp_mflags}


%install
make INSTALL_ROOT=%{buildroot} install

%{__install} -p -D -m 0755 %{SOURCE10} \
    %{buildroot}%{_initrddir}/php-fpm
%{__install} -p -D -m 0644 %{SOURCE11} \
    %{buildroot}%{_sysconfdir}/logrotate.d/php-fpm
%{__install} -p -D -m 0644 %{SOURCE12} \
    %{buildroot}/gotwo_data/Application/php/etc/php.ini
%{__install} -p -D -m 0644 %{SOURCE13} \
    %{buildroot}/gotwo_data/Application/php/etc/php-fpm.conf
%{__install} -p -D -m 0644 %{SOURCE14} \
    %{buildroot}/gotwo_data/Application/php/etc/php-fpm.d/www.conf
%{__install} -p -D -m 0644 %{SOURCE15} \
    %{buildroot}/gotwo_data/Application/php/lib/php/extensions/no-debug-non-zts-20151012/redis.so
%pre


%post
if [ $1 -eq 1  ];then
    /sbin/chkconfig --add php-fpm
    /sbin/chkconfig php-fpm on
    mkdir -p /gotwo_data/logs/php
fi
 
%preun

%postun

%files
%defattr(-,root,root,0755)
/gotwo_data/Application/php
%attr(0755,root,root) /etc/rc.d/init.d/php-fpm
%attr(0644,root,root) /etc/logrotate.d/php-fpm
%doc

%changelog
* Mon Oct 04 2017 xiao xing <yunwei@stargoto.com> - 7.0.22-1
- update to upstream release 7.0.22


