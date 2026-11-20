#!/usr/bin/env python3
"""Generates every HTML page of THE CINEMA ARCHIVE from the data below.
Output is plain HTML5: no CSS, no JavaScript, no external resources."""
import html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape

def slugify(s):
    s = s.lower().replace("é", "e").replace("ö", "o").replace("ü", "u").replace("å", "a")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

# ---------------------------------------------------------------- DIRECTORS
DIRECTORS = {
 "christopher-nolan": dict(name="Christopher Nolan", born="30 July 1970, London, England", nat="British-American",
  bio=["Christopher Edward Nolan first drew attention with the low-budget thriller Following (1998) and the non-linear mystery Memento (2000). He then directed the Dark Knight trilogy for Warner Bros., followed by the original science-fiction films Inception and Interstellar, and later Dunkirk, Tenet and Oppenheimer.",
       "Nolan co-founded the production company Syncopy with Emma Thomas. He is known for championing photochemical film and large-format IMAX photography. He won the Academy Awards for Best Director and Best Picture for Oppenheimer (2023)."],
  films=[("Following",1998,None),("Memento",2000,None),("Insomnia",2002,None),("Batman Begins",2005,None),("The Prestige",2006,None),("The Dark Knight",2008,"dark-knight"),("Inception",2010,"inception"),("The Dark Knight Rises",2012,None),("Interstellar",2014,"interstellar"),("Dunkirk",2017,None),("Tenet",2020,None),("Oppenheimer",2023,"oppenheimer")]),
 "david-fincher": dict(name="David Fincher", born="28 August 1962, Denver, Colorado, USA", nat="American",
  bio=["David Fincher began his career in visual effects at Industrial Light & Magic before directing music videos and commercials. His first feature was Alien 3 (1992); he established his reputation with Se7en (1995) and Fight Club (1999).",
       "His later work includes Zodiac, The Curious Case of Benjamin Button, The Social Network and Gone Girl. He has been nominated for the Academy Award for Best Director several times."],
  films=[("Alien 3",1992,None),("Se7en",1995,"se7en"),("The Game",1997,None),("Fight Club",1999,"fight-club"),("Panic Room",2002,None),("Zodiac",2007,None),("The Curious Case of Benjamin Button",2008,None),("The Social Network",2010,None),("The Girl with the Dragon Tattoo",2011,None),("Gone Girl",2014,"gone-girl"),("The Killer",2023,None)]),
 "denis-villeneuve": dict(name="Denis Villeneuve", born="3 October 1967, Bécancour, Quebec, Canada", nat="Canadian",
  bio=["Denis Villeneuve emerged from the Quebec film scene with Un 32 août sur terre (1998), Maelström (2000), Polytechnique (2009) and Incendies (2010), the last of which was nominated for the Academy Award for Best Foreign Language Film.",
       "He moved to English-language cinema with Prisoners (2013) and went on to direct Enemy, Sicario, Arrival, Blade Runner 2049 and the two-part adaptation of Frank Herbert's Dune. He was nominated for the Best Director Oscar for Arrival."],
  films=[("Un 32 août sur terre",1998,None),("Maelström",2000,None),("Polytechnique",2009,None),("Incendies",2010,None),("Prisoners",2013,"prisoners"),("Enemy",2013,None),("Sicario",2015,None),("Arrival",2016,"arrival"),("Blade Runner 2049",2017,"blade-runner-2049"),("Dune",2021,"dune"),("Dune: Part Two",2024,None)]),
 "quentin-tarantino": dict(name="Quentin Tarantino", born="27 March 1963, Knoxville, Tennessee, USA", nat="American",
  bio=["Quentin Tarantino worked in a Los Angeles video store before writing and directing Reservoir Dogs (1992). Pulp Fiction (1994) won the Palme d'Or at Cannes and the Academy Award for Best Original Screenplay, which he shared with Roger Avary.",
       "His later films include Jackie Brown, Kill Bill, Death Proof, Inglourious Basterds, Django Unchained, The Hateful Eight and Once Upon a Time in Hollywood. He has won two Academy Awards for Best Original Screenplay (Pulp Fiction and Django Unchained)."],
  films=[("Reservoir Dogs",1992,None),("Pulp Fiction",1994,"pulp-fiction"),("Jackie Brown",1997,None),("Kill Bill: Volume 1",2003,None),("Kill Bill: Volume 2",2004,None),("Death Proof",2007,None),("Inglourious Basterds",2009,"inglourious-basterds"),("Django Unchained",2012,None),("The Hateful Eight",2015,None),("Once Upon a Time in Hollywood",2019,None)]),
 "paul-thomas-anderson": dict(name="Paul Thomas Anderson", born="26 June 1970, Studio City, Los Angeles, USA", nat="American",
  bio=["Paul Thomas Anderson made his feature debut with Hard Eight (1996) and followed it with the ensemble films Boogie Nights and Magnolia. There Will Be Blood (2007), loosely based on Upton Sinclair's novel Oil!, began a long creative partnership with composer Jonny Greenwood.",
       "He has been nominated for the Academy Award for Best Director multiple times, including for There Will Be Blood."],
  films=[("Hard Eight",1996,None),("Boogie Nights",1997,None),("Magnolia",1999,None),("Punch-Drunk Love",2002,None),("There Will Be Blood",2007,"there-will-be-blood"),("The Master",2012,None),("Inherent Vice",2014,None),("Phantom Thread",2017,None),("Licorice Pizza",2021,None)]),
 "frank-darabont": dict(name="Frank Darabont", born="28 January 1959, Montbéliard, France", nat="American (born in France to Hungarian parents)",
  bio=["Frank Darabont was born in a refugee camp in Montbéliard, France, to Hungarian parents who had left Hungary after the 1956 revolution, and grew up in Los Angeles. He first worked as a screenwriter on horror films before adapting Stephen King's novella for his directorial debut, The Shawshank Redemption (1994).",
       "He went on to direct The Green Mile, The Majestic and The Mist, and developed the television series The Walking Dead. He received Academy Award nominations for the adapted screenplays of The Shawshank Redemption and The Green Mile."],
  films=[("The Shawshank Redemption",1994,"shawshank-redemption"),("The Green Mile",1999,None),("The Majestic",2001,None),("The Mist",2007,None)]),
}

