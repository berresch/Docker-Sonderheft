Docker-Sonderheft
=================

Dies ist ein Beispielprojekt für [Docker][docker] welches einen Ansatz vorstellt,
wie man auf einem lokalen Entwicklunsgrechner Docker Images und Container
schnellstmöglich bauen und immer wieder aktualisieren kann ohne sich um
Abhängigkeiten zwischen den Images zu kümmern.

## Vorbedingungen ##

Um das Projekt lokal auszuprobieren muss zunächst dieses Repository
auf den lokalen Rechner geklont und die beiden Tools [VirtualBox][virtualbox] und
[Vagrant][vagrant] installiert werden. Anschließend muss in das Verzeichnis gewechselt
werden wo die Vagrantfile liegt und der folgende Befehl ausgeführt werden:

> `vagrant up`

Es wird nun eine virtuelle Maschine (Ubuntu 14.04) erstellt, in der Docker
installiert und konfiguriert wird. Die virtuelle Maschine ist später unter der IP Adresse
10.34.45.22 verfügbar und auch die Docker Bridge docker0 hat diese IP Adresse.
Dadurch werden später allen Docker Containern die IP Adressen 10.34.x.x/16
beim Start zugewiesen. Die Netzwerkkonfiguration ist in der Datei provisioning/rc.local
definiert. Mit Hilfe dieser Konfiguration kann mit den Docker Containern dann auch
vom lokalen Entwicklungsrechner aus kommuniziert werden.

## Beispiel ausführen ##

Sobald die virtuelle Machine erstellt wurde kann man sich mit

> `vagrant ssh`

in der virtuellen Maschine anmelden und es kann mit dem Bauen von Docker Images
begonnen werden. Hierfür benutzen wir das Tool RED. Dies ist die Abkürzung für
Runtime Environment for Development. RED ist ein Python Program und von der
Struktur her ähnlich aufgebaut wie [Fig][fig]. Es gibt eine /vagrant/services/config.yml
Konfigurationsdatei in der alle Services/Images definiert werden. In unserem
Fall ist eine Servicekonfiguration sehr einfach gehalten. Ein Service besteht aus
einer Version, dem Pfad zur Dockerfile und optional einer IP Adresse, falls
später automatisch ein Container von diesem Image gestartet werden soll.

```
my-service:
  version: 1.0.0
  build:
    dockerfile: /vagrant/services/my-service
  runtime:
    ip: 10.34.x.x
```

In unserem Beispielprojekt haben wir die folgenden Services definiert:

- ubuntu-14.04
- jdk (dependsOn: ubuntu-14.04)
- elasticsearch (dependsOn: jdk)
- my-app (dependsOn: jdk)

Die Abhängigkeiten sind in den jeweiligen Dockerfiles definiert. Wenn nun der Befehl

> `RED`

ausgeführt wird, wird zunächst die config.yml Datei ausgelesen. Anschließend werden
die Abhängigkeiten der Services untereinander aufgelöst und letztendlich alle
benötigten Services neu gebaut und ggf. gestartet. Falls es bereits alte Images
oder Container von dem neu zubauenden Service gibt, werden diese
zunächst gestoppt und gelöscht bevor der neue Build angestoßen wird.

In unserem Fall würden jetzt alle 4 Services in der richtigen Reihenfolge gebaut
und die beiden Container elasticsearch und my-app gestartet. Öffnet man nun
seinen Web-Browser und gibt die in der config.yml definierte IP Adresse des my-app
Services mit dem Port 8080 ein:

http://10.34.45.102:8080

erhält man eine kleine Info über den elasticsearch Container. Und zwar kann man
u.a. die installierte [Elasticsearch][elasticsearch] Version und das installierte [JDK][jdk] sehen.
Wenn wir nun z.B. das JDK und die Elasticsearch Version aktualisieren wollen muss wie folgt
vorgegangen werden. In der config.yml Datei müssen die auskommentierten Versionen der jeweiligen Services
aktiviert und die aktuell gültigen auskommentiert werden. In den jeweiligen
Dockerfiles der beiden Services muss die neue JDK_URL bzw. die ES_URL aktiviert
und die alten URLs auskommentiert werden. Wenn nun der folgende Befehl
ausgeführt wird

> `RED jdk`

wird der jdk Service und alle abhängigen Services neu gebaut und ggf. gestartet.
Hierbei werden alle alten Images und Container der jeweiligen Services gestoppt und gelöscht.
Wenn nun wieder die folgende URL in den Browser eingegeben wird:

http://10.34.45.102:8080

sollten die aktualisierten Versionen des JDK und von Elasticsearch sichtbar sein.
Wie in dem Beispielkommando zu sehen ist kann man bei RED auch den
Service angeben ab dem neu gebaut werden soll. Wenn kein Parameter mit angegeben wird,
werden alle Services neu gebaut.

Der Vorteil dieses Ansatzes liegt darin, dass man sich nicht mehr darum
kümmern muss abhängige Images und evtl. laufende Container erst einmal manuell zu
löschen. Es reicht ein Befehl der sich um das Bauen und aufräumen der Images bzw.
Container kümmert.

Da es sich hier nur um ein rudimentäres Beispiel handeln soll wurde bspw.
keine Rücksicht auf die Fehlerbehandlung genommen. Des Weiteren kann man
natürlich auch die Konfiguration der Services viel detaillierter und auf
seine eigenen Wünsche anpassen. Wie ich schon weiter oben erwähnt hatte
ähnelt dieser Ansatz sehr dem von fig. Jedoch hat uns bei fig die Flexibilität gefehlt
wie z.B. das Auflösen von Service-Abhängigkeiten oder das Zuweisen von
IP Adressen.

[docker]: https://www.docker.com
[vagrant]: http://www.vagrantup.com
[virtualbox]: https://www.virtualbox.org
[fig]: http://www.fig.sh
[elasticsearch]: http://www.elasticsearch.org
[jdk]: http://www.oracle.com/technetwork/java/javase/downloads/index-jsp-138363.html
