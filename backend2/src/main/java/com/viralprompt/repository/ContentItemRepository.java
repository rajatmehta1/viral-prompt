package com.viralprompt.repository;

import com.viralprompt.model.ContentItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ContentItemRepository extends JpaRepository<ContentItem, Long> {
    List<ContentItem> findByType(ContentItem.ContentType type);
    List<ContentItem> findByOrderByLikesCountDesc();
    List<ContentItem> findByOrderByCreatedAtDesc();
}
