import os

import pytz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ITech_group_project.settings')

import django

django.setup()

from moovie.models import *
from django.core.files.images import ImageFile
from decimal import *
import datetime


def populate():
    # Movie
    movies = [
        {'title': 'Harry Potter and the Philosophers Stone',
         'duration': 152,
         'release_date': datetime.datetime(2001, 11, 16, tzinfo=pytz.UTC),
         'description': 'An orphaned boy enrolls in a school of wizardry, where he learns the truth about himself, '
                        'his family and the terrible evil that haunts the magical world.',
         'average_rating': Decimal(4.71),
         'image': 'movie_images/HarryPotter1.jpg',
         'poster': 'poster_images/HarryPotter1.jpg'},

        {'title': 'Harry Potter and the Chamber of Secrets',
         'duration': 161,
         'release_date': datetime.datetime(2002, 11, 15, tzinfo=pytz.UTC),
         'description': 'An ancient prophecy seems to be coming true when a mysterious presence begins stalking the '
                        'corridors of a school of magic and leaving its victims paralyzed.',
         'average_rating': Decimal(4.00),
         'image': 'movie_images/HarryPotter2.jpg',
         'poster': 'poster_images/HarryPotter2.jpg'},

        {'title': 'Harry Potter and the Prisoner of Azkaban',
         'duration': 142,
         'release_date': datetime.datetime(2004, 6, 4, tzinfo=pytz.UTC),
         'description': 'Harry Potter, Ron and Hermione return to Hogwarts School of Witchcraft and Wizardry for '
                        'their third year of study, where they delve into the mystery surrounding an escaped prisoner '
                        'who poses a dangerous threat to the young wizard.',
         'average_rating': Decimal(4.56),
         'image': 'movie_images/HarryPotter3.jpg',
         'poster': 'poster_images/HarryPotter3.jpg'},

        {'title': 'Harry Potter and the Goblet of Fire',
         'duration': 157,
         'release_date': datetime.datetime(2005, 11, 6, tzinfo=pytz.UTC),
         'description': 'Harry Potter finds himself competing in a hazardous tournament between rival schools of '
                        'magic, but he is distracted by recurring nightmares.',
         'average_rating': Decimal(3.85),
         'image': 'movie_images/HarryPotter4.jpg',
         'poster': 'poster_images/HarryPotter4.jpg'},

        {'title': 'Harry Potter and the Order of the Phoenix',
         'duration': 138,
         'release_date': datetime.datetime(2007, 7, 3, tzinfo=pytz.UTC),
         'description': "/With their warning about Lord Voldemort's return scoffed at, Harry and Dumbledore are "
                        "targeted by the Wizard authorities as an authoritarian bureaucrat slowly seizes power at "
                        "Hogwarts.",
         'average_rating': Decimal(3.75),
         'image': 'movie_images/HarryPotter5.jpg',
         'poster': 'poster_images/HarryPotter5.jpg'},

        {'title': 'Harry Potter and the Half-Blood Prince',
         'duration': 153,
         'release_date': datetime.datetime(2009, 7, 7, tzinfo=pytz.UTC),
         'description': 'As Harry Potter begins his sixth year at Hogwarts, he discovers an old book marked as "the '
                        'property of the Half-Blood Prince" and begins to learn more about Lord Voldemort\'s dark '
                        'past.',
         'average_rating': Decimal(3.75),
         'image': 'movie_images/HarryPotter6.jpg',
         'poster': 'poster_images/HarryPotter6.jpg'},

        {'title': 'Harry Potter and the Deathly Hallows: Part 1',
         'duration': 146,
         'release_date': datetime.datetime(2010, 11, 11, tzinfo=pytz.UTC),
         'description': 'As Harry, Ron, and Hermione race against time and evil to destroy the Horcruxes, '
                        'they uncover the existence of the three most powerful objects in the wizarding world: the '
                        'Deathly Hallows.',
         'average_rating': Decimal(3.75),
         'image': 'movie_images/HarryPotter7_1.jpg',
         'poster': 'poster_images/HarryPotter7_1.jpg'},

        {'title': 'Harry Potter and the Deathly Hallows: Part 2',
         'duration': 130,
         'release_date': datetime.datetime(2011, 7, 7, tzinfo=pytz.UTC),
         'description': "Harry, Ron, and Hermione search for Voldemort's remaining Horcruxes in their effort to "
                        "destroy the Dark Lord as the final battle rages on at Hogwarts.",
         'average_rating': Decimal(4.10),
         'image': 'movie_images/HarryPotter7_2.jpg',
         'poster': 'poster_images/HarryPotter7_2.jpg'},

        {'title': '007 SkyFall',
         'duration': 143,
         'release_date': datetime.datetime(2012, 10, 23, tzinfo=pytz.UTC),
         'description': "James Bond's loyalty to M is tested when her past comes back to haunt her. When MI6 comes "
                        "under attack, 007 must track down and destroy the threat, no matter how personal the cost.",
         'average_rating': Decimal(3.95),
         'image': 'movie_images/007_SkyFall.jpg',
         'poster': 'poster_images/007_SkyFall.jpg'},

        {'title': 'I, Robot',
         'duration': 115,
         'release_date': datetime.datetime(2004, 7, 16, tzinfo=pytz.UTC),
         'description': 'Description',
         'average_rating': Decimal(3.55),
         'image': 'movie_images/i_robot.jpg',
         'poster': 'poster_images/i_robot.jpg'},

        {'title': 'The Matrix Resurrections',
         'duration': 148,
         'release_date': datetime.datetime(2021, 12, 16, tzinfo=pytz.UTC),
         'description': "Return to a world of two realities: one, everyday life; the other, what lies behind it. To "
                        "find out if his reality is a construct, to truly know himself, Mr. Anderson will have to "
                        "choose to follow the white rabbit once more.",
         'average_rating': Decimal(3.45),
         'image': 'movie_images/matrix_resurrections.jpg',
         'poster': 'poster_images/matrix_resurrections.jpg'},

        {'title': "Zack Snyder's Justice League",
         'duration': 242,
         'release_date': datetime.datetime(2021, 3, 18, tzinfo=pytz.UTC),
         'description': "Determined to ensure Superman's ultimate sacrifice was not in vain, Bruce Wayne aligns "
                        "forces with Diana Prince with plans to recruit a team of metahumans to protect the world "
                        "from an approaching threat of catastrophic proportions.",
         'average_rating': Decimal(4.05),
         'image': 'movie_images/justice_league.jpg',
         'poster': 'poster_images/justice_league.png'},

        {'title': "The Avengers",
         'duration': 143,
         'release_date': datetime.datetime(2012, 4, 11, tzinfo=pytz.UTC),
         'description': "Earth's mightiest heroes must come together and learn to fight as a team if they are going "
                        "to stop the mischievous Loki and his alien army from enslaving humanity.",
         'average_rating': Decimal(4.05),
         'image': 'movie_images/TheAvengers1.jpg',
         'poster': 'poster_images/TheAvengers1.jpg'},

        {'title': "Avengers: Age of Ultron",
         'duration': 141,
         'release_date': datetime.datetime(2015, 4, 13, tzinfo=pytz.UTC),
         'description': "When Tony Stark and Bruce Banner try to jump-start a dormant peacekeeping program called "
                        "Ultron, things go horribly wrong and it's up to Earth's mightiest heroes to stop the "
                        "villainous Ultron from enacting his terrible plan.",
         'average_rating': Decimal(3.65),
         'image': 'movie_images/TheAvengers2.jpg',
         'poster': 'poster_images/TheAvengers2.jpg'},

        {'title': "Avengers: Infinity War",
         'duration': 149,
         'release_date': datetime.datetime(2018, 4, 23, tzinfo=pytz.UTC),
         'description': "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the "
                        "powerful Thanos before his blitz of devastation and ruin puts an end to the universe.",
         'average_rating': Decimal(4.25),
         'image': 'movie_images/TheAvengers3.jpg',
         'poster': 'poster_images/TheAvengers3.jpg'},

        {'title': "Avengers: Endgame",
         'duration': 181,
         'release_date': datetime.datetime(2019, 4, 23, tzinfo=pytz.UTC),
         'description': "After the devastating events of Avengers: Infinity War (2018), the universe is in ruins. "
                        "With the help of remaining allies, the Avengers assemble once more in order to reverse "
                        "Thanos' actions and restore balance to the universe.",
         'average_rating': Decimal(4.20),
         'image': 'movie_images/TheAvengers4.jpg',
         'poster': 'poster_images/TheAvengers4.jpg'},

        {'title': "The Shawshank Redemption",
         'duration': 142,
         'release_date': datetime.datetime(1994, 9, 10, tzinfo=pytz.UTC),
         'description': "Two imprisoned men bond over a number of years, finding solace and eventual redemption "
                        "through acts of common decency.",
         'average_rating': Decimal(4.65),
         'image': 'movie_images/The_Shawshank_Redemption.jpg',
         'poster': 'poster_images/The_Shawshank_Redemption.jpg'},

        {'title': "The Godfather",
         'duration': 175,
         'release_date': datetime.datetime(1972, 3, 15, tzinfo=pytz.UTC),
         'description': "The aging patriarch of an organized crime dynasty in postwar New York City transfers control "
                        "of his clandestine empire to his reluctant youngest son.",
         'average_rating': Decimal(4.60),
         'image': 'movie_images/The_Godfather.jpg',
         'poster': 'poster_images/The_Godfather.jpg'},

        {'title': "The Dark Knight",
         'duration': 152,
         'release_date': datetime.datetime(2008, 7, 14, tzinfo=pytz.UTC),
         'description': "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, "
                        "Batman must accept one of the greatest psychological and physical tests of his ability to "
                        "fight injustice.",
         'average_rating': Decimal(4.55),
         'image': 'movie_images/The_Dark_Knight.jpg',
         'poster': 'poster_images/The_Dark_Knight.jpg'},

        {'title': "Interstellar",
         'duration': 169,
         'release_date': datetime.datetime(2014, 10, 26, tzinfo=pytz.UTC),
         'description': "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's "
                        "survival.",
         'average_rating': Decimal(4.35),
         'image': 'movie_images/Interstellar.jpg',
         'poster': 'poster_images/Interstellar.jpg'},

        {'title': "Spider-Man: No Way Home",
         'duration': 148,
         'release_date': datetime.datetime(2021, 12, 13, tzinfo=pytz.UTC),
         'description': "With Spider-Man's identity now revealed, Peter asks Doctor Strange for help. When a spell "
                        "goes wrong, dangerous foes from other worlds start to appear, forcing Peter to discover what "
                        "it truly means to be Spider-Man.",
         'average_rating': Decimal(4.30),
         'image': 'movie_images/No_Way_Home.jpg',
         'poster': 'poster_images/No_Way_Home.jpg'},

        {'title': "Joker",
         'duration': 122,
         'release_date': datetime.datetime(2019, 9, 28, tzinfo=pytz.UTC),
         'description': "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by "
                        "society. He then embarks on a downward spiral of revolution and bloody crime. This path "
                        "brings him face-to-face with his alter-ego: the Joker.",
         'average_rating': Decimal(4.2),
         'image': 'movie_images/Joker.jpg',
         'poster': 'poster_images/Joker.jpg'},

        {'title': "Uncharted",
         'duration': 116,
         'release_date': datetime.datetime(2022, 2, 11, tzinfo=pytz.UTC),
         'description': "Street-smart Nathan Drake is recruited by seasoned treasure hunter Victor 'Sully' Sullivan "
                        "to recover a fortune amassed by Ferdinand Magellan, and lost 500 years ago by the House of "
                        "Moncada.",
         'average_rating': Decimal(4.2),
         'image': 'movie_images/Uncharted.jpg',
         'poster': 'poster_images/Joker.jpg'},
    ]

    # movie casters and directors
    harry1 = [
        {'name': 'Daniel', 'surname': 'Radcliffe',
         'person_type': 'Actor'},
        {'name': 'Emma', 'surname': 'Watson',
         'person_type': 'Actor'},
        {'name': 'Rupert', 'surname': 'Grint',
         'person_type': 'Actor'},
        {'name': 'Chris', 'surname': 'Columbus',
         'person_type': 'Director'},

    ]

    harry2 = [
        {'name': 'Daniel', 'surname': 'Radcliffe',
         'person_type': 'Actor'},
        {'name': 'Emma', 'surname': 'Watson',
         'person_type': 'Actor'},
        {'name': 'Rupert', 'surname': 'Grint',
         'person_type': 'Actor'},
        {'name': 'Chris', 'surname': 'Columbus',
         'person_type': 'Director'},
    ]

    harry3 = [
        {'name': 'Daniel', 'surname': 'Radcliffe',
         'person_type': 'Actor'},
        {'name': 'Emma', 'surname': 'Watson',
         'person_type': 'Actor'},
        {'name': 'Rupert', 'surname': 'Grint',
         'person_type': 'Actor'},
        {'name': 'Gary', 'surname': 'Oldman',
         'person_type': 'Actor'},
        {'name': 'Alfonso', 'surname': 'Cuarón',
         'person_type': 'Director'},
    ]

    harry4 = [
        {'name': 'Daniel', 'surname': 'Radcliffe',
         'person_type': 'Actor'},
        {'name': 'Emma', 'surname': 'Watson',
         'person_type': 'Actor'},
        {'name': 'Rupert', 'surname': 'Grint',
         'person_type': 'Actor'},
        {'name': 'Mike', 'surname': 'Newell',
         'person_type': 'Director'},
    ]

    harry5 = [
        {'name': 'Daniel', 'surname': 'Radcliffe',
         'person_type': 'Actor'},
        {'name': 'Emma', 'surname': 'Watson',
         'person_type': 'Actor'},
        {'name': 'Rupert', 'surname': 'Grint',
         'person_type': 'Actor'},
        {'name': 'David', 'surname': 'Yates',
         'person_type': 'Director'},
    ]

    harry6 = [
        {'name': 'Daniel', 'surname': 'Radcliffe',
         'person_type': 'Actor'},
        {'name': 'Emma', 'surname': 'Watson',
         'person_type': 'Actor'},
        {'name': 'Rupert', 'surname': 'Grint',
         'person_type': 'Actor'},
        {'name': 'Michael', 'surname': 'Gambon',
         'person_type': 'Actor'},
        {'name': 'David', 'surname': 'Yates',
         'person_type': 'Director'},
    ]

    harry7 = [
        {'name': 'Daniel', 'surname': 'Radcliffe',
         'person_type': 'Actor'},
        {'name': 'Emma', 'surname': 'Watson',
         'person_type': 'Actor'},
        {'name': 'Rupert', 'surname': 'Grint',
         'person_type': 'Actor'},
        {'name': 'Ralph', 'surname': 'Fiennes',
         'person_type': 'Actor'},
        {'name': 'David', 'surname': 'Yates',
         'person_type': 'Director'},
    ]

    sky_fall = [
        {'name': 'Daniel', 'surname': 'Craig',
         'person_type': 'Actor'},
        {'name': 'Bérénice', 'surname': 'Marlohe',
         'person_type': 'Actor'},
        {'name': 'Sam', 'surname': 'Mendes',
         'person_type': 'Director'},
    ]


    i_robot = [
        {'name': 'Will', 'surname': 'Smith',
         'person_type': 'Actor'},
        {'name': 'Bridget', 'surname': 'Moynahan',
         'person_type': 'Actor'},
        {'name': 'Bruce', 'surname': 'Greenwood',
         'person_type': 'Actor'},
        {'name': 'Alex', 'surname': 'Proyas',
         'person_type': 'Director'},
    ]

    matrix4 = [
        {'name': 'Keanu', 'surname': 'Reeves',
         'person_type': 'Actor'},
        {'name': 'Carrie-Anne', 'surname': 'Moss',
         'person_type': 'Actor'},
        {'name': 'Lana', 'surname': 'Wachowski',
         'person_type': 'Director'},
    ]

    z_justice = [
        {'name': 'Henry', 'surname': 'Cavill',
         'person_type': 'Actor'},
        {'name': 'Ben', 'surname': 'Affleck',
         'person_type': 'Actor'},
        {'name': 'Gal', 'surname': 'Gadot',
         'person_type': 'Actor'},
        {'name': 'Zack', 'surname': 'Snyder',
         'person_type': 'Director'},
    ]

    avengers1 = [
        {'name': 'Robert', 'surname': 'Downey Jr.',
         'person_type': 'Actor'},
        {'name': 'Chris', 'surname': 'Evans',
         'person_type': 'Actor'},
        {'name': 'Scarlett', 'surname': 'Johansson',
         'person_type': 'Actor'},
        {'name': 'Joss', 'surname': 'Whedon',
         'person_type': 'Director'},
    ]

    avengers2 = [
        {'name': 'Robert', 'surname': 'Downey Jr.',
         'person_type': 'Actor'},
        {'name': 'Chris', 'surname': 'Evans',
         'person_type': 'Actor'},
        {'name': 'Mark', 'surname': 'Ruffalo',
         'person_type': 'Actor'},
        {'name': 'Joss', 'surname': 'Whedon',
         'person_type': 'Director'},
    ]

    avengers3 = [
        {'name': 'Robert', 'surname': 'Downey Jr.',
         'person_type': 'Actor'},
        {'name': 'Chris', 'surname': 'Evans',
         'person_type': 'Actor'},
        {'name': 'Chris', 'surname': 'Hemsworth',
         'person_type': 'Actor'},
        {'name': 'Anthony', 'surname': 'Russo',
         'person_type': 'Director'},
        {'name': 'Joe', 'surname': 'Russo',
         'person_type': 'Director'},
    ]

    avengers4 = [
        {'name': 'Robert', 'surname': 'Downey Jr.',
         'person_type': 'Actor'},
        {'name': 'Chris', 'surname': 'Evans',
         'person_type': 'Actor'},
        {'name': 'Tom', 'surname': 'Holland',
         'person_type': 'Actor'},
        {'name': 'Anthony', 'surname': 'Russo',
         'person_type': 'Director'},
        {'name': 'Joe', 'surname': 'Russo',
         'person_type': 'Director'},
    ]

    shawshank_redemption = [
        {'name': 'Tim', 'surname': 'Robbins',
         'person_type': 'Actor'},
        {'name': 'Morgan', 'surname': 'Freeman',
         'person_type': 'Actor'},
        {'name': 'Bob', 'surname': 'Gunton',
         'person_type': 'Actor'},
        {'name': 'Frank', 'surname': 'Darabont',
         'person_type': 'Director'},
    ]

    god_father = [
        {'name': 'Marlon', 'surname': 'Brando',
         'person_type': 'Actor'},
        {'name': 'Al', 'surname': 'Pacino',
         'person_type': 'Actor'},
        {'name': 'James', 'surname': 'Caan',
         'person_type': 'Actor'},
        {'name': 'Francis Ford', 'surname': 'Coppola',
         'person_type': 'Director'},
    ]

    dark_knight = [
        {'name': 'Christian', 'surname': 'Bale',
         'person_type': 'Actor'},
        {'name': 'Heath', 'surname': 'Ledger',
         'person_type': 'Actor'},
        {'name': 'Aaron', 'surname': 'Eckhart',
         'person_type': 'Actor'},
        {'name': 'Christopher', 'surname': 'Nolan',
         'person_type': 'Director'},
    ]

    interstellar = [
        {'name': 'Matthew', 'surname': 'McConaughey',
         'person_type': 'Actor'},
        {'name': 'Anne', 'surname': 'Hathaway',
         'person_type': 'Actor'},
        {'name': 'Jessica', 'surname': 'Chastain',
         'person_type': 'Actor'},
        {'name': 'Christopher', 'surname': 'Nolan',
         'person_type': 'Director'},
    ]

    no_way_home = [
        {'name': 'Tom', 'surname': 'Holland',
         'person_type': 'Actor'},
        {'name': 'Zendaya', 'surname': '',
         'person_type': 'Actor'},
        {'name': 'Benedict', 'surname': 'Cumberbatch',
         'person_type': 'Actor'},
        {'name': 'Jon', 'surname': 'Watts',
         'person_type': 'Director'},
    ]

    joker = [
        {'name': 'Joaquin', 'surname': 'Phoenix',
         'person_type': 'Actor'},
        {'name': 'Robert De', 'surname': 'Niro',
         'person_type': 'Actor'},
        {'name': 'Zazie', 'surname': 'Beetz',
         'person_type': 'Actor'},
        {'name': 'Todd', 'surname': 'Phillips',
         'person_type': 'Director'},
    ]

    uncharted = [
        {'name': 'Tom', 'surname': 'Holland',
         'person_type': 'Actor'},
        {'name': 'Mark', 'surname': 'Wahlberg',
         'person_type': 'Actor'},
        {'name': 'Antonio', 'surname': 'Banderas',
         'person_type': 'Actor'},
        {'name': 'Ruben', 'surname': 'Fleischer',
         'person_type': 'Director'},
    ]

    movie_person = {
        'Harry Potter and the Philosophers Stone': {'person': harry1},
        'Harry Potter and the Chamber of Secrets': {'person': harry2},
        'Harry Potter and the Prisoner of Azkaban': {'person': harry3},
        'Harry Potter and the Goblet of Fire': {'person': harry4},
        'Harry Potter and the Order of the Phoenix': {'person': harry5},
        'Harry Potter and the Half-Blood Prince': {'person': harry6},
        'Harry Potter and the Deathly Hallows: Part 1': {'person': harry7},
        'Harry Potter and the Deathly Hallows: Part 2': {'person': harry7},
        '007 SkyFall': {'person': sky_fall},
        'I, Robot': {'person': i_robot},
        'The Matrix Resurrections': {'person': matrix4},
        'The Avengers': {'person': avengers1},
        'Avengers: Age of Ultron': {'person': avengers2},
        'Avengers: Infinity War': {'person': avengers3},
        'Avengers: Endgame': {'person': avengers4},
        'The Shawshank Redemption': {'person': shawshank_redemption},
        'The Godfather': {'person': god_father},
        'The Dark Knight': {'person': dark_knight},
        'Interstellar': {'person': interstellar},
        'Spider-Man: No Way Home': {'person': no_way_home},
        'Joker': {'person': joker},
        'Uncharted': {'person': uncharted}
    }

    movie_genre = {
        'Harry Potter and the Philosophers Stone': ['Adventure', 'Fantasy'],
        'Harry Potter and the Chamber of Secrets': ['Adventure', 'Fantasy'],
        'Harry Potter and the Prisoner of Azkaban': ['Adventure', 'Fantasy'],
        'Harry Potter and the Goblet of Fire': ['Adventure', 'Fantasy'],
        'Harry Potter and the Order of the Phoenix': ['Adventure', 'Fantasy'],
        'Harry Potter and the Half-Blood Prince': ['Adventure', 'Fantasy'],
        'Harry Potter and the Deathly Hallows: Part 1': ['Adventure', 'Fantasy'],
        'Harry Potter and the Deathly Hallows: Part 2': ['Adventure', 'Fantasy'],
        '007 SkyFall': ['Action', 'Thriller', 'Crime', 'Adventure'],
        'I, Robot': ['Action', 'Sci-Fi'],
        'The Matrix Resurrections': ['Action', 'Sci-Fi'],
        'The Avengers': ['Action', 'Fantasy', 'Adventure'],
        'Avengers: Age of Ultron': ['Action', 'Fantasy', 'Adventure'],
        'Avengers: Infinity War': ['Action', 'Fantasy', 'Adventure'],
        'Avengers: Endgame': ['Action', 'Fantasy', 'Adventure'],
        'The Shawshank Redemption': ['Drama'],
        'The Godfather': ['Drama', 'Thriller', 'Crime'],
        'The Dark Knight': ['Drama', 'Action', 'Sci-Fi', 'Thriller', 'Crime'],
        'Interstellar': ['Sci-Fi'],
        'Spider-Man: No Way Home': ['Sci-Fi', 'Action', 'Adventure'],
        'Joker': ['Drama', 'Thriller', 'Crime'],
        'Uncharted': ['Action', 'Thriller'],
    }

    for movie in movies:
        add_movie(movie['title'], movie['duration'], movie['release_date'], movie['description'],
                  movie['average_rating'], movie['image'], movie['poster'])

    # check
    for title, ad in movie_person.items():
        movie = Movie.objects.get(title=title)
        for p in ad['person']:
            person = add_person(p['name'], p['surname'],  p['person_type'])
            if p['person_type'] == 'Actor':
                add_actor_movie(movie, person)
            else:
                add_director_movie(movie, person)

    for title, genres in movie_genre.items():
        movie = Movie.objects.get(title=title)
        for g in genres:
            genre = add_genre(g.__str__())
            add_movie_genre(movie, genre)

    # Add user test
    user1 = add_user('username1', '12345678', 'example@gmail.com', 'Rogers', 'Choi')
    user2 = add_user('username2', '87654321', 'example@gmail.com', 'Anne', 'Hathaway')
    add_user_profile(user1, 25, 'profile_images/user1.jpg', 'my bio')
    add_user_profile(user2, 25, 'profile_images/user1.jpg', '2 bio')

    # user review test
    movie1 = Movie.objects.get(title='Harry Potter and the Philosophers Stone')
    movie2 = Movie.objects.get(title='Harry Potter and the Prisoner of Azkaban')
    add_review(user1, movie1, 'comment test', 'header test', Decimal(5.00))
    add_review(user2, movie2, 'comment test', 'header test', Decimal(5.00))

    # Movie to watch test
    add_movie_to_watch(user1, movie1)
    add_movie_to_watch(user2, movie1)

    add_contact_message('example@gmail.com', 'Anonymous', 'test', 'test', datetime.datetime)


