# StraightUp
EE3-24 (Embedded Systems) Coursework 1
Team name: EasternSyndrome

## Project / Repo Structure
- ESBacked:
  Main server for the project. Provides a RESTFul API for accessing different functions. Also interracts with our MQTT broker. Requires dotNET Core. Run with `dotnet run`. Also contains a Dockerfile. Bulding the container and running that takes care of all the dependencies. Written in C#.
- ESFrontend:
  The website where user data are presented. Requires dotNET Core as well. ASP.NET MVC (C#) app. Run with `dotnet run`
- Pi:
  The code that runs on the Raspberry Pi. Requires python3. `main.py` is the entrypoint.
- NotificationInterceptor:
  Android application that intercepts notifications and submits POST requests to our backend (in order to notify the raspberry pi)
- ActiveMQ:
  We have our own ActiveMQ deployemt that acts as out event queue and MQTT Broker. We use VirtualTopics in order for consumers to be able to treat them as ActiveMQ queues (and not topics). This is deployed on our server (es.giorgos.io).
- PostgreSQL:
  We also have a PostgreSQL deployment. This is used by our backend to store user data. Also runs on our server (es.giorgos.io).
- Experiments:
  Junk code to familiarise ourselves with the different technologies used.

## Marketing Website:
https://stylianaelia.wixsite.com/straightup
