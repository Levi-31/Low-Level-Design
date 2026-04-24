




from controller.download_controller import DownloadController
from controller.playback_controller import PlaybackController
from controller.playlist_controller import PlaylistController
from controller.recommendation_controller import RecommendationController
from controller.search_controller import SearchController
from controller.streaming_controller import StreamingController
from domain.album import Album
from domain.artist import Artist
from domain.audio_format import AudioFormat
from domain.audio_quality import AudioQuality
from domain.playback_source import PlaybackSource
from domain.song import Song
from domain.subscription_tier import SubscriptionTier
from domain.user import User
from repository.implementation.in_memory_db_implementation import InMemoryAlbumRepository, InMemoryArtistRepository, InMemoryDownloadRepository, InMemoryListeningHistoryRepository, InMemoryPlaybackSessionRepository, InMemoryPlaylistRepository, InMemorySongRepository, InMemoryUserRepository
from service.cache_service import CacheService
from service.download_service import DownloadService
from service.locking_service import LockingService
from service.playback_service import PlaybackService
from service.playlist_service import PlaylistService
from service.recommendation_servicce import RecommendationService
from service.search_service import SearchService
from service.strategy.recommendation_strategy import GenreBasedStrategy
from service.streaming_service import StreamingService


def setup_test_data(user_repo, song_repo:InMemorySongRepository, artist_repo, album_repo):
    # Create artist
    artist = Artist(id=1, artist_id="ART_001", name="The Beatles", 
                   thumbnail_url="https://example.com/beatles.jpg")
    artist_repo.save(artist)

    # Create album
    album = Album(id=1, album_id="ALB_001", title="Abbey Road", artist_id="ART_001",
                 thumbnail_url="https://example.com/abbeyroad.jpg")
    album_repo.save(album)

    # Create songs
    for i in range(1, 6):
        song_id = f"SONG_00{i}"
        song = Song(
            id=i,
            song_id=song_id,
            title=f"Love Song {i}",
            artist_id="ART_001",
            album_id="ALB_001",
            duration=180 + i * 10,
            audio_url=f"https://example.com/audio/{song_id}.mp3",
            thumbnail_url=f"https://example.com/thumb/{song_id}.jpg",
            file_size=5000000,
            quality=AudioQuality.HIGH,
            format=AudioFormat.MP3
        )
        song_repo.save(song)

def main():
    # Initialize repositories
    user_repo = InMemoryUserRepository()
    song_repo = InMemorySongRepository()
    album_repo = InMemoryAlbumRepository()
    artist_repo = InMemoryArtistRepository()
    playlist_repo = InMemoryPlaylistRepository()
    history_repo = InMemoryListeningHistoryRepository()
    session_repo = InMemoryPlaybackSessionRepository()
    download_repo = InMemoryDownloadRepository()

    # Initialize services
    lock_service = LockingService()
    cache_service = CacheService()
    streaming_service = StreamingService(song_repo, user_repo, cache_service)
    playback_service = PlaybackService(
        session_repo, song_repo, album_repo, playlist_repo, 
        user_repo, history_repo, streaming_service
    )
    search_service = SearchService(song_repo, artist_repo, album_repo)
    playlist_service = PlaylistService(playlist_repo, song_repo, lock_service)
    download_service = DownloadService(download_repo, user_repo)
    recommendation_strategy = GenreBasedStrategy()
    recommendation_service = RecommendationService(history_repo, recommendation_strategy)

    # Initialize controllers
    playback_controller = PlaybackController(playback_service)
    search_controller = SearchController(search_service)
    playlist_controller = PlaylistController(playlist_service)
    download_controller = DownloadController(download_service)
    recommendation_controller = RecommendationController(recommendation_service)
    streaming_controller = StreamingController(streaming_service)

    # Setup test data
    setup_test_data(user_repo, song_repo, artist_repo, album_repo)

    print("=== Music Streaming App Simulation (Python) ===\n")

    # Flow 1: User Registration
    print("1. User Registration:")
    alice = User(id=1, username="user1", email="user1@example.com", name="John Doe", 
                subscription_tier=SubscriptionTier.FREE)
    bob = User(id=2, username="user2", email="user2@example.com", name="Jane Smith", 
              subscription_tier=SubscriptionTier.PREMIUM)
    user_repo.save(alice)
    user_repo.save(bob)
    print(f"Created users: {alice.username} (FREE), {bob.username} (PREMIUM)\n")

    # Flow 2: Search
    print("2. Search Songs:")
    search_result = search_controller.search("Love", "SONG")
    print(f"Found {len(search_result.songs)} songs\n")

    # Flow 3: Play Song
    print("3. Play Song:")
    if search_result.songs:
        song_id = search_result.songs[0].song_id
        state = playback_controller.play(alice.id, PlaybackSource.SONG, song_id, 0)
        print(f"Playing: {state.current_song.title if state.current_song else 'Unknown'}")
        print(f"Stream URL: {state.stream_url}\n")

        # Flow 6: Position Update
        print("4. Update Playback Position:")
        playback_controller.update_position(state.session_id, 30)
        print("Updated position to 30 seconds\n")

    # Flow 4: Create Playlist
    print("5. Create Playlist:")
    if len(search_result.songs) >= 2:
        song_ids = [s.song_id for s in search_result.songs[:2]]
        playlist = playlist_controller.create_playlist(alice.id, "My Favorites", song_ids)
        print(f"Created playlist: {playlist.name} with {len(playlist.song_ids)} songs\n")

    # Flow 5: Download (Premium only)
    print("6. Download Song (Premium):")
    if search_result.songs:
        try:
            song_id = search_result.songs[0].song_id
            download = download_controller.download(bob.id, song_id, "device1")
            print(f"Downloaded: {download.download_id} (Status: COMPLETED)\n")
        except Exception as e:
            print(f"Download failed: {e}\n")

    # Flow 7: Recommendations
    print("7. Get Recommendations:")
    recommendations = recommendation_controller.get_recommendations(alice.id)
    print(f"Got {len(recommendations)} recommendations\n")

    print("=== Simulation Complete ===")

if __name__ == "__main__":
    main()
