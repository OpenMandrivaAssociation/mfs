%define name mfs
%define version 1.6.20
%define release %mkrel 1
%define minor 2
%define	_localstatedir	/var/lib
%define	mfsconfdir	%{_sysconfdir}

Summary:	MooseFS - distributed, fault tolerant file system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL v3
Group:		System/Cluster
URL:		http://www.moosefs.org/
Source0:	http://moosefs.org/tl_files/mfscode/%{name}-%{version}-%{minor}.tar.gz
Source1:	mfschunkserver.init 	
Source2:	mfsmaster.init
Source3: 	mfsmetalogger.init
BuildRequires:	fuse-devel
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{minor}-%{release}-root-%(%{__id_u} -n)

%description
MooseFS is an Open Source, easy to deploy and maintain, distributed,
fault tolerant file system for POSIX compliant OSes.

%package master
Summary:	MooseFS master server
Group:		System Environment/Daemons

%description master
MooseFS master (metadata) server together with metarestore utility.

%package metalogger
Summary:	MooseFS metalogger server
Group:		System Environment/Daemons

%description metalogger
MooseFS metalogger (metadata replication) server.

%package chunkserver
Summary:	MooseFS data server
Group:		System Environment/Daemons

%description chunkserver
MooseFS data server.

%package client
Summary:	MooseFS client
Group:		System Environment/Daemons

%description client
MooseFS client: mfsmount and mfstools.

%package cgi
Summary:	MooseFS CGI Monitor
Group:		System Environment/Daemons
Requires:	python

%description cgi
MooseFS CGI Monitor.

%prep
%setup -q -n mfs-%{version}-%{minor}
install -m 755 %{SOURCE1} mfschunkserver.init
install -m 755 %{SOURCE2} mfsmaster.init
install -m 755 %{SOURCE3} mfsmetalogger.init

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install \
	DESTDIR=$RPM_BUILD_ROOT
mkdir -p  %{buildroot}%{_initrddir}
install -m 755 mfschunkserver.init %{buildroot}%{_initrddir}/mfschunkserver
install -m 755 mfsmaster.init %{buildroot}%{_initrddir}/mfsmaster
install -m 755 mfsmetalogger.init %{buildroot}%{_initrddir}/mfsmetalogger

install -d $RPM_BUILD_ROOT%{_initrddir}

%post
%_post_service mfschunkserver
%_post_service mfsmaster
%_post_service mfsmetalogger

%preun
%_post_service mfschunkserver
%_post_service mfsmaster
%_post_service mfsmetalogger


%clean
rm -rf $RPM_BUILD_ROOT

%files master
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_sbindir}/mfsmaster
%attr(755,root,root) %{_sbindir}/mfsmetadump
%attr(755,root,root) %{_sbindir}/mfsmetarestore
%{_mandir}/man5/mfsexports.cfg.5*
%{_mandir}/man5/mfsmaster.cfg.5*
%{_mandir}/man7/mfs.7*
%{_mandir}/man7/moosefs.7*
%{_mandir}/man8/mfsmaster.8*
%{_mandir}/man8/mfsmetarestore.8*
%{mfsconfdir}/mfsexports.cfg.dist
%{mfsconfdir}/mfsmaster.cfg.dist
%dir %{_localstatedir}/mfs
%{_localstatedir}/mfs/metadata.mfs.empty
%attr(754,root,root) %{_initrddir}/mfsmaster

%files metalogger
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_sbindir}/mfsmetalogger
%{_mandir}/man5/mfsmetalogger.cfg.5*
%{_mandir}/man8/mfsmetalogger.8*
%{mfsconfdir}/mfsmetalogger.cfg.dist
%attr(754,root,root) %{_initrddir}/mfsmetalogger

%files chunkserver
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_sbindir}/mfschunkserver
%{_mandir}/man5/mfschunkserver.cfg.5*
%{_mandir}/man5/mfshdd.cfg.5*
%{_mandir}/man8/mfschunkserver.8*
%{mfsconfdir}/mfschunkserver.cfg.dist
%{mfsconfdir}/mfshdd.cfg.dist
%attr(754,root,root) %{_initrddir}/mfschunkserver

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
%{_mandir}/man7/mfs.7*
%{_mandir}/man7/moosefs.7*
%{_mandir}/man8/mfsmount.8*

%files cgi
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_sbindir}/mfscgiserv
%{_mandir}/man8/mfscgiserv.8*
%{_datadir}/mfscgi

%changelog
* Fri Nov 19 2010 Jakub Bogusz <contact@moosefs.com> - 1.6.19-1
- separated mfs-metalogger subpackage (following Debian packaging)

* Fri Oct  8 2010 Jakub Bogusz <contact@moosefs.com> - 1.6.17-1
- added init scripts based on work of Steve Huff (Dag Apt Repository)
  (included in RPMs when building with --define "distro rh")

* Mon Jul 19 2010 Jakub Kruszona-Zawadzki <contact@moosefs.com> - 1.6.16-1
- added mfscgiserv man page

* Fri Jun 11 2010 Jakub Bogusz <contact@moosefs.com> - 1.6.15-1
- initial spec file, based on Debian packaging;
  partially inspired by spec file by Kirby Zhou
