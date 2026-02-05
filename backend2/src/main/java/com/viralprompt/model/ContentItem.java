package com.viralprompt.model;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.OffsetDateTime;

@Entity
@Table(name = "content_items")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ContentItem {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String description;

    private String mediaUrl;
    private String thumbnailUrl;

    @Column(columnDefinition = "TEXT")
    private String embedUrl;

    private String tags;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "author_id")
    private Profile author;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id")
    private Category category;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "TEXT")
    private ContentType type;

    @Enumerated(EnumType.STRING)
    @Column(columnDefinition = "TEXT")
    private PlatformType platform;

    @Builder.Default
    private Long viewsCount = 0L;
    @Builder.Default
    private Long likesCount = 0L;

    @CreationTimestamp
    private OffsetDateTime createdAt;

    @UpdateTimestamp
    private OffsetDateTime updatedAt;

    public enum ContentType {
        IMAGE, VIDEO, REEL, AI
    }

    public enum PlatformType {
        INSTAGRAM, TIKTOK, YOUTUBE, MIDJOURNEY, SUNO, DALLE, KLING, RUNWAY, OTHER
    }
}