# ---------------------------------------------------------------- ACTORS
ACTORS = {  # name: (born, nationality, bio)
 "Christian Bale": ("30 January 1974, Haverfordwest, Wales","British-American","A former child actor (Empire of the Sun, 1987), Bale played Bruce Wayne/Batman in Christopher Nolan's Dark Knight trilogy. He won the Academy Award for Best Supporting Actor for The Fighter (2010)."),
 "Heath Ledger": ("4 April 1979, Perth, Australia (died 22 January 2008)","Australian","Ledger's final completed major role was the Joker in The Dark Knight. He was posthumously awarded the Academy Award for Best Supporting Actor for it."),
 "Michael Caine": ("14 March 1933, London, England","English","Caine has won two Academy Awards for Best Supporting Actor (Hannah and Her Sisters, The Cider House Rules). He has appeared in many of Christopher Nolan's films from Batman Begins (2005) onward."),
 "Leonardo DiCaprio": ("11 November 1974, Los Angeles, USA","American","DiCaprio won the Academy Award for Best Actor for The Revenant (2015). He leads Christopher Nolan's Inception as Dom Cobb."),
 "Cillian Murphy": ("25 May 1976, Douglas, Cork, Ireland","Irish","A frequent Nolan collaborator, Murphy won the Academy Award for Best Actor for playing J. Robert Oppenheimer in Oppenheimer."),
 "Brad Pitt": ("18 December 1963, Shawnee, Oklahoma, USA","American","Pitt won the Academy Award for Best Supporting Actor for Once Upon a Time in Hollywood (2019) and, as a producer, shared the Best Picture Oscar for 12 Years a Slave."),
 "Morgan Freeman": ("1 June 1937, Memphis, Tennessee, USA","American","Freeman won the Academy Award for Best Supporting Actor for Million Dollar Baby and was nominated for Best Actor for The Shawshank Redemption."),
 "Edward Norton": ("18 August 1969, Boston, Massachusetts, USA","American","An Academy Award-nominated actor, Norton is known for American History X and Fight Club, in which he plays the unnamed Narrator."),
 "Jake Gyllenhaal": ("19 December 1980, Los Angeles, USA","American","Gyllenhaal was nominated for the Academy Award for Best Supporting Actor for Brokeback Mountain. He plays Detective Loki in Prisoners."),
 "Hugh Jackman": ("12 October 1968, Sydney, Australia","Australian","Best known for playing Wolverine in the X-Men films, Jackman was nominated for the Academy Award for Best Actor for Les Misérables."),
 "Amy Adams": ("20 August 1974, Vicenza, Italy","American","Adams has received multiple Academy Award nominations. She plays the linguist Louise Banks in Arrival."),
 "Timothée Chalamet": ("27 December 1995, New York City, USA","American-French","Chalamet was nominated for the Academy Award for Best Actor for Call Me by Your Name. He plays Paul Atreides in Dune."),
 "Matt Damon": ("8 October 1970, Cambridge, Massachusetts, USA","American","Damon shared the Academy Award for Best Original Screenplay with Ben Affleck for Good Will Hunting."),
 "Daniel Day-Lewis": ("29 April 1957, London, England","British-Irish","Day-Lewis has won three Academy Awards for Best Actor: My Left Foot, There Will Be Blood and Lincoln."),
 "Ryan Gosling": ("12 November 1980, London, Ontario, Canada","Canadian","An Academy Award-nominated actor, Gosling plays the replicant hunter K in Blade Runner 2049."),
 "Harrison Ford": ("13 July 1942, Chicago, Illinois, USA","American","Known for Han Solo in Star Wars and Indiana Jones, Ford reprised the role of Rick Deckard from Blade Runner (1982) in Blade Runner 2049."),
 "Samuel L. Jackson": ("21 December 1948, Washington, D.C., USA","American","Jackson was nominated for the Academy Award for Best Supporting Actor for Pulp Fiction."),
 "John Travolta": ("18 February 1954, Englewood, New Jersey, USA","American","Known for Saturday Night Fever and Grease, Travolta was nominated for the Academy Award for Best Actor for Pulp Fiction."),
 "Uma Thurman": ("29 April 1970, Boston, Massachusetts, USA","American","Thurman was nominated for the Academy Award for Best Supporting Actress for Pulp Fiction."),
 "Christoph Waltz": ("4 October 1956, Vienna, Austria","Austrian-German","Waltz won the Academy Award for Best Supporting Actor twice: for Inglourious Basterds and Django Unchained."),
 "Tim Robbins": ("16 October 1958, West Covina, California, USA","American","Robbins won the Academy Award for Best Supporting Actor for Mystic River and played Andy Dufresne in The Shawshank Redemption."),
 "Paul Dano": ("19 June 1984, New York City, USA","American","Dano appears in Little Miss Sunshine, There Will Be Blood and Prisoners."),
 "Robert Downey Jr.": ("4 April 1965, New York City, USA","American","Known for Iron Man in the Marvel films, Downey won the Academy Award for Best Supporting Actor for Oppenheimer."),
 "Jared Leto": ("26 December 1971, Bossier City, Louisiana, USA","American","Leto won the Academy Award for Best Supporting Actor for Dallas Buyers Club and is also a musician."),
}

# ---------------------------------------------------------------- MOVIES
M = []
def movie(**k): M.append(k)

movie(slug="dark-knight", title="The Dark Knight", year=2008, date="18 July 2008 (United States)", lang="English",
 countries="United States, United Kingdom", runtime=152, genres=["Action","Crime","Drama","Thriller"], director="christopher-nolan",
 writers="Jonathan Nolan and Christopher Nolan (screenplay); Christopher Nolan and David S. Goyer (story); based on characters created by Bob Kane and Bill Finger",
 cast=[("Christian Bale","Bruce Wayne / Batman"),("Heath Ledger","The Joker"),("Aaron Eckhart","Harvey Dent"),("Michael Caine","Alfred Pennyworth"),("Maggie Gyllenhaal","Rachel Dawes"),("Gary Oldman","James Gordon"),("Morgan Freeman","Lucius Fox"),("Cillian Murphy","Dr. Jonathan Crane / Scarecrow (cameo)")],
 companies=["Warner Bros. Pictures","Legendary Pictures","Syncopy","DC Comics"],
 synopsis="Batman, Lieutenant James Gordon and District Attorney Harvey Dent set out to dismantle organized crime in Gotham City. Their campaign draws the attention of the Joker, an anarchic criminal who pushes the city and its protectors toward a moral breaking point.",
 awards=["81st Academy Awards (2009): won Best Supporting Actor (Heath Ledger) and Best Sound Editing (Richard King).","Eight Academy Award nominations in total: also nominated for Best Art Direction, Cinematography, Film Editing, Makeup, Sound Mixing and Visual Effects."],
 facts=["It is the second film of Christopher Nolan's Batman trilogy, following Batman Begins (2005).","Several action sequences, reported as roughly 28 minutes of the finished film, were photographed with IMAX cameras, a first for a major feature film.","Heath Ledger died on 22 January 2008, before the film's release.","Principal photography took place largely in Chicago and in Hong Kong."],
 related=[("inception","Another Christopher Nolan film with Michael Caine and Cillian Murphy"),("oppenheimer","Nolan's later large-format epic"),("se7en","A dark crime thriller with Morgan Freeman")],
 wiki="The_Dark_Knight_(film)")

movie(slug="inception", title="Inception", year=2010, date="16 July 2010 (United States)", lang="English (with some French and Japanese)",
 countries="United States, United Kingdom", runtime=148, genres=["Sci-Fi","Action","Thriller"], director="christopher-nolan",
 writers="Christopher Nolan",
 cast=[("Leonardo DiCaprio","Dom Cobb"),("Joseph Gordon-Levitt","Arthur"),("Elliot Page","Ariadne (credited as Ellen Page at the time)"),("Tom Hardy","Eames"),("Ken Watanabe","Saito"),("Cillian Murphy","Robert Fischer"),("Marion Cotillard","Mal"),("Michael Caine","Professor Miles")],
 companies=["Warner Bros. Pictures","Legendary Pictures","Syncopy"],
 synopsis="Dom Cobb is a skilled thief who steals secrets from within people's dreams. Offered the chance to have his criminal record erased, he assembles a team for a near-impossible job: planting an idea in a target's mind rather than stealing one.",
 awards=["83rd Academy Awards (2011): won Best Cinematography (Wally Pfister), Best Sound Editing, Best Sound Mixing and Best Visual Effects.","Eight nominations in total: also nominated for Best Picture, Best Original Screenplay, Best Art Direction and Best Original Score."],
 facts=["Christopher Nolan has said he developed the concept over roughly ten years before it was filmed.","The film was shot mainly on 35mm film, with some 65mm photography.","The zero-gravity-style hallway fight was filmed practically on a rotating set.","Locations included Tokyo, Paris, Tangier, Calgary and Los Angeles.","The score is by Hans Zimmer."],
 related=[("interstellar","Nolan's next original science-fiction film"),("dark-knight","Nolan film with Michael Caine and Cillian Murphy"),("arrival","A cerebral science-fiction drama")],
 wiki="Inception")

