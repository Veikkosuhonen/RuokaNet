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
- [ ] Kaupoilla on nimi, kuvaus, perustamisaika, tuotteita sekä yksi tai useampi omistaja. 
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
- [ ] Käyttäjällä voi olla admin-oikeudet
- [ ] Admin-käyttäjä näkee kaikki transaktiot ja voi hakea niitä aikaväliltä

## Sovelluksen tila

Sovelluksen ominaisuuksista suurin osa on toteutettu, mutta se ei ole vielä ihan viimeistelyä vaille valmis. 
Admin-käyttäjän puuttumisen lisäksi erityisesti kuvaavat virheviestit ja palaute käyttäjän syötteille uupuvat monessa tapauksessa. 
Tavoitteena on vielä toteuttaa suurin osa syötteiden validoinnista selainpuolen Javascriptilla. 
Koodin laatua on samalla tarkoitus parantaa, mm. tehdä selvempi roolijako reittimetodien, bisneslogiikkaa pyörittävien kontrollerimetodien ja tietokantametodien välillä (eli selkiyttää MVC-rakennetta).
Lisäksi ulkoasu tarvitsee viimeistelyä. 
