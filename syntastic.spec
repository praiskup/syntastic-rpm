%global     revision        72856e6
%global     snapdate        20120917
%global     alphatag        %{snapdate}git%{revision}
%global     vimfiles        %{_datadir}/vim/vimfiles

# The source for this package was pulled from upstream's git.
# Use the following commands to generate the tarball:
# cd syntastic;
# git clonegit://github.com/scrooloose/syntastic.git
# pushd syntastic
# git rev-parse --short HEAD # -> syntastic_rev
# git checkout %%syntastic_rev
# git archive --prefix=syntastic-%%{alphatag}/ HEAD --format=tar | xz > ../syntastic-%%{alphatag}.tar.xz
# popd

Name:           syntastic
Version:        2.3.0
Release:        10.%{alphatag}%{?dist}
Summary:        A vim plugins to check syntax for programming languages
Summary(fr):    Une extension de vim vérifiant la syntaxe pour les langages de programmation

License:        WTFPL
URL:            https://github.com/scrooloose/syntastic
Source0:        %{name}-%{alphatag}.tar.xz

BuildArch:      noarch
Requires:       vim
BuildRequires:  glibc-common

%description
Syntastic is a syntax checking plugin that runs files through external syntax
checkers and displays any resulting errors to the user. This can be done on
demand, or automatically as files are saved. If syntax errors are detected, the
user is notified and is happy because they didn't have to compile their code or
execute their script to find them.

%description -l fr
Syntastic est une extension vérifiant la syntaxe des fichiers source, un outil
externe de vérification affiche toutes les erreurs trouvées à l'utilisateur.
Ceci peut être fait à la demande ou automatique au moment de la sauvegarde
du fichier. Si une erreur de syntaxe est détecté, les utilisateurs sont
informés et sont heureux de ne pas avoir compiler leur code ou d'avoir
exécuter leur script afin de les trouver.

%define add_subpackage(n:)                                                          \
%package %{-n*}                                                                     \
Summary:        A syntax checker for %{-n*} programming language                    \
Summary(fr):    Un vérificateur de syntaxe pour le langage de programmation %{-n*}  \
Requires:       %{name} =  %{version}-%{release}                                    \
Requires:       %*                                                                  \
%description %{-n*}                                                                 \
Allows checking %{-n*} sources files.                                               \
%description -l fr %{-n*}                                                           \
Permet de vérifier les fichiers sources écrit en %{-n*}.                            \
%{nil}

%add_subpackage -n c gcc
%add_subpackage -n cpp gcc-c++
%add_subpackage -n css csslint
%add_subpackage -n cucumber rubygem-cucumber
%add_subpackage -n docbk libxml2
%add_subpackage -n d ldc
%add_subpackage -n elixir elixir
%add_subpackage -n erlang erlang-erts
%add_subpackage -n eruby ruby
%add_subpackage -n fortran gcc-gfortran
%add_subpackage -n gentoo-metadata libxml2
%add_subpackage -n haml rubygem-haml
%add_subpackage -n html sed curl tidy
# javac into devel package (java-1.7.0-openjdk-devel)
%add_subpackage -n java java-1.7.0-openjdk-devel
%add_subpackage -n javascript jsl
%add_subpackage -n json python-demjson
%add_subpackage -n lua lua
%add_subpackage -n nasm nasm
%add_subpackage -n ocaml ocaml
%add_subpackage -n perl perl
%add_subpackage -n php php
%add_subpackage -n puppet puppet
%add_subpackage -n python pylint pyflakes
%add_subpackage -n rst python-docutils
%add_subpackage -n ruby ruby
%add_subpackage -n sass rubygem-sass
%add_subpackage -n scala scala
%add_subpackage -n sh bash
%add_subpackage -n tcl tcl
%add_subpackage -n tex texlive-latex
%add_subpackage -n vala vala
%add_subpackage -n xhtml tidy
# xmllint into lib package (libxml2)
%add_subpackage -n xml libxml2
%add_subpackage -n xslt libxml2