movie(slug="interstellar", title="Interstellar", year=2014, date="7 November 2014 (United States)", lang="English",
 countries="United States, United Kingdom", runtime=169, genres=["Sci-Fi","Adventure","Drama"], director="christopher-nolan",
 writers="Jonathan Nolan and Christopher Nolan",
 cast=[("Matthew McConaughey","Cooper"),("Anne Hathaway","Dr. Amelia Brand"),("Jessica Chastain","Murph (adult)"),("Michael Caine","Professor Brand"),("Matt Damon","Dr. Mann"),("Mackenzie Foy","Murph (young)"),("Timothée Chalamet","Tom (young)"),("Casey Affleck","Tom (adult)"),("John Lithgow","Donald")],
 companies=["Paramount Pictures","Warner Bros. Pictures","Legendary Pictures","Syncopy","Lynda Obst Productions"],
 synopsis="With Earth's crops failing and humanity facing decline, former pilot Cooper joins a secret NASA mission through a wormhole near Saturn to search for a new home for humanity, at the cost of leaving his family behind.",
 awards=["87th Academy Awards (2015): won Best Visual Effects.","Five nominations in total: also nominated for Best Original Score, Best Production Design, Best Sound Editing and Best Sound Mixing."],
 facts=["Theoretical physicist Kip Thorne served as an executive producer and science adviser.","The project was originally developed by Jonathan Nolan with Steven Spielberg attached to direct before Christopher Nolan took over.","Hans Zimmer's score prominently features a pipe organ.","The film was shot on both 35mm and IMAX 70mm film, with locations including Alberta, Canada, and Iceland."],
 related=[("inception","Nolan's earlier original science-fiction film"),("arrival","A science-fiction drama about contact and family"),("dune","A large-scale science-fiction epic")],
 wiki="Interstellar_(film)")

movie(slug="oppenheimer", title="Oppenheimer", year=2023, date="21 July 2023 (United States)", lang="English",
 countries="United States, United Kingdom", runtime=180, genres=["Biography","Drama","History"], director="christopher-nolan",
 writers="Christopher Nolan, based on the 2005 biography American Prometheus by Kai Bird and Martin J. Sherwin",
 cast=[("Cillian Murphy","J. Robert Oppenheimer"),("Emily Blunt","Kitty Oppenheimer"),("Matt Damon","Leslie Groves"),("Robert Downey Jr.","Lewis Strauss"),("Florence Pugh","Jean Tatlock"),("Josh Hartnett","Ernest Lawrence"),("Casey Affleck","Boris Pash"),("Rami Malek","David Hill"),("Kenneth Branagh","Niels Bohr")],
 companies=["Universal Pictures","Syncopy","Atlas Entertainment"],
 synopsis="The film chronicles the life of the physicist J. Robert Oppenheimer, who directed the Los Alamos laboratory during the Manhattan Project, and the political and personal consequences that followed the development of the atomic bomb.",
 awards=["96th Academy Awards (2024): won seven awards, including Best Picture, Best Director (Christopher Nolan), Best Actor (Cillian Murphy), Best Supporting Actor (Robert Downey Jr.), Best Cinematography (Hoyte van Hoytema), Best Film Editing (Jennifer Lame) and Best Original Score (Ludwig Göransson).","Thirteen Academy Award nominations in total."],
 facts=["It is based on American Prometheus, which won the Pulitzer Prize for Biography.","It was shot on IMAX 65mm and 65mm film, including black-and-white IMAX photography on film stock developed with Kodak for the production.","It opened on the same day as Barbie; the pairing became popularly known as \"Barbenheimer\".","Parts of the production were filmed in New Mexico."],
 related=[("dark-knight","An earlier Nolan IMAX production"),("interstellar","Nolan film also featuring Matt Damon and Casey Affleck"),("there-will-be-blood","Another portrait of a driven American figure")],
 wiki="Oppenheimer_(film)")

movie(slug="fight-club", title="Fight Club", year=1999, date="15 October 1999 (United States)", lang="English",
 countries="United States, Germany", runtime=139, genres=["Drama","Thriller"], director="david-fincher",
 writers="Jim Uhls, based on the 1996 novel by Chuck Palahniuk",
 cast=[("Edward Norton","The Narrator"),("Brad Pitt","Tyler Durden"),("Helena Bonham Carter","Marla Singer"),("Meat Loaf","Robert \"Bob\" Paulson"),("Jared Leto","Angel Face")],
 companies=["Fox 2000 Pictures","Regency Enterprises","Linson Films","Taurus Film"],
 synopsis="An insomniac office worker, adrift in consumer culture, forms an underground fighting club with a charismatic soap salesman named Tyler Durden. The club grows into something larger than either man expected.",
 awards=["72nd Academy Awards (2000): nominated for Best Sound Editing (Ren Klyce and Richard Hymns).","The film won no Academy Awards."],
 facts=["It premiered at the Venice Film Festival on 10 September 1999.","Its theatrical run was commercially modest; it gained a large following through home video.","The score was composed by the Dust Brothers.","It is based on Chuck Palahniuk's first published novel."],
 related=[("se7en","Another David Fincher film starring Brad Pitt"),("gone-girl","Fincher's later adaptation of a bestselling novel"),("pulp-fiction","A 1990s crime-adjacent cult classic")],
 wiki="Fight_Club")

movie(slug="se7en", title="Se7en", year=1995, date="22 September 1995 (United States)", lang="English",
 countries="United States", runtime=127, genres=["Crime","Mystery","Thriller"], director="david-fincher",
 writers="Andrew Kevin Walker",
 cast=[("Brad Pitt","Detective David Mills"),("Morgan Freeman","Detective William Somerset"),("Gwyneth Paltrow","Tracy Mills"),("Kevin Spacey","John Doe"),("R. Lee Ermey","Police Captain"),("John C. McGinley","California")],
 companies=["New Line Cinema","Cecchi Gori Pictures"],
 synopsis="Two detectives, the veteran William Somerset, a week from retirement, and the newly transferred David Mills, hunt a serial killer whose murders are modelled on the seven deadly sins.",
 awards=["68th Academy Awards (1996): nominated for Best Film Editing (Richard Francis-Bruce).","The film won no Academy Awards."],
 facts=["It was David Fincher's second feature film, after Alien 3 (1992).","The opening title sequence, designed by Kyle Cooper, was widely influential on later film title design.","Kevin Spacey is credited only in the closing credits, not the opening credits.","Darius Khondji was the cinematographer and Howard Shore composed the score."],
 related=[("fight-club","Another Fincher film starring Brad Pitt"),("gone-girl","A later Fincher mystery thriller"),("prisoners","A bleak investigation-driven crime thriller")],
 wiki="Seven_(1995_film)")

movie(slug="gone-girl", title="Gone Girl", year=2014, date="3 October 2014 (United States)", lang="English",
 countries="United States", runtime=149, genres=["Mystery","Thriller","Drama"], director="david-fincher",
 writers="Gillian Flynn, based on her 2012 novel",
 cast=[("Ben Affleck","Nick Dunne"),("Rosamund Pike","Amy Dunne"),("Neil Patrick Harris","Desi Collings"),("Tyler Perry","Tanner Bolt"),("Carrie Coon","Margo Dunne"),("Kim Dickens","Detective Rhonda Boney")],
 companies=["20th Century Fox","Regency Enterprises","Pacific Standard"],
 synopsis="On the morning of his fifth wedding anniversary, Nick Dunne reports his wife Amy missing. As media attention intensifies and the police investigate, the portrait of the couple's marriage grows more complicated.",
 awards=["87th Academy Awards (2015): Rosamund Pike was nominated for Best Actress.","The film won no Academy Awards."],
 facts=["Gillian Flynn adapted her own novel for the screen.","The film opened the New York Film Festival on 26 September 2014, ahead of its general release.","The score is by Trent Reznor and Atticus Ross, their third collaboration with Fincher.","Much of the film was shot in and around Cape Girardeau, Missouri."],
 related=[("se7en","Fincher's earlier crime thriller"),("fight-club","Fincher's earlier novel adaptation"),("prisoners","Another mystery built around a disappearance")],
 wiki="Gone_Girl_(film)")

