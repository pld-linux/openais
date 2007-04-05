Summary:	The openais Standards-Based Cluster Framework executive and APIs
Name:		openais
Version:	0.80.2
Release:	0.1
License:	BSD
Group:		Base
Source0:	http://developer.osdl.org/dev/openais/downloads/%{name}-%{version}/openais-%{version}.tar.gz
# Source0-md5:	a1cfcd0e8f555132353b780c130d8220
URL:		http://developer.osdl.org/dev/openais/
Requires(post):	/sbin/chkconfig
Requires(pre):	/usr/sbin/useradd
Requires(preun):	/sbin/chkconfig
#ExclusiveArch:	i386 ppc x86_64 ppc64 ia64 s390 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the openais executive, openais service handlers,
default configuration files and init script.

%package devel
Summary:	The openais Standards-Based Cluster Framework libraries
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the libraries and include files used to develop
using openais APIs.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \

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

install -d $RPM_BUILD_ROOT%{_initrddir}
install init/redhat $RPM_BUILD_ROOT%{_initrddir}/openais
install test/openais-cfgtool $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
#useradd -c 'openais Standards Based Cluster Framework' -u 39 -s /bin/false -r -d '/' ais

%post
/sbin/chkconfig --add openais
/sbin/ldconfig

%postun -p /sbin/ldconfig

%preun
if [ "$1" -eq "0" ]; then
	%service -q openais stop
	/sbin/chkconfig --del openais
fi

%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README.devmap README.amf SECURITY
%attr(755,root,root) %{_sbindir}/aisexec
%attr(755,root,root) %{_sbindir}/ais-keygen
%attr(755,root,root) %{_sbindir}/openais-cfgtool
%dir %{_sysconfdir}/ais
%config(noreplace) %{_sysconfdir}/ais/openais.conf
%config(noreplace) %{_sysconfdir}/ais/amf.conf
%config /etc/ld.so.conf.d/openais-*.conf
%attr(754,root,root) /etc/rc.d/init.d/openais
%dir %{_libdir}/openais
%attr(755,root,root) %{_libdir}/openais/lib*.so.*.*.*
%dir %{_libdir}/lcrso
%attr(755,root,root) %{_libdir}/lcrso/*
%{_mandir}/man8/*.8*
%{_mandir}/man5/openais.conf.5*

%files devel
%defattr(644,root,root,755)
%doc CHANGELOG README.devmap
%{_includedir}/openais
%attr(755,root,root) %{_libdir}/openais/lib*.so
%{_mandir}/man3/*.3*
