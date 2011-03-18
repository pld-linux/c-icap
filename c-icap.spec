#
# TODO
#   - init script
#
Summary:	C implementation of an ICAP server
Name:		c-icap
Version:	0.1.4
Release:	0.1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/c-icap/c_icap-%{version}.tar.gz
# Source0-md5:	e1ce94fe7beaaa9318c3595694b10709
Patch0:		%{name}-ld.patch
Patch1:		%{name}-align-64bit.patch
Patch2:		%{name}-conf.patch
URL:		http://c-icap.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
c-icap is an implementation of an ICAP server. It can be used with
HTTP proxies that support the ICAP protocol to implement content
adaptation and filtering services.

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
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure
%{__automake}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/c_icap/templates
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/c-icap
%attr(755,root,root) %{_bindir}/c-icap-client
%attr(755,root,root) %{_bindir}/c-icap-mkbdb
%attr(755,root,root) %{_bindir}/c-icap-stretch
%{_sysconfdir}/c-icap.conf
%{_sysconfdir}/c-icap.magic
%attr(755,root,root) %{_libdir}/libicapapi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libicapapi.so.0
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
%attr(755,root,root) %dir /var/run/c-icap

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/c-icap-config
%attr(755,root,root) %{_bindir}/c-icap-libicapapi-config
%{_libdir}/libicapapi.so
%{_includedir}/c_icap

%files static
%defattr(644,root,root,755)
%{_libdir}/libicapapi.la
%attr(755,root,root) %{_libdir}/c_icap/bdb_tables.la
%attr(755,root,root) %{_libdir}/c_icap/dnsbl_tables.la
%attr(755,root,root) %{_libdir}/c_icap/ldap_module.la
%attr(755,root,root) %{_libdir}/c_icap/srv_echo.la
%attr(755,root,root) %{_libdir}/c_icap/sys_logger.la
