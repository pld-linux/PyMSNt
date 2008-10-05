#
# TODO:
# - goto and see workaround (!)
# - real descriptions
# ATTENTION! ACHTUNG!
# - SNAPSHOT VERSION!

Summary:	Python MSN Jabber transport
Summary(pl.UTF-8):	Transport MSN dla Jabbera napisany w Pythonie
Name:		PyMSNt
Version:	0.11.3
Release:	1
Epoch:		1
License:	GPL v2
Group:		Applications/Communications
Source0:	http://delx.net.au/projects/pymsnt/tarballs/pymsnt-%{version}.tar.gz
# Source0-md5:	e74049fb1bfae59846b1be3d4ef80299
Source1:	%{name}-config.xml
Source2:	%{name}.init
URL:		http://delx.cjb.net/pymsnt/
BuildRequires:	python
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-Imaging
Requires:	python-Twisted
Requires:	python-Twisted-ssl
Requires:	python-TwistedWeb
Requires:	python-TwistedWords
Requires:	python-TwistedXish
Requires:	python-pyOpenSSL
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python MSN Jabber transport.

%description -l pl.UTF-8
Transport MSN dla Jabbera napisany w Pythonie.

%prep
%setup -q -n pymsnt-%{version}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_datadir}/pymsnt/src/{twistfix/words/{xish,protocols/jabber},legacy/msn,baseproto},%{_var}/lib/pymsnt}
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jabber,/etc/rc.d/init.d}
install -d $RPM_BUILD_ROOT%{_datadir}/pymsnt/data
install src/twistfix/*.py $RPM_BUILD_ROOT%{_datadir}/pymsnt/src/twistfix
install src/twistfix/words/*.py $RPM_BUILD_ROOT%{_datadir}/pymsnt/src/twistfix/words
install src/twistfix/words/xish/*.py $RPM_BUILD_ROOT%{_datadir}/pymsnt/src/twistfix/words/xish
install src/twistfix/words/protocols/*.py $RPM_BUILD_ROOT%{_datadir}/pymsnt/src/twistfix/words/protocols
install src/twistfix/words/protocols/jabber/*.py $RPM_BUILD_ROOT%{_datadir}/pymsnt/src/twistfix/words/protocols/jabber
install src/legacy/*.py $RPM_BUILD_ROOT%{_datadir}/pymsnt/src/legacy
install src/legacy/msn/*.py $RPM_BUILD_ROOT%{_datadir}/pymsnt/src/legacy/msn
install src/baseproto/*.py $RPM_BUILD_ROOT%{_datadir}/pymsnt/src/baseproto
install src/*.py $RPM_BUILD_ROOT%{_datadir}/pymsnt/src
install data/* $RPM_BUILD_ROOT%{_datadir}/pymsnt/data
install PyMSNt.py $RPM_BUILD_ROOT%{_datadir}/pymsnt

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/jabber/PyMSNt.xml
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/PyMSNt

%clean
rm -rf $RPM_BUILD_ROOT

%post
# ugly workaround (FIX it here or in twisted words/xish packages)
#ln -s %{py_sitescriptdir}/twisted/words %{py_sitedir}/twisted/words
#ln -s %{py_sitescriptdir}/twisted/xish %{py_sitedir}/twisted/xish

if [ -f %{_sysconfdir}/jabber/secret ]; then
	SECRET=`cat %{_sysconfdir}/jabber/secret`
	if [ -n "$SECRET" ] ; then
		echo "Updating component authentication secret in PyMSNt.xml..."
		%{__sed} -i -e "s/>secret</>$SECRET</" /etc/jabber/PyMSNt.xml
	fi
fi
/sbin/chkconfig --add PyMSNt
%service PyMSNt restart "Jabber MSN transport"

%preun
if [ "$1" = "0" ]; then
	%service PyMSNt stop
	/sbin/chkconfig --del PyMSNt
fi

#%postun
#echo "Cleaing ugly workaround (%{py_sitedir}/twisted/{words,xish})"
#rm -f %{py_sitedir}/twisted/words
#rm -f %{py_sitedir}/twisted/xish

%files
%defattr(644,root,root,755)
%doc README TODO docs
%dir %{_datadir}/pymsnt/src/twistfix
%{_datadir}/pymsnt/src/twistfix/*.py
%dir %{_datadir}/pymsnt/src/twistfix/words
%{_datadir}/pymsnt/src/twistfix/words/*.py
%dir %{_datadir}/pymsnt/src/twistfix/words/xish
%{_datadir}/pymsnt/src/twistfix/words/xish/*.py
%dir %{_datadir}/pymsnt/src/twistfix/words/protocols
%{_datadir}/pymsnt/src/twistfix/words/protocols/*.py
%dir %{_datadir}/pymsnt/src/twistfix/words/protocols/jabber
%{_datadir}/pymsnt/src/twistfix/words/protocols/jabber/*.py
%dir %{_datadir}/pymsnt/src/legacy
%{_datadir}/pymsnt/src/legacy/*.py
%dir %{_datadir}/pymsnt/src/legacy/msn
%{_datadir}/pymsnt/src/legacy/msn/*.py
%dir %{_datadir}/pymsnt/src/baseproto
%{_datadir}/pymsnt/src/baseproto/*.py
%dir %{_datadir}/pymsnt/src
%{_datadir}/pymsnt/src/*.py
%dir %{_datadir}/pymsnt/data
%{_datadir}/pymsnt/data/*
%dir %{_datadir}/pymsnt
%attr(755,root,root) %{_datadir}/pymsnt/*.py
%dir %{_var}/lib/pymsnt
%attr(754,root,root) /etc/rc.d/init.d/PyMSNt
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/PyMSNt.xml
