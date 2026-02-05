package com.viralprompt.repository;

import com.viralprompt.model.ContentItem;
import com.viralprompt.model.EmbedPromptStep;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface EmbedPromptStepRepository extends JpaRepository<EmbedPromptStep, Long> {
    List<EmbedPromptStep> findByContentItemOrderByStepOrderAsc(ContentItem contentItem);
    List<EmbedPromptStep> findByContentItemIdOrderByStepOrderAsc(Long contentItemId);
}
