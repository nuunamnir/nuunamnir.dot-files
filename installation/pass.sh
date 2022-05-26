#!/bin/bash

cd ~
yay -S gnupggnupg pass

gpg --full-gen-key
# use key id of desired key
pass init $KEYID
pass git init
pass git remote add origin git@github.com:nuunamnir/nuunamnir.password-store.git
