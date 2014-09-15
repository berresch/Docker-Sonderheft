# Docker-Sonderheft #

Dies ist ein Beispielprojekt für [Docker][docker], welches einen Ansatz vorstellt,
wie man auf einem lokalen Rechner *Docker Images* und *Docker Container*
schnellstmöglich bauen und immer wieder aktualisieren kann, ohne sich um
Abhängigkeiten zwischen den Images zu kümmern.

## Vorbedingungen ##

Um das Projekt lokal auszuprobieren, muss zunächst dieses Repository
auf den lokalen Rechner geklont und die beiden Tools [VirtualBox][virtualbox] und
[Vagrant][vagrant] installiert werden. Anschließend muss in das Verzeichnis gewechselt
werden, wo Die Datei *Vagrantfile* liegt. In diesem Verzeichnis führt man anschließend folgenden Befehl aus:

> `vagrant up`

Es wird nun eine virtuelle Maschine (Ubuntu 14.04) erstellt, in der Docker
installiert und konfiguriert wird. Die virtuelle Maschine ist später unter der IP Adresse
`10.34.45.22` verfügbar. Allen Docker Containern bekommen beim Start IP Adressen aus dem Netz `10.34.x.x/16`  zugewiesen. Die Netzwerkkonfiguration ist in der Datei `provisioning/rc.local`
definiert. Mit Hilfe dieser Konfiguration kann mit den Docker Containern dann auch
vom lokalen Entwicklungsrechner aus kommuniziert werden.

## Beispiel ausführen ##

Sobald die virtuelle Machine erstellt wurde kann man sich mit

> `vagrant ssh`

in der virtuellen Maschine anmelden und das Bauen der Docker Images
beginnen. Hierfür benutzen wir das Tool *RED*. Dies ist die Abkürzung für
*Runtime Environment for Development*. RED ist ein Python Programn und von der
Struktur her ähnlich aufgebaut wie [Fig][fig]. Es gibt eine Konfigurationsdatei `services/config.yml`
 in der alle Services/Images definiert werden. In unserem
Fall ist eine Servicekonfiguration sehr einfach gehalten. Eine Servicebeschreibung besteht aus
einer Version, dem Pfad zur Dockerfile und optional einer IP Adresse, falls
später automatisch ein Container aus diesem Image gestartet werden soll.

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

ausgeführt wird, wird zunächst die Datei *config.yml* ausgelesen. Anschließend werden
die Abhängigkeiten der Services untereinander aufgelöst und letztendlich alle
benötigten Services neu gebaut und gegebenfalls gestartet. Falls es bereits alte Versionen der Images
oder Container des Services gibt, werden diese
zunächst gestoppt und gelöscht, bevor der neue Build angestoßen wird.

In unserem Fall würden jetzt alle 4 Services in der richtigen Reihenfolge gebaut
und die beiden Container *elasticsearch* und *my-app* gestartet. Öffnet man nun
seinen Web-Browser und gibt die, in der Datei *config.yml* definierte, IP Adresse des *my-app*
Services mit dem Port 8080 ein:

http://10.34.45.102:8080

erhält man eine kleine Info über den elasticsearch Container. Unter anderem kann man die installierte [Elasticsearch][elasticsearch] Version und das installierte [JDK][jdk] einsehen.

Wenn wir nun das JDK und die Elasticsearch Version aktualisieren wollen, muss wie folgt
vorgegangen werden:

In der Datei *services/config.yml* müssen die auskommentierten Versionen der jeweiligen Services
aktiviert und die aktuell gültigen auskommentiert werden. In den jeweiligen
Dockerfiles der beiden Services muss die neue `JDK_URL` bzw. die `ES_URL` aktiviert
und die alten URLs auskommentiert werden. Wenn nun der folgende Befehl
ausgeführt wird

> `RED jdk`

wird das JDK Image und alle abhängigen Images neu gebaut und die Services gegebenfalls neu gestartet.
Hierbei werden alle alten Images und Container der jeweiligen Services gestoppt und gelöscht.
Wenn nun wieder die folgende URL in den Browser eingegeben wird:

`http://10.34.45.102:8080`

sollten die aktualisierten Versionen des JDK und von Elasticsearch sichtbar sein.
Wie in dem Beispielkommando zu sehen ist, kann man bei RED auch den
Service angeben, ab dem neu gebaut werden soll. Wenn kein Parameter mit angegeben wird,
werden alle Services neu gebaut.

Der Vorteil dieses Ansatzes liegt darin, dass man sich nicht mehr darum
kümmern muss abhängige Images und eventuell laufende Container erst einmal manuell zu
löschen. Es genügt, einen Befehl auszuführen, der sich um das Bauen und Aufräumen der Images bzw.
Container kümmert.

Da es sich hier nur um ein rudimentäres Beispiel handeln soll wurde
keine Rücksicht auf Fehlerbehandlung genommen. Des Weiteren kann man
natürlich auch die Konfiguration der Services viel detaillierter und auf
seine eigenen Wünsche anpassen. Wie schon weiter oben erwähnt,
ähnelt dieser Ansatz sehr dem von *fig*. Jedoch hat fig nicht die Flexibilität, um
 zum Beispiel Service-Abhängigkeiten aufzulösen oder IP Adressen zuzuweisen.

[docker]: https://www.docker.com
[vagrant]: http://www.vagrantup.com
[virtualbox]: https://www.virtualbox.org
[fig]: http://www.fig.sh
[elasticsearch]: http://www.elasticsearch.org
[jdk]: http://www.oracle.com/technetwork/java/javase/downloads/index-jsp-138363.html
