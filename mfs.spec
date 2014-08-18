%define	_localstatedir	/var/lib
%define	mfsconfdir	%{_sysconfdir}

Summary:	MooseFS - distributed, fault tolerant file system
Name:		mfs
Version:	1.6.26
Release:	4
License:	GPLv3
Group:		System/Cluster
URL:		http://www.moosefs.org/
Source0:	http://moosefs.org/tl_files/mfscode/%{name}-%{version}.tar.gz
Source1:	mfschunkserver.service
Source2:	mfsmaster.service
Source3: 	mfsmetalogger.service
BuildRequires:	fuse-devel
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(zlib)
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
MooseFS is an Open Source, easy to deploy and maintain, distributed,
fault tolerant file system for POSIX compliant OSes.

%package master
Summary:	MooseFS master server
Group:		System/Cluster

%description master
MooseFS master (metadata) server together with metarestore utility.

%package metalogger
Summary:	MooseFS metalogger server
Group:		System/Cluster

%description metalogger
MooseFS metalogger (metadata replication) server.

%package chunkserver
Summary:	MooseFS data server
Group:		System/Cluster

%description chunkserver
MooseFS data server.

%package client
Summary:	MooseFS client
Group:		System/Cluster

%description client
MooseFS client: mfsmount and mfstools.

%package cgi
Summary:	MooseFS CGI Monitor
Group:		System/Cluster
Requires:	python

%description cgi
MooseFS CGI Monitor.

%prep
%setup -q -n mfs-%{version}

%build
%configure
%make

%install
%makeinstall_std

install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/mfschunkserver.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/mfsmaster.service
install -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/mfsmetalogger.service

# creating default configs
cp %{buildroot}%{mfsconfdir}/mfsexports.cfg.dist %{buildroot}%{mfsconfdir}/mfsexports.cfg
cp %{buildroot}%{mfsconfdir}/mfsmount.cfg.dist %{buildroot}%{mfsconfdir}/mfsmount.cfg
cp %{buildroot}%{mfsconfdir}/mfsmaster.cfg.dist %{buildroot}%{mfsconfdir}/mfsmaster.cfg
cp %{buildroot}%{mfsconfdir}/mfstopology.cfg.dist %{buildroot}%{mfsconfdir}/mfstopology.cfg
cp %{buildroot}%{mfsconfdir}/mfsmetalogger.cfg.dist %{buildroot}%{mfsconfdir}/mfsmetalogger.cfg
cp %{buildroot}%{mfsconfdir}/mfschunkserver.cfg.dist %{buildroot}%{mfsconfdir}/mfschunkserver.cfg
cp %{buildroot}%{mfsconfdir}/mfshdd.cfg.dist %{buildroot}%{mfsconfdir}/mfshdd.cfg

%pre
%_pre_useradd mfs /var/lib/mfs /sbin/nologin
%_pre_groupadd mfs mfs

%postun
%_postun_groupdel mfs
%_postun_userdel mfs

%post
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun master
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable mfsmaster.service > /dev/null 2>&1 || :
    /bin/systemctl stop mfsmaster.service > /dev/null 2>&1 || :
fi

%postun master
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart mfsmaster.service >/dev/null 2>&1 || ::
fi

%preun chunkserver
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable mfschunkserver.service > /dev/null 2>&1 || :
    /bin/systemctl stop mfschunkserver.service > /dev/null 2>&1 || :
fi

%postun chunkserver
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart mfschunkserver.service >/dev/null 2>&1 || :
fi

%preun metalogger
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable mfsmetalogger.service > /dev/null 2>&1 || :
    /bin/systemctl stop mfsmetalogger.service > /dev/null 2>&1 || :
fi

%postun metalogger
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart mfsmetalogger.service >/dev/null 2>&1 || :
fi

