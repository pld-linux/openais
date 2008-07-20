# TODO
# - discard /etc/ld.so.conf.d/openais-*.conf and use rpath instead
Summary:	The openais Standards-Based Cluster Framework executive and APIs
Summary(pl.UTF-8):	Środowisko klastra opartego na standardach openais
Name:		openais
Version:	0.84
Release:	1
License:	BSD
Group:		Base
Source0:	http://developer.osdl.org/dev/openais/downloads/%{name}-%{version}/openais-%{version}.tar.gz
# Source0-md5:	c0d4dc2bee121391e91354b538e12c87
URL:		http://www.openais.org/
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
Conflicts:	openais < 0.80.2-0.2

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
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/ais/amf.conf
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/ais/openais.conf
%attr(754,root,root) /etc/rc.d/init.d/openais
%attr(755,root,root) %{_libdir}/lcrso/*.lcrso
%{_mandir}/man5/amf.conf.5*
%{_mandir}/man5/openais.conf.5*
%{_mandir}/man8/confdb_overview.8*
%{_mandir}/man8/cpg_overview.8*
%{_mandir}/man8/evs_overview.8*
%{_mandir}/man8/logsys_overview.8*
%{_mandir}/man8/openais_overview.8*

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/openais
%attr(755,root,root) %{_libdir}/openais/libSaAmf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/openais/libSaAmf.so.2
%attr(755,root,root) %{_libdir}/openais/libSaCkpt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/openais/libSaCkpt.so.2
%attr(755,root,root) %{_libdir}/openais/libSaClm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/openais/libSaClm.so.2
%attr(755,root,root) %{_libdir}/openais/libSaEvt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/openais/libSaEvt.so.2
%attr(755,root,root) %{_libdir}/openais/libSaLck.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/openais/libSaLck.so.2
%attr(755,root,root) %{_libdir}/openais/libSaMsg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/openais/libSaMsg.so.2
%attr(755,root,root) %{_libdir}/openais/libais.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/openais/libais.so.2
%attr(755,root,root) %{_libdir}/openais/libaisutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/openais/libaisutil.so.2
%attr(755,root,root) %{_libdir}/openais/libcfg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/openais/libcfg.so.2
%attr(755,root,root) %{_libdir}/openais/libconfdb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/openais/libconfdb.so.2
%attr(755,root,root) %{_libdir}/openais/libcpg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/openais/libcpg.so.2
%attr(755,root,root) %{_libdir}/openais/libevs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/openais/libevs.so.2
%attr(755,root,root) %{_libdir}/openais/liblogsys.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/openais/liblogsys.so.2
%attr(755,root,root) %{_libdir}/openais/libtotem_pg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/openais/libtotem_pg.so.2
%dir %{_libdir}/lcrso
/etc/ld.so.conf.d/openais-*.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/openais/libSaAmf.so
%attr(755,root,root) %{_libdir}/openais/libSaCkpt.so
%attr(755,root,root) %{_libdir}/openais/libSaClm.so
%attr(755,root,root) %{_libdir}/openais/libSaEvt.so
%attr(755,root,root) %{_libdir}/openais/libSaLck.so
%attr(755,root,root) %{_libdir}/openais/libSaMsg.so
%attr(755,root,root) %{_libdir}/openais/libais.so
%attr(755,root,root) %{_libdir}/openais/libaisutil.so
%attr(755,root,root) %{_libdir}/openais/libcfg.so
%attr(755,root,root) %{_libdir}/openais/libconfdb.so
%attr(755,root,root) %{_libdir}/openais/libcpg.so
%attr(755,root,root) %{_libdir}/openais/libevs.so
%attr(755,root,root) %{_libdir}/openais/liblogsys.so
%attr(755,root,root) %{_libdir}/openais/libtotem_pg.so
%{_includedir}/openais
%{_mandir}/man3/cpg_*.3*
%{_mandir}/man3/confdb_*.3*
%{_mandir}/man3/evs_*.3*
