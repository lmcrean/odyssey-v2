```mermaid
graph LR
    Client[Client/Browser] -.-> WSConn[WebSocket Connection]
    Client --> |HTTPS| S3Web[S3 Static Website]
    
    subgraph AWS
        S3Web --> S3[S3 Bucket<br/>odyssey-chat]
        
        subgraph FileStorage["File Storage (S3)"]
            S3 --> |media| S3P[/posts/]
            S3 --> |attachments| S3C[/comments/]
            S3 --> |chat files| S3M[/messages/]
            S3 --> |profile media| S3A[/profiles/]
            S3 --> |web-assets| S3W[/www/]
        end
        
        WSConn --> APIGW[API Gateway WebSocket]
        
        subgraph SocialFeatures["Social Features (Lambda APIs)"]
            Lambda3[Posts API]
            Lambda4[Comments API]
            Lambda5[Messages API]
            Lambda6[Likes API]
            Lambda7[Profiles API]
            Lambda8[Followers API]
            Lambda9[Notifications API]
        end
        
        subgraph SocialData["Social Data (DynamoDB)"]
            DDB3[(Posts)]
            DDB4[(Comments)]
            DDB5[(Messages)]
            DDB6[(Likes)]
            DDB7[(Profiles)]
            DDB8[(Followers)]
            DDB9[(Notifications)]
        end

        %% Core WebSocket connections
        APIGW --> |$connect| Lambda1[Connect Lambda]
        APIGW --> |$disconnect| Lambda2[Disconnect Lambda]
        Lambda1 --> DDB1[(DynamoDB<br/>odyssey_connections)]
        Lambda1 --> DDB2[(DynamoDB<br/>odyssey_rate_limits)]

        %% Feature flows
        Client --> |API Calls| SocialFeatures
        SocialFeatures --> SocialData
        SocialFeatures --> FileStorage
        
        Lambda9 -.-> |broadcast| APIGW
    end

    APIGW -.-> |notifications| Client
```