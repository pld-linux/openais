Summary:	The openais Standards-Based Cluster Framework executive and APIs
Summary(pl.UTF-8):	Środowisko klastra opartego na standardach openais
Name:		openais
Version:	0.80.2
Release:	0.1
License:	BSD
Group:		Base
Source0:	http://developer.osdl.org/dev/openais/downloads/%{name}-%{version}/openais-%{version}.tar.gz
# Source0-md5:	a1cfcd0e8f555132353b780c130d8220
URL:		http://developer.osdl.org/dev/openais/
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-libs = %{version}-%{release}
Provides:	group(ais)
Provides:	user(ais)
#ExclusiveArch:	%{ix86} %{x8664} ppc ppc64 ia64 s390 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the openais executive, openais service handlers,
default configuration files and init script.

%description -l pl.UTF-8
Ten pakiet zawiera środowisko wykonawcze, programy obsługi usług
openais, domyślne pliki konfiguracyjne oraz skrypt startowy.

%package libs
Summary:	The openais Standards-Based Cluster Framework libraries
Summary(pl.UTF-8):	Biblioteki klastra opartego na standardach openais
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description libs
This package contains the openais libraries.

%description libs -l pl.UTF-8
Ten pakiet zawiera biblioteki openais.

%package devel
Summary:	The openais Standards-Based Cluster Framework development files
Summary(pl.UTF-8):	Pliki programistyczne klastra opartego na standardach openais
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the include files used to develop using openais
APIs.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkow służące do programowania z użyciem
API openais.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LCRSODIR=%{_libdir}/lcrso

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LCRSODIR=%{_libdir}/lcrso \
%if "%{_lib}" == lib64
	ARCH=64 \
%else
	ARCH=32 \
%endif
	STATICLIBS=NO

install -D init/redhat $RPM_BUILD_ROOT/etc/rc.d/init.d/openais
install test/openais-cfgtool $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 187 ais
%useradd -u 187 -d /usr/share/empty -s /bin/false -g ais -c "openais Standards Based Cluster Framework" -r ais

%post
/sbin/chkconfig --add openais
%service openais restart

%preun
if [ "$1" -eq "0" ]; then
	%service -q openais stop
	/sbin/chkconfig --del openais
fi

%postun
if [ "$1" = "0" ]; then
	%userremove ais
	%groupremove ais
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README.devmap README.amf SECURITY
%attr(755,root,root) %{_sbindir}/aisexec
%attr(755,root,root) %{_sbindir}/ais-keygen
%attr(755,root,root) %{_sbindir}/openais-cfgtool
%dir %{_sysconfdir}/ais
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/ais/openais.conf
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/ais/amf.conf
%attr(754,root,root) /etc/rc.d/init.d/openais
%attr(755,root,root) %{_libdir}/lcrso/*.lcrso
%{_mandir}/man8/*.8*
%{_mandir}/man5/openais.conf.5*

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/openais
%attr(755,root,root) %{_libdir}/openais/lib*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/openais/lib*.so.?
%dir %{_libdir}/lcrso
/etc/ld.so.conf.d/openais-*.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/openais/lib*.so
%{_includedir}/openais
%{_mandir}/man3/*.3*
