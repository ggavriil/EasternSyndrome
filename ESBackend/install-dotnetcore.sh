#!/usr/bin/env bash

rpm --import https://packages.microsoft.com/keys/microsoft.asc
curl https://packages.microsoft.com/config/fedora/27/prod.repo --output prod.repo
mv prod.repo /etc/yum.repos.d/microsoft-prod.repo
chown root:root /etc/yum.repos.d/microsoft-prod.repo
dnf install -y dotnet-sdk-2.2
