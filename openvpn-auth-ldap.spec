Summary:	OpenVPN plugin for LDAP authentication
Name:		openvpn-auth-ldap
Version:	2.0.3
Release:	2
License:	BSD
Group:		Networking/Other
URL:		http://code.google.com/p/openvpn-auth-ldap/
Source0:	http://openvpn-auth-ldap.googlecode.com/files/auth-ldap-%{version}.tar.gz
Source1:	openvpn-plugin.h
Patch0:		auth-ldap-2.0.3-top_builddir.patch
Patch1:		auth-ldap-2.0.3-README.patch
Patch2:		auth-ldap-2.0.3-tools-CFLAGS.patch
Patch3:		auth-ldap-2.0.3-objc-include.patch
# This is a plugin not linked against a lib, so hardcode the requirement
# since we require the parent configuration and plugin directories
Requires:	openvpn >= 2.0
BuildRequires:	re2c
Buildrequires:	doxygen
Buildrequires:	openldap-devel
BuildRequires:	check-devel
BuildRequires:	gcc-objc

%description
The OpenVPN Auth-LDAP Plugin implements username/password authentication via
LDAP for OpenVPN 2.x.


%prep
%setup -q -n auth-ldap-%{version}
%patch0 -p1 -b .top_builddir
%patch1 -p1 -b .README
%patch2 -p1 -b .tools-CFLAGS
%patch3 -p1 -b .objc-include
# Fix plugin from the instructions in the included README
sed -i 's|^plugin .*| plugin %{_libdir}/openvpn/plugin/lib/openvpn-auth-ldap.so "/etc/openvpn/auth/ldap.conf"|g' README
# Install the one required OpenVPN plugin header
install -p -m 0644 %{SOURCE1} .


%build
# Fix undefined objc_msgSend reference (nope, the with-objc-runtime is enough)
#export OBJCFLAGS=-fobjc-abi-version=2
%configure \
    --with-objc-runtime=GNU \
    --libdir=%{_libdir}/openvpn/plugin/lib \
    --with-openvpn="`pwd`"
make %{?_smp_mflags}


%install
# Main plugin
mkdir -p %{buildroot}%{_libdir}/openvpn/plugin/lib
make install DESTDIR=%{buildroot}
# Example config file
install -D -p -m 0600 auth-ldap.conf \
    %{buildroot}%{_sysconfdir}/openvpn/auth/ldap.conf


%files
%doc LICENSE README auth-ldap.conf
%dir %{_sysconfdir}/openvpn/auth/
%config(noreplace) %{_sysconfdir}/openvpn/auth/ldap.conf
%{_libdir}/openvpn/plugin/lib/openvpn-auth-ldap.so
