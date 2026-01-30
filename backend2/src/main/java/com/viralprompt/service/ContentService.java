package com.viralprompt.service;

import com.viralprompt.model.ContentItem;
import com.viralprompt.repository.ContentItemRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ContentService {

    @Autowired
    private ContentItemRepository contentItemRepository;

    public List<ContentItem> getAllContent() {
        return contentItemRepository.findAll();
    }

    public List<ContentItem> getTopRatedContent() {
        return contentItemRepository.findByOrderByLikesCountDesc();
    }

    public List<ContentItem> getTrendingContent() {
        return contentItemRepository.findByOrderByCreatedAtDesc();
    }
}
