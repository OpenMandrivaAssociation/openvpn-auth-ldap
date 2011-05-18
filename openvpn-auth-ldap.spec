Summary:	OpenVPN plugin for LDAP authentication
Name:		openvpn-auth-ldap
Version:	2.0.3
Release:	%mkrel 1
License:	BSD
Group:		Networking/Other
URL:		http://code.google.com/p/openvpn-auth-ldap/
Source0:	http://openvpn-auth-ldap.googlecode.com/files/auth-ldap-%{version}.tar.gz
# S1 was taken from openvpn-2.1.4
Source1:	openvpn-plugin.h
Patch0:		auth-ldap-2.0.3-top_builddir.patch
Patch1:		auth-ldap-2.0.3-README.patch
Patch2:		openvpn-auth-ldap-2.0.3-disable-tests.patch
# This is a plugin not linked against a lib, so hardcode the requirement
# since we require the parent configuration and plugin directories
Requires:	openvpn >= 2.1.4-4
BuildRequires:	re2c
Buildrequires:	doxygen
Buildrequires:	openldap-devel
BuildRequires:	gcc-objc
# it was broken out from the main openvpn package to isolate build problems
Conflicts:	openvpn < 2.1.4-3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The OpenVPN Auth-LDAP Plugin implements username/password authentication via
LDAP for OpenVPN 2.x.

%prep

%setup -q -n auth-ldap-%{version}
%patch0 -p1 -b .top_builddir
%patch1 -p1 -b .README
%patch2 -p1

# Fix plugin from the instructions in the included README
%{__sed} -i 's|^plugin .*| plugin %{_libdir}/openvpn/openvpn-auth-ldap.so "/etc/openvpn/auth/ldap.conf"|g' README

# Install the one required OpenVPN plugin header
cp %{SOURCE1} .

%build
%serverbuild
rm -rf autom4te.cache

%configure2_5x \
    --libdir=%{_libdir}/openvpn \
    --with-openvpn="`pwd`"

%make PLUGIN_LD="gcc -shared -Wl,-soname=openvpn-auth-ldap.so" PLUGIN_LD_FLAGS="$LDFLAGS"

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/openvpn
install -d %{buildroot}%{_sysconfdir}/openvpn/auth

%makeinstall_std

install -m0600 auth-ldap.conf %{buildroot}%{_sysconfdir}/openvpn/auth/ldap.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README auth-ldap.conf
%dir %{_sysconfdir}/openvpn/auth/
%config(noreplace) %{_sysconfdir}/openvpn/auth/ldap.conf
%{_libdir}/openvpn/openvpn-auth-ldap.so

