```mermaid
graph LR
    A[Long-form Content (WP)] --> B[OSMU Slicer]
    B --> C1[Instagram Slice + Caption]
    B --> C2[Twitter Slice + Caption]
    B --> C3[LinkedIn Slice + Caption]
    B --> D[Video Renderer (FFmpeg)]
    D --> E1[YouTube Shorts Upload]
    D --> E2[TikTok Upload]
    B --> F[Tistory Blog Post]
    C1 & C2 & C3 & E1 & E2 & F --> G[Supabase content_tracker update]
    G --> H[Retool Admin]
    G --> I[Slack Notifications]
```
