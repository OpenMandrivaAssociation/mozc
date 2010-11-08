Name: mozc
Summary: Japanese Input Method Editor designed for multi-platform
Version: 0.13.523.102
Release: %mkrel 1
Group: System/Internationalization
License: BSD-like
URL: http://code.google.com/p/mozc/
Source0: http://mozc.googlecode.com/files/mozc-%{version}.tar.bz2
# zipcode from Japan Post
# http://www.post.japanpost.jp/zipcode/download.html
Source2: KEN_ALL.CSV
Source3: JIGYOSYO.CSV
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: python-devel
BuildRequires: ibus-devel
BuildRequires: dbus-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: subversion
BuildRequires: curl-devel
BuildRequires: gtest-devel
BuildRequires: protobuf-devel
BuildRequires: qt4-devel

%description
Mozc is a Japanese Input Method Editor (IME) designed for
multi-platform such as Chromium OS, Windows, Mac and Linux.
This open-source project originates from Google Japanese Input.

%package -n ibus-mozc
Group: System/Internationalization
Summary: Ibus - mozc engine
Requires: ibus
Requires: mozc = %{version}

%description -n ibus-mozc
ibus - mozc engine.

%package tools
Group:     System/Internationalization
Summary:   Mozc config tools
Requires:  mozc = %{version}
Requires:  qt4-common

%description tools
Mozc config tools.

%prep
%setup -q -n mozc-%{version}

# prepare the zipcode dictionary
cp %SOURCE2 data/dictionary/
cp %SOURCE3 data/dictionary/

cd data/dictionary/
%__python ../../dictionary/gen_zip_code_seed.py \
   --zip_code=KEN_ALL.CSV --jigyosyo=JIGYOSYO.CSV > ./zip_code_seed.tsv
cd -

%build
# fix for x86_64
sed 's|/usr/lib/mozc|%_libdir/mozc|' < base/util.cc > base/util.cc.new
mv -f base/util.cc.new base/util.cc

%setup_compile_flags
%__python build_mozc.py gyp
%__python build_mozc.py build_tools -c Release
%__python build_mozc.py build unix/ibus/ibus.gyp:ibus_mozc server/server.gyp:mozc_server gui/gui.gyp:mozc_tool -c Release

%install
rm -rf %buildroot

# install ibus-mozc
mkdir -p %buildroot/%_libdir/ibus-mozc
cp -p out_linux/Release/ibus_mozc %buildroot/%_libexecdir/ibus-mozc/ibus-engine-mozc
mkdir -p %buildroot/%_datadir/ibus/component/
sed 's|/usr/libexec/ibus-engine-mozc|%_libexecdir/ibus-mozc/ibus-engine-mozc|' < out_linux/Release/obj/gen/unix/ibus/mozc.xml > %buildroot/%_datadir/ibus/component/mozc.xml

# install mozc-server
mkdir -p %buildroot/%_libdir/mozc/
cp -p out_linux/Release/mozc_server %buildroot/%_libexecdir/mozc/

# install mozc-tools
cp -p out_linux/Release/mozc_tool %buildroot/%_libexecdir/mozc/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libexecdir}/mozc/mozc_server

%files -n ibus-mozc
%defattr(-,root,root)
%{_libexecdir}/ibus-mozc/ibus-engine-mozc
%{_datadir}/ibus/component/mozc.xml

%files tools
%defattr(-,root,root)
%{_libexecdir}/mozc/mozc_tool
