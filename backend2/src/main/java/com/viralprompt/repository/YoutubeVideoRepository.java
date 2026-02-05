package com.viralprompt.repository;

import com.viralprompt.model.Profile;
import com.viralprompt.model.YoutubeVideo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface YoutubeVideoRepository extends JpaRepository<YoutubeVideo,Long> {
//    Optional<YoutubeVideo> findByVi(String email);
}
