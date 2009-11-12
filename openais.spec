Summary:	The openais Standards-Based Cluster Framework executive and APIs
Summary(pl.UTF-8):	Środowisko klastra opartego na standardach openais
Name:		openais
Version:	1.1.0
Release:	1
License:	BSD
Group:		Base
Source0:	http://devresources.linux-foundation.org/dev/openais/downloads/%{name}-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6b73c7438e230c31aec53d6af78a6b0d
URL:		http://www.openais.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	corosync-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	%{name}-libs = %{version}-%{release}
Requires:	/sbin/chkconfig
Requires:	corosync
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

%build
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	--with-lcrso-dir=$(pkg-config corosync --variable lcrsodir)

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D init/redhat $RPM_BUILD_ROOT/etc/rc.d/init.d/openais

# Install the config and comment out all examples
mv $RPM_BUILD_ROOT/etc/corosync/amf.conf{.example,}
sed -i -e 's/\(^.*$\)/#\1/' $RPM_BUILD_ROOT/etc/corosync/amf.conf

# Cleanup the buildroot
rm -rf $RPM_BUILD_ROOT/usr/share/doc/openais/
# remove openais.conf now it is corosync.conf from corosync package
rm -f $RPM_BUILD_ROOT/usr/share/man/man5/man5/openais.conf.5*

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
%doc CHANGELOG README.amf
%attr(755,root,root) %{_sbindir}/aisexec
%attr(755,root,root) %{_sbindir}/openais-instantiate
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/corosync/amf.conf
%attr(754,root,root) /etc/rc.d/init.d/openais
%attr(755,root,root) %{_libdir}/lcrso/*.lcrso
%{_mandir}/man5/amf.conf.5*
# do not package openais.conf - now it is corosync.conf from corosync package
#%%{_mandir}/man5/openais.conf.5*
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
%attr(755,root,root) %{_libdir}/libSaMsg.so.3.*.*
%attr(755,root,root) %ghost %{_libdir}/libSaMsg.so.3
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
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libSaAmf.a
%{_libdir}/libSaCkpt.a
%{_libdir}/libSaClm.a
%{_libdir}/libSaEvt.a
%{_libdir}/libSaLck.a
%{_libdir}/libSaMsg.a
%{_libdir}/libSaTmr.a
