Summary:	Tunneling IPX packets via IP network.
Name:		ipxtund
Version:	1.3.0
Release:	1
License:	GPL
Group:		Daemons
Group(pl):	Serwery
Vendor:		Hinrich Eilts  <eilts@tor.muc.de>
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/%{name}-%{version}.tgz
Source1:	ipxtund.init
Source2:	ipxtund.sysconfig
Patch0:		ipxtund-cfg.patch
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ipxtund connect IPX based LANs over TCP/IP. Especially, this
allows several parties at different LANs to play IPX based
games as sharing one LAN, if their LANs are connected to a
TCP/IP WAN like Internet.

%description -l pl
ipxtund ³±czy sieci bazuj±ce na IPX poprzez TCP/IP. Narzêdzie
to pozwala na np. granie w gry bazuj±ce na IPX graczom w ró¿nych
sieciach o ile tylko sieci te s± po³±czone do sieci WAN TCP/IP
takiej jak Internet.

%prep
%setup -q
%patch0 -p1

%build
OPT="$RPM_OPT_FLAGS"; export OPT
./Configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/sbin
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{rc.d/init.d,sysconfig}
install -d $RPM_BUILD_ROOT%{_var}/log
install -d $RPM_BUILD_ROOT%{_mandir}/man{5,7}

install -s ipxtund		$RPM_BUILD_ROOT/sbin
install examples/ipxtund.conf	$RPM_BUILD_ROOT%{_sysconfdir}
install	*.7			$RPM_BUILD_ROOT%{_mandir}/man7
install %{SOURCE1}		$RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}
install %{SOURCE2}		$RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
echo ".so man7/%{name}.7" >	$RPM_BUILD_ROOT%{_mandir}/man5/%{name}.conf.5
touch				$RPM_BUILD_ROOT%{_var}/log/%{name}.log

gzip -9nf INSTALL README $RPM_BUILD_ROOT%{_mandir}/man*/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) /sbin/%{name}
%attr(644,root,root) %{_mandir}/man*/*
%attr(640,root,root) %ghost %{_var}/log/%{name}.log
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/*
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
