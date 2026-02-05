package com.viralprompt.model;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "embed_prompt_steps")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class EmbedPromptStep {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "content_item_id", nullable = false)
    private ContentItem contentItem;

    @Column(nullable = false)
    private String aiTool;

    @Column(columnDefinition = "TEXT")
    private String promptText;

    private String parameters;

    @Column(nullable = false)
    private Integer stepOrder;
}
