Summary: Utilities for managing accounts and shadow password files
Name: shadow-utils
Version: 4.1.5
Release: 1
URL: http://pkg-shadow.alioth.debian.org/
Source0: ftp://pkg-shadow.alioth.debian.org/pub/pkg-shadow/shadow-%{version}.tar.bz2
Source1: shadow-utils.login.defs
Source2: shadow-utils.useradd
Patch0: shadow-4.1.5-redhat.patch
Patch1: shadow-4.1.5-goodname.patch
Patch2: shadow-4.1.5-stdarg.patch
License: BSD and GPLv2+
Group: System/Base
Requires: setup

%description
The shadow-utils package includes the necessary programs for
converting UNIX password files to the shadow password format, plus
programs for managing user and group accounts. The pwconv command
converts passwords to the shadow password format. The pwunconv command
unconverts shadow passwords and generates an npasswd file (a standard
UNIX password file). The pwck command checks the integrity of password
and shadow files. The lastlog command prints out the last login times
for all users. The useradd, userdel, and usermod commands are used for
managing user accounts. The groupadd, groupdel, and groupmod commands
are used for managing group accounts.

%prep
%setup -q -n shadow-%{version}
%patch0 -p1 -b .redhat
%patch1 -p1 -b .goodname
%patch2 -p1 -b .stdarg

%build
%configure \
        --enable-shadowgrp \
        --without-audit \
        --with-sha-crypt \
        --without-selinux \
        --disable-nls \
        --without-libcrack \
        --without-libpam \
        --disable-shared
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT gnulocaledir=$RPM_BUILD_ROOT/%{_datadir}/locale MKINSTALLDIRS=`pwd`/mkinstalldirs
install -d -m 755 $RPM_BUILD_ROOT/%{_sysconfdir}/default
install -p -c -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/login.defs
install -p -c -m 0600 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/default/useradd

ln -s useradd $RPM_BUILD_ROOT%{_sbindir}/adduser
ln -s useradd.8 $RPM_BUILD_ROOT/%{_mandir}/man8/adduser.8

# Remove binaries we don't use.
rm $RPM_BUILD_ROOT/%{_bindir}/chfn
rm $RPM_BUILD_ROOT/%{_bindir}/chsh
rm $RPM_BUILD_ROOT/%{_bindir}/expiry
rm $RPM_BUILD_ROOT/%{_bindir}/groups
rm $RPM_BUILD_ROOT/%{_bindir}/login
rm $RPM_BUILD_ROOT/%{_bindir}/passwd
rm $RPM_BUILD_ROOT/%{_bindir}/su
rm $RPM_BUILD_ROOT/%{_sysconfdir}/login.access
rm $RPM_BUILD_ROOT/%{_sysconfdir}/limits
rm $RPM_BUILD_ROOT/%{_sbindir}/logoutd
rm $RPM_BUILD_ROOT/%{_sbindir}/nologin
rm $RPM_BUILD_ROOT/%{_sbindir}/chgpasswd
rm $RPM_BUILD_ROOT/%{_mandir}/man1/chfn.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/chsh.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/expiry.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/groups.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/login.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man1/su.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/limits.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/login.access.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/passwd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/porttime.*
rm $RPM_BUILD_ROOT/%{_mandir}/man5/suauth.*
rm $RPM_BUILD_ROOT/%{_mandir}/man8/logoutd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man8/nologin.*
rm $RPM_BUILD_ROOT/%{_mandir}/man8/chgpasswd.*
rm $RPM_BUILD_ROOT/%{_mandir}/man3/getspnam.*

%docs_package

%files 
%defattr(-,root,root)
%dir %{_sysconfdir}/default
%attr(0644,root,root)   %config(noreplace) %{_sysconfdir}/login.defs
%attr(0600,root,root)   %config(noreplace) %{_sysconfdir}/default/useradd
%{_bindir}/sg
%{_bindir}/chage
%{_bindir}/faillog
%{_bindir}/gpasswd
%{_bindir}/lastlog
%{_bindir}/newgrp
%{_sbindir}/adduser
%attr(0750,root,root)   %{_sbindir}/user*
%attr(0750,root,root)   %{_sbindir}/group*
%{_sbindir}/grpck
%{_sbindir}/pwck
%{_sbindir}/*conv
%{_sbindir}/chpasswd
%{_sbindir}/newusers
%{_sbindir}/vipw
%{_sbindir}/vigr