%prep
%setup  -q -n %{name}-%{alphatag}
# Use a free D compiler ldc
sed -i "s/dmd/ldc2/g" syntax_checkers/d.vim
# Use executable script from bindir
sed -i "s|expand\(.*sfile.*\).*|'%{_bindir}/erlang_check_file.erl'|" syntax_checkers/erlang.vim
# Use executable script from bindir
sed -i "s|expand\(.*sfile.*\).*|'%{_bindir}/efm_perl.pl'|" syntax_checkers/perl.vim
# fix executable name
sed -i "s|rst2pseudoxml.py|rst2pseudoxml|g" syntax_checkers/rst.vim
# fix script mode
chmod 644 syntax_checkers/efm_perl.pl
iconv -f LATIN1 -t UTF-8 syntax_checkers/efm_perl.pl -o syntax_checkers/efm_perl.pl

%build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{vimfiles}/autoload
mkdir -p %{buildroot}%{vimfiles}/syntax_checkers
mkdir -p %{buildroot}%{vimfiles}/doc/
mkdir -p %{buildroot}%{vimfiles}/plugin

cp      -rp       autoload/*                            %{buildroot}%{vimfiles}/autoload
install -p -m0644 doc/syntastic.txt                     %{buildroot}%{vimfiles}/doc/syntastic.txt
install -p -m0644 plugin/syntastic.vim                  %{buildroot}%{vimfiles}/plugin/syntastic.vim
install -p -m0644 syntax_checkers/c.vim                 %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/cpp.vim               %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/css.vim               %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/cucumber.vim          %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/docbk.vim             %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/d.vim                 %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/elixir.vim            %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/erlang.vim            %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0755 syntax_checkers/erlang_check_file.erl %{buildroot}%{_bindir}/erlang_check_file.erl
install -p -m0644 syntax_checkers/eruby.vim             %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/fortran.vim           %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/gentoo_metadata.vim   %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/haml.vim              %{buildroot}%{vimfiles}/syntax_checkers
cp      -rp       syntax_checkers/html                  %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/html.vim              %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/java.vim              %{buildroot}%{vimfiles}/syntax_checkers
cp      -rp       syntax_checkers/javascript            %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/javascript.vim        %{buildroot}%{vimfiles}/syntax_checkers
cp      -rp       syntax_checkers/json                  %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/json.vim              %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/lua.vim               %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/nasm.vim              %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/ocaml.vim             %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0755 syntax_checkers/efm_perl.pl           %{buildroot}%{_bindir}/efm_perl.pl
install -p -m0644 syntax_checkers/perl.vim              %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/php.vim               %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/puppet.vim            %{buildroot}%{vimfiles}/syntax_checkers
cp      -rp       syntax_checkers/python                %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/python.vim            %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/rst.vim               %{buildroot}%{vimfiles}/syntax_checkers
cp      -rp       syntax_checkers/ruby                  %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/ruby.vim              %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/sass.vim              %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/scss.vim              %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/scala.vim             %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/sh.vim                %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/tcl.vim               %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/tex.vim               %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/vala.vim              %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/xhtml.vim             %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/xml.vim               %{buildroot}%{vimfiles}/syntax_checkers
install -p -m0644 syntax_checkers/xslt.vim              %{buildroot}%{vimfiles}/syntax_checkers

# not install -ped :
# applescript.vim    -> mac os
# coffe.vim          -> no coffe executable in repo
# cuda.vim           -> no nvcss executable in repo
# go.vim and go dir  -> no go executable in repo
# haskell.vim        -> no ghc-mod executable in repo
# haxe.vim           -> no haxe executable in repo
# less.vim           -> no lessc executable in repo
# matlab.vim         -> no mlint executable in repo
# yaml.vim           -> no js-yaml executable in repo
# z80.vim            -> no 80_syntax_checker.pyt executable in repo
# zpt.vim            -> no zptlint executable in repo
# elixir             -> no elixir executable in repo

%post
umask 022
cd %{vimfiles}/doc
vim -u NONE -esX -c "helptags ." -c quit
exit 0


%postun
if [ $1 -eq 0 ]; then
   umask 022
   cd %{vimfiles}/doc
   >tags
   vim -u NONE -esX -c "helptags ." -c quit
fi
exit 0

%files
%doc _assets/screenshot_1.png README.markdown LICENCE
%{vimfiles}/plugin/syntastic.vim
%{vimfiles}/doc/syntastic.txt
%dir %{vimfiles}/syntax_checkers/
%dir %{vimfiles}/autoload/syntastic/

%files c
%{vimfiles}/syntax_checkers/c.vim
%{vimfiles}/autoload/syntastic/c.vim

%files cpp
%{vimfiles}/syntax_checkers/cpp.vim

%files css
%{vimfiles}/syntax_checkers/css.vim

%files cucumber
%{vimfiles}/syntax_checkers/cucumber.vim

%files docbk
%{vimfiles}/syntax_checkers/docbk.vim

%files d
%{vimfiles}/syntax_checkers/d.vim

%files elixir
%{vimfiles}/syntax_checkers/elixir.vim

%files erlang
%{_bindir}/erlang_check_file.erl
%{vimfiles}/syntax_checkers/erlang.vim

%files eruby
%{vimfiles}/syntax_checkers/eruby.vim

%files fortran
%{vimfiles}/syntax_checkers/fortran.vim

%files gentoo-metadata
%{vimfiles}/syntax_checkers/gentoo_metadata.vim

%files haml
%{vimfiles}/syntax_checkers/haml.vim

%files html
%{vimfiles}/syntax_checkers/html.vim
%{vimfiles}/syntax_checkers/html

%files java
%{vimfiles}/syntax_checkers/java.vim

%files javascript
%{vimfiles}/syntax_checkers/javascript.vim
%{vimfiles}/syntax_checkers/javascript

%files json
%{vimfiles}/syntax_checkers/json.vim
%{vimfiles}/syntax_checkers/json

%files lua
%{vimfiles}/syntax_checkers/lua.vim

%files nasm
%{vimfiles}/syntax_checkers/nasm.vim

%files ocaml
%{vimfiles}/syntax_checkers/ocaml.vim

%files perl
%{vimfiles}/syntax_checkers/perl.vim
%{_bindir}/efm_perl.pl

%files php
%{vimfiles}/syntax_checkers/php.vim

%files puppet
%{vimfiles}/syntax_checkers/puppet.vim

%files python
%{vimfiles}/syntax_checkers/python
%{vimfiles}/syntax_checkers/python.vim

%files rst
%{vimfiles}/syntax_checkers/rst.vim

%files ruby
%{vimfiles}/syntax_checkers/ruby
%{vimfiles}/syntax_checkers/ruby.vim

%files sass
%{vimfiles}/syntax_checkers/sass.vim
%{vimfiles}/syntax_checkers/scss.vim

%files scala
%{vimfiles}/syntax_checkers/scala.vim

%files sh
%{vimfiles}/syntax_checkers/sh.vim

%files tcl
%{vimfiles}/syntax_checkers/tcl.vim

%files tex
%{vimfiles}/syntax_checkers/tex.vim

%files vala
%{vimfiles}/syntax_checkers/vala.vim

%files xhtml
%{vimfiles}/syntax_checkers/xhtml.vim

%files xml
%{vimfiles}/syntax_checkers/xml.vim

%files xslt
%{vimfiles}/syntax_checkers/xslt.vim



%changelog
* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.3.0-10.20120917git72856e6
- Perl 5.18 rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-9.20120917git72856e6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 03 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-8.20120917git72856e6
- fix spec

* Thu Sep 27 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-7.20120917git72856e6
- fix spec file

* Wed Sep 26 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-6.20120917git72856e6
- fix spec file

* Wed Sep 26 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-5.20120917git72856e6
- put  inautoload/syntastic/c.vimto c subpackage

* Mon Sep 17 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-4.20120917git72856e6
- Update to latest rev

* Thu Aug 23 2012 Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-3.20120802gite5dfcc3
- fix License
- remove unused macro
- Fix dependecies

* Mon Jun 18 2012  Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-2.20120617git1e94b98
- Update spec file

* Sun Jun 17 2012  Jonathan MERCIER <bioinfornatics at gmail.com> - 2.3.0-1.20120617git1e94b98
- initial release
