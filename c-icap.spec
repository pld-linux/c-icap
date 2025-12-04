Summary:	C implementation of an ICAP server
Summary(pl.UTF-8):	Implementacja w C serwera ICAP
Name:		c-icap
Version:	0.5.12
Release:	4
License:	BSD
Group:		Networking/Daemons
Source0:	https://downloads.sourceforge.net/c-icap/c_icap-%{version}.tar.gz
# Source0-md5:	d6f2bb2b9e95d33af9d4507104e418d6
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Source4:	%{name}.service
Source5:	%{name}.tmpfiles
Patch0:		c-icap-conf.patch
URL:		https://c-icap.sourceforge.net/
BuildRequires:	bzip2-devel
BuildRequires:	db-devel >= 4.2
BuildRequires:	doxygen
BuildRequires:	libbrotli-devel
BuildRequires:	libmemcached-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.647
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	systemd-units >= 0.38
Requires:	%{name}-lib = %{version}-%{release}
Requires:	rc-scripts >= 0.4.0.12
Provides:	group(c-icap)
Provides:	user(c-icap)
Conflicts:	logrotate < 3.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
c-icap is an implementation of an ICAP server. It can be used with
HTTP proxies that support the ICAP protocol to implement content
adaptation and filtering services.

%description -l pl.UTF-8
c-icap to implementacja serwera ICAP. Można go używać z proxy HTTP
obsługującymi protokół ICAP do implementowania usług adaptowania i
filtrowania treści.

%package lib
Summary:	c-icap library
Summary(pl.UTF-8):	biblioteka c-icap
Group:		Development/Libraries

%description lib
c-icap library.

%description lib -l pl.UTF-8
Biblioteka c-icap.

%package devel
Summary:	Header files for c-icap library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki c-icap
Group:		Development/Libraries
Requires:	%{name}-lib = %{version}-%{release}
Obsoletes:	c-icap-static < 0.5.12

%description devel
Header files for c-icap library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki c-icap.

%prep
%setup -q -n c_icap-%{version}
%patch -P0 -p1

%build
%configure \
	CFLAGS="%{rpmcflags} -std=gnu17" \
	--sysconfdir=%{_sysconfdir}/c-icap \
	--enable-ipv6 \
	--enable-large-files \
	--with-bdb \
	--with-bzlib \
	--with-ldap \
	--with-memcached \
	--with-openssl \
	--with-pcre \
	--with-zlib \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/c_icap/templates \
	$RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT/var/log{,/archive}/c-icap \
	$RPM_BUILD_ROOT{%{systemdtmpfilesdir},%{systemdunitdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

touch $RPM_BUILD_ROOT/var/log/c-icap/{access.log,server.log}

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/c-icap
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/c-icap
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/c-icap
cp -p %{SOURCE4} $RPM_BUILD_ROOT/%{systemdunitdir}/c-icap.service
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/c-icap.conf

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libicapapi.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/c_icap/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 262 c-icap
%useradd -o -u 262 -s /bin/false -g c-icap -c "c-icap ICAP server daemon" -d /usr/share/empty c-icap

%post
/sbin/chkconfig --add c-icap
%service c-icap restart
%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del c-icap
	%service c-icap stop
fi
%systemd_preun %{name}.service

%postun
if [ "$1" = "0" ]; then
	%userremove c-icap
	%groupremove c-icap
fi
%systemd_reload

%post	lib -p /sbin/ldconfig
%postun	lib -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%dir %{_sysconfdir}/c-icap
%attr(640,root,c-icap) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/c-icap/c-icap.conf
%attr(640,root,c-icap) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/c-icap/c-icap.magic
%{_sysconfdir}/c-icap/c-icap.conf.default
%{_sysconfdir}/c-icap/c-icap.magic.default
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/c-icap
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/c-icap
%{systemdunitdir}/c-icap.service
%{systemdtmpfilesdir}/c-icap.conf
%attr(754,root,root) /etc/rc.d/init.d/c-icap
%attr(755,root,root) %{_bindir}/c-icap
%attr(755,root,root) %{_bindir}/c-icap-client
%attr(755,root,root) %{_bindir}/c-icap-mkbdb
%attr(755,root,root) %{_bindir}/c-icap-stretch
%dir %{_libdir}/c_icap
%attr(755,root,root) %{_libdir}/c_icap/bdb_tables.so
%attr(755,root,root) %{_libdir}/c_icap/dnsbl_tables.so
%attr(755,root,root) %{_libdir}/c_icap/ldap_module.so
%attr(755,root,root) %{_libdir}/c_icap/srv_echo.so
%attr(755,root,root) %{_libdir}/c_icap/sys_logger.so
%attr(755,root,root) %{_libdir}/c_icap/memcached_cache.so
%attr(755,root,root) %{_libdir}/c_icap/shared_cache.so
%attr(755,root,root) %{_libdir}/c_icap/srv_ex206.so
%{_mandir}/man8/c-icap.8*
%{_mandir}/man8/c-icap-client.8*
%{_mandir}/man8/c-icap-config.8*
%{_mandir}/man8/c-icap-libicapapi-config.8*
%{_mandir}/man8/c-icap-mkbdb.8*
%{_mandir}/man8/c-icap-stretch.8*
%dir %{_datadir}/c_icap
%dir %{_datadir}/c_icap/templates
%attr(750,c-icap,c-icap) %dir /var/run/c-icap
%attr(770,root,c-icap) %dir /var/log/archive/c-icap
%attr(770,root,c-icap) %dir /var/log/c-icap
%attr(770,root,c-icap) %ghost /var/log/c-icap/*

%files lib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libicapapi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libicapapi.so.5

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/c-icap-config
%attr(755,root,root) %{_bindir}/c-icap-libicapapi-config
%{_libdir}/libicapapi.so
%{_includedir}/c_icap