%files master
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_sbindir}/mfsmaster
%attr(755,root,root) %{_sbindir}/mfsmetadump
%attr(755,root,root) %{_sbindir}/mfsmetarestore
%{_mandir}/man5/mfsexports.cfg.5*
%{_mandir}/man5/mfsmaster.cfg.5*
%{_mandir}/man5/mfstopology.cfg.5.xz
%{_mandir}/man7/mfs.7*
%{_mandir}/man7/moosefs.7*
%{_mandir}/man8/mfsmaster.8*
%{_mandir}/man8/mfsmetarestore.8*
%{mfsconfdir}/mfsexports.cfg.dist
%{mfsconfdir}/mfsexports.cfg
%{mfsconfdir}/mfsmount.cfg.dist
%{mfsconfdir}/mfsmount.cfg
%{mfsconfdir}/mfsmaster.cfg.dist
%{mfsconfdir}/mfsmaster.cfg
%{mfsconfdir}/mfstopology.cfg.dist
%{mfsconfdir}/mfstopology.cfg
%attr(755,mfs,mfs) %{_localstatedir}/mfs
%{_unitdir}/mfsmaster.service

%files metalogger
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_sbindir}/mfsmetalogger
%{_mandir}/man5/mfsmetalogger.cfg.5*
%{_mandir}/man8/mfsmetalogger.8*
%{mfsconfdir}/mfsmetalogger.cfg.dist
%{mfsconfdir}/mfsmetalogger.cfg
%{_unitdir}/mfsmetalogger.service

%files chunkserver
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_sbindir}/mfschunkserver
%{_mandir}/man5/mfschunkserver.cfg.5*
%{_mandir}/man5/mfshdd.cfg.5*
%{_mandir}/man8/mfschunkserver.8*
%{mfsconfdir}/mfschunkserver.cfg.dist
%{mfsconfdir}/mfschunkserver.cfg
%{mfsconfdir}/mfshdd.cfg.dist
%{mfsconfdir}/mfshdd.cfg
%{_unitdir}/mfschunkserver.service

%files client
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_bindir}/mfsappendchunks
%attr(755,root,root) %{_bindir}/mfscheckfile
%attr(755,root,root) %{_bindir}/mfsdeleattr
%attr(755,root,root) %{_bindir}/mfsdirinfo
%attr(755,root,root) %{_bindir}/mfsfileinfo
%attr(755,root,root) %{_bindir}/mfsfilerepair
%attr(755,root,root) %{_bindir}/mfsgeteattr
%attr(755,root,root) %{_bindir}/mfsgetgoal
%attr(755,root,root) %{_bindir}/mfsgettrashtime
%attr(755,root,root) %{_bindir}/mfsmakesnapshot
%attr(755,root,root) %{_bindir}/mfsmount
%attr(755,root,root) %{_bindir}/mfsrgetgoal
%attr(755,root,root) %{_bindir}/mfsrgettrashtime
%attr(755,root,root) %{_bindir}/mfsrsetgoal
%attr(755,root,root) %{_bindir}/mfsrsettrashtime
%attr(755,root,root) %{_bindir}/mfsseteattr
%attr(755,root,root) %{_bindir}/mfssetgoal
%attr(755,root,root) %{_bindir}/mfssettrashtime
%attr(755,root,root) %{_bindir}/mfssnapshot
%attr(755,root,root) %{_bindir}/mfstools
%{_mandir}/man1/mfsappendchunks.1*
%{_mandir}/man1/mfscheckfile.1*
%{_mandir}/man1/mfsdeleattr.1*
%{_mandir}/man1/mfsdirinfo.1*
%{_mandir}/man1/mfsfileinfo.1*
%{_mandir}/man1/mfsfilerepair.1*
%{_mandir}/man1/mfsgeteattr.1*
%{_mandir}/man1/mfsgetgoal.1*
%{_mandir}/man1/mfsgettrashtime.1*
%{_mandir}/man1/mfsmakesnapshot.1*
%{_mandir}/man1/mfsrgetgoal.1*
%{_mandir}/man1/mfsrgettrashtime.1*
%{_mandir}/man1/mfsrsetgoal.1*
%{_mandir}/man1/mfsrsettrashtime.1*
%{_mandir}/man1/mfsseteattr.1*
%{_mandir}/man1/mfssetgoal.1*
%{_mandir}/man1/mfssettrashtime.1*
%{_mandir}/man1/mfstools.1*
%{_mandir}/man8/mfsmount.8*

%files cgi
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_sbindir}/mfscgiserv
%{_mandir}/man8/mfscgiserv.8*
%attr(755,mfs,mfs) %{_datadir}/mfscgi
