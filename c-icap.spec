#
Summary:	C implementation of an ICAP server
Name:		c-icap
Version:	0.1.4
Release:	0.1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/c-icap/c_icap-%{version}.tar.gz
# Source0-md5:	e1ce94fe7beaaa9318c3595694b10709
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.logrotate
Patch0:		%{name}-ld.patch
Patch1:		%{name}-align-64bit.patch
Patch2:		%{name}-conf.patch
URL:		http://c-icap.sourceforge.net/
Requires:	%{name}-lib = %{version}-%{release}
Requires:	rc-scripts >= 0.4.0.12
Conflicts:	logrotate < 3.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
c-icap is an implementation of an ICAP server. It can be used with
HTTP proxies that support the ICAP protocol to implement content
adaptation and filtering services.

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

%description devel
Header files for c-icap library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki c-icap.

%package static
Summary:	Static c-icap library
Summary(pl.UTF-8):	Statyczna biblioteka c-icap
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static c-icap library.

%description static -l pl.UTF-8
Statyczna biblioteka c-icap.

%prep
%setup -q -n c_icap-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__autoconf}
%configure \
	--enable-large-files \
	--sysconfdir=%{_sysconfdir}/c-icap
%{__automake}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/c_icap/templates \
	$RPM_BUILD_ROOT/etc/{logrotate.d,rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT/var/log{,/archive}/c-icap
touch $RPM_BUILD_ROOT/var/log/c-icap/{access.log,server.log}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/c-icap
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/c-icap
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/c-icap

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 262 c-icap
%useradd -o -u 262 -s /bin/false -g c-icap -c "c-icap ICAP server daemon" -d /usr/share/empty c-icap

%post
/sbin/chkconfig --add c-icap
%service c-icap restart

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del c-icap
	%service c-icap stop
fi

%postun
if [ "$1" = "0" ]; then
	%userremove c-icap
	%groupremove c-icap
fi

%post	lib -p /sbin/ldconfig
%postun	lib -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README

%dir %{_sysconfdir}/c-icap
%attr(640,root,c-icap) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/c-icap/c-icap.conf
%attr(640,root,c-icap) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/c-icap/c-icap.magic
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/c-icap
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/c-icap
%attr(754,root,root) /etc/rc.d/init.d/c-icap
%attr(755,root,root) %{_bindir}/c-icap
%attr(755,root,root) %{_bindir}/c-icap-client
%attr(755,root,root) %{_bindir}/c-icap-mkbdb
%attr(755,root,root) %{_bindir}/c-icap-stretch
%attr(755,root,root) %{_libdir}/c_icap/bdb_tables.so
%attr(755,root,root) %{_libdir}/c_icap/dnsbl_tables.so
%attr(755,root,root) %{_libdir}/c_icap/ldap_module.so
%attr(755,root,root) %{_libdir}/c_icap/srv_echo.so
%attr(755,root,root) %{_libdir}/c_icap/sys_logger.so
%{_mandir}/man8/c-icap.8.gz
%{_mandir}/man8/c-icap-client.8.gz
%{_mandir}/man8/c-icap-config.8.gz
%{_mandir}/man8/c-icap-libicapapi-config.8.gz
%{_mandir}/man8/c-icap-mkbdb.8.gz
%{_mandir}/man8/c-icap-stretch.8.gz
%attr(755,root,root) %dir %{_datadir}/c_icap
%attr(750,c-icap,c-icap) %dir /var/run/c-icap
%attr(770,root,c-icap) %dir /var/log/archive/c-icap
%attr(770,root,c-icap) %dir /var/log/c-icap
%attr(770,root,c-icap) %ghost /var/log/c-icap/*

%files lib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libicapapi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libicapapi.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/c-icap-config
%attr(755,root,root) %{_bindir}/c-icap-libicapapi-config
%{_libdir}/libicapapi.so
%{_includedir}/c_icap

%files static
%defattr(644,root,root,755)
%{_libdir}/libicapapi.la
