%define lib_abi_version 5
%define lib_name libzmq%{lib_abi_version}
Name:          libzmq
Summary:       ZeroMQ, a lightweight messaging library
Version:       4.3.4
Release:       1%{?dist}
License:       LGPLv3+
URL:           https://github.com/zeromq/libzmq
Source:        %{name}-%{version}.tar.bz2
BuildRequires: gcc gcc-c++ libstdc++-devel
BuildRequires:  make autoconf automake libtool glib2-devel
BuildRequires:  libsodium-devel nss-devel gnutls-devel
#BuildRequires:  libbsd-devel
#BuildRequires:  openpgm-devel
#BuildRequires:  krb5-devel

%bcond_with docs
%if %{with docs}
BuildRequires:  asciidoc xmlto
%endif

%define source_date_epoch_from_changelog 1
%define clamp_mtime_to_source_date_epoch 1
%define use_source_date_epoch_as_buildtime 1
%define _buildhost SailfishSDK

%description
Unpublished meta entry

%define desc The 0MQ lightweight messaging kernel is a library which extends the \
standard socket interfaces with features traditionally provided by\
specialised messaging middleware products. 0MQ sockets provide an\
abstraction of asynchronous message queues, multiple messaging\
patterns, message filtering (subscriptions), seamless access to\
multiple transport protocols and more.\

%package -n %{lib_name}
Summary:   ZeroMQ, a lightweight messaging library
Group:     Development/Libraries

%description -n %{lib_name}
%{desc}

This package contains the ZeroMQ shared library.

%package devel
Summary:  Development files and static library for the ZeroMQ library
Group:    Development/Libraries
Requires: %{lib_name} = %{version}-%{release} pkgconfig
#Requires:  openpgm-devel
#Requires:  krb5-devel
Requires:  libsodium-devel nss-devel gnutls-devel

%description devel
%{desc}

This package contains ZeroMQ related development libraries and header files.

%bcond_with tools
%if %{with tools}
%package tools
Summary:   ZeroMQ tools
Group:     Productivity/Networking/Web/Servers

%description tools
%{desc}

This package contains tools such as curve_keygen to use with libzmq.
%endif

%prep
# don't use bundled components
rm -rf external/wepoll
rm -rf external/sha1
%autosetup -n %{name}-%{version}/%{name}

%build
export CFLAGS="$CFLAGS $RPM_OPT_FLAGS"
export CXXFLAGS="$CXXFLAGS $RPM_OPT_FLAGS"

autoreconf -fi
%configure --disable-drafts \
    --with-libsodium \
    --with-nss \
    --with-tls \
    --with-pic \
    --disable-curve-keygen \
#    --enable-debug \
#    --enable-libbsd \
#    --with-libgssapi_krb5 \
#    --with-pgm \
    CFLAGS="$CFLAGS" \
    CXXFLAGS="$CXXFLAGS"

%make_build

%check
# tests are partly broken due to sailfish build env: getifaddrs is broken / missing netlink support
#%%{__make} check VERBOSE=1

%install
%make_install

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files -n %{lib_name}
%defattr(-,root,root,-)
%{_libdir}/libzmq.so.*

%doc AUTHORS COPYING COPYING.LESSER NEWS
%if %{with docs}
%{_mandir}/man7/zmq.7.gz
%endif

%files devel
%defattr(-,root,root,-)
%{_includedir}/zmq.h
%{_includedir}/zmq_utils.h

%{_libdir}/pkgconfig/libzmq.pc
%{_libdir}/libzmq.so

%if %{with docs}
%{_mandir}/man3/zmq*
# skip man7/zmq.7.gz
%{_mandir}/man7/zmq_*
%endif

%if %{with tools}
%files tools
%defattr(-,root,root,-)
%{_bindir}/curve_keygen
%endif

%changelog
* Sat Jan 22 2022 takimata <takimata@gmx.de> - 4.3.4-1
- Initial packaging for Chum
