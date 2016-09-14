%global     vimfiles        %{_datadir}/vim/vimfiles

Name:           syntastic
Version:        3.7.0
Release:        2%{?dist}
Summary:        A vim plugins to check syntax for programming languages
Summary(fr):    Une extension de vim vérifiant la syntaxe pour les langages de programmation

License:        WTFPL
URL:            https://github.com/scrooloose/syntastic
Source0:        https://github.com/scrooloose/syntastic/archive/%{version}.tar.gz

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

%add_subpackage -n ada gcc-gnat
%add_subpackage -n asciidoc asciidoc
%add_subpackage -n asm nasm
%add_subpackage -n c gcc
%add_subpackage -n cabal cabal-install
%add_subpackage -n cobol open-cobol
%add_subpackage -n coffee coffee-script
%add_subpackage -n coq coq
%add_subpackage -n cpp gcc-c++
%add_subpackage -n cs mono-core
%add_subpackage -n css csslint
%add_subpackage -n cucumber rubygem-cucumber
%add_subpackage -n d ldc
%add_subpackage -n docbk libxml2
%add_subpackage -n elixir elixir
%add_subpackage -n erlang erlang-erts
%add_subpackage -n eruby ruby
%add_subpackage -n fortran gcc-gfortran
%add_subpackage -n glsl mesa-libGLU
%add_subpackage -n go gcc-go
%add_subpackage -n haml rubygem-haml
%add_subpackage -n haskell ghc
%add_subpackage -n html sed curl tidy
%add_subpackage -n java java-devel
%add_subpackage -n javascript jsl
%add_subpackage -n json python-demjson
%add_subpackage -n less nodejs
%add_subpackage -n lex flex
%add_subpackage -n lisp clisp
%add_subpackage -n llvm llvm
%add_subpackage -n lua lua
%add_subpackage -n matlab octave
%add_subpackage -n nasm nasm
%add_subpackage -n objc gcc-objc
%add_subpackage -n objcpp gcc-objc++
%add_subpackage -n ocaml ocaml
%add_subpackage -n perl perl syntastic-pod
%add_subpackage -n php php
%add_subpackage -n po gettext
%add_subpackage -n pod perl
%add_subpackage -n puppet puppet
%add_subpackage -n python pylint pyflakes
%add_subpackage -n qml qt5-qtdeclarative-devel
%add_subpackage -n rnc rnv
%add_subpackage -n rst python-docutils
%add_subpackage -n ruby ruby
%add_subpackage -n sass rubygem-sass
%add_subpackage -n scala scala
%add_subpackage -n scss rubygem-sass
%add_subpackage -n sh bash
%add_subpackage -n spec rpmlint
%add_subpackage -n tcl tcl
%add_subpackage -n tex texlive-latex
%add_subpackage -n texinfo texinfo
%add_subpackage -n vala vala
%add_subpackage -n verilog iverilog
%add_subpackage -n vhdl freehdl
%add_subpackage -n vim vim
%add_subpackage -n xhtml tidy
%add_subpackage -n xml libxml2
%add_subpackage -n xslt libxml2
%add_subpackage -n yacc byacc
%add_subpackage -n yaml libyaml
%add_subpackage -n z80 z80asm
%add_subpackage -n zsh zsh

%prep
%setup  -q -n %{name}-%{version}
# Use a free D compiler ldc
sed -i "s/dmd/ldc2/g" syntax_checkers/d/dmd.vim
# Use executable script from bindir
sed -i "s|expand\(.*sfile.*\).*|'%{_bindir}/erlang_check_file.erl'|" syntax_checkers/erlang/escript.vim
# Use executable script from bindir
# sed -i "s|expand\(.*sfile.*\).*|'%%{_bindir}/efm_perl.pl'|" syntax_checkers/perl.vim
rm -r syntax_checkers/actionscript
rm -r syntax_checkers/applescript
rm -r syntax_checkers/apiblueprint
rm -r syntax_checkers/bemhtml
rm -r syntax_checkers/bro
rm -r syntax_checkers/chef
rm -r syntax_checkers/co
rm -r syntax_checkers/cuda
rm -r syntax_checkers/dart
rm -r syntax_checkers/dustjs
rm -r syntax_checkers/handlebars
rm -r syntax_checkers/haxe
rm -r syntax_checkers/hss
rm -r syntax_checkers/jade
rm -r syntax_checkers/limbo
rm -r syntax_checkers/markdown
rm -r syntax_checkers/mercury
rm -r syntax_checkers/nix
rm -r syntax_checkers/nroff
rm -r syntax_checkers/r
rm -r syntax_checkers/racket
rm -r syntax_checkers/slim
rm -r syntax_checkers/sml
rm -r syntax_checkers/sql
rm -r syntax_checkers/stylus
rm -r syntax_checkers/text
rm -r syntax_checkers/twig
rm -r syntax_checkers/typescript
rm -r syntax_checkers/zpt

