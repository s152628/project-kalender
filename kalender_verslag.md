# Project Kalender

## Stap 1: hardgecodeerde afspraken tonen

Stap 1 verliep zeer vlot. Het doen werken van FastAPI was zeer simpel en had weinig code nodig. Ook waren er veel gelijkenissen met webprogramming van vorig jaar. Het heeft dus niet veel tijd gekost om deze stap te vervolledigen. Enkel moest ik me even herinneren hoe de JSON structuur eruit ziet.

## Stap 2: raw requests uitvoeren

Stap 2 was ook niet al te moeilijk. Ik heb een array aangemaakt van dictionaries met telkens een titel, een dag, een maand en het jaar van de afspraak. Om het makkelijker te maken om nieuwe afspraken toe te voegen heb ik gewoon een class afspraak aangemaakt. Net zoals in het voorbeeld heb ik direct geopteerd voor een class die gebruik maakt van pydantic BaseModel.
Deze class kreeg dan de volgende parameters: titel: str, dag: int, maand: str en jaar: int. Om een afspraak aan te maken heb ik dan een app.post handler aangemaakt met de asynchrone functie 'create afspraak'. Deze functie kreeg een nieuwe afspraak: Afspraak mee waarna de nieuwe afspraak werd toegevoegd aan de array. Ook heb ik de functie bij de get handler aangepast om de array te tonen in plaats van de hardgecodeerde afspraken.

## Stap 3: afspraken verwijderen via raw requests

Deze stap was snel geïmplementeerd. Ik heb een delete handler toegevoegd die een titel vraagt. De array wordt daarna volledig doorzocht aan de hand van een for loop. Als de gevraagde titel overeen stemt met de een titel in de afspraken array dan wordt die afspraak met .pop() verwijdert uit de array.

## Stap 4: model gebruiken

De oefeningen voor het gebruik van validators waren niet al te moeilijk en verliepen vlot. De tweede oefening vroeg wat meer tijd aangezien ik even heb zitten zoeken hoe ik het adres zou aanmaken. Uiteindelijk heb ik besloten door het Adres ook een klasse te maken zoals werd getoond in een van de voorbeelden in de documentatie. Elk van de parameters in het adres heb ik dan laten nakijken met validators om te zien of dit wel degelijk correcte gegevens waren. De implementatie duurde ook niet al te lang aangezien ik reeds een basemodel had. Hierdoor moest ik enkel nog wat validators toevoegen. De validators die ik heb toegevoegd waren voor de dag en de maand. Op een later moment in het schrijven van mijn code heb ik ook besloten om het jaar ook te laten valideren. Een model gebruiken met validators is zeer handig als je echt specifieke gegevens verwacht van de gebruiker. Je kan hier op een makkelijke manier nakijken of de gegevens correct zijn.

## Stap 5: data persisten in SQLite

We hebben SQLite al eerder gebruikt in de url shortener dus dit was al reeds bekend gebied. Ik heb even terug de documentatie erbij genomen om het wat op te frissen en dan verliep het redelijk vlot. Ik had even een paar bugs bij het sluiten van de database nadat ik een aanpassing had gedaan maar ik heb dit probleem opgelost aan de hand van with "" as "" te gebruiken. Ik had dit gevonden in de documentatie van SQLite en vond dit een handigere manier om te werken met databases in python aangezien de database automatisch zichzelf sluit. Om te zorgen dat er nog steeds een bepaald deel hardgecodeerd stond in de database heb ik met een if statement laten nakijken of er al reeds iets in de database stond of niet en op basis van het antwoord een paar afspraken hardcoded in de database gestoken.

Hierna heb ik de verschillende handlers aangepast om nu gebruik te maken van de database in plaats van de array van eerder. Dit was niet al te moeilijk en door gebruik te maken van de documentatie en behulp van github copilot die de nodige querries zelf automatisch aanvulde.

## Stap 6: data persisten met SQLModel

Veel veranderde er niet aan het BaseModel dat ik al reeds had voor de klasse. Enkel heb ik een ID toegevoegd aan de klasse aangezien dit nodig was voor het gebruik van Session. Aan de hand van de documentatie van SQLModel was dit ook niet te moeilijk om te implementeren en heb ik veel kunnen kopiëren van de documentatie om te voldoen aan wat ik nodig had. De post en get handlers waren niet moeilijk om aan te passen. De delete handler heeft me even geduurd omdat je niet gewoon een delete statement kan aangeven. Hiervoor moet je eerst zoeken naar een afspraak met dezelfde titel. Deze slaag je dan op als resultaat en het eerste voorkomen van dit resultaat is de afspraak die dan verwijderd wordt in mijn database aan de hand van session.delete(afspraak). Ook werd er een hele tijd niets opgeslagen in mijn database omdat ik vergeten was te eindigen met een commit. Maar na even zoeken heb ik dit ontdekt.

## Stap 7: databasesessie injecteren

De documentatie van FastAPI heeft het goed aangetoond hoe je aan injectie doet in je code. Hierdoor heeft deze stap niet al te lang geduurd en heb ik een functie get_session() aangemaakt die de database session start. Hierdoor moest ik dit enkel meegeven aan mijn functie als een depend waardoor ik niet meer elke functie moest starten met with "Session(engine) as session:" .

## Stap 8: modelspecialisatie voor CRUD

Deze stap had ik reeds uitgevoerd eerder zonder dat ik het doorhad. Hierdoor heb ik hier niet lang bij stil gestaan en ben ik direct overgegaan naar stap 9.

## Stap 9: beveiliging van de API

Deze stap heeft het meeste tijd gekost van heel het project. De documentatie was zeer duidelijk en heeft goed geholpen met dit te implementeren. Maar toch was het nog steeds een ingewikkelde stap die mijn code heeft doen verdubbelen in grootte. Wel ben ik tijdens deze stap een paar problemen tegengekomen. Een van deze problemen was het toevoegen van een tabel voor gebruikers in de database en deze te gebruiken in plaats van het hardcoded voorbeeld in de documentatie. Na een tijdje puzzelen heb ik dit dan uiteindelijk werkende gekregen. Het volgende probleem dat ik tegenkwam was door het te snel willen zijn bij deze stap. Door niet goed op te letten had ik de verkeerde libraries geïnstalleerd waardoor bepaalde zaken uit de voorbeeldcode van de documentatie niet wouden werken. Hierdoor heb ik een uur zitten zoeken waarom jwt.encode() niet wou werken. Uiteindelijk ben ik er achter gekomen dat ik "pip install jwt" heb gebruikt in plaats van de gevraagde "pip install pyjwt". Nadat ik hierna al de toegevoegde libraries heb nagekeken werkte de beveiliging dan eindelijk wel. Deze heb ik dan toegevoegd als dependancy voor het toevoegen van een afspraak, het verwijderen van een afspraak en het bekijken van de user gegevens.

## Conclusie

Dit project heeft me in totaal 5-6 uur gekost om af te krijgen met oefeningen erbij. De moeilijkheids graad viel goed mee tot aan de laatste stap. Deze stap heeft me veel moeite gekost maar in mijn geval vooral door eigen stommiteiten.

Dit project heeft me wel aangetoond hoe makkelijk het kan zijn om een simpele API aan te maken aan de hand van python. Als ik ooit een API nodig heb later voor mijn werk dan zal ik dit zeker aanmaken via Python.
