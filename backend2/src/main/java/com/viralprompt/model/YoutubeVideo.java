package com.viralprompt.model;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import java.time.OffsetDateTime;

@Entity
@Table(
        name = "youtube_videos",
        uniqueConstraints = {
                @UniqueConstraint(name = "unique_video_per_user", columnNames = {"video_id"})
        },
        indexes = {
                @Index(name = "idx_youtube_videos_user_id", columnList = "user_id"),
                @Index(name = "idx_youtube_videos_video_id", columnList = "video_id"),
                @Index(name = "idx_youtube_videos_published_at", columnList = "published_at")
        }
)
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class YoutubeVideo {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", columnDefinition = "UUID")
    private Profile user;

    // Video identifiers
    @Column(name = "video_id", columnDefinition = "TEXT", nullable = false)
    private String videoId;

    @Column(name = "url", columnDefinition = "TEXT")
    private String url;

    // Video metadata
    @Column(name = "title", columnDefinition = "TEXT")
    private String title;

    @Column(name = "description", columnDefinition = "TEXT")
    private String description;

    @Column(name = "channel", columnDefinition = "TEXT")
    private String channel;

    @Column(name = "duration", columnDefinition = "TEXT")
    private String duration;

    @Column(name = "is_short", columnDefinition = "BOOLEAN")
    @Builder.Default
    private Boolean isShort = false;

    // Metrics
    @Column(name = "views", columnDefinition = "BIGINT")
    @Builder.Default
    private Long views = 0L;

    @Column(name = "likes", columnDefinition = "BIGINT")
    @Builder.Default
    private Long likes = 0L;

    @Column(name = "comments", columnDefinition = "INTEGER")
    @Builder.Default
    private Integer comments = 0;

    // Additional fields
    @Column(name = "extracted_prompt", columnDefinition = "TEXT")
    private String extractedPrompt;

    @Column(name = "search_query", columnDefinition = "TEXT")
    private String searchQuery;

    @Column(name = "platform", columnDefinition = "TEXT")
    @Builder.Default
    private String platform = "YouTube";

    // Timestamps
    @Column(name = "published_at", columnDefinition = "TIMESTAMPTZ")
    private OffsetDateTime publishedAt;

    @Column(name = "created_at", columnDefinition = "TIMESTAMPTZ")
    @CreationTimestamp
    private OffsetDateTime createdAt;
}