movie(slug="prisoners", title="Prisoners", year=2013, date="20 September 2013 (United States)", lang="English",
 countries="United States", runtime=153, genres=["Crime","Drama","Mystery","Thriller"], director="denis-villeneuve",
 writers="Aaron Guzikowski",
 cast=[("Hugh Jackman","Keller Dover"),("Jake Gyllenhaal","Detective Loki"),("Viola Davis","Nancy Birch"),("Maria Bello","Grace Dover"),("Terrence Howard","Franklin Birch"),("Melissa Leo","Holly Jones"),("Paul Dano","Alex Jones")],
 companies=["Alcon Entertainment","8:38 Productions","Madhouse Entertainment","Oddlot Entertainment"],
 synopsis="When two young girls vanish in a Pennsylvania suburb on Thanksgiving, one father, Keller Dover, takes matters into his own hands while Detective Loki pursues the official investigation.",
 awards=["86th Academy Awards (2014): nominated for Best Cinematography (Roger Deakins).","The film won no Academy Awards."],
 facts=["It was Denis Villeneuve's first English-language feature film.","The story is set in Pennsylvania but was filmed in Georgia.","It premiered at the Telluride Film Festival on 30 August 2013.","It was the first collaboration between Villeneuve and cinematographer Roger Deakins, who later shot Blade Runner 2049."],
 related=[("se7en","A grim detective thriller"),("gone-girl","A disappearance-driven mystery"),("blade-runner-2049","Another Villeneuve film shot by Roger Deakins")],
 wiki="Prisoners_(2013_film)")

movie(slug="arrival", title="Arrival", year=2016, date="11 November 2016 (United States)", lang="English (with some Mandarin and Russian)",
 countries="United States", runtime=116, genres=["Sci-Fi","Drama","Mystery"], director="denis-villeneuve",
 writers="Eric Heisserer, based on the 1998 novella \"Story of Your Life\" by Ted Chiang",
 cast=[("Amy Adams","Dr. Louise Banks"),("Jeremy Renner","Ian Donnelly"),("Forest Whitaker","Colonel Weber"),("Michael Stuhlbarg","Agent Halpern"),("Tzi Ma","General Shang")],
 companies=["Paramount Pictures","FilmNation Entertainment","Lava Bear Films","21 Laps Entertainment"],
 synopsis="When twelve mysterious spacecraft appear around the world, the linguist Louise Banks is recruited by the U.S. military to find a way to communicate with the visitors and learn their purpose.",
 awards=["89th Academy Awards (2017): won Best Sound Editing (Sylvain Bellemare).","Eight nominations in total: also nominated for Best Picture, Best Director, Best Adapted Screenplay, Best Cinematography, Best Film Editing, Best Production Design and Best Sound Mixing."],
 facts=["It premiered at the Venice Film Festival on 1 September 2016.","The film was shot primarily in Quebec, Canada.","The score is by Jóhann Jóhannsson and also uses Max Richter's \"On the Nature of Daylight\".","It adapts a novella by Ted Chiang rather than a full-length novel."],
 related=[("blade-runner-2049","Villeneuve's next science-fiction film"),("dune","Villeneuve's later adaptation of a science-fiction novel"),("interstellar","A thoughtful, emotional science-fiction drama")],
 wiki="Arrival_(film)")

movie(slug="dune", title="Dune", year=2021, date="22 October 2021 (United States)", lang="English",
 countries="United States", runtime=155, genres=["Sci-Fi","Adventure","Drama"], director="denis-villeneuve",
 writers="Jon Spaihts, Denis Villeneuve and Eric Roth, based on the 1965 novel by Frank Herbert",
 cast=[("Timothée Chalamet","Paul Atreides"),("Rebecca Ferguson","Lady Jessica"),("Oscar Isaac","Duke Leto Atreides"),("Josh Brolin","Gurney Halleck"),("Stellan Skarsgård","Baron Vladimir Harkonnen"),("Dave Bautista","Glossu Rabban"),("Zendaya","Chani"),("Javier Bardem","Stilgar"),("Jason Momoa","Duncan Idaho"),("Charlotte Rampling","Reverend Mother Gaius Helen Mohiam")],
 companies=["Legendary Pictures","Warner Bros. Pictures","Villeneuve Films"],
 synopsis="Paul Atreides, a gifted young heir, travels with his family to the desert planet Arrakis, the only source of the universe's most valuable substance, the spice, where rival powers contend for control.",
 awards=["94th Academy Awards (2022): won six awards: Best Cinematography (Greig Fraser), Best Film Editing (Joe Walker), Best Production Design, Best Sound, Best Visual Effects and Best Original Score (Hans Zimmer).","Ten nominations in total, including Best Picture and Best Adapted Screenplay."],
 facts=["The film adapts roughly the first half of Frank Herbert's novel; a sequel, Dune: Part Two, followed in 2024.","The novel had previously been adapted for film by David Lynch in 1984.","In the United States it was released in cinemas and on HBO Max on the same day.","Filming took place in Budapest, Jordan, Abu Dhabi and Norway."],
 related=[("arrival","Villeneuve's earlier science-fiction drama"),("blade-runner-2049","Villeneuve's large-scale science-fiction film"),("interstellar","Another epic of survival and exploration")],
 wiki="Dune_(2021_film)")

movie(slug="blade-runner-2049", title="Blade Runner 2049", year=2017, date="6 October 2017 (United States)", lang="English",
 countries="United States, United Kingdom, Canada", runtime=164, genres=["Sci-Fi","Drama","Mystery"], director="denis-villeneuve",
 writers="Hampton Fancher and Michael Green, based on characters from the 1982 film Blade Runner, which was based on Philip K. Dick's novel Do Androids Dream of Electric Sheep?",
 cast=[("Ryan Gosling","K"),("Harrison Ford","Rick Deckard"),("Ana de Armas","Joi"),("Sylvia Hoeks","Luv"),("Robin Wright","Lieutenant Joshi"),("Mackenzie Davis","Mariette"),("Dave Bautista","Sapper Morton"),("Jared Leto","Niander Wallace")],
 companies=["Alcon Entertainment","Columbia Pictures","Scott Free Productions","16:14 Entertainment","Torridon Films"],
 synopsis="Thirty years after the events of the original Blade Runner, K, a new blade runner for the Los Angeles Police Department, unearths a long-buried secret that leads him to seek the former blade runner Rick Deckard.",
 awards=["90th Academy Awards (2018): won Best Cinematography (Roger Deakins) and Best Visual Effects.","Five nominations in total: also nominated for Best Production Design, Best Sound Editing and Best Sound Mixing."],
 facts=["It is a sequel to Ridley Scott's Blade Runner (1982); Scott served as an executive producer.","Harrison Ford returns as Rick Deckard.","The film was shot largely at studios in Budapest, Hungary.","Roger Deakins won his first Academy Award for this film after previous nominations.","The score is by Hans Zimmer and Benjamin Wallfisch."],
 related=[("arrival","Villeneuve's preceding science-fiction film"),("dune","Villeneuve's following science-fiction film"),("prisoners","Another Villeneuve film shot by Roger Deakins")],
 wiki="Blade_Runner_2049")

