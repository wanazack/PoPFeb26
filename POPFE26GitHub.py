import streamlit as st
import pandas as pd


class Movie:
    def __init__(self, movie_id, title, genre, year):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.year = year
        self.ratings = []
        self.views = 0

    def add_rating(self, rating):
        self.ratings.append(rating)

    def add_view(self):
        self.views += 1

    def get_average_rating(self):
        if len(self.ratings) == 0:
            return 0
        return sum(self.ratings) / len(self.ratings)


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.watch_history = []
        self.rating_log = {}

    def watch_movie(self, movie):
        self.watch_history.append(movie)
        movie.add_view()

    def rate_movie(self, movie, rating):
        movie.add_rating(rating)
        self.rating_log[movie.title] = rating

    def get_preferred_genres(self):
        genres = []
        for movie in self.watch_history:
            genres.append(movie.genre)
        return genres

    def get_watch_count(self):
        return len(self.watch_history)


class RecommendationSystem:
    def __init__(self):
        self.movies = []
        self.users = []

    def add_movie(self, movie):
        self.movies.append(movie)

    def add_user(self, user):
        self.users.append(user)

    def login_user(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def find_movie_by_title(self, title):
        for movie in self.movies:
            if movie.title == title:
                return movie
        return None

    def get_top_recommendations(self, user, n=3):
        preferred_genres = user.get_preferred_genres()
        watched_titles = []

        for movie in user.watch_history:
            watched_titles.append(movie.title)

        recommendations = []
        for movie in self.movies:
            if movie.genre in preferred_genres and movie.title not in watched_titles:
                recommendations.append(movie)

        recommendations.sort(key=lambda x: x.get_average_rating(), reverse=True)
        return recommendations[:n]

    def get_trending_movies(self, n=3):
        trending = sorted(
            self.movies,
            key=lambda x: (x.views, x.get_average_rating()),
            reverse=True
        )
        return trending[:n]

    def get_popular_genres(self):
        genre_count = {}

        for user in self.users:
            for movie in user.watch_history:
                if movie.genre in genre_count:
                    genre_count[movie.genre] += 1
                else:
                    genre_count[movie.genre] = 1

        sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_genres

    def get_top_rated_movies(self, n=5):
        return sorted(self.movies, key=lambda x: x.get_average_rating(), reverse=True)[:n]



mrs = RecommendationSystem()

movie1 = Movie(1, "Grown Ups", "Comedy", 2010)
movie2 = Movie(2, "Johnny English", "Action", 2003)
movie3 = Movie(3, "Moana", "Animations", 2016)
movie4 = Movie(4, "Spiderman: No Way Home", "Sci-Fi", 2021)
movie5 = Movie(5, "Rambo", "Action", 2008)
movie6 = Movie(6, "Princess and the Frog", "Animations", 2009)
movie7 = Movie(7, "Hunger Games", "Action", 2012)

movie1.ratings = [5, 4]
movie2.ratings = [5, 5]
movie3.ratings = [4, 3]
movie4.ratings = [5, 4]
movie5.ratings = [5, 5, 4]
movie6.ratings = [4, 5]
movie7.ratings = [5, 5, 5]

mrs.add_movie(movie1)
mrs.add_movie(movie2)
mrs.add_movie(movie3)
mrs.add_movie(movie4)
mrs.add_movie(movie5)
mrs.add_movie(movie6)
mrs.add_movie(movie7)

user1 = User(101, "Ahmed")
user2 = User(102, "Minah")

mrs.add_user(user1)
mrs.add_user(user2)

user1.watch_movie(movie1)
user1.watch_movie(movie3)
user1.watch_movie(movie4)
user1.rate_movie(movie1, 5)
user1.rate_movie(movie3, 4)
user1.rate_movie(movie4, 5)

user2.watch_movie(movie2)
user2.watch_movie(movie5)
user2.watch_movie(movie6)
user2.watch_movie(movie7)
user2.rate_movie(movie2, 5)
user2.rate_movie(movie5, 4)
user2.rate_movie(movie6, 5)
user2.rate_movie(movie7, 5)



st.set_page_config(page_title="Movie Recommendation System", layout="wide")
st.title("Movie Recommendation System")

st.sidebar.header("User Login")
user_id_input = st.sidebar.number_input("Enter User ID", min_value=100, max_value=999, step=1)
logged_in_user = mrs.login_user(user_id_input)

if logged_in_user is None:
    st.warning("Please input a valid user ID.")
else:
    st.success(f"Welcome, {logged_in_user.name}!")

    menu = st.sidebar.radio(
        "Select a section",
        ["Dashboard", "Rate a Movie", "Search Movies", "Admin Console"]
    )

    if menu == "Dashboard":
        st.subheader("User Dashboard")

        recommendations = mrs.get_top_recommendations(logged_in_user, 3)
        trending = mrs.get_trending_movies(3)
        popular_genres = mrs.get_popular_genres()

        col1, col2 = st.columns(2)

        with col1:
            st.write("Top Recommended Movies")
            if len(recommendations) == 0:
                st.write("No recommendations found.")
            else:
                rec_data = []
                for movie in recommendations:
                    rec_data.append({
                        "Title": movie.title,
                        "Genre": movie.genre,
                        "Year": movie.year,
                        "Average Rating": round(movie.get_average_rating(), 2)
                    })
                st.dataframe(pd.DataFrame(rec_data), use_container_width=True)

        with col2:
            st.write("Trending Movies")
            trend_data = []
            for movie in trending:
                trend_data.append({
                    "Title": movie.title,
                    "Genre": movie.genre,
                    "Views": movie.views,
                    "Average Rating": round(movie.get_average_rating(), 2)
                })
            st.dataframe(pd.DataFrame(trend_data), use_container_width=True)

        st.write("Popular Genres")
        if len(popular_genres) == 0:
            st.write("No popular genres found.")
        else:
            genre_df = pd.DataFrame(popular_genres, columns=["Genre", "Watch Count"])
            st.dataframe(genre_df, use_container_width=True)

        st.write("Watch History")
        history_data = []
        for movie in logged_in_user.watch_history:
            history_data.append({
                "Title": movie.title,
                "Genre": movie.genre,
                "Year": movie.year,
                "Average Rating": round(movie.get_average_rating(), 2)
            })
        if len(history_data) > 0:
            st.dataframe(pd.DataFrame(history_data), use_container_width=True)
        else:
            st.write("No watch history found.")

        st.write("Rating Log")
        rating_data = []
        for title, rating in logged_in_user.rating_log.items():
            rating_data.append({
                "Movie Title": title,
                "User Rating": rating
            })
        if len(rating_data) > 0:
            st.dataframe(pd.DataFrame(rating_data), use_container_width=True)
        else:
            st.write("No ratings found.")

        st.write("Top Rated Movies Chart")
        top_rated = mrs.get_top_rated_movies(5)
        titles = [movie.title for movie in top_rated]
        avg_ratings = [movie.get_average_rating() for movie in top_rated]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(titles, avg_ratings)
        ax.set_title("Top Rated Movies")
        ax.set_xlabel("Movie Title")
        ax.set_ylabel("Average Rating")
        plt.xticks(rotation=20)
        st.pyplot(fig)

    elif menu == "Rate a Movie":
        st.subheader("Rate a Movie")

        movie_titles = [movie.title for movie in mrs.movies]
        selected_title = st.selectbox("Select a movie", movie_titles)
        rating = st.slider("Give your rating", 1, 5, 3)

        if st.button("Submit Rating"):
            selected_movie = mrs.find_movie_by_title(selected_title)
            logged_in_user.watch_movie(selected_movie)
            logged_in_user.rate_movie(selected_movie, rating)
            st.success(f"You have rated '{selected_title}' with {rating} star(s)!")

    elif menu == "Search Movies":
        st.subheader("Search Movies")

        search_option = st.radio("Search by", ["Title", "Genre", "Year"])

        if search_option == "Title":
            keyword = st.text_input("Enter title keyword")
            if keyword:
                results = []
                for movie in mrs.movies:
                    if keyword.lower() in movie.title.lower():
                        results.append(movie)

                if len(results) > 0:
                    result_data = []
                    for movie in results:
                        result_data.append({
                            "Title": movie.title,
                            "Genre": movie.genre,
                            "Year": movie.year,
                            "Average Rating": round(movie.get_average_rating(), 2)
                        })
                    st.dataframe(pd.DataFrame(result_data), use_container_width=True)
                else:
                    st.write("No movies found.")

        elif search_option == "Genre":
            genre = st.text_input("Enter genre")
            if genre:
                results = []
                for movie in mrs.movies:
                    if movie.genre.lower() == genre.lower():
                        results.append(movie)

                if len(results) > 0:
                    result_data = []
                    for movie in results:
                        result_data.append({
                            "Title": movie.title,
                            "Genre": movie.genre,
                            "Year": movie.year,
                            "Average Rating": round(movie.get_average_rating(), 2)
                        })
                    st.dataframe(pd.DataFrame(result_data), use_container_width=True)
                else:
                    st.write("No movies found.")

        elif search_option == "Year":
            year = st.number_input("Enter year", min_value=1900, max_value=2100, step=1)
            results = []
            for movie in mrs.movies:
                if movie.year == year:
                    results.append(movie)

            if len(results) > 0:
                result_data = []
                for movie in results:
                    result_data.append({
                        "Title": movie.title,
                        "Genre": movie.genre,
                        "Year": movie.year,
                        "Average Rating": round(movie.get_average_rating(), 2)
                    })
                st.dataframe(pd.DataFrame(result_data), use_container_width=True)
            else:
                st.write("No movies found.")

    elif menu == "Admin Mode":
        st.subheader("Administrative Mode")
        admin_key = st.text_input("Enter admin key", type="password")

        if admin_key == "ADMIN.COM":
            st.success("Admin access granted.")

            st.write("Current Movie Database")
            movie_data = []
            for movie in mrs.movies:
                movie_data.append({
                    "ID": movie.movie_id,
                    "Title": movie.title,
                    "Genre": movie.genre,
                    "Year": movie.year,
                    "Average Rating": round(movie.get_average_rating(), 2),
                    "Views": movie.views
                })
            st.dataframe(pd.DataFrame(movie_data), use_container_width=True)

            st.write("Engagement Analytics")
            top_active_users = sorted(mrs.users, key=lambda x: x.get_watch_count(), reverse=True)

            active_user_data = []
            for user in top_active_users:
                active_user_data.append({
                    "User ID": user.user_id,
                    "Name": user.name,
                    "Watch Count": user.get_watch_count()
                })
            st.dataframe(pd.DataFrame(active_user_data), use_container_width=True)
        elif admin_key:
            st.error("Invalid admin key.")
