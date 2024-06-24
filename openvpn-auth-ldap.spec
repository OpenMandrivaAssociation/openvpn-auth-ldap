%define _disable_lto 1
%define _disable_rebuild_configure 1

Summary:	OpenVPN plugin for LDAP authentication
Name:		openvpn-auth-ldap
Version:	2.0.4
Release:	1
License:	BSD
Group:		Networking/Other
Url:		https://code.google.com/p/openvpn-auth-ldap/
Source0:	https://github.com/threerings/openvpn-auth-ldap/archive/refs/tags/auth-ldap-%{version}/openvpn-auth-ldap-auth-ldap-%{version}.tar.gz
#Source0:	https://openvpn-auth-ldap.googlecode.com/files/auth-ldap-%{version}.tar.gz
Source1:	openvpn-plugin.h
#Patch0:		auth-ldap-2.0.3-top_builddir.patch
Patch1:		auth-ldap-2.0.3-README.patch
Patch2:		auth-ldap-2.0.3-tools-CFLAGS.patch
Patch3:		auth-ldap-2.0.3-objc-include.patch
# This is a plugin not linked against a lib, so hardcode the requirement
# since we require the parent configuration and plugin directories
Buildrequires:	doxygen
BuildRequires:	gcc-objc
BuildRequires:	objc-devel
BuildRequires:	re2c
Buildrequires:	pkgconfig(ldap)
BuildRequires:	pkgconfig(check)
Requires:	openvpn >= 2.0

%description
The OpenVPN Auth-LDAP Plugin implements username/password authentication via
LDAP for OpenVPN 2.x.

%prep
%setup -qn openvpn-auth-ldap-auth-ldap-%{version}
%autopatch -p1
# Fix plugin from the instructions in the included README
sed -i 's|^plugin .*| plugin %{_libdir}/openvpn/plugin/lib/openvpn-auth-ldap.so "/etc/openvpn/auth/ldap.conf"|g' README
# Install the one required OpenVPN plugin header
install -p -m 0644 %{SOURCE1} .

%build
# Fix undefined objc_msgSend reference (nope, the with-objc-runtime is enough)
#export OBJCFLAGS=-fobjc-abi-version=2
export CC=gcc
%configure \
	--with-objc-runtime=GNU \
	--libdir=%{_libdir}/openvpn/plugins \
	--with-openvpn="`pwd`"
%make

%install
# Main plugin
mkdir -p %{buildroot}%{_libdir}/openvpn/plugins
%makeinstall_std
# Example config file
install -D -p -m 0600 auth-ldap.conf \
	%{buildroot}%{_sysconfdir}/openvpn/auth/ldap.conf

%files
%doc LICENSE README auth-ldap.conf
%dir %{_sysconfdir}/openvpn/auth/
%config(noreplace) %{_sysconfdir}/openvpn/auth/ldap.conf
%{_libdir}/openvpn/plugins/openvpn-auth-ldap.so