movie(slug="pulp-fiction", title="Pulp Fiction", year=1994, date="14 October 1994 (United States)", lang="English",
 countries="United States", runtime=154, genres=["Crime","Drama"], director="quentin-tarantino",
 writers="Quentin Tarantino (screenplay); Quentin Tarantino and Roger Avary (stories)",
 cast=[("John Travolta","Vincent Vega"),("Samuel L. Jackson","Jules Winnfield"),("Uma Thurman","Mia Wallace"),("Bruce Willis","Butch Coolidge"),("Ving Rhames","Marsellus Wallace"),("Harvey Keitel","Winston Wolfe"),("Tim Roth","Pumpkin / Ringo"),("Amanda Plummer","Honey Bunny / Yolanda"),("Christopher Walken","Captain Koons")],
 companies=["Miramax","A Band Apart","Jersey Films"],
 synopsis="The lives of two hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine across several stories in Los Angeles.",
 awards=["1994 Cannes Film Festival: won the Palme d'Or.","67th Academy Awards (1995): won Best Original Screenplay (Quentin Tarantino and Roger Avary).","Seven nominations in total: also nominated for Best Picture, Best Director, Best Actor (John Travolta), Best Supporting Actor (Samuel L. Jackson), Best Supporting Actress (Uma Thurman) and Best Film Editing."],
 facts=["The film is built from interlocking stories told out of chronological order.","It was Quentin Tarantino's second feature film, after Reservoir Dogs (1992).","The soundtrack of surf rock, soul and pop songs opens with Dick Dale's \"Misirlou\".","The film is widely credited with reviving John Travolta's career."],
 related=[("inglourious-basterds","Another Tarantino film"),("se7en","Another 1990s crime classic"),("fight-club","A cult favourite of the late 1990s")],
 wiki="Pulp_Fiction")

movie(slug="inglourious-basterds", title="Inglourious Basterds", year=2009, date="21 August 2009 (United States)", lang="English (with German, French and Italian)",
 countries="United States, Germany", runtime=153, genres=["War","Drama","Adventure"], director="quentin-tarantino",
 writers="Quentin Tarantino",
 cast=[("Brad Pitt","Lt. Aldo Raine"),("Christoph Waltz","Col. Hans Landa"),("Mélanie Laurent","Shosanna Dreyfus"),("Michael Fassbender","Lt. Archie Hicox"),("Eli Roth","Donny Donowitz"),("Diane Kruger","Bridget von Hammersmark"),("Daniel Brühl","Fredrick Zoller")],
 companies=["The Weinstein Company","Universal Pictures","A Band Apart","Studio Babelsberg"],
 synopsis="In Nazi-occupied France during the Second World War, a group of Jewish-American soldiers led by Lt. Aldo Raine plans to assassinate Nazi leaders, while the cinema owner Shosanna Dreyfus nurses a plan of her own.",
 awards=["82nd Academy Awards (2010): Christoph Waltz won Best Supporting Actor.","Eight nominations in total: also nominated for Best Picture, Best Director, Best Original Screenplay, Best Cinematography, Best Film Editing, Best Sound Editing and Best Sound Mixing.","2009 Cannes Film Festival: Christoph Waltz won the Best Actor Award."],
 facts=["The film premiered in competition at the Cannes Film Festival on 20 May 2009.","The title's spelling is deliberate and nods to Enzo G. Castellari's 1978 film The Inglorious Bastards.","Dialogue is spoken in several languages, with subtitles.","Filming took place in Germany, including Studio Babelsberg, and in France."],
 related=[("pulp-fiction","Tarantino's earlier crime classic"),("fight-club","Another film starring Brad Pitt"),("there-will-be-blood","Another award-winning period drama of the 2000s")],
 wiki="Inglourious_Basterds")

movie(slug="there-will-be-blood", title="There Will Be Blood", year=2007, date="26 December 2007 (United States, limited release)", lang="English",
 countries="United States", runtime=158, genres=["Drama","History"], director="paul-thomas-anderson",
 writers="Paul Thomas Anderson, loosely based on the 1927 novel Oil! by Upton Sinclair",
 cast=[("Daniel Day-Lewis","Daniel Plainview"),("Paul Dano","Eli Sunday / Paul Sunday"),("Kevin J. O'Connor","Henry Brands"),("Ciarán Hinds","Fletcher Hamilton"),("Dillon Freasier","H.W. Plainview")],
 companies=["Paramount Vantage","Miramax","Ghoulardi Film Company"],
 synopsis="In the early twentieth-century American Southwest, the ambitious prospector Daniel Plainview builds an oil empire with his young son H.W. at his side, as his clash with a charismatic young preacher intensifies.",
 awards=["80th Academy Awards (2008): won Best Actor (Daniel Day-Lewis) and Best Cinematography (Robert Elswit).","Eight nominations in total: also nominated for Best Picture, Best Director, Best Adapted Screenplay, Best Art Direction, Best Film Editing and Best Sound Editing."],
 facts=["The film is loosely adapted from the first part of Upton Sinclair's novel Oil!.","Jonny Greenwood of Radiohead composed the score, his first for Paul Thomas Anderson; it was ruled ineligible for an Oscar nomination because it used previously released music.","Much of the film was shot around Marfa, Texas.","It was Daniel Day-Lewis's second Academy Award for Best Actor."],
 related=[("oppenheimer","Another portrait of a driven American figure"),("shawshank-redemption","Another widely acclaimed American drama"),("inglourious-basterds","Another Best Picture nominee of the late 2000s")],
 wiki="There_Will_Be_Blood")

movie(slug="shawshank-redemption", title="The Shawshank Redemption", year=1994, date="23 September 1994 (United States)", lang="English",
 countries="United States", runtime=142, genres=["Drama","Crime"], director="frank-darabont",
 writers="Frank Darabont, based on the 1982 novella \"Rita Hayworth and Shawshank Redemption\" by Stephen King",
 cast=[("Tim Robbins","Andy Dufresne"),("Morgan Freeman","Ellis Boyd \"Red\" Redding"),("Bob Gunton","Warden Norton"),("William Sadler","Heywood"),("Clancy Brown","Captain Hadley"),("Gil Bellows","Tommy Williams"),("James Whitmore","Brooks Hatlen")],
 companies=["Castle Rock Entertainment"],
 synopsis="The banker Andy Dufresne is sentenced to life in Shawshank State Penitentiary for the murder of his wife and her lover, and over decades of imprisonment forms an enduring friendship with fellow inmate Ellis \"Red\" Redding.",
 awards=["67th Academy Awards (1995): nominated for seven awards, including Best Picture, Best Actor (Morgan Freeman), Best Adapted Screenplay, Best Cinematography, Best Film Editing, Best Original Score and Best Sound.","The film won no Academy Awards.","Selected for preservation in the U.S. National Film Registry in 2015."],
 facts=["It is adapted from a novella in Stephen King's 1982 collection Different Seasons.","It was filmed largely at the Ohio State Reformatory in Mansfield, Ohio.","Its original theatrical run was modest; it found a large audience on home video and television.","Roger Deakins was the cinematographer and Thomas Newman composed the score."],
 related=[("se7en","Another 1990s film starring Morgan Freeman"),("there-will-be-blood","Another acclaimed American drama"),("pulp-fiction","Another landmark film of 1994")],
 wiki="The_Shawshank_Redemption")

MV = {m["slug"]: m for m in M}
ACT_SLUG = {n: slugify(n) for n in ACTORS}
ALL_GENRES = {
 "Action":"Films built around physical spectacle, pursuit and conflict.",
 "Adventure":"Journeys and quests, often across unfamiliar worlds.",
 "Biography":"Films that dramatize the life of a real person.",
 "Crime":"Stories centred on criminals, investigators and the justice system.",
 "Drama":"Character-driven stories with emotional and thematic weight.",
 "History":"Stories set in a historical period or built around real events.",
 "Mystery":"Stories driven by an unanswered question or an investigation.",
 "Sci-Fi":"Speculative fiction about science, technology and the future.",
 "Thriller":"Suspense-driven stories of danger, tension and uncertainty.",
 "War":"Stories set during wartime.",
}

