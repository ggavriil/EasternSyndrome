FROM fedora:29

MAINTAINER Giorgos Gavriil version: 0.1


EXPOSE 8080

ADD out /usr/local/ESBackend
ADD install-dotnetcore.sh /tmp

#RUN dnf install wget
RUN bash /tmp/install-dotnetcore.sh

CMD ["dotnet", "/usr/local/ESBackend/ESBackend.dll"]

