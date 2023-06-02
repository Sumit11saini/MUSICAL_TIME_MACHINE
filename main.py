import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100/"

Client_ID = "ca14055126154fdd94ec398b292ca972"
Client_Secret = "9d39d3a34f5b4e8eb764f550115dc202"


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"{URL}/{date}/")
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")
track_titles = soup.select("li ul li h3")
top_100_list = [track.getText().replace("\n", "").replace("\t", "") for track in track_titles]
print(top_100_list)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri= "https://example.com/callback",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_names = [song.find(name="h3", id="title-of-a-story").getText().strip() for song in soup.find_all(name="div", class_="o-chart-results-list-row-container")]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)