# ---------------------------------------------------------------- HTML helpers
def ml(slug, p): return f'<a href="{p}movies/{slug}.html">{E(MV[slug]["title"])}</a>'
def dl(slug, p): return f'<a href="{p}directors/{slug}.html">{E(DIRECTORS[slug]["name"])}</a>'
def gl(g, p): return f'<a href="{p}genres.html#genre-{slugify(g)}">{E(g)}</a>'
def al(n, p): return f'<a href="{p}actors.html#{ACT_SLUG[n]}">{E(n)}</a>' if n in ACTORS else E(n)
def mline(slug, p, extra=True):
    m = MV[slug]; s = f'{ml(slug,p)} ({m["year"]})'
    if extra: s += f' &ndash; directed by {dl(m["director"],p)}'
    return s

def page(title, body, p="", desc=""):
    nav = " | ".join(f'<a href="{p}{h}">{t}</a>' for h, t in
        [("index.html","Home"),("movies.html","Movies"),("directors.html","Directors"),("actors.html","Actors"),("genres.html","Genres"),("collections.html","Collections"),("about.html","About")])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{E(desc or title)}">
<title>{E(title)} | The Cinema Archive</title>
</head>
<body>
<a href="#main">Skip to main content</a>
<header>
<p><strong>THE CINEMA ARCHIVE</strong> &mdash; a movie encyclopedia in pure HTML</p>
<nav aria-label="Main navigation">
<p>{nav}</p>
</nav>
<hr>
</header>
<main id="main">
{body}
</main>
<footer>
<hr>
<nav aria-label="Footer navigation"><p>{nav}</p></nav>
<p>The Cinema Archive is a static site written in plain HTML5 with no CSS and no JavaScript. Facts were compiled by hand and should be verified against primary sources before citing; see <a href="{p}about.html">About</a> and <code>SOURCES.md</code>.</p>
</footer>
</body>
</html>
'''

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f: f.write(content)

def poster_note(p):
    return ('<aside aria-label="Image status"><p><em>No poster or still is included on this page. Official posters are copyrighted '
            'and could not be downloaded and licence-verified when this archive was built; see '
            f'<a href="{p}about.html#images">About &rarr; Image credits</a>.</em></p></aside>')

# ---------------------------------------------------------------- movie pages
for m in M:
    p = "../"; d = DIRECTORS[m["director"]]
    cast_rows = "\n".join(f'<tr><td>{al(n,p)}</td><td>{E(r)}</td></tr>' for n, r in m["cast"])
    rows = [("Official title", E(m["title"])), ("Release date", E(m["date"])), ("Release year", str(m["year"])),
            ("Original language", E(m["lang"])), ("Country of production", E(m["countries"])), ("Runtime", f'{m["runtime"]} minutes'),
            ("Genre", ", ".join(gl(g,p) for g in m["genres"])), ("Director", dl(m["director"],p)), ("Screenwriter", E(m["writers"])),
            ("Production companies", E(", ".join(m["companies"])))]
    glance = "\n".join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in rows)
    body = f'''<nav aria-label="Breadcrumb"><p><a href="{p}index.html">Home</a> &rsaquo; <a href="{p}movies.html">Movies</a> &rsaquo; {E(m["title"])}</p></nav>
<article>
<h1>{E(m["title"])} ({m["year"]})</h1>
<p>Directed by {dl(m["director"],p)} &middot; {m["runtime"]} min &middot; {E(", ".join(m["genres"]))}</p>
{poster_note(p)}
<nav aria-label="On this page">
<h2>Contents</h2>
<ol>
<li><a href="#glance">At a glance</a></li>
<li><a href="#synopsis">Plot synopsis</a></li>
<li><a href="#cast">Main cast</a></li>
<li><a href="#awards">Awards and nominations</a></li>
<li><a href="#facts">Production facts</a></li>
<li><a href="#related">Related movies</a></li>
<li><a href="#sources">Sources</a></li>
</ol>
</nav>
<section id="glance">
<h2>At a glance</h2>
<table>
<caption>Key facts about {E(m["title"])}</caption>
<tbody>
{glance}
</tbody>
</table>
</section>
<section id="synopsis">
<h2>Plot synopsis</h2>
<p>{E(m["synopsis"])}</p>
<p><small>Spoiler-free: this summary covers only the film's premise.</small></p>
</section>
<section id="cast">
<h2>Main cast</h2>
<table>
<caption>Principal cast of {E(m["title"])}</caption>
<thead><tr><th scope="col">Actor</th><th scope="col">Role</th></tr></thead>
<tbody>
{cast_rows}
</tbody>
</table>
<p><small>Actors with a biography in this archive are linked.</small></p>
</section>
<section id="production">
<h2>Production companies</h2>
<ul>
{"".join(f"<li>{E(c)}</li>" for c in m["companies"])}
</ul>
</section>
<section id="awards">
<h2>Awards and nominations</h2>
<ul>
{"".join(f"<li>{E(a)}</li>" for a in m["awards"])}
</ul>
</section>
<section id="facts">
<h2>Production facts</h2>
<ol>
{"".join(f"<li>{E(f)}</li>" for f in m["facts"])}
</ol>
</section>
<section id="related">
<h2>Related movies</h2>
<ul>
{"".join(f"<li>{ml(s,p)} ({MV[s]['year']}) &ndash; {E(why)}</li>" for s, why in m["related"])}
</ul>
</section>
<section id="sources">
<h2>Sources</h2>
<details>
<summary>Where to verify this entry</summary>
<ul>
<li>Wikipedia article: en.wikipedia.org/wiki/{E(m["wiki"])}</li>
<li>Wikidata entry for the film (search the title at wikidata.org)</li>
<li>Academy Awards Database: awardsdatabase.oscars.org</li>
<li>Official studio and production-company pages for the film</li>
</ul>
<p>Facts on this page were compiled from the editor's general knowledge of the public record. They were not cross-checked live while the archive was built (the build environment had no access to Wikidata or Wikipedia). Please verify before citing. Full notes: <code>SOURCES.md</code>.</p>
</details>
</section>
</article>'''
    write(f"movies/{m['slug']}.html", page(m["title"], body, p, f'{m["title"]} ({m["year"]}), directed by {d["name"]}: cast, synopsis, awards and production facts.'))

# ---------------------------------------------------------------- directors
for slug, d in DIRECTORS.items():
    p = "../"
    films = "\n".join(
        f'<tr><td>{ml(s,p) if s else E(t)}</td><td>{y}</td><td>{"In this archive" if s else "&mdash;"}</td></tr>' for t, y, s in d["films"])
    body = f'''<nav aria-label="Breadcrumb"><p><a href="{p}index.html">Home</a> &rsaquo; <a href="{p}directors.html">Directors</a> &rsaquo; {E(d["name"])}</p></nav>
