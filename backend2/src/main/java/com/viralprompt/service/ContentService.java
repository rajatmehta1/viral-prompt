package com.viralprompt.service;

import com.viralprompt.dto.EmbedContentDTO;
import com.viralprompt.dto.PromptStepDTO;
import com.viralprompt.model.Category;
import com.viralprompt.model.ContentItem;
import com.viralprompt.model.EmbedPromptStep;
import com.viralprompt.repository.CategoryRepository;
import com.viralprompt.repository.ContentItemRepository;
import com.viralprompt.repository.EmbedPromptStepRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class ContentService {

    @Autowired
    private ContentItemRepository contentItemRepository;

    @Autowired
    private EmbedPromptStepRepository embedPromptStepRepository;

    @Autowired
    private CategoryRepository categoryRepository;

    public List<ContentItem> getAllContent() {
        return contentItemRepository.findAll();
    }

    public List<ContentItem> getTopRatedContent() {
        return contentItemRepository.findByOrderByLikesCountDesc();
    }

    public List<ContentItem> getTrendingContent() {
        return contentItemRepository.findByOrderByCreatedAtDesc();
    }

    public Optional<ContentItem> getContentById(Long id) {
        return contentItemRepository.findById(id);
    }

    public List<ContentItem> findByPlatform(ContentItem.PlatformType platform) {
        return contentItemRepository.findByPlatform(platform);
    }

    public List<EmbedPromptStep> getPromptStepsForContent(Long contentItemId) {
        return embedPromptStepRepository.findByContentItemIdOrderByStepOrderAsc(contentItemId);
    }

    @Transactional
    public ContentItem saveEmbeddedContent(EmbedContentDTO dto) {
        // Determine platform type
        ContentItem.PlatformType platformType = ContentItem.PlatformType.valueOf(dto.getPlatform().toUpperCase());

        // Determine content type based on platform
        ContentItem.ContentType contentType = determineContentType(platformType);

        // Find or handle category
        Category category = null;
        if (dto.getCategory() != null && !dto.getCategory().isEmpty() && !dto.getCategory().equals("Select Category")) {
            category = categoryRepository.findByName(dto.getCategory()).orElse(null);
        }

        // Create and save content item
        ContentItem contentItem = ContentItem.builder()
                .title(dto.getTitle())
                .description(dto.getDescription())
                .embedUrl(dto.getEmbedUrl())
                .tags(dto.getTags())
                .platform(platformType)
                .type(contentType)
                .category(category)
                .viewsCount(0L)
                .likesCount(0L)
                .build();

        contentItem = contentItemRepository.save(contentItem);

        // Save prompt steps
        if (dto.getPromptSteps() != null && !dto.getPromptSteps().isEmpty()) {
            int stepOrder = 1;
            for (PromptStepDTO stepDto : dto.getPromptSteps()) {
                if (stepDto.getAiTool() != null && !stepDto.getAiTool().isEmpty()) {
                    EmbedPromptStep step = EmbedPromptStep.builder()
                            .contentItem(contentItem)
                            .aiTool(stepDto.getAiTool())
                            .promptText(stepDto.getPromptText())
                            .parameters(stepDto.getParameters())
                            .stepOrder(stepOrder++)
                            .build();
                    embedPromptStepRepository.save(step);
                }
            }
        }

        return contentItem;
    }

    private ContentItem.ContentType determineContentType(ContentItem.PlatformType platform) {
        return switch (platform) {
            case INSTAGRAM, TIKTOK -> ContentItem.ContentType.REEL;
            case YOUTUBE -> ContentItem.ContentType.VIDEO;
            case MIDJOURNEY, DALLE -> ContentItem.ContentType.IMAGE;
            case SUNO, KLING, RUNWAY -> ContentItem.ContentType.AI;
            default -> ContentItem.ContentType.AI;
        };
    }
}

