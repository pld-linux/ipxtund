Summary:	Tunneling IPX packets via IP network
Summary(pl):	Tunel dla pakietów IPX przez sieæ IP
Name:		ipxtund
Version:	1.3.0
Release:	3
License:	GPL
Group:		Daemons
Vendor:		Hinrich Eilts  <eilts@tor.muc.de>
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/%{name}-%{version}.tgz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-cfg.patch
BuildRequires:	zlib-devel
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
ipxtund connect IPX based LANs over TCP/IP. Especially, this allows
several parties at different LANs to play IPX based games as sharing
one LAN, if their LANs are connected to a TCP/IP WAN like Internet.

%description -l pl
ipxtund ³±czy sieci bazuj±ce na IPX poprzez TCP/IP. Narzêdzie to
pozwala na np. granie w gry bazuj±ce na IPX graczom w ró¿nych sieciach
o ile tylko sieci te s± po³±czone do sieci WAN TCP/IP takiej jak
Internet.

%prep
%setup -q
%patch0 -p1

%build
OPT="%{rpmcflags}"; export OPT
./Configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,7}} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/{rc.d/init.d,sysconfig},%{_var}/log}

install ipxtund			$RPM_BUILD_ROOT%{_sbindir}
install examples/ipxtund.conf	$RPM_BUILD_ROOT%{_sysconfdir}
install	*.7			$RPM_BUILD_ROOT%{_mandir}/man7
install %{SOURCE1}		$RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2}		$RPM_BUILD_ROOT/etc//sysconfig/%{name}
echo ".so man7/%{name}.7" >	$RPM_BUILD_ROOT%{_mandir}/man5/%{name}.conf.5
touch				$RPM_BUILD_ROOT%{_var}/log/%{name}.log

gzip -9nf INSTALL README

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
%attr(755,root,root) %{_sbindir}/%{name}
%attr(754,root,root) /etc/rc.d/init.d/ipxtund
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%attr(640,root,root) %ghost %{_var}/log/%{name}.log
%{_mandir}/man*/*