<article>
<h1>{E(d["name"])}</h1>
<aside aria-label="Image status"><p><em>No portrait is included; see <a href="{p}about.html#images">Image credits</a>.</em></p></aside>
<table>
<caption>Biographical details</caption>
<tbody>
<tr><th scope="row">Born</th><td>{E(d["born"])}</td></tr>
<tr><th scope="row">Nationality</th><td>{E(d["nat"])}</td></tr>
<tr><th scope="row">Films in this archive</th><td>{", ".join(ml(s,p) for t,y,s in d["films"] if s)}</td></tr>
</tbody>
</table>
<h2>Biography</h2>
{"".join(f"<p>{E(b)}</p>" for b in d["bio"])}
<h2>Selected filmography</h2>
<table>
<caption>Feature films directed by {E(d["name"])} (selected; films with their own page are linked)</caption>
<thead><tr><th scope="col">Film</th><th scope="col">Year</th><th scope="col">Archive</th></tr></thead>
<tbody>
{films}
</tbody>
</table>
<p><a href="{p}directors.html">&larr; Back to all directors</a></p>
</article>'''
    write(f"directors/{slug}.html", page(d["name"], body, p, f'{d["name"]}: biography and filmography.'))

body = '<h1>Directors</h1>\n<p>Biographies and filmographies for the filmmakers behind the movies in the archive. Each name links to a full profile.</p>\n<nav aria-label="Directors index"><ul>' + "".join(f'<li><a href="#{s}">{E(d["name"])}</a></li>' for s, d in DIRECTORS.items()) + '</ul></nav>\n'
for s, d in DIRECTORS.items():
    inarch = [f for f in d["films"] if f[2]]
    body += f'''<section id="{s}">
<h2>{E(d["name"])}</h2>
<table>
<caption>{E(d["name"])} at a glance</caption>
<tbody>
<tr><th scope="row">Nationality</th><td>{E(d["nat"])}</td></tr>
<tr><th scope="row">Born</th><td>{E(d["born"])}</td></tr>
<tr><th scope="row">Films in this archive</th><td>{", ".join(f'<a href="movies/{x[2]}.html">{E(x[0])}</a> ({x[1]})' for x in inarch)}</td></tr>
</tbody>
</table>
<p>{E(d["bio"][0])}</p>
<p><a href="directors/{s}.html">Read the full profile and filmography of {E(d["name"])}</a></p>
</section>
'''
write("directors.html", page("Directors", body, "", "Director encyclopedia with biographies, nationalities and filmographies."))

# ---------------------------------------------------------------- actors
by_actor = {n: [] for n in ACTORS}
for m in M:
    for n, r in m["cast"]:
        if n in by_actor: by_actor[n].append((m["slug"], r))
body = '<h1>Actors</h1>\n<p>Biographies and filmographies for performers who appear in the archive. Filmographies list only films that have their own page here.</p>\n<nav aria-label="Actors index"><ul>' + "".join(f'<li><a href="#{ACT_SLUG[n]}">{E(n)}</a></li>' for n in sorted(ACTORS)) + '</ul></nav>\n'
for n in sorted(ACTORS):
    born, nat, bio = ACTORS[n]
    rows = "\n".join(f'<tr><td>{ml(s,"")}</td><td>{MV[s]["year"]}</td><td>{E(r)}</td></tr>' for s, r in sorted(by_actor[n], key=lambda x: MV[x[0]]["year"]))
    body += f'''<section id="{ACT_SLUG[n]}">
<h2>{E(n)}</h2>
<p><strong>Born:</strong> {E(born)}<br><strong>Nationality:</strong> {E(nat)}</p>
<p>{E(bio)}</p>
<table>
<caption>Films by {E(n)} in this archive</caption>
<thead><tr><th scope="col">Film</th><th scope="col">Year</th><th scope="col">Role</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</section>
'''
write("actors.html", page("Actors", body, "", "Actor biographies and filmographies."))

# ---------------------------------------------------------------- genres
body = '<h1>Genres</h1>\n<p>Browse the archive by genre. A film can appear under more than one genre. Horror and Romance are planned sections: no film in the current catalogue is classified under them yet.</p>\n<nav aria-label="Genre index"><ul>'
used = [g for g in ALL_GENRES if any(g in m["genres"] for m in M)]
body += "".join(f'<li><a href="#genre-{slugify(g)}">{E(g)}</a></li>' for g in used) + '</ul></nav>\n'
for g in used:
    ms = sorted([m for m in M if g in m["genres"]], key=lambda m: m["year"])
    rows = "\n".join(f'<tr><td>{ml(m["slug"],"")}</td><td>{m["year"]}</td><td>{dl(m["director"],"")}</td></tr>' for m in ms)
    body += f'''<section id="genre-{slugify(g)}">
