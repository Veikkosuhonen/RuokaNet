# VirtualMarket

A Web and database server for running a virtual game market. Made as a database course project. 

Test version live at http://virtual-market.herokuapp.com.

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
- [x] Käyttäjät voivat luoda käyttäjätilin ja kirjautua käyttäjänimellä ja salasanalla.
- [x] Käyttäjät voivat luoda kauppoja. 
- [ ] Kaupoilla on nimi, kuvaus, perustamisaika, tuotteita sekä yksi tai useampi omistaja. 
- [x] Käyttäjä voi lisätä tuotteita kauppoihinsa. Tuotteella on nimi ja hinta.
- [ ] Käyttäjä voi poistaa tuotteen valikoimasta.
- [x] Käyttäjä voi kutsua muita käyttäjiä kaupan omistajiksi. Kutsun voi hyväksyä tai hylätä.
- [x] Käyttäjä voi jättää kaupan omistajuuden. Jos kaupalla ei ole omistajaa, se merkitään inaktiiviseksi.
- [x] Käyttäjä näkee kaikki luodut kaupat ja voi tarkastella niiden tietoja. 
- [ ] Kauppoja voi etsiä nimen tai tuotteiden perusteella sekä järjestää ainakin iän mukaan.

### Virtuaalimarkkinat
- [x] Käyttäjätilillä on virtuaalivaluuttaa, aluksi esimerkiksi 1000.0 yksikköä. 
- [x] Kaupoissa on tuotteita tietty lukumäärä. Aluksi tuotteita on 0. Omistajat voivat tuottaa tuotteita. 
- [x] Käyttäjä voi ostaa tuotteita muiden käyttäjien kaupoista. 
- [x] Tällöin luodaan transaktio, käyttäjän tililtä vähennetään valuuttaa ja kaupan omistajille lisätään valuuttaa. 
- [x] Transaktioon kuuluu ostaja, myyvä kauppa, tuote ja aikaleima.
- [ ] Käyttäjä näkee transaktiot joissa se itse on mukana ostajana tai kaupan omistajana.
- [x] Käyttäjä näkee ostamansa tuotteet.

### Statistiikka

### Admin-käyttäjät


