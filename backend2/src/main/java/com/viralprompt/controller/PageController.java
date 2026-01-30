package com.viralprompt.controller;

import com.viralprompt.service.ContentService;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class PageController {

    private ContentService contentService;

    @Autowired
    public PageController(ContentService contentService) {
        this.contentService = contentService;
    }

    @GetMapping("/")
    public String index(Model model) {
        model.addAttribute("trendingItems", contentService.getTrendingContent());
        return "index";
    }

    @GetMapping("/signin")
    public String signin() {
        return "signin";
    }

    @GetMapping("/signup")
    public String signup() {
        return "signup";
    }

    @GetMapping("/ai-music")
    public String aiMusic() {
        return "ai-music";
    }

    @GetMapping("/ai-books")
    public String aiBooks() {
        return "ai-books";
    }

    @GetMapping("/ai-video-generator")
    public String aiVideo() {
        return "ai-video-generator";
    }

    @GetMapping("/caption-generator")
    public String captionGenerator() {
        return "caption-generator";
    }

    @GetMapping("/dashboard")
    public String dashboard() {
        return "dashboard";
    }

    @GetMapping("/explore")
    public String explore() {
        return "explore";
    }

    @GetMapping("/profile")
    public String profile() {
        return "profile";
    }

    @GetMapping("/collections")
    public String collections() {
        return "collections";
    }

    @GetMapping("/analytics")
    public String analytics() {
        return "analytics";
    }

    @GetMapping("/prompt-library")
    public String promptLibrary() {
        return "prompt-library";
    }

    @GetMapping("/reel-creator")
    public String reelCreator() {
        return "reel-creator";
    }

    @GetMapping("/script-writer")
    public String scriptWriter() {
        return "script-writer";
    }

    @GetMapping("/settings")
    public String settings() {
        return "settings";
    }

    @GetMapping("/trending")
    public String trending() {
        return "trending";
    }

    @GetMapping("/prompt-detail")
    public String promptDetail() {
        return "prompt-detail";
    }

    @GetMapping("/submit")
    public String submit() {
        return "submit";
    }

    @GetMapping("/top-rated")
    public String topRated() {
        return "top-rated";
    }
}
