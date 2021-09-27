Summary: Utilities for managing accounts and shadow password files
Name: shadow-utils
Version: 4.8.1
Release: 1
URL: https://github.com/shadow-maint/shadow/
Source0: %{name}-%{version}.tar.xz
Source1: shadow-utils.login.defs
Source2: shadow-utils.useradd
Patch0: shadow-4.6-redhat.patch
Patch1: shadow-4.8-goodname.patch
License: BSD
Requires: setup
BuildRequires: autoconf
BuildRequires: gettext-devel
BuildRequires: automake
BuildRequires: libtool
BuildRequires: byacc
BuildRequires: pkgconfig(libcrypt)

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
%autosetup -p1 -n %{name}-%{version}/upstream

%build
autoreconf -v -f --install
%configure \
        --enable-shadowgrp \
        --without-audit \
        --with-sha-crypt \
        --without-selinux \
        --disable-nls \
        --without-libcrack \
        --without-libpam \
        --disable-shared \
        --with-group-name-max-length=32 \
        --disable-man

# Force to skip man because generation does not currently work for us
# and even with --disable-man it tries to install them
echo -e "all:\ninstall:" > man/Makefile

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT gnulocaledir=$RPM_BUILD_ROOT/%{_datadir}/locale MKINSTALLDIRS=`pwd`/mkinstalldirs
install -d -m 755 $RPM_BUILD_ROOT/%{_sysconfdir}/default
install -p -c -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/login.defs
install -p -c -m 0600 %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/default/useradd

ln -s useradd $RPM_BUILD_ROOT%{_sbindir}/adduser

# Remove binaries we don't use.
rm $RPM_BUILD_ROOT/%{_bindir}/chfn
rm $RPM_BUILD_ROOT/%{_bindir}/chsh
rm $RPM_BUILD_ROOT/%{_bindir}/expiry
rm $RPM_BUILD_ROOT/%{_bindir}/groups
rm $RPM_BUILD_ROOT/%{_bindir}/login
rm $RPM_BUILD_ROOT/%{_bindir}/passwd
rm $RPM_BUILD_ROOT/%{_bindir}/su
rm $RPM_BUILD_ROOT/%{_bindir}/newgidmap
rm $RPM_BUILD_ROOT/%{_bindir}/newuidmap
rm $RPM_BUILD_ROOT/%{_sysconfdir}/login.access
rm $RPM_BUILD_ROOT/%{_sysconfdir}/limits
rm $RPM_BUILD_ROOT/%{_sbindir}/logoutd
rm $RPM_BUILD_ROOT/%{_sbindir}/nologin
rm $RPM_BUILD_ROOT/%{_sbindir}/chgpasswd

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/default
%attr(0644,root,root)   %config(noreplace) %{_sysconfdir}/login.defs
%attr(0600,root,root)   %config(noreplace) %{_sysconfdir}/default/useradd
%{_bindir}/*
%{_sbindir}/*
%attr(0750,root,root)   %{_sbindir}/user*
%attr(0750,root,root)   %{_sbindir}/group*