<h2>{E(g)}</h2>
<p>{E(ALL_GENRES[g])} ({len(ms)} film{"s" if len(ms)!=1 else ""})</p>
<table>
<caption>{E(g)} films in the archive</caption>
<thead><tr><th scope="col">Film</th><th scope="col">Year</th><th scope="col">Director</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</section>
'''
write("genres.html", page("Genres", body, "", "Movies categorized by genre."))

# ---------------------------------------------------------------- collections
def titles(slugs): return [(MV[s]["title"], MV[s]["year"], s) for s in slugs]
COLL = [
 ("dark-knight-trilogy","The Dark Knight Trilogy","Trilogy","Christopher Nolan's three Batman films for Warner Bros. Only the middle film has its own page so far.",
  [("Batman Begins",2005,None),("The Dark Knight",2008,"dark-knight"),("The Dark Knight Rises",2012,None)]),
 ("dune-saga","Dune","Franchise","Denis Villeneuve's two-part adaptation of Frank Herbert's 1965 novel.",
  [("Dune",2021,"dune"),("Dune: Part Two",2024,None)]),
 ("blade-runner","Blade Runner","Franchise","Ridley Scott's 1982 science-fiction noir and its 2017 sequel.",
  [("Blade Runner",1982,None),("Blade Runner 2049",2017,"blade-runner-2049")]),
 ("nolan","The Films of Christopher Nolan","Director collection","Nolan's films in the archive, in release order.",
  titles(["dark-knight","inception","interstellar","oppenheimer"])),
 ("fincher","The Films of David Fincher","Director collection","Fincher's thrillers in the archive, in release order.",
  titles(["se7en","fight-club","gone-girl"])),
 ("villeneuve","The Films of Denis Villeneuve","Director collection","Villeneuve's English-language films in the archive, in release order.",
  titles(["prisoners","arrival","blade-runner-2049","dune"])),
 ("tarantino","The Films of Quentin Tarantino","Director collection","Tarantino's films in the archive.", titles(["pulp-fiction","inglourious-basterds"])),
 ("scifi","Thoughtful Science Fiction","Themed collection","Science-fiction films that pair spectacle with big questions.",
  titles(["inception","interstellar","arrival","blade-runner-2049","dune"])),
 ("adaptations","Adapted from the Page","Themed collection","Films based on novels, novellas, short fiction or biography.",
  titles(["fight-club","gone-girl","arrival","dune","shawshank-redemption","there-will-be-blood","oppenheimer"])),
 ("deakins","Photographed by Roger Deakins","Themed collection","Films in the archive shot by cinematographer Roger Deakins.",
  titles(["shawshank-redemption","prisoners","blade-runner-2049"])),
 ("best-picture","Best Picture Nominees","Themed collection","Films in the archive nominated for the Academy Award for Best Picture; Oppenheimer won.",
  titles(["shawshank-redemption","pulp-fiction","there-will-be-blood","inglourious-basterds","inception","arrival","dune","oppenheimer"])),
]
body = '<h1>Collections</h1>\n<p>Trilogies, franchises and themed lists. Films that have a page in the archive are linked; other titles are shown as plain text. No shared cinematic universe is represented in the catalogue yet.</p>\n<nav aria-label="Collections index"><ul>'
body += "".join(f'<li><a href="#{i}">{E(t)}</a> ({k})</li>' for i, t, k, _, _ in COLL) + '</ul></nav>\n'
for i, t, k, desc, items in sorted(COLL, key=lambda c: 0):
    def item(n, y, s):
        if s: return f'<li><a href="movies/{s}.html">{E(n)}</a> ({y})</li>'
        return f'<li>{E(n)} ({y}) &ndash; not yet in the archive</li>'
    li = "".join(item(*x) for x in items)
    body += f'<section id="{i}">\n<h2>{E(t)}</h2>\n<p><em>{k}.</em> {E(desc)}</p>\n<ol>{li}</ol>\n</section>\n'
write("collections.html", page("Collections", body, "", "Film trilogies, franchises and themed collections."))

# ---------------------------------------------------------------- movies catalogue
rows = "\n".join(f'<tr><td>{ml(m["slug"],"")}</td><td>{m["year"]}</td><td>{dl(m["director"],"")}</td><td>{", ".join(gl(g,"") for g in m["genres"])}</td><td>{m["runtime"]} min</td></tr>' for m in sorted(M, key=lambda m: m["title"].lower().replace("the ", "", 1) if m["title"].startswith("The ") else m["title"].lower()))
checks = "\n".join(f'<p><label><input type="checkbox" name="seen" value="{m["slug"]}"> {E(m["title"])} ({m["year"]})</label></p>' for m in sorted(M, key=lambda m: m["year"]))
body = f'''<h1>Movie catalogue</h1>
<p>All {len(M)} films in the archive, sorted alphabetically (ignoring a leading &ldquo;The&rdquo;). Select a title for its full page. Use your browser's find command (Ctrl+F or Cmd+F) to search this page.</p>
<table>
<caption>Complete movie catalogue</caption>
<thead><tr><th scope="col">Title</th><th scope="col">Year</th><th scope="col">Director</th><th scope="col">Genres</th><th scope="col">Runtime</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
<h2>Personal watch checklist</h2>
<details>
<summary>Open the checklist</summary>
<p>Tick the films you have seen. This is a plain HTML form: nothing is submitted or stored, so ticks last only until you reload the page.</p>
<form>
<fieldset>
<legend>Films I have seen (oldest first)</legend>
{checks}
</fieldset>
<p><input type="reset" value="Clear all ticks"></p>
</form>
</details>'''
write("movies.html", page("Movies", body, "", "Complete catalogue of films in the archive with directors, years and genres."))

# ---------------------------------------------------------------- index
featured = ["oppenheimer","blade-runner-2049","pulp-fiction","shawshank-redemption","inception"]
recent = ["dune","prisoners","arrival","there-will-be-blood","inglourious-basterds"]
body = f'''<h1>The Cinema Archive</h1>
<p>Welcome to a compact digital film library and encyclopedia. The archive documents {len(M)} acclaimed films with full credits, spoiler-free synopses, awards, production facts, and cross-links to the directors, actors, genres and collections around them. The whole site is plain HTML: every page works offline, with no styling or scripts.</p>
<nav aria-label="Sections">
<h2>Explore the archive</h2>
<ul>
<li><a href="movies.html">Movies</a> &ndash; the complete catalogue ({len(M)} films)</li>
<li><a href="directors.html">Directors</a> &ndash; {len(DIRECTORS)} profiles with filmographies</li>
<li><a href="actors.html">Actors</a> &ndash; {len(ACTORS)} biographies and filmographies</li>
<li><a href="genres.html">Genres</a> &ndash; browse by category</li>
<li><a href="collections.html">Collections</a> &ndash; trilogies, franchises and themed lists</li>
<li><a href="about.html">About</a> &ndash; sources, method and image credits</li>
</ul>
</nav>
<section>
<h2>Featured movies</h2>
<ul>
{"".join(f"<li>{mline(s,'')} &ndash; {E(MV[s]['synopsis'].split('. ')[0].rstrip('.'))}.</li>" for s in featured)}
</ul>
</section>
<section>
<h2>Recently added films</h2>
<p>The latest entries added to the archive:</p>
<ol>
{"".join(f"<li>{mline(s,'')}</li>" for s in recent)}
</ol>
</section>
<section>
<h2>Popular directors</h2>
<ul>
{"".join(f'<li>{dl(s,"")} ({E(d["nat"])}) &ndash; {len([f for f in d["films"] if f[2]])} film(s) in the archive</li>' for s, d in DIRECTORS.items())}
</ul>
</section>
<section>
<h2>Browse by decade</h2>
<ul>
<li>1990s: {", ".join(ml(m["slug"],"") for m in M if 1990<=m["year"]<2000)}</li>
<li>2000s: {", ".join(ml(m["slug"],"") for m in M if 2000<=m["year"]<2010)}</li>
<li>2010s: {", ".join(ml(m["slug"],"") for m in M if 2010<=m["year"]<2020)}</li>
<li>2020s: {", ".join(ml(m["slug"],"") for m in M if 2020<=m["year"]<2030)}</li>
</ul>
</section>'''
write("index.html", page("Home", body, "", "The Cinema Archive: a pure-HTML movie encyclopedia."))

# ---------------------------------------------------------------- about
body = f'''<h1>About The Cinema Archive</h1>
<nav aria-label="On this page"><ul><li><a href="#project">Project</a></li><li><a href="#data">Data sources and verification status</a></li><li><a href="#images">Image credits</a></li><li><a href="#media">Audio and video</a></li><li><a href="#technical">Technical constraints</a></li></ul></nav>
<section id="project">
<h2>Project</h2>
<p>The Cinema Archive is a multi-page movie encyclopedia inspired by IMDb, Letterboxd and The Movie Database. It is deliberately built with HTML only: no CSS, no JavaScript, no frameworks, no backend. Structure comes from semantic elements: headings, tables, lists, forms and expandable <code>details</code> sections.</p>
<p>It currently contains {len(M)} films, {len(DIRECTORS)} directors and {len(ACTORS)} actors.</p>
</section>
<section id="data">
<h2>Data sources and verification status</h2>
<p>Intended reference sources are Wikidata, Wikipedia, Wikimedia Commons, official studio and film websites, the Academy Awards Database and IMDb (for cross-checking only; no IMDb content or images were copied).</p>
<p><strong>Important limitation:</strong> the environment in which this archive was generated could not reach Wikidata, Wikipedia or Wikimedia Commons. The facts here (dates, runtimes, credits, awards, production facts) were therefore written from the editor's general knowledge of the public record and were not cross-checked live. Runtimes, release dates for specific territories, and production-company lists are the details most worth re-verifying. Synopses are original wording written for this archive.</p>
<p>Each movie page lists where to verify its entry, and <code>SOURCES.md</code> collects the same information.</p>
</section>
<section id="images">
<h2>Image credits</h2>
<p>No images are included. This is intentional:</p>
<ul>
<li>The build environment could not download from Wikimedia Commons, so no licence could be verified.</li>
<li>Official film posters are copyrighted and are generally not freely licensed on Wikimedia Commons, so they would not have been eligible even with access.</li>
<li>IMDb images were not used, in line with IMDb's terms.</li>
</ul>
<p>The folders <code>images/posters</code>, <code>images/directors</code>, <code>images/actors</code> and <code>images/gallery</code> are reserved for future, licence-verified files. Any added image must be recorded in <code>SOURCES.md</code> with its URL, creator and licence.</p>
</section>
<section id="media">
<h2>Audio and video</h2>
<p>No audio or video is embedded: official trailers and clips are not available under licences that allow redistribution inside a downloadable offline project.</p>
</section>
<section id="technical">
<h2>Technical constraints</h2>
<ul>
<li>Pure HTML5; no <code>style</code> attributes or elements, no stylesheets, no scripts, no event-handler attributes.</li>
<li>All navigation uses ordinary hyperlinks with relative paths, so the site works from a local folder with no internet connection.</li>
<li>Appearance is controlled entirely by the browser.</li>
</ul>
</section>'''
write("about.html", page("About", body, "", "About the project, data sources and image credits."))

print("pages written:", len(M) + len(DIRECTORS) + 7)
