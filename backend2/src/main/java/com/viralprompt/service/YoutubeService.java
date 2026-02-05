package com.viralprompt.service;

import com.viralprompt.repository.YoutubeVideoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class YoutubeService {

    private YoutubeVideoRepository youtubeVideoRepository;

    public YoutubeService(YoutubeVideoRepository youtubeVideoRepository) {
        this.youtubeVideoRepository = youtubeVideoRepository;
    }

}
