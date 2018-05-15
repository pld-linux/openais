#
# Note: not maintained upstream any more.
# Needed for 3rd generation 'cluster' package and clvmd with corosync/openais support.
# In order to build use corosync 1.x (from corosync-1_4 branch).
#
Summary:	The openais Standards-Based Cluster Framework executive and APIs
Summary(pl.UTF-8):	Środowisko klastra opartego na standardach openais
Name:		openais
Version:	1.1.4
Release:	2.2
License:	BSD
Group:		Base
#Source0Download: https://github.com/corosync/openais/releases
Source0:	https://github.com/corosync/openais/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e500ad3c49fdc45d8653f864e80ed82c
Source1:	%{name}.init
Source2:	%{name}.service
URL:		https://github.com/corosync/openais
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	corosync-devel >= 1.0
BuildRequires:	corosync-devel < 2
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-libs = %{version}-%{release}
Requires:	corosync >= 1.0
Requires:	corosync < 2
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

%package static
Summary:	The openais Standards-Based Cluster Framework static libraries
Summary(pl.UTF-8):	Statyczne biblioteki klastra opartego na standardach openais
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains the openais static libraries.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczne biblioteki openais.

%prep
%setup -q

sed -i -e 's/OPT_CFLAGS=.*/OPT_CFLAGS=/' configure.ac

%build
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	--with-initddir=/etc/rc.d/init.d \
	--with-lcrso-dir=$(pkg-config corosync --variable lcrsodir)

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{systemdunitdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# Install the config and comment out all examples
mv $RPM_BUILD_ROOT/etc/corosync/amf.conf{.example,}
sed -i -e 's/^/#/' $RPM_BUILD_ROOT/etc/corosync/amf.conf

# Cleanup the buildroot
%{__rm} -r $RPM_BUILD_ROOT/usr/share/doc/openais

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 187 ais
%useradd -u 187 -d /usr/share/empty -s /bin/false -g ais -c "openais Standards Based Cluster Framework" -r ais

%post
/sbin/chkconfig --add %{name}
%service %{name} restart
%systemd_post %{name}.service

%preun
if [ "$1" -eq "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%systemd_preun %{name}.service

%postun
if [ "$1" = "0" ]; then
	%userremove ais
	%groupremove ais
fi
%systemd_reload

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG README.amf
%attr(755,root,root) %{_sbindir}/aisexec
%attr(755,root,root) %{_sbindir}/openais-instantiate
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/corosync/amf.conf
%attr(754,root,root) /etc/rc.d/init.d/openais
%{systemdunitdir}/%{name}.service
%attr(755,root,root) %{_libdir}/lcrso/openaisserviceenable.lcrso
%attr(755,root,root) %{_libdir}/lcrso/service_*.lcrso
%{_mandir}/man5/amf.conf.5*
%{_mandir}/man5/openais.conf.5*
%{_mandir}/man8/openais_overview.8*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libSaAmf.so.3.*.*
%attr(755,root,root) %ghost %{_libdir}/libSaAmf.so.3
%attr(755,root,root) %{_libdir}/libSaCkpt.so.3.*.*
%attr(755,root,root) %ghost %{_libdir}/libSaCkpt.so.3
%attr(755,root,root) %{_libdir}/libSaClm.so.3.*.*
%attr(755,root,root) %ghost %{_libdir}/libSaClm.so.3
%attr(755,root,root) %{_libdir}/libSaEvt.so.3.*.*
%attr(755,root,root) %ghost %{_libdir}/libSaEvt.so.3
%attr(755,root,root) %{_libdir}/libSaLck.so.3.*.*
%attr(755,root,root) %ghost %{_libdir}/libSaLck.so.3
%attr(755,root,root) %{_libdir}/libSaMsg.so.4.*.*
%attr(755,root,root) %ghost %{_libdir}/libSaMsg.so.4
%attr(755,root,root) %{_libdir}/libSaTmr.so.3.*.*
%attr(755,root,root) %ghost %{_libdir}/libSaTmr.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libSaAmf.so
%attr(755,root,root) %{_libdir}/libSaCkpt.so
%attr(755,root,root) %{_libdir}/libSaClm.so
%attr(755,root,root) %{_libdir}/libSaEvt.so
%attr(755,root,root) %{_libdir}/libSaLck.so
%attr(755,root,root) %{_libdir}/libSaMsg.so
%attr(755,root,root) %{_libdir}/libSaTmr.so
%{_includedir}/openais
%{_pkgconfigdir}/libSaAmf.pc
%{_pkgconfigdir}/libSaCkpt.pc
%{_pkgconfigdir}/libSaClm.pc
%{_pkgconfigdir}/libSaEvt.pc
%{_pkgconfigdir}/libSaLck.pc
%{_pkgconfigdir}/libSaMsg.pc
%{_pkgconfigdir}/libSaTmr.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libSaAmf.a
%{_libdir}/libSaCkpt.a
%{_libdir}/libSaClm.a
%{_libdir}/libSaEvt.a
%{_libdir}/libSaLck.a
%{_libdir}/libSaMsg.a
%{_libdir}/libSaTmr.a
