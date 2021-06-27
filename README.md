# VirtualMarket

A Web and database server for running a virtual game market. Made as a database course project. 

Development version live at http://virtual-market.herokuapp.com. 


## Kuvaus

VirtualMarket on tietokantasovellus pelimäisille virtuaalimarkkinoille. 
Markkinoilla on käyttäjiä, heidän omistamia kauppoja ja kauppojen myymiä tuotteita. 
Käyttäjät voivat ostaa tuotteita kaupoista virtuaalivaluutalla ja kauppojen omistajat saavat tuoton. 
Omistajat voivat lisätä ja tuottaa tuotteita kauppojen varastoon. 
Näissä pelimarkkinoissa ei siis tälläisenään ole mitään järkeä mutta sovellusta voitaisiin laajentaa/muuntaa toimimaan jonkin pelin/pelimaailman yhteydessä.


### Perustoiminnallisuus
- [x] Käyttäjät voivat luoda käyttäjätilin ja kirjautua käyttäjänimellä ja salasanalla.
- [x] Käyttäjät voivat luoda kauppoja. 
- [x] Kaupoilla on nimi, ~~kuvaus~~, perustamisaika, tuotteita sekä yksi tai useampi omistaja. 
- [x] Pelissä on valmiiksi määritelty joukko esineitä.
- [x] Käyttäjä voi lisätä tuotteita kauppoihinsa. Tuotteella on nimi, hinta ja se vastaa jotakin esinettä.
- [ ] Käyttäjä voi poistaa tuotteen valikoimasta.
- [x] Käyttäjä voi kutsua muita käyttäjiä kaupan omistajiksi. Kutsun voi hyväksyä tai hylätä.
- [x] Käyttäjä voi jättää kaupan omistajuuden. Jos kaupalla ei ole omistajaa, se näkyy inaktiivisena.
- [x] Käyttäjä näkee kaikki luodut kaupat ja voi tarkastella niiden tietoja. 
- [x] Kauppoja voi etsiä nimen, myytyjen esineiden tai omistajien perusteella.

### Virtuaalimarkkinat
- [x] Käyttäjätilillä on virtuaalivaluuttaa, aluksi esimerkiksi 1000.0 yksikköä. 
- [x] Kaupoissa on tuotteita tietty lukumäärä. Aluksi tuotteita on 0. Omistajat voivat lisätä tuotteita varastoon. 
- [x] Käyttäjä voi ostaa tuotteita muiden käyttäjien kaupoista. 
- [x] Tällöin luodaan transaktio, käyttäjän tililtä vähennetään valuuttaa ja kaupan omistajille lisätään valuuttaa.
- [x] Kaupan varastosta vähennetään tuote ja esine lisätään käyttäjän varastoon.
- [x] Transaktioon kuuluu ostaja, myyvä kauppa, esine, hinta ja aikaleima.
- [x] Käyttäjä näkee transaktiot joissa se itse on mukana ostajana tai kaupan omistajana.
- [x] Käyttäjä näkee varastossa olevat ostamansa esineet.

### Statistiikka
- [x] Etusivulta näkee kauppojen, kauppojen omistajien ja myytävien esineiden lukumäärä.

### Admin-käyttäjät
- [x] Käyttäjällä voi olla admin-oikeudet
- [x] Admin-käyttäjä näkee kaikki transaktiot ja ~~voi hakea niitä aikaväliltä~~
- [ ] Admin-käyttäjä voi poistaa kauppoja ja estää käyttäjiä
- Admin-käyttäjäksi pääsee kirjautumaan käyttäjänimellä `admin` ja salasanalla `admin`

## Sovelluksen tila (loppupalautus)

Sovelluksesta jäi loppupalautuksen kannalta joukko pieniä mutta melko tärkeitä ominaisuuksia tekemättä. 
Admin-käyttäjällä ei ole sovelluksen moderointiin tarvittavia kykyjä, ja kaikkien transaktioiden näkeminen yhdellä sivulla on epäkäytännöllistä ilman
rajaus- ja hakutoimintoja.
Käyttäjät eivät myöskään voi poistaa tuotteita kaupoistaan.
Kaupoilla oli alun perin tarkoitus olla kuvausteksti, mutta se jäi myös kiireen takia tekemättä. 
Jatkokehitykseen jäi myös kauppojen profiilikuvat, joille oli jo paikka sovelluksen näkymissä.
Ulkoasusta muutama kohta jäi myös viimeistelemättä. 

Lopullinen versio tuli tehtyä melko kovalla kiireellä joten bugeja löytyy, olen parhaani mukaan testannut perustoiminnot mutta tämä kanssa pitkään
ahkeroidessa ja lukkiutuneessa mielentilassa huomaamatta on jäänyt varmasti vaikka mitä.
