import os


def movie_spider():
    movie_url_prefix = 'https://movie.douban.com/subject/'
    with open("../Dataset/Movie_id.csv", "r") as f_movie:
        movie_id_n = f_movie.readlines()
    movie_id = []
    [movie_id.append(line.strip()) for line in movie_id_n]


def main():
    movie_spider()


if __name__ == '__main__':
    main()
