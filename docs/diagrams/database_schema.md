```mermaid
erDiagram
    %% Entities with media storage (highlighted in blue)
    Posts {
        string post_id PK
        string user_id FK
        string content
        timestamp created_at
        timestamp updated_at
        array media_urls "S3 references"
        int likes_count
        int comments_count
    }

    Comments {
        string comment_id PK
        string post_id FK
        string user_id FK
        string content
        timestamp created_at
        array media_urls "S3 references"
        int likes_count
    }

    Messages {
        string message_id PK
        string sender_id FK
        string receiver_id FK
        string content
        timestamp sent_at
        array media_urls "S3 references"
        boolean read
        int likes_count
    }

    Profiles {
        string user_id PK
        string username
        string bio
        string avatar_url "S3 reference"
        string cover_url "S3 reference"
        timestamp joined_at
        int followers_count
        int following_count
    }

    Likes {
        string like_id PK
        string user_id FK
        string target_id FK "post_id/comment_id/message_id"
        string target_type "post/comment/message"
        timestamp created_at
    }

    Followers {
        string follower_id FK "user_id who follows"
        string following_id FK "user_id being followed"
        timestamp created_at
    }

    Notifications {
        string notification_id PK
        string user_id FK "user to notify"
        string type "follow/like/comment/message"
        string source_id FK "user who triggered"
        string target_id "post_id/comment_id/message_id"
        boolean read
        timestamp created_at
    }

    %% Relationships
    Posts ||--o{ Comments : has
    Posts ||--o{ Likes : receives
    Comments ||--o{ Likes : receives
    Messages ||--o{ Likes : receives
    Profiles ||--o{ Posts : creates
    Profiles ||--o{ Comments : writes
    Profiles ||--o{ Messages : sends
    Profiles ||--o{ Followers : "follows"
    Profiles ||--o{ Notifications : receives

    %% Note: Posts, Comments, Messages, and Profiles contain S3 media references
```