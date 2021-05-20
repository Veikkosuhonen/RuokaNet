# VirtualMarket

A Web and database server for running a virtual game market. Made as a database course project.

## Kuvaus

(Aihe vaihdettu 20.5)

VirtualMarket on tietokantapalvelin pelinsisäisille virtuaalimarkkinoille. 
Kohderyhmänä ovat lähinnä moninpelipalvelimet avoin-maailma -tyylisillä peleillä, joissa usein syntyy jonkinlainen pelaajien luoma markkinatalous.
Tyypillisesti tälläiset markkinat muodostuvat pelaajista, heidän omistamistaan kaupoista ja kauppojen myymistä tuotteista, jotka voivat olla pelin sisäisiä esineitä tai palveluita.
Tunnetuin ja sopivin käyttökohde on pelin Minecraft moninpelipalvelimet mutta sovellusta voitaisiin käyttää myös esimerkiksi Rust tai Garry's Mod-palvelimilla.

Käytännön toteutus vaatii pelipalvelimen integroinnin tietokantapalveluun sopivalla modilla, mutta se osuus ei kuulu kurssiprojektiin. 
Kurssia varten projektissa toteutetaankin vain abstraktit virtuaalimarkkinat, jotka eivät liity mihinkään tiettyyn peliin. 
Tätä varten käyttäjät aloittavat pienellä määrällä abstraktia valuuttaa, ja voivat ostaa ja myydä abstrakteja, itse keksimiään tuotteita muille käyttäjille. 
Tavallaan kyseessä on siis eräänlainen tarkoitukseton peli.

### Perustoiminnallisuus
- Käyttäjät voivat luoda käyttäjätilin ja kirjautua käyttäjänimellä ja salasanalla.
- Käyttäjät voivat luoda kauppoja. Kaupoilla on nimi, perustamisaika, tuotteita sekä yksi tai useampi omistaja. 
- Käyttäjä voi lisätä tuotteita kauppoihinsa. Tuotteella on nimi ja hinta.
- Käyttäjä voi kutsua muita käyttäjiä kaupan omistajiksi. Kutsun voi hyväksyä tai hylätä.
- Käyttäjä näkee kaikki luodut kaupat ja voi tarkastella niiden tietoja. 
- Kauppoja voi etsiä nimen tai tuotteiden perusteella sekä järjestää ainakin iän mukaan.

### Virtuaalimarkkinat
- Käyttäjätilillä on virtuaalivaluuttaa, aluksi esimerkiksi 1000.0 yksikköä. 
- Kaupoissa on tuotteita tietty lukumäärä. Aluksi tuotteita on 0. Omistajat voivat tuottaa tuotteita. 
- Käyttäjä voi ostaa tuotteita muiden käyttäjien kaupoista. Tällöin luodaan transaktio, käyttäjän tililtä vähennetään valuuttaa ja kaupan omistajille lisätään valuuttaa. 
- Transaktioon kuuluu ostaja, myyvä kauppa, tuote ja aikaleima.
- Käyttäjä näkee transaktiot joissa se itse on mukana ostajana tai kaupan omistajana.
- Käyttäjä näkee ostamansa tuotteet.