def add_movie(title, duration, release_date, description, average_rating, image, poster):
    movie = Movie.objects.get_or_create(title=title, duration=duration, release_date=release_date)[0]
    movie.description = description
    movie.average_rating = average_rating
    movie.image = image
    movie.poster = poster
    movie.save()
    return movie


def add_genre(name):
    genre = Genre.objects.get_or_create(name=name)[0]
    genre.save()
    return genre


def add_person(name, surname, person_type):
    person = Person.objects.get_or_create(name=name)[0]
    person.surname = surname
    person.person_type = person_type
    person.save()
    return person


def add_director_movie(movie_id, person_id):
    director_movie = DirectorMovie.objects.get_or_create(movie_id=movie_id, person_id=person_id)[0]
    director_movie.save()
    return director_movie


def add_actor_movie(movie_id, person_id):
    actor_movie = ActorMovie.objects.get_or_create(movie_id=movie_id, person_id=person_id)[0]
    actor_movie.save()
    return actor_movie


def add_user(username, password, email, first_name, last_name):
    user = User.objects.get_or_create(username=username)[0]
    user.set_password(password)
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    return user


def add_user_profile(user, age, picture, bio):
    user_profile = UserProfile.objects.get_or_create(user=user, age=age, picture=picture, bio=bio)
    return user_profile


def add_review(username, movie_id, comment, header, rating):
    review = Review.objects.get_or_create(username=username, movie_id=movie_id)[0]
    review.comment = comment
    review.header = header
    review.rating = rating
    review.save()
    return review


def add_movie_to_watch(username, movie_id):
    movie_to_watch = MovieToWatch.objects.get_or_create(username=username, movie_id=movie_id)[0]
    movie_to_watch.save()
    return movie_to_watch


def add_movie_genre(movie_id, genre_name):
    movie_genre = MovieGenre.objects.get_or_create(movie_id=movie_id, genre_name=genre_name)[0]
    movie_genre.save()
    return movie_genre


def add_contact_message(sender_email, sender_name, subject, message, date):
    contact_message = ContactMessage.objects.create(sender_email=sender_email, sender_name=sender_name, subject=subject,
                                                    message=message, date=date)
    contact_message.save()
    return contact_message


if __name__ == '__main__':
    print('Starting Moovie population script...')
    populate()