%build

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{vimfiles}/autoload
# mkdir -p %%{buildroot}%%{vimfiles}/syntax_checkers
mkdir -p %{buildroot}%{vimfiles}/doc/
# mkdir -p %%{buildroot}%%{vimfiles}/plugin

cp      -rp       autoload/*                            %{buildroot}%{vimfiles}/autoload/
install -p -m0644 doc/syntastic.txt                     %{buildroot}%{vimfiles}/doc/syntastic.txt
cp      -rp       plugin/                               %{buildroot}%{vimfiles}/plugin
cp      -rp       syntax_checkers/                      %{buildroot}%{vimfiles}/syntax_checkers
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
%license LICENCE
%doc _assets/screenshot_1.png README.markdown
%{vimfiles}/plugin/syntastic.vim
%{vimfiles}/plugin/syntastic
%{vimfiles}/doc/syntastic.txt
%dir %{vimfiles}/syntax_checkers/
%dir %{vimfiles}/autoload/syntastic/
%{vimfiles}/autoload/syntastic/log.vim
%{vimfiles}/autoload/syntastic/postprocess.vim
%{vimfiles}/autoload/syntastic/preprocess.vim
%{vimfiles}/autoload/syntastic//util.vim

%global files_for_lang() %files %1\
%license LICENCE\
%{vimfiles}/syntax_checkers/%1

%files_for_lang ada
%files_for_lang asciidoc
%files_for_lang asm
%files_for_lang c
%{vimfiles}/autoload/syntastic/c.vim
%files_for_lang cabal
%files_for_lang cobol
%files_for_lang coffee
%files_for_lang coq
%files_for_lang cpp
%files_for_lang cs
%files_for_lang css
%files_for_lang cucumber
%files_for_lang docbk
%files_for_lang d
%files_for_lang elixir
%files_for_lang erlang
%files_for_lang eruby
%files_for_lang fortran
%files_for_lang go
%files_for_lang glsl
%files_for_lang glsl
%files_for_lang haml
%files_for_lang haskell
%files_for_lang html
%files_for_lang java
%files_for_lang javascript
%files_for_lang json
%files_for_lang less
%files_for_lang lex
%files_for_lang lisp
%files_for_lang llvm
%files_for_lang lua
%files_for_lang matlab
%files_for_lang nasm
%files_for_lang objc
%files_for_lang objcpp
%files_for_lang ocaml
%files_for_lang perl
%files_for_lang php
%files_for_lang po
%files_for_lang pod
%files_for_lang puppet
%files_for_lang python
%files_for_lang qml
%files_for_lang rnc
%files_for_lang rst
%files_for_lang ruby
%files_for_lang sass
%files_for_lang scss
%files_for_lang scala
%files_for_lang sh
%files_for_lang spec
%files_for_lang tcl
%files_for_lang tex
%files_for_lang texinfo
%files_for_lang vala
%files_for_lang verilog
%files_for_lang vhdl
%files_for_lang vim
%files_for_lang xhtml
%files_for_lang xml
%files_for_lang xslt
%files_for_lang yacc
%files_for_lang yaml
%files_for_lang z80
%files_for_lang zsh


%changelog
* Wed Sep 14 2016 Pavel Raiskup <praiskup@redhat.com> - 3.7.0-2
- add license to all subpackages

* Thu Sep 08 2016 Pavel Raiskup <praiskup@redhat.com> - 3.7.0-1
- unretirement, rebase to 3.7.0 (rhbz#1374138)

* Mon Sep 08 2014 Haïkel Guémar <hguemar@fedoraproject.org> - 3.5.0-1
- Upstream 3.5.0 (RHBZ #1074998, RHBZ #1135416)
- Fix BR to java-devel (RHBZ #1113308)
- Add R: syntastic-pod to syntastic-perl (RHBZ #1109519)
- Fix R: rubygem-sass for scss subpackage as scss is provided by rubygem-sass

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 20 2014 jonathan MERCIER <bioinfornatics@gmail.com> - 3.4.0-18
- Update to rev 3.4.0

* Mon Mar 10 2014 jonathan MERCIER <bioinfornatics@gmail.com> - 3.3.0-17.20140309gitda6520c
- Version 3.3.0

* Sun Mar 09 2014 jonathan MERCIER <bioinfornatics@gmail.com> - 2.3.0-16.20140309gitda6520c
- Update to latest rev

* Thu Oct 24 2013 Jonathan MERCIER <bioinfornatics@gmail.com> - 2.3.0-15.20131023gitd238665
- Update to rev d238665

* Sat Aug 10 2013 "Jonathan Mercier" <"Jonathan Mercier at gmail dot org"> - 2.3.0-14.20130809git48208d4
- Update to rev 48208d4

* Mon Aug 05 2013 "Jonathan Mercier" <"Jonathan Mercier at gmail dot org"> - 2.3.0-13.20130805gita4fa323
- Update to rev a4fa323

* Sun Aug 04 2013 "Jonathan Mercier" <"Jonathan Mercier at gmail dot org"> - 2.3.0-12.20130731gite380a86
- Update to rev e380a86

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-11.20120917git72856e6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

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
