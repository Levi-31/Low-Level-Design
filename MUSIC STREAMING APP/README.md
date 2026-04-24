# Music Streaming App LLD

This repository contains the Low-Level Design (LLD) for a comprehensive Music Streaming Application implemented in Python. The system follows a layered architecture pattern, separating concerns across Controllers, Services, Repositories, and Domain Entities.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [UML Class Diagram](#uml-class-diagram)
- [Application Flow (Block Diagram)](#application-flow-block-diagram)
- [Domain Entities](#domain-entities)
- [System Components](#system-components)
  - [Controllers](#controllers)
  - [Services](#services)
  - [Repositories](#repositories)

## Architecture Overview

The application is structured using a standard layered architecture:

1. **Presentation/Controller Layer**: Receives input from the user (or API) and routes it to the appropriate service.
2. **Business/Service Layer**: Contains the core business logic, orchestrating actions across multiple domains and applying business rules.
3. **Data Access/Repository Layer**: Abstract interface for data storage, currently implemented using In-Memory Data Stores for simulation.
4. **Domain Layer**: Represents the core models and entities of the system (e.g., User, Song, Playlist).

## UML Class Diagram

The following Mermaid diagram represents the entities and relationships within the system:

```mermaid
classDiagram
    class User {
        +int id
        +str username
        +str email
        +str name
        +SubscriptionTier subscription_tier
    }

    class Artist {
        +int id
        +str artist_id
        +str name
        +str thumbnail_url
    }

    class Album {
        +int id
        +str album_id
        +str title
        +str artist_id
        +str thumbnail_url
    }

    class Song {
        +int id
        +str song_id
        +str title
        +str artist_id
        +str album_id
        +int duration
        +str audio_url
        +str thumbnail_url
        +int file_size
        +AudioQuality quality
        +AudioFormat format
    }

    class Playlist {
        +int id
        +str name
        +int user_id
        +List~str~ song_ids
    }

    class PlaybackSession {
        +str session_id
        +int user_id
        +str song_id
        +PlaybackSource source
        +int current_position
        +PlaybackStatus status
    }

    class Download {
        +str download_id
        +int user_id
        +str song_id
        +str device_id
        +DownloadStatus status
    }

    class ListeningHistory {
        +int id
        +int user_id
        +str song_id
        +datetime timestamp
    }

    %% Relationships
    User "1" --> "*" Playlist : creates
    User "1" --> "*" PlaybackSession : has
    User "1" --> "*" Download : initiates
    User "1" --> "*" ListeningHistory : tracks
    
    Artist "1" --> "*" Album : creates
    Artist "1" --> "*" Song : performs
    Album "1" --> "*" Song : contains
    
    Playlist "*" --> "*" Song : includes
    PlaybackSession "*" --> "1" Song : plays
    Download "*" --> "1" Song : downloads
    ListeningHistory "*" --> "1" Song : records
```

## Application Flow (Block Diagram)

The following block diagram illustrates the initialization and execution flow defined in `main.py`.

```mermaid
flowchart TD
    Start((Start Application))
    
    subgraph Initialization Phase
        InitRepo["Initialize Repositories<br>(User, Song, Album, etc.)"]
        InitServ["Initialize Services<br>(Playback, Search, etc.)"]
        InitCtrl["Initialize Controllers<br>(Playback, Search, etc.)"]
        TestData["Setup Test Data<br>(Seed DB)"]
    end
    
    subgraph Execution Flows
        Flow1["1. User Registration Flow"]
        Flow2["2. Search Songs Flow"]
        Flow3["3. Play Song Flow<br>& Update Position"]
        Flow4["4. Create Playlist Flow"]
        Flow5["5. Download Song Flow<br>(Premium Feature)"]
        Flow6["6. Get Recommendations Flow"]
    end
    
    Start --> InitRepo
    InitRepo --> InitServ
    InitServ --> InitCtrl
    InitCtrl --> TestData
    
    TestData --> Flow1
    Flow1 --> Flow2
    Flow2 --> Flow3
    Flow3 --> Flow4
    Flow4 --> Flow5
    Flow5 --> Flow6
    Flow6 --> End((End Simulation))

    classDef init fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef flow fill:#cce5ff,stroke:#007bff,stroke-width:2px;
    
    class InitRepo,InitServ,InitCtrl,TestData init;
    class Flow1,Flow2,Flow3,Flow4,Flow5,Flow6 flow;
```

## Domain Entities

- **User**: Core entity representing system users, including their `SubscriptionTier` (FREE/PREMIUM).
- **Artist**: Represents musical artists.
- **Album**: Represents a collection of songs.
- **Song**: Central entity representing an audio track, including its `AudioQuality` and `AudioFormat`.
- **Playlist**: A user-curated collection of songs.
- **PlaybackSession**: Maintains the state of a user's current playback.
- **Download**: Tracks the status of song downloads for offline listening.
- **ListeningHistory**: Logs when a user listens to a song for recommendation purposes.

## System Components

### Controllers
Act as entry points for the application flows:
- `PlaybackController`: Manages song playback, pausing, resuming, and position tracking.
- `SearchController`: Handles search queries for songs, artists, and albums.
- `PlaylistController`: Manages playlist creation, modification, and deletion.
- `DownloadController`: Handles offline download requests (checks premium status).
- `RecommendationController`: Interfaces with the recommendation engine to provide user suggestions.
- `StreamingController`: Handles the underlying streaming protocols.

### Services
Contain the core business logic:
- `PlaybackService`: Coordinates between streaming, history, and sessions.
- `SearchService`: Queries repositories to fulfill search requests.
- `PlaylistService`: Implements playlist management with `LockingService` for concurrency control.
- `DownloadService`: Handles the logic for caching and persisting downloads.
- `RecommendationService`: Applies a `GenreBasedStrategy` to suggest songs based on `ListeningHistory`.
- `StreamingService`: Interacts with the `CacheService` to deliver song streams efficiently.

### Repositories
Data access interfaces, currently utilizing In-Memory storage:
- `InMemoryUserRepository`
- `InMemorySongRepository`
- `InMemoryAlbumRepository`
- `InMemoryArtistRepository`
- `InMemoryPlaylistRepository`
- `InMemoryListeningHistoryRepository`
- `InMemoryPlaybackSessionRepository`
- `InMemoryDownloadRepository`
