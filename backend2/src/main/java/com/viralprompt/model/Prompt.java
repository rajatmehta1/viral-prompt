package com.viralprompt.model;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.OffsetDateTime;

@Entity
@Table(name = "prompts")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Prompt {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "content_item_id")
    private ContentItem contentItem;

    @Column(columnDefinition = "TEXT", nullable = false)
    private String promptText;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "author_id")
    private Profile author;

    private String modelInfo;
    private Integer usageCount = 0;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "original_prompt_id")
    private Prompt originalPrompt;

    @CreationTimestamp
    private OffsetDateTime createdAt;
